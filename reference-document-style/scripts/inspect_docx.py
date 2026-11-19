#!/usr/bin/env python3
"""Read Word OOXML formatting evidence. Python 3, standard library only."""
import argparse
import json
import posixpath
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote
from zipfile import BadZipFile, ZipFile

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
STRICT_W = '{http://purl.oclc.org/ooxml/wordprocessingml/main}'
MANY = {'lvl', 'lvlOverride', 'tab', 'col', 'headerReference', 'footerReference'}
SKIP = {'pPrChange', 'rPrChange', 'sectPrChange', 'numberingChange', 'ins', 'del', 'moveFrom', 'moveTo'}


def local(tag):
    return tag.rsplit('}', 1)[-1]


def val(node, child):
    found = node.find(W + child) if node is not None else None
    return found.get(W + 'val') if found is not None else None


def raw(node, omit=()):
    """Losslessly retain common list/paragraph units, toggles and repeated values."""
    if node is None:
        return {}
    result = {local(k): v for k, v in node.attrib.items() if not local(k).startswith('rsid')}
    for child in node:
        key = local(child.tag)
        if not child.tag.startswith(W) or key in omit or key in SKIP:
            continue
        value = raw(child)
        if key in MANY:
            result.setdefault(key, []).append(value)
        else:
            result[key] = value
    if not result:
        return True
    return result['val'] if set(result) == {'val'} else result


def xml(archive, path):
    root = ET.fromstring(archive.read(path))
    if root.tag.startswith(STRICT_W):
        for element in root.iter():
            element.tag = element.tag.replace(STRICT_W, W, 1)
            element.attrib = {k.replace(STRICT_W, W, 1): v for k, v in element.attrib.items()}
    return root


def related(archive, part=''):
    directory, filename = posixpath.split(part)
    rels = posixpath.join(directory, '_rels', filename + '.rels')
    if rels not in archive.namelist():
        return {}
    out = {}
    for item in xml(archive, rels):
        if item.get('TargetMode') == 'External':
            continue
        target = unquote(item.get('Target', ''))
        path = posixpath.normpath(posixpath.join(directory, target)).lstrip('/')
        out.setdefault(item.get('Type', '').rsplit('/', 1)[-1], path)
    return out


def body_elements(node, wanted):
    """Walk one XML story. Do not double-count nested text boxes or alternate content."""
    for child in node:
        tag = local(child.tag)
        if child.tag == W + wanted:
            yield child
        elif tag == 'AlternateContent':
            branch = next((e for e in child if local(e.tag) == 'Fallback'), None)
            if branch is None and len(child):
                branch = child[0]
            if branch is not None:
                yield from body_elements(branch, wanted)
        elif child.tag.startswith(W) and tag not in {'del', 'moveFrom', 'drawing', 'pict', 'object', 'pPr', 'rPr'}:
            yield from body_elements(child, wanted)


def observe(groups, properties, position):
    if not properties or properties is True:
        return
    key = json.dumps(properties, ensure_ascii=False, sort_keys=True)
    group = groups.setdefault(key, {'raw': properties, 'count': 0, 'examples': []})
    group['count'] += 1
    if len(group['examples']) < 3:
        group['examples'].append(position)


def style_data(node):
    fields = {k: val(node, k) for k in ('name', 'basedOn', 'next', 'link') if val(node, k)}
    fields['type'] = node.get(W + 'type')
    for prop in ('pPr', 'rPr'):
        if node.find(W + prop) is not None:
            fields[prop] = raw(node.find(W + prop))
    return fields


def theme_data(root):
    result = {}
    scheme = root.find('.//{*}fontScheme')
    if scheme is not None:
        for family in scheme:
            if local(family.tag) in {'majorFont', 'minorFont'}:
                result[local(family.tag)] = {
                    e.get('script', local(e.tag)): e.get('typeface')
                    for e in family if e.get('typeface') is not None
                }
    return result


def numbering_data(root, ids, used_styles):
    abstracts = {n.get(W + 'abstractNumId'): n for n in root.findall(W + 'abstractNum')}
    instances = {n.get(W + 'numId'): n for n in root.findall(W + 'num')}
    abstract_ids = {val(instances.get(n), 'abstractNumId') for n in ids}
    candidates = {}
    for aid, definition in abstracts.items():
        linked = [val(level, 'pStyle') for level in definition.findall(W + 'lvl')]
        linked = [style for style in linked if style in used_styles]
        if linked:
            candidates[aid] = linked
    candidate_instances = {aid: [nid for nid, node in instances.items()
                                 if val(node, 'abstractNumId') == aid] for aid in candidates}
    return {
        'instances': {k: raw(instances[k]) if k in instances else None for k in sorted(ids)},
        'abstracts': {k: raw(n) for k, n in abstracts.items() if k in abstract_ids or k in candidates},
        'style_link_candidates': candidates,
        'candidate_instances': candidate_instances,
    }


def inspect(archive):
    main = related(archive).get('officeDocument')
    if main is None:
        raise ValueError('缺少 Word 主文档关联')
    body = xml(archive, main).find(W + 'body')
    if body is None:
        raise ValueError('主文档没有 Word 正文')
    parts = related(archive, main)

    def optional(kind):
        return xml(archive, parts[kind]) if kind in parts else ET.Element('empty')

    style_root = optional('styles')
    styles = {e.get(W + 'styleId'): e for e in style_root.findall(W + 'style')}
    default = next((key for key, e in styles.items() if e.get(W + 'type') == 'paragraph'
                    and e.get(W + 'default') in {'true', '1', 'on'}), None)
    used, char_styles, num_ids = {}, set(), set()
    p_formats, r_formats, sections = {}, {}, []

    def chain(key):
        visited = set()
        while key and key not in visited:
            yield key
            visited.add(key)
            key = val(styles.get(key), 'basedOn')

    for index, paragraph in enumerate(body_elements(body, 'p'), 1):
        pp = paragraph.find(W + 'pPr')
        pid = val(pp, 'pStyle') or default
        sample = used.setdefault(pid or '(implicit)', {'count': 0, 'examples': []})
        sample['count'] += 1
        if len(sample['examples']) < 3:
            sample['examples'].append(index)
        if pp is not None:
            observe(p_formats, raw(pp, {'pStyle', 'sectPr'}), index)
            section = pp.find(W + 'sectPr')
            if section is not None:
                sections.append(raw(section))
        numid = paragraph.find('./' + W + 'pPr/' + W + 'numPr/' + W + 'numId')
        if numid is None:
            for sid in chain(pid):
                style = styles.get(sid)
                if style is not None:
                    numid = style.find('./' + W + 'pPr/' + W + 'numPr/' + W + 'numId')
                if numid is not None:
                    break
        if numid is not None and numid.get(W + 'val') not in {None, '0'}:
            num_ids.add(numid.get(W + 'val'))
        for rid, run in enumerate(body_elements(paragraph, 'r'), 1):
            rp = run.find(W + 'rPr')
            if rp is not None:
                char_id = val(rp, 'rStyle')
                if char_id:
                    char_styles.add(char_id)
                # Retain rStyle together with any local overrides for this run.
                observe(r_formats, raw(rp), [index, rid])

    end_section = body.find(W + 'sectPr')
    if end_section is not None:
        sections.append(raw(end_section))
    families = {pid: list(chain(pid)) for pid in sorted(set(used) | char_styles) if pid != '(implicit)'}
    style_ids = {key for family in families.values() for key in family}
    nums = numbering_data(optional('numbering'), num_ids, set(used))
    return {
        'scope': '正文含表格段落。examples 使用段落号或 [段落号, 文本运行号]，均从 1 开始。相同直接属性按出现次数合并。只报告 XML 声明；节的页眉页脚关联不证明可见。未统计页眉页脚、文本框、删除内容；兼容分支优先读取 fallback。style_link_candidates 仅为编号级别内的样式关联线索。',
        'units': 'sz/szCs 为半磅；pgSz/pgMar、常规缩进与段前后、linePitch 通常为 1/20 磅；缩进 *Chars 为 1/100 字符，段距 *Lines 为 1/100 行。spacing.line 随 lineRule 解释，auto 按 1/240 行，exact/atLeast 按 1/20 磅；显式单位保留原文。',
        'paragraph_usage': used,
        'style_chains': families,
        'styles': {key: style_data(styles[key]) if key in styles else None for key in sorted(style_ids)},
        'document_defaults': raw(style_root.find(W + 'docDefaults')),
        'theme_fonts': theme_data(optional('theme')),
        'sections': sections,
        'direct_paragraph_formats': list(p_formats.values()),
        'direct_run_formats': list(r_formats.values()),
        'numbering': nums,
    }


def main():
    parser = argparse.ArgumentParser(description='只读提取 Word 正文、样式和编号原始证据，以 JSON 输出。')
    parser.add_argument('docx', type=Path)
    args = parser.parse_args()
    try:
        if args.docx.suffix.lower() != '.docx':
            raise ValueError('文件扩展名应为 .docx')
        with ZipFile(args.docx) as archive:
            result = inspect(archive)
    except (OSError, KeyError, ValueError, BadZipFile, RuntimeError, ET.ParseError) as exc:
        parser.exit(2, '无法读取 Word 文档。请检查文件是否可访问、已解密且为有效的 .docx。' + str(exc) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
