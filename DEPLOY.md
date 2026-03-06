# 🚀 快速部署指南

## 方式 1：Vercel（推荐 ⭐⭐⭐⭐⭐）

**最简单，30 秒搞定！**

### 步骤：

1. **访问 Vercel**
   ```
   https://vercel.com/new
   ```

2. **登录**（GitHub/Google/GitLab 都可以）

3. **导入项目**
   - 点击 "Add New Project"
   - 选择 "Import Git Repository"
   - 或者直接把 `snake-game` 文件夹拖到 Vercel

4. **部署**
   - 点击 "Deploy"
   - 等待 30 秒
   - 获得公开链接！🎉

### 命令行方式（如果你已登录 Vercel）：
```bash
cd snake-game
vercel --prod
```

---

## 方式 2：GitHub Pages（稳定 ⭐⭐⭐⭐）

### 步骤：

1. **创建 GitHub 仓库**
   ```bash
   cd snake-game
   gh repo create cyber-snake --public
   ```

2. **推送代码**
   ```bash
   git add -A
   git commit -m "🐍 Cyber Snake Game"
   git push -u origin main
   ```

3. **启用 Pages**
   - 访问：`https://github.com/你的用户名/cyber-snake/settings/pages`
   - Source 选择 `main` 分支
   - 点击 "Save"

4. **访问**
   ```
   https://你的用户名.github.io/cyber-snake/
   ```

---

## 方式 3：Netlify（简单 ⭐⭐⭐⭐）

### 步骤：

1. **访问 Netlify Drop**
   ```
   https://app.netlify.com/drop
   ```

2. **拖拽文件夹**
   - 把整个 `snake-game` 文件夹拖到页面

3. **获得链接**
   - 立即生成公开链接！

---

## 方式 4：Cloudflare Pages（免费 ⭐⭐⭐⭐）

### 步骤：

1. **访问**
   ```
   https://pages.cloudflare.com/
   ```

2. **连接 GitHub**
   - 选择 `cyber-snake` 仓库

3. **部署**
   - 点击 "Deploy"

---

## 📱 手机访问

部署后，用手机浏览器访问生成的链接即可！

**推荐：Vercel 或 Netlify** - 最快最简单！

---

## 🎮 本地测试

在部署前，可以先本地测试：

```bash
cd snake-game
python3 -m http.server 8888
```

然后访问：`http://localhost:8888`

---

**需要帮助？** 把部署链接发给我，我帮你测试！🐍
