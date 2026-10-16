# 胖东来专供版个人网站

线上地址：https://harry-lyl.github.io/pdl-resume-site/

从 `../site-mirror` 复制改写，内容对齐《胖东来专供版简历》(`lyl-v10-AIGC中台版.pen` 中 x=11200 的三页)，目标职位：胖东来商贸集团 · 数据工程（数据分析与产品方向）。

## 与原版的关键差异

- 所有文案中英双语同步改写在两个文件：`index.html`（SSR）+ `_next/static/chunks/0ccz6j2vqtl32.js`（客户端数据源，`zh:"...",en:"..."` 成对），两处必须同步改。
- 所有资源路径已从绝对路径（`/_next/`、`/videos/`、`/images/`）改为相对路径（`./_next/`…），因为本项目是 GitHub Pages **项目站**（挂在 `/pdl-resume-site/` 子路径下），原站是用户站（根路径）。
- 改写脚本留档：`pdl_content.py`，可重跑/改造。

## 常用操作

本地预览（子路径模拟）：

```bash
cd ~/Desktop/简历/03-作品与项目/个人网站
python3 -m http.server 8931
# 打开 http://127.0.0.1:8931/site-mirror-pdl/
```

更新上线（改完文件后）：

```bash
cd ~/Desktop/简历/03-作品与项目/个人网站/site-mirror-pdl
git add -A && git commit -m "说明" && git push
# 约 1 分钟生效
```

注意：`.nojekyll` 必须保留——没有它 GitHub Pages 的 Jekyll 会忽略 `_next/` 目录。
