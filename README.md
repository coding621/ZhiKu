# 知库 ZhiKu · 本地知识库

> 零云端、零账号的本地知识库：把文档丢进文件夹，全库秒搜。
> 提供 **浏览器版** 与 **独立桌面版（exe）** 两种形态，核心同一套代码。

- ✅ 全文搜索：中文两字即可命中，命中词高亮，支持多词 AND 与目录过滤
- ✅ 多格式：Markdown / TXT / HTML 剪藏 / PDF / Word / Excel / PPT / 图片
- ✅ 多知识库目录：最多 100 个，界面里增删，保存即重建索引
- ✅ 独立 exe：pywebview + WebView2 原生窗口，不依赖浏览器
- ✅ 开机自启动开关（写入当前用户启动项）
- ✅ 索引缓存自动增量更新；删除索引文件即可完全重建
- ✅ 无第三方运行时依赖（Python 标准库 HTTP 服务 + SQLite）

---

## 目录

- [快速开始](#快速开始)
- [使用说明](#使用说明)
- [支持的格式](#支持的格式)
- [两种形态](#两种形态)
- [工作原理](#工作原理)
- [从源码构建](#从源码构建)
- [API 一览](#api-一览)
- [配置与数据位置](#配置与数据位置)
- [常见问题](#常见问题)

---

## 快速开始

### 方式一：桌面版（推荐）

1. 下载 `ZhiKu.exe`（或从 [Releases](../../releases) 获取）
2. 双击运行 —— 弹出独立应用窗口，不打开浏览器
3. 点侧栏 **⚙ 设置** → 添加电脑上的任意文件夹作为知识库目录
4. 丢文档进去 → 侧栏「重新扫描」→ 开始搜索

### 方式二：浏览器版（开发/便携）

需要 Python 3.10+，以及解析库：

```powershell
pip install pypdf python-docx openpyxl python-pptx   # 可选，装了才能解析对应格式
python kb-server.py                                   # 打开 http://127.0.0.1:8360/
```

---

## 使用说明

| 操作 | 方式 |
|---|---|
| 搜索 | 顶部搜索框输入，**`/`** 键随时聚焦；支持多词（空格 = 且） |
| 浏览 | 侧栏按 **知识库目录 → 一级子文件夹** 分组点击过滤 |
| 阅读 | 点击列表项，右侧阅读区打开；Markdown 自动渲染排版 |
| 记笔记 | **＋ 新建笔记**，选择目标目录，写 Markdown 直接保存为 `.md` 文件 |
| 加目录 | **⚙ 设置** → 输入路径 → 添加 → 保存（≤ 100 个） |
| 开机自启 | **⚙ 设置** → 勾选「开机自动启动」→ 保存 |
| 手动同步 | 侧栏「重新扫描」（外部新增/修改的文件） |
| 快捷键 | `/` 聚焦搜索，`Esc` 关闭弹窗/返回列表 |

### 知识库目录结构

每个配置的目录就是一个「知识库」，其**一级子文件夹自动成为侧栏分组**：

```text
E:\资料\技术笔记\          ← 在设置里添加这个目录
├── 架构\                  ← 侧栏分组：技术笔记/架构
│   └── 分布式系统.md
├── 面试\                  ← 侧栏分组：技术笔记/面试
│   └── 题集.pdf
└── 速查.md                ← 直接属于根：技术笔记
```

---

## 支持的格式

| 格式 | 索引 | 阅读视图 |
|---|:---:|---|
| `.md` `.txt` `.csv` `.json` `.xml` `.yaml` 等纯文本 | ✅ | Markdown 渲染 / 等宽原文 |
| `.html` `.htm`（网页剪藏） | ✅ | 沙箱 iframe（脚本禁用） |
| `.pdf` | ✅ | 内嵌 PDF 查看器 |
| `.docx` | ✅ | 抽取文本预览 + 打开原文件 |
| `.xlsx` `.xlsm` | ✅ | 逐表抽取文本预览 |
| `.pptx` | ✅ | 逐页抽取文本预览 |
| `.png` `.jpg` `.gif` `.webp` `.svg` 等图片 | — | 直接查看 |

> 不支持旧版 `.doc` / `.xls` / `.ppt`（另存为新版即可）。图片未做 OCR。

---

## 两种形态

| | 浏览器版 | 桌面版 exe |
|---|---|---|
| 入口 | `python kb-server.py` | 双击 `ZhiKu.exe` |
| 界面 | 系统浏览器标签页 | pywebview 原生窗口（WebView2 内核） |
| 依赖 | Python 环境 | 无（Win10/11 自带 WebView2 运行时） |
| 数据目录 | 脚本所在目录 | `%LOCALAPPDATA%\ZhiKu` |
| 适用 | 开发调试、已有 Python 环境 | 日常使用、分发给他人 |

命令行参数（两种形态通用）：

```text
--port 8360      指定端口（默认 8360，被占用时自动 +1）
--no-browser     不自动打开浏览器
--gui            强制独立窗口模式
--no-window      exe 下退回浏览器模式
--rescan-only    只重建索引后退出
```

---

## 工作原理

```mermaid
flowchart LR
    A["知识库目录<br>（文件即数据）"] -->|"启动/手动扫描<br>mtime 增量比对"| B["文本抽取<br>md/html/pdf/docx/xlsx/pptx"]
    B --> C["SQLite 索引<br>index.db"]
    C -->|"① LIKE 多词预筛"| D["② Python 计分<br>词频 + 标题加权 + 时间衰减"]
    D --> E["③ 摘要截取<br>前端高亮 <mark>"]
    E --> F["按格式分流渲染<br>md / pdf / 沙箱 html …"]
```

- **文件是唯一数据源**：`index.db` 只是可随时删除的缓存；笔记功能直接写 `.md` 文件进目录
- **搜索不用分词器**：中文 2 字查询在 FTS5 trigram 下查不到，个人规模语料 `LIKE` 预筛 + 自建计分更可靠（实测 5000 篇 / 200MB 约 300ms）
- **安全**：所有渲染前先 HTML 转义（防 XSS）；文件读取做根目录越界校验（防路径穿越）；HTML 剪藏在无权限沙箱中渲染

---

## 从源码构建

### 环境

- Windows 10/11，Python 3.10+
- 打包另需：`pywebview`、`pyinstaller`（构建虚拟环境与运行环境分离）

### 开发运行

```powershell
git clone <repo> && cd <repo>
python kb-server.py            # 浏览器模式
python kb-server.py --gui      # 独立窗口模式（需先 pip install pywebview）
```

### 打包 exe

```powershell
python -m venv _build\venv
_build\venv\Scripts\python -m pip install pywebview pyinstaller pypdf python-docx openpyxl python-pptx
_build\venv\Scripts\python -m PyInstaller zhiiku.spec --noconfirm
# 产物：dist\ZhiKu.exe（单文件，约 26MB）
```

打包要点（`zhiiku.spec`）：

- `datas`：把 `static/index.html` 打进包内，运行时从 `sys._MEIPASS` 读取
- `console=False`：无控制台黑窗口
- `hiddenimports`：pywebview 的 `edgechromium` / `winforms` 后端

---

## API 一览

本地服务只监听 `127.0.0.1`，无鉴权（纯本机使用）。

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/` | 前端页面 |
| GET | `/api/meta` | 目录分组、计数、设置概要 |
| GET | `/api/search?q=&root=&sub=` | 全文搜索（关键词 / 目录 / 子目录） |
| GET | `/api/doc?path=` | 文档详情与正文 |
| GET | `/api/raw?path=` | 原始文件（阅读内嵌 / 下载） |
| POST | `/api/note` | 新建 Markdown 笔记 `{folder,title,body}` |
| GET | `/api/settings` | 设置（目录列表、自启动状态） |
| POST | `/api/settings` | 保存设置 `{roots[],autostart}`（≤100 个目录） |
| GET | `/api/rescan` | 手动增量重建索引 |

---

## 配置与数据位置

| | 浏览器版（开发） | 桌面版 exe |
|---|---|---|
| 配置 | `<脚本目录>\config.json` | `%LOCALAPPDATA%\ZhiKu\config.json` |
| 索引 | `<脚本目录>\index.db` | `%LOCALAPPDATA%\ZhiKu\index.db` |
| 默认知识库 | `<脚本目录>\kb\` | `%LOCALAPPDATA%\ZhiKu\kb\` |

`config.json` 示例：

```json
{
  "port": 8360,
  "autostart": false,
  "roots": ["E:\\资料\\技术笔记", "D:\\工作\\项目文档"]
}
```

可直接编辑该文件管理目录列表；`autostart` 建议通过设置界面修改（会同步写注册表启动项）。

---

## 常见问题

**搜索变慢了？**
搜索耗时与语料总字节数成正比。几千篇以内无感；如需更快，删除 `index.db` 后重启可重建（不会动你的文件）。

**自启动后找不到窗口？**
自启动指向 exe 的当前位置，移动 `ZhiKu.exe` 后需在设置里重开一次开关。

**打开 exe 提示缺少 WebView2？**
Win10/11 一般自带。缺失时安装微软官方 [WebView2 Runtime](https://developer.microsoft.com/microsoft-edge/webview2/)（用户级安装，无需管理员）。

**分享给别人注意什么？**
`kb/` 或知识库目录里放的是你的个人文档，上传 GitHub 时请确认不要提交真实数据（本仓库 `.gitignore` 已排除索引、配置与构建产物）。

---

## 仓库结构

```text
.
├── kb-server.py          # 后端服务 + GUI 入口（标准库 HTTP + 索引 + 抽取）
├── static/
│   └── index.html        # 前端单文件（界面 + 搜索 + 离线 Markdown 渲染器）
├── zhiiku.spec           # PyInstaller 打包配置
├── kb/                   # 示例知识库（可替换为你自己的内容）
│   ├── 工作资料/
│   ├── 技术文档/
│   ├── 学习资料/
│   └── 收藏/
├── config.json           # 运行配置（本地，不入库）
├── index.db              # 搜索索引缓存（本地，不入库）
└── dist/
    └── ZhiKu.exe         # 打包产物（本地，不入库）
```
