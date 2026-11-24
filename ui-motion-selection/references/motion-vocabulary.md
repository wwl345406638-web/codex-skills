# 中英动效术语与选型

索引依《网页交互术语》七页的顺序整理，共 77 项。以下场景、数值和降级写法是便于设计与实现的建议起点。按用户动作查相关一组，将选中的词与目标、参数和终态一起写进设计输入。

## 1. 滚动交互 · Scroll Interaction

| 术语 | 如何写进页面设计 |
| --- | --- |
| Parallax Scrolling 视差滚动、Scroll Zoom 滚动缩放 | 产品故事背景可随滚动位移 0→24 px，或缩放 1→1.04；选一个轴或属性，标题、按钮保持原位。减弱动态时固定背景。 |
| Smooth Scrolling 平滑滚动、Inertial Scrolling 惯性滚动 | 目录跳转给出锚点、固定导航偏移和焦点去向；触控滑动优先系统惯性，用户输入可打断。减弱动态时立即到达锚点。 |
| Scroll Reveal 滚动显现 | 首屏以下的案例进入视口约 15% 时，Y 从 12 px 到 0，透明度从 0 到 1，220 ms，一次。静态或无脚本时内容可读。 |
| Scroll Scrubbing 滚动进度绑定、Scroll Pinning 滚动吸附固定、Scrollytelling 滚动叙事 | 讲解三步工序时可让图示固定一屏，按章节滚动进度切换三态。分别给出进度区间、固定范围、结束位置；窄屏改顺序图文。 |
| Horizontal Scroll 横向滚动、Scroll Snap 滚动吸附 | 横向产品图集可按每张起点吸附，提供上一张／下一张入口。保留纵向浏览，键盘可离开图集。 |

## 2. 指针交互 · Cursor Interaction

| 术语 | 如何写进页面设计 |
| --- | --- |
| Magnetic Hover 磁吸交互、Elastic Interaction 弹性交互 | 展示按钮只移动内层，最大约 4 px，离开后回到原点；拖放成功可轻微回弹。外层热区固定，告警和高频导航用稳态反馈。 |
| Cursor Follower 光标跟随、Cursor Trail 鼠标拖尾 | 只在创意展示区使用。给出跟随延迟或尾迹寿命，移出即清除；保留系统指针，覆盖层设为不接收点击。触屏用静态形象。 |
| Spotlight Effect 聚光灯效果、Mouse Parallax 鼠标视差、3D Tilt Effect 三维倾斜 | 稀疏产品卡按目的择一，如 120 px 半径的光斑、前景最大 6 px 位移或图片绕 X/Y 轴 ±3°。仅在精细指针下启用，复位后文字和点击目标稳定。 |
| Hover Reveal 悬浮显现、Hover Distortion 悬浮扭曲 | 补充说明在悬停和键盘聚焦时出现，触屏可点开；图片形变限定在缩略图蒙层。主要标签常显。 |
| Ripple Effect 涟漪效果 | 按压确认可在按钮内从触点扩散一次，裁切在热区内；键盘激活可改底色，成功或失败另有明确结果。 |

## 3. 页面转场 · Page Transition

| 术语 | 如何写进页面设计 |
| --- | --- |
| Shared Element Transition 共享元素转场、FLIP Animation 布局动画 | 从产品列表进入详情时，用同一产品 ID 对应两处缩略图。FLIP 记录起止布局，从反向变换恢复终态；中断或关动效时直接落到当前页面。 |
| Morphing Transition 形态变换、Seamless Transition 无缝转场 | 指定过渡前后哪个对象保持身份，例如同一张图片从缩略框展开到主图。用共同锚点、占位与加载完成时机维持连续。 |
| Mask Reveal 遮罩显现、Clip-path Transition 裁剪路径转场、Curtain Reveal 幕布式转场 | 在案例封面用一种揭示方式，注明遮罩源点、范围与持续时间；主导航和操作区始终可点。 |
| Crossfade 交叉淡化、Depth Transition 景深转场 | 切换产品视图可让旧图淡出、新图淡入，共 180 ms；需要空间层级时再定义前后景的缩放或模糊。旧层退出时移除其输入焦点。 |
| Staggered Animation 交错动画 | 少量同组元素依次出现，可从间隔 40–50 ms 起调，给整组设完成时间。长表格直接出现。 |

## 4. 文字排版 · Typography Animation

| 术语 | 如何写进页面设计 |
| --- | --- |
| Kinetic Typography 动态字体排版、Variable Font Animation 可变字体动画 | 对短标题指定移动方向或可用字轴，例如已加载可变字体的 wght 由 450 到 600；校验字体支持中文，预留最大占宽。 |
| Text Mask Reveal 文字遮罩显现、Split Text Animation 文字拆分动画、Staggered Text Reveal 文字逐字交错显现 | 按行、词或字决定分组与时间差；中文注意断行。为读屏保留完整文本，把重复的装饰字形隐藏于无障碍树。 |
| Text Scramble 文字解码重组、Typewriter Effect 打字机效果 | 可给短装饰语设置一次播放及结束文案；减弱动态时直接显示全文。业务单号、导航、错误与按钮标签立即可读。 |
| Text Marquee 文字跑马灯、Rolling Text 文字滚动切换 | 辅助公告轮播提供常驻入口和可触摸、可键盘操作的暂停键。滚动切词预留最长文本宽度；关动效后静态呈现。 |
| Text Shine 文字流光、Blur Reveal 模糊渐清显现、Gradient Text Animation 文字动态渐变 | 展示标题选其一。写明高光次数、模糊半径终值 0 或渐变范围；全过程保持可读，正文使用稳定字色。 |

## 5. 材质与光影 · Material & Lighting

| 术语 | 如何写进页面设计 |
| --- | --- |
| Glassmorphism 玻璃拟态、Liquid Glass 液态玻璃、Refraction Effect 光学折射 | 浮层先定底色、不透明度、模糊半径及描边，再考虑装饰边缘的折射。地图文字或读数背后用稳定底色；性能受限时使用实底。 |
| Specular Highlight 镜面高光、Glow Effect 辉光效果 | 产品表面指定光源方向及高光宽度；点位可用固定窄光晕配轮廓和文本。避免高光遮住刻度。 |
| Animated Gradient 动态渐变、Mesh Gradient 网格渐变、Aurora Effect 极光动效 | 为品牌封面选色标、节点位置与变化范围；可先画静态网格渐变，确有叙事需要再加运动。 |
| Border Beam 边框流光、Shimmer Effect 微光扫过 | 营销卡的边缘流光或完成后的表面扫光只播一次；加载骨架可短时扫光，完成或失败即停止。告警级别有可读标签。 |
| Noise Texture Animation 动态噪点纹理 | 仅覆盖背景，明确颗粒尺度、透明度和覆盖面积；静态颗粒可提供同样材质感并降低重绘。 |

## 6. 沉浸式与创意动效 · Immersive Motion

| 术语 | 如何写进页面设计 |
| --- | --- |
| WebGL Interaction 实时三维交互、Shader Animation 着色器动画、Ray Marching 光线步进渲染 | 旋转查看模型时写明输入、镜头限制及目标物。着色器和光线步进只在材质或体积确实需要时采用；实测目标设备，保留静态图和信息列表。 |
| Particle Morphing 粒子形态变换、Interactive Particle System 交互式粒子系统 | 写清两种形态、采样数量、输入影响半径和回位条件。展示粒子与真实传感点使用独立图层和图例。 |
| Fluid Simulation 流体模拟、Image Displacement 图像置换变形 | 视觉展示可指定流动范围或置换图及最大偏移。用作工业示意时标注来源；工程流量、流向与水位从业务数据读取。 |
| Procedural Animation 程序化动画、Physics-based Animation 基于物理的动画 | 写明驱动输入、约束和终止条件，例如拖动释放后夹紧在允许行程。静态图指定可复现的一帧。 |
| Camera Dolly 相机推进与拉远、Depth of Field 景深效果、Chromatic Aberration 色散效果 | 相机推进写观察目标、起止位置与复位姿态；景深写焦点，色散限于装饰边缘。标注层、读数及操作保持清晰。 |
| 3D Model Exploded View 三维模型爆炸视图、Interactive Point Cloud 交互式点云 | 拆解给出部件 ID、轴向、位移与收拢入口。点云给出坐标系、点大小、抽稀和选取规则。无模型或点云数据时用注明来源的示意视图。 |

## 7. 底层运动属性 · Motion Principles

| 术语 | 怎样指定参数 |
| --- | --- |
| Easing 缓动、Cubic Bézier 三次贝塞尔曲线 | 入场一般 ease-out，退出可稍短并用 ease-in。示例为 180 ms、cubic-bezier(0.2,0,0,1)，时长与曲线分别记录。 |
| Spring Physics 弹簧物理、Damping 阻尼、Stiffness 刚度、Overshoot 超调 | 先确定是否允许越过终点及稳定时间。例如对采用质量–弹簧–阻尼模型的拖放反馈，可从 mass 1、stiffness 250、damping 30 试起，按实际库与手感调节。关键读数和主导航到位即停。 |
| Momentum 动量、Lerp 线性插值 | 拖动结束后若需惯性，指定速度边界与衰减；平滑跟随需给出时间尺度，逐帧插值按时间差调整，避免刷新率改变手感。 |
| Stagger 交错延迟、Choreography 动效编排 | Stagger 描述同组相邻元素的启动间隔。编排描述主次与相依关系，例如先更新选中行，再让明细淡入；无需让用户等待整组播完。 |

## 原技能中的两种补充反馈

- **悬停上浮**适用于留白充足的可点击卡片。只移动视觉层约 2 px，键盘用焦点环；密集表格改用行底色或边线。
- **数字递增**适用于首次露出的非关键演示 KPI。标出终值、单位和精度；实时值、告警值、业务关键数以及减少动态效果时直接呈现终值。
