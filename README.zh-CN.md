# Thought2English — 把中文或英文笔记变成地道英文（macOS）

[English](README.md) · **中文**

**一个 macOS 菜单栏 + 窗口小工具：把你随手写的中文/英文笔记，一键变成两份英文：口语脚本（Spoken Script）和正式写作（Formal Writing）。使用你自己的 Gemini 或 DeepSeek API Key。**（仓库名是 `englearn`，App 名叫 Thought2English。）

![Thought2English 写作页：草稿变成口语脚本、正式写作和说明](Assets/screenshots/writeeng.png)

## 安装

```bash
brew tap risingjerry/thought2english
brew install --cask thought2english
```

更新：`brew upgrade --cask thought2english`。也可以从 [Releases](https://github.com/risingjerry/englearn/releases) 下载 zip，或自己编译（见下文）。

装好后打开 **Settings**，选择 Provider 并填入 API Key。

## 亮点

- **一次两份输出**：Spoken Script（更口语、更像真实表达，偏圈内表达）和 Formal Writing（更正式、适合工作）。也可以只要其中一份。
- **自带 Key**：支持 Gemini / DeepSeek，模型和 Base URL 可改。
- **可调**：领域（General、Life、Food、Fitness、AI、Web3、Reading、Investing）、术语程度（Plain / Native）、风格（TradFi / Research 或 Crypto Twitter）、自定义词表。
- **说明**解释为什么这样改，**Compare** 对比视图高亮新增内容。
- 用系统语音**朗读**，**复制**，在 **History** 里翻历史。
- **菜单栏小窗**，随手就能用。

## 截图

![写作页（中文输入）](Assets/screenshots/writecn.png)

![历史](Assets/screenshots/history.png)

![设置](Assets/screenshots/settings.png)

菜单栏小窗：

![菜单栏：写作](Assets/screenshots/menubar-write.png)

![菜单栏：历史](Assets/screenshots/menubar-history.png)

![菜单栏：设置](Assets/screenshots/menubar-settings.png)

## 使用

1. 打开 Thought2English
2. 在 Write 页粘贴中文或英文
3. 选择输出（Spoken / Formal / Both）
4. 点 Generate，然后复制、对比或朗读

默认值：DeepSeek 的 Base URL 为 `https://api.deepseek.com`、模型 `deepseek-chat`；Gemini 的 Base URL 为 `https://generativelanguage.googleapis.com`、模型 `gemini-3-flash-preview`。

## 工作原理

App 把你的文字、领域、术语程度、风格和词表拼成提示词，发给你选的模型服务，再把回复拆成 Spoken、Formal 和说明三部分。历史记录存在本地 SQLite 文件里。它是 SwiftUI 应用，用 Swift Package Manager 构建，没有第三方依赖。

## 限制与要求

- macOS 13 或更高。
- 需要你自己的 Gemini 或 DeepSeek API Key，费用由服务商计。
- App 未经 Apple 公证。
- API Key 以**明文**存在 App 偏好设置里（暂未使用钥匙串），详见 [PRIVACY.md](PRIVACY.md)。
- 没有自动化测试；CI 只检查能否编译。

## 从源码构建

```bash
git clone https://github.com/risingjerry/englearn.git
cd englearn
./scripts/package_app.sh        # 生成 dist/Thought2English.app
open dist/Thought2English.app
```

## 常见问题

### 怎么把粗糙的中文笔记变成自然的英文？
粘贴到 Write 页点 Generate，会得到口语脚本和正式写作两个版本，以及措辞说明。

### 用的是哪个 AI 模型？
Gemini 或 DeepSeek，用你自己的 Key。可以在 Settings 里改模型名和 Base URL。

### 我的文字和 Key 会被上传吗？
只有点 Generate 或 Test Connection 时，才会把你的文字（以及词表、选项）发给你选的服务商，没有其他服务器。Key 以明文保存在本机偏好设置里。详见 [PRIVACY.md](PRIVACY.md)。

### 为什么 App 叫 Thought2English，仓库叫 englearn？
Thought2English 是产品名；`englearn` 是最初的包名和仓库名，可执行文件仍沿用。

### macOS 打不开这个 App？
App 未经公证。右键选择「打开」，或到「系统设置 → 隐私与安全性」里允许。

### 历史记录存在哪？怎么删？
在 `~/Library/Application Support/Thought2English/history.sqlite`，删掉这个文件即可。

## 卸载

```bash
brew uninstall --cask --zap thought2english
```

或者把 `Thought2English.app` 拖进废纸篓，并删除 `~/Library/Application Support/Thought2English` 和偏好设置文件 `~/Library/Preferences/com.englearn.app.plist`（这也会清掉保存的 API Key）。移除 tap：`brew untap risingjerry/thought2english`。

## 许可证

MIT，见 [LICENSE](LICENSE)。

---

如果它让你的英文更像你自己，点个 star 能让更多人找到它。

[![Star History Chart](https://api.star-history.com/svg?repos=risingjerry/englearn&type=Date)](https://star-history.com/#risingjerry/englearn&Date)
