# 原型验证记录

日期：2026-10-17。对象：本目录 `app.html`；依据：SPEC.md 的 R-001、R-002 与 [DESIGN.md](DESIGN.md)。使用本机 Chromium，通过 `http://127.0.0.1:8876/app.html` 运行，Playwright 执行交互和几何检查，再逐张查看关键截图。

## 实际结果

[33 项自动检查](output/playwright/results.json)全部通过，脚本见 [checks.js](output/playwright/checks.js)，运行原始输出见 [results.txt](output/playwright/results.txt)。

| 检查 | 实际结果 |
| --- | --- |
| 正式集合 | 保留既有一件藏品与原有长标题；未补造说明或增加测试藏品 |
| 列表 → 详情 → 返回 | 原件和混合样本均能打开正确详情；完整标题、完整说明及段落保留；返回后内容顺序不变 |
| 滚动位置与焦点 | 键盘返回恢复原入口；在 375px 长列表中浏览器后退前后 scrollY 均为 2803，焦点恢复到原入口；浏览器前进可重新进入同件详情 |
| 1440 / 768 / 375px | 分别为三列、两列、单列；列表及详情无横向滚动；标题最多两行、摘要最多三行；入口独立、无重叠，触控高度至少 44px |
| 混合文字 | 覆盖短标题、原有长标题、极长标题、长说明、无说明；卡片省略可见，详情保留全文 |
| 缺失与空态 | 无说明显示“暂无说明”；1440px、375px 空集合显示“还没有藏品”，没有无效按钮 |
| 键盘 | Tab 到查看入口，Enter 打开，Shift+Tab 到返回入口，Enter 返回；查看和返回均有可见焦点 |
| 放大阅读 | 在 1440 / 768 / 375px 下用 CSS `zoom: 2` 检查 200% 放大；无横向溢出，列表自动减少列数，详情全文及返回行为正常 |
| 直接打开 / 无效地址 | 直接打开详情可以返回收藏；不存在的藏品地址显示列表 |
| 运行错误 | 验证期间未捕获 JavaScript 运行错误。首次启动的 favicon 404 已通过内嵌空图标解决 |

## 截图复核

- [正式列表 1440px](output/playwright/list-1440.png)
- [混合文本 1440px](output/playwright/mixed-1440.png)、[768px](output/playwright/mixed-768.png)、[375px](output/playwright/mixed-375.png)
- [完整详情 1440px](output/playwright/detail-1440.png)、[375px](output/playwright/detail-375.png)
- [200% 放大列表](output/playwright/list-zoom-200.png)、[200% 放大详情](output/playwright/detail-zoom-200.png)
- [空收藏 1440px](output/playwright/empty-1440.png)、[375px](output/playwright/empty-375.png)

已查看上述关键截图：暖纸色、墨色衬线标题和铜色操作与设计依据一致；卡片边界、留白和标题—摘要—入口的顺序清楚；长标题与摘要出现省略而未挤压操作；详情保持连续阅读宽度。测试截图的虚构内容均标明“虚构测试”，只通过浏览器响应替换集合用于检查，不写入正式页面数据。

实际使用的文字色与两种背景按相对亮度公式计算，最低文字对比度为 5.43:1；焦点色与背景为 8.20:1 或更高。操作同时使用文字与下划线识别。

## 验证边界

本次检查覆盖 Chromium 及上述视口与样本。200% 检查采用 CSS 放大模拟，未验证浏览器菜单原生缩放；未进行屏幕阅读器和其他浏览器实测，因此不声称通过完整无障碍认证或跨浏览器验收。当前单文件原型的两项浏览要求在上述检查范围内通过，没有发现阻断问题。

## 复跑

在本目录运行 `python3 -m http.server 8876 --bind 127.0.0.1`。另一个终端用 Playwright CLI 打开该地址，将 `output/playwright/checks.js` 的完整函数作为 `run-code` 参数执行。脚本输出检查数组，并重新保存截图；不会修改正式集合。自动脚本只操作本地原型，无在线服务依赖。
