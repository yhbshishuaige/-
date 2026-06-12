# BOOTFACE

小米手环 8 Pro 的类终端极简表盘原型。

## 尺寸

- 设备：Xiaomi Smart Band 8 Pro
- 画布：336 x 480 px
- 风格：AMOLED 纯黑背景，终端绿点阵启动动画

## 当前原型

- 预览页：`preview/index.html`
- 绘制逻辑：`preview/watchface.js`
- 启动帧导出：`tools/export_boot_frames.py`
- 启动文案：`Hello world!`
- 主界面信息：时间、日期、步数、心率、天气、电量

## 本地预览

当前预览服务：

```powershell
http://127.0.0.1:4173/
```

如果需要重新启动：

```powershell
cd "Z:\表盘自定义\try1\第一次尝试\preview"
python -m http.server 4173 --bind 127.0.0.1
```

## 导出启动帧

```powershell
python "Z:\表盘自定义\try1\第一次尝试\tools\export_boot_frames.py"
```

导出的 PNG 帧会放在：

```text
images/boot/boot_000.png ... boot_036.png
```

## 动画设计

启动时字符从中心逐个拼出：

```text
H
He
Hel
Hell
Hello
Hello 
Hello w
Hello wo
Hello wor
Hello worl
Hello world!
```

每增加一个字符，已有字符串会向左移动，最终让整句保持在屏幕中心附近。动画结束后淡入主表盘。

## 后续制作路线

1. 确认预览里的布局、字号和绿色是否满意。
2. 导出启动动画 PNG 帧到 `images/boot`。
3. 在表盘编辑器中把 PNG 帧配置为启动动画。
4. 把主界面的时间、日期、步数、电量等元素替换为手环支持的动态组件。

现有 `第一次尝试.fprj` 目前还是空项目，暂未直接修改。
