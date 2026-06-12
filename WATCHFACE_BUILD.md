# BOOTFACE 真机表盘制作说明

目标设备：小米手环 8 Pro，336 x 480。

## 已生成内容

- `micreate_project/BOOTFACE.fprj`：Mi Create / EasyFace 风格的草稿项目。
- `micreate_project/images/`：草稿项目使用的平铺 PNG 资源。
- `images/boot/`：启动动画帧，`boot_000.png` 到 `boot_036.png`。
- `images/watchface/`：完整素材包，包含普通模式、root 模式、数字、图标、标签和预览图。

## 推荐打开方式

1. 打开 Mi Create。
2. 选择小米手环 8 Pro / 336 x 480 设备。
3. 打开 `micreate_project/BOOTFACE.fprj`。
4. 如果图片资源没有自动加载，确认 `micreate_project/images/` 与 `BOOTFACE.fprj` 在同一目录层级下，或在 Mi Create 中重新绑定图片。
5. 检查以下动态元素：
   - Hours：小时
   - Minutes：分钟
   - Month：月份
   - Day：日期
   - BatteryPercent：电量百分比
6. 构建导出表盘包。

## 重要限制

网页 Demo 里的三连击、自动输入 `su`、切换 root 模式，是 JavaScript 状态机。真实小米手环表盘通常不支持任意 JavaScript，所以不能保证原样实现。

可行替代方案：

- 普通真机版：使用 `images/micreate/0000.png` 作为背景，动态显示时间、日期和电量。
- root 视觉版：使用 `images/watchface/background/root_static.png` 做成另一张静态表盘。
- 如果 Mi Create 支持点击动作或多页面，可以尝试把普通背景和 root 背景做成两个页面，用点击区域切换。

## 资源说明

`micreate_project/images/` 是为了尽量适配 Mi Create 的平铺资源：

- `0000.png`：普通模式背景，不含时间、日期、电量百分比。
- `0001.png` 到 `0010.png`：大号时间数字 0-9。
- `0011.png`：大号冒号。
- `0012.png` 到 `0021.png`：小号数字 0-9。
- `0022.png`：日期小圆点。
- `0023.png`：百分号。
- `0024.png`：透明空白占位图。

`images/watchface/` 是更完整的设计素材：

- `background/user_static.png`：普通绿色完整预览背景。
- `background/root_static.png`：root 暗红完整预览背景。
- `digits/`：绿色和红色数字切片。
- `icons/`：电量、提示符、光标。
- `labels/`：终端文字标签。

## 重新生成

```powershell
python tools\export_boot_frames.py
python tools\export_watchface_assets.py
python tools\export_micreate_project.py
```

## 安装到手环

Mi Create 编译成功后，通常会在 `output` 目录生成表盘文件。安装方式取决于你使用的手机和工具：

- 官方 Mi Fitness：一般只支持有限照片表盘，不适合完整自定义 `.bin`。
- Android 社区方案：常见做法是通过支持自定义表盘导入的工具或改版 Mi Fitness 安装。

如果你把 Mi Create 导出的文件发给我，我可以继续帮你检查命名、资源和结构。
