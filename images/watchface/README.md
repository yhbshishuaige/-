# BOOTFACE watchface assets

These files are prepared for Xiaomi Smart Band 8 Pro watchface authoring.

Recommended Mi Create setup:

- Device: Xiaomi Smart Band 8 Pro / 336 x 480
- Base background: `background/user_static.png`
- Optional root preview background: `background/root_static.png`
- Boot animation frames: `../boot/boot_000.png` ... `../boot/boot_036.png`
- Time digits: `digits/green/digit_0.png` ... `digit_9.png` plus `colon.png`

Important limitation:

The web demo's triple-tap + `su` state machine is JavaScript. Real Xiaomi band watchfaces generally support static layers, system data, animations, and tap actions, but not arbitrary JavaScript logic. For the real band, use `root_static.png` as an alternate preview/page if your editor supports tap actions, or keep it as a visual variant.

Suggested layout coordinates:

- Time: x=168, y=116, centered
- Date: x=168, y=202, centered
- Divider: x=34..302, y=244
- Data rows: y=270, 304, 338, 372
- Battery icon: x=34, y=420
- Prompt: x=34, y=446
