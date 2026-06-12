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
- 交互彩蛋：三连击表盘后自动输入 `su`，切换为 root 暗红模式；root 模式下再次三连击自动输入 `exit` 返回普通模式

## 本地预览

当前预览服务：

```powershell
http://127.0.0.1:4173/
```

如果预览服务已经开着，直接在浏览器打开：

```text
http://127.0.0.1:4173/
```

如果需要重新启动本地演示：

```powershell
cd "Z:\表盘自定义\try1\第一次尝试\preview"
python -m http.server 4173 --bind 127.0.0.1
```

## GitHub Pages Demo

仓库根目录的 `index.html` 是公开演示入口。推送到 GitHub 后，可以在仓库 Settings -> Pages 中选择从 `main` 分支的根目录发布。

当前远程仓库对应的项目页地址预计是：

```text
https://yhbshishuaige.github.io/-/
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

## 交互设计

- 普通模式底部提示符是 `$` 加实心闪烁光标。
- 连续点击表盘三下，会在底部自动输入 `su`，随后切换到 root 模式。
- root 模式提示符变成 `#`，整体配色变成暗红色。
- root 模式下连续点击表盘三下，会自动输入 `exit` 并返回普通模式。

## 后续制作路线

1. 确认预览里的布局、字号和绿色是否满意。
2. 导出启动动画 PNG 帧到 `images/boot`。
3. 在表盘编辑器中把 PNG 帧配置为启动动画。
4. 把主界面的时间、日期、步数、电量等元素替换为手环支持的动态组件。

现有 `第一次尝试.fprj` 目前还是空项目，暂未直接修改。
