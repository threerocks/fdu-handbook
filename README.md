# 从 FDE 到 FDU：重新定义 AI 交付

一套以 Markdown 为唯一正文来源的中文 AI 交付手册。包含导读与序言、八章正文、补充材料、九张封面和六张机制图。

## 阅读

- [在线课程网站](https://threerocks.github.io/fdu-handbook/)
- [下载 PDF 电子书](https://threerocks.github.io/fdu-handbook/downloads/fdu-handbook.pdf)
- [GitHub 源码仓库](https://github.com/threerocks/fdu-handbook)
- [章节源码](chapters/)
- [编排记录](docs/editorial-notes.md)
- [质量检查](docs/quality-report.md)

网页使用 [haidang1810/md2html](https://github.com/haidang1810/md2html) 的 Claude 风格模板，保留纸色背景、橙色交互、侧栏目录、手机抽屉目录和深浅色切换。为章节导航、离线资源与 PDF 分页增加了项目主题层。上游模板原文件保留在 `vendor/md2html/`。

封面沿用选定参考图的白色陶瓷、拉丝金属与钴蓝核心。机制图按更新后的 [Diagram Design](https://github.com/cathrynlavery/diagram-design) 规范制作，HTML 为图稿源文件，SVG 用于网页和 PDF。

## 修改正文与重新构建

日常只编辑 `chapters/*.md`，章节名称与顺序由 `book.json` 管理。不要直接改生成的 HTML 或 PDF。

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
npm install
npx playwright install chromium
python3 scripts/build.py
npm run pdf
```

`build.py` 生成 `dist/site/`。`npm run pdf` 在独立无头浏览器中检查桌面与手机页面，输出两个相同的 PDF 文件：

- `dist/fdu-handbook.pdf`
- `dist/site/downloads/fdu-handbook.pdf`，对应网页下载按钮

macOS 默认使用已安装的 Google Chrome；也可通过 `CHROME_PATH` 指定浏览器。在其他平台使用 Playwright 安装的 Chromium。构建和阅读无需在线字体或 CDN。

```sh
python3 -m http.server 8764 --bind 127.0.0.1 --directory dist/site
```

然后打开 `http://127.0.0.1:8764`。

## 工程结构

| 路径 | 用途 |
| --- | --- |
| `chapters/` | 可维护正文，唯一正式内容源 |
| `source/完整原稿.md` | 收到的原稿，按字节保留 |
| `source/*ledger.json` | 截断、重复与字符图的整理记录 |
| `assets/covers/` | 整书与八章封面，已清理嵌入隐私元数据 |
| `assets/diagrams/` | 六张机制图的 HTML 与 SVG |
| `theme/` | 网页、打印样式与项目局部图稿配色 |
| `scripts/` | 导入、构建、PDF 导出与校验脚本 |
| `vendor/` | 上游渲染模板及其许可证 |
| `dist/site/` | 可直接打开或托管的完整静态网站 |
| `qa/` | 本地检查结果与截图，不用于公开分发 |

`scripts/prepare_content.py` 是首次导入记录，不属于日常构建流程。它不会在已有章节时覆盖正文。`scripts/create_diagrams.py` 可重建 HTML 图稿，随后按 Diagram Design 的导出工具生成 SVG。

## GitHub 发布

`main` 分支保存 Markdown、图片与构建脚本；`gh-pages` 分支保存已检查的静态网站与 PDF。GitHub Pages 从 `gh-pages` 的根目录提供服务。

修改后先构建并检查，再发布成品：

```sh
python3 scripts/build.py
npm run pdf
python3 scripts/check_content.py
git add chapters assets scripts theme book.json README.md
git commit -m "Update handbook"
git push origin main
python3 scripts/publish_pages.py
```

发布脚本使用 Git 现有凭据，将成品增量提交到 `gh-pages`，不会强制覆盖远程历史。

本工程未替作者指定正文的开放许可。第三方模板保留其 MIT 许可证；自行创作正文与图片的许可应在公开版本中另行明确。仅上传到公开仓库并不自动授予读者转载或改编权。

## 字体

PDF 随工程附带 Noto Sans CJK SC 的离线字体，许可证在 `assets/fonts/LICENSE.txt`。原始下载地址记录在 `source/upstream-versions.json`。为避免 PDF 复制文本时导出部首字符，打印字体移除了未使用的 CJK 部首及兼容字别名；常规汉字字形没有修改。

图稿内嵌本版所需字符的字体子集。修改图中文字后，可用官方原始 OTF 运行 `python3 scripts/prepare_font.py <字体路径>`，再运行 `python3 scripts/create_diagrams.py` 和 `python3 scripts/export_diagrams.py` 重建图稿。字体准备额外需要 `fonttools[woff]`。
