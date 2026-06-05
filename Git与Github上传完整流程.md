# Git 与 GitHub 上传完整流程（从零到推送）

> 以你当前的仓库 `AI_Algorithm` 为例，手把手讲清楚每一步在做什么、为什么这么做。

---

## 一、整体逻辑概览

整个过程分为 **三个大阶段**：

| 阶段 | 做什么 | 在哪里操作 |
|------|--------|-----------|
| **① 本地准备** | 初始化 Git 仓库、写代码、提交（commit） | 你的电脑（本地） |
| **② 关联远程** | 在 GitHub 创建空仓库，把本地仓库和远程仓库"绑"在一起 | GitHub 网页 + 本地终端 |
| **③ 推送同步** | 把本地的提交推送到 GitHub | 本地终端 |

核心理解：**Git 是版本管理工具，GitHub 是代码托管网站**。你的代码"本体"在本地，GitHub 是它的远程备份 + 协作平台。

---

## 二、你当前的仓库状态（已经走完了前两步）

```
远程地址：https://github.com/judy66995/AI_Algorithm.git  （简称 AI_Algorithm）
当前分支：main
工作区状态：干净（所有文件都已提交，没有未保存的修改）
```

你只需要执行推送命令即可。但下面我会从头讲起，让你彻底理解每一步。

---

## 三、阶段①：本地初始化与提交

### 3.1 初始化本地 Git 仓库

```bash
git init
```

**这句话在做什么？**  
在你当前的文件夹里创建一个隐藏目录 `.git/`。这个 `.git/` 目录就是整个仓库的"数据库"——所有版本历史、分支信息、配置全部存在里面。删除 `.git/` 就等于删除了整个仓库的版本记录（但不会删除你的代码文件）。

### 3.2 写代码、创建文件

这就是你日常写代码的过程。比如你创建了 `26_6_5/main.py` 等文件。

### 3.3 查看文件状态

```bash
git status
```

**这句话在做什么？**  
对比"当前文件夹里的文件"和"上次提交的快照"，告诉你：
- 🔴 **红色文件**：新文件或修改过的文件，还没被 Git 跟踪（untracked / modified）
- 🟢 **绿色文件**：已经加入暂存区，准备好被提交（staged）

### 3.4 把文件加入暂存区

```bash
git add .
# 或者指定具体文件：
git add 26_6_5/main.py
```

**这句话在做什么？**  
把文件的当前内容"拍一张快照"，放到一个叫**暂存区（staging area）**的中间区域。  

`git add .` 里的 `.` 代表当前目录下的所有文件。

> 为什么要分"暂存区"和"提交"两步？  
> 因为你可以**选择性提交**——比如你改了 5 个文件，但只想把其中 3 个相关的改动打包成一次提交，另外 2 个留到下一次。暂存区让你有这个机会。

### 3.5 提交（commit）

```bash
git commit -m "你的提交信息"
```

**这句话在做什么？**  
把暂存区里的所有文件快照**正式存入仓库历史**。每一次 commit 都会生成一个唯一的 ID（如 `50171cb`），你可以随时回到任何一个 commit 时的代码状态。

> `-m` 后面跟的是提交说明。写清楚你这次改了什么，比如 `"finish：最长连续数列"`。好的 commit message 是给自己和别人的礼物。

---

## 四、阶段②：关联远程仓库（GitHub）

### 4.1 在 GitHub 网页上创建空仓库

1. 打开 https://github.com/judy66995
2. 点击右上角 `+` → `New repository`
3. 填写仓库名（如 `AI_Algorithm`）
4. **不要勾选** "Add a README file"（如果已经勾了，需要在本地先 `git pull` 合并）
5. 点击 `Create repository`

创建后 GitHub 会给你一个地址，如：  
`https://github.com/judy66995/AI_Algorithm.git`

### 4.2 在本地添加远程地址

```bash
git remote add AI_Algorithm https://github.com/judy66995/AI_Algorithm.git
```

**这句话在做什么？**

拆解开来：

| 部分 | 含义 |
|------|------|
| `git remote add` | 添加一个远程仓库的"快捷方式" |
| `AI_Algorithm` | 你给这个远程地址起的**别名**（可以叫任何名字，常见的是 `origin`） |
| `https://...` | 远程仓库的完整 URL |

**通俗理解**：你告诉 Git："以后我说 `AI_Algorithm`，你就要理解成 `https://github.com/judy66995/AI_Algorithm.git` 这个地址"。

### 4.3 查看已配置的远程地址

```bash
git remote -v
```

输出示例：
```
AI_Algorithm  https://github.com/judy66995/AI_Algorithm.git (fetch)
AI_Algorithm  https://github.com/judy66995/AI_Algorithm.git (push)
```

- `(fetch)`：从这个地址**拉取**代码
- `(push)`：向这个地址**推送**代码

---

## 五、阶段③：推送与后续同步

### 5.1 首次推送

```bash
git push -u AI_Algorithm main
```

**这句话在做什么？**

| 部分 | 含义 |
|------|------|
| `git push` | 把本地的提交推送到远程仓库 |
| `-u` | `--set-upstream` 的缩写，建立"跟踪关系"，之后只需要 `git push` 即可 |
| `AI_Algorithm` | 你要推到哪个远程仓库（之前用 `remote add` 起的别名） |
| `main` | 你要推送的是哪个分支 |

**通俗理解**：把本地 `main` 分支上的所有 commit，上传到 GitHub 上 `AI_Algorithm` 仓库的 `main` 分支。

> `-u` 参数只需要**第一次**推送时加。它会在本地和远程分支之间建立一个"上下游关系"，这样以后你直接敲 `git push`（不带参数），Git 就知道要推到哪去了。

### 5.2 之后日常推送（三件套）

每次写完代码后：

```bash
git add .                        # ① 把所有修改加入暂存区
git commit -m "描述你改了什么"     # ② 提交到本地仓库
git push                         # ③ 推送到 GitHub（因为已经 -u 过了）
```

### 5.3 从 GitHub 拉取最新代码

```bash
git pull
```

当别人（或其他设备）向同一个仓库推送了新代码，你需要先拉取再推送：

```bash
git pull          # 先拉取远程最新代码
# 解决冲突（如果有的话）
git push          # 再推送你的代码
```

---

## 六、常见情况速查

### 情况 1：全新项目，从零开始

```bash
# 本地操作
git init
git add .
git commit -m "first commit"

# 关联远程（先在 GitHub 网页创建空仓库，拿到地址）
git remote add origin https://github.com/你的用户名/仓库名.git

# 推送
git push -u origin main
```

### 情况 2：GitHub 上的仓库已有 README，本地也有代码（合并）

```bash
git remote add origin https://github.com/你的用户名/仓库名.git
git pull origin main --allow-unrelated-histories   # 先拉取并合并
# 解决冲突
git add .
git commit -m "merge remote and local"
git push -u origin main
```

### 情况 3：克隆别人的仓库到本地

```bash
git clone https://github.com/某人/某仓库.git
cd 某仓库
# 已经自动配好 remote（名为 origin），直接可以写代码、提交、推送（如果你有权限的话）
```

### 情况 4：给远程仓库改地址 / 改别名

```bash
# 修改已有 remote 的地址
git remote set-url AI_Algorithm https://github.com/judy66995/新仓库名.git

# 删除一个 remote
git remote remove 旧别名

# 重命名 remote
git remote rename 旧名 新名
```

### 情况 5：推送时提示认证失败

```bash
# 如果用 HTTPS 地址，GitHub 不再支持密码登录，需要用 Personal Access Token：
# 1. GitHub 网页 → Settings → Developer settings → Personal access tokens → Generate
# 2. 复制 token
# 3. 推送时用户名填你的 GitHub 用户名，密码填 token

# 或者改用 SSH 方式（推荐，一劳永逸）：
# 1. 生成 SSH key：ssh-keygen -t ed25519 -C "你的邮箱"
# 2. 把公钥添加到 GitHub：Settings → SSH and GPG keys
# 3. 修改 remote 地址为 SSH 格式：
git remote set-url AI_Algorithm git@github.com:judy66995/AI_Algorithm.git
```

---

## 七、几张理解 Git 工作流的核心图

### 工作区 → 暂存区 → 本地仓库 → 远程仓库

```
┌─────────────┐    git add     ┌────────────┐   git commit   ┌─────────────┐   git push    ┌─────────────┐
│  工作目录    │  ───────────→  │   暂存区    │ ────────────→  │  本地仓库    │ ───────────→  │  GitHub远程  │
│ (你的文件)   │               │  (staging)  │               │  (.git/)     │               │  (云端备份)  │
└─────────────┘               └────────────┘               └─────────────┘               └─────────────┘
                                     ↑                                                         │
                                     │                       git pull / git fetch              │
                                     └─────────────────────────────────────────────────────────┘
```

### 完整日常流程总结

| 命令 | 方向 | 作用 |
|------|------|------|
| `git add` | 工作区 → 暂存区 | 选择哪些改动要提交 |
| `git commit` | 暂存区 → 本地仓库 | 正式记录一次版本 |
| `git push` | 本地仓库 → 远程仓库 | 上传到 GitHub |
| `git pull` | 远程仓库 → 工作区 | 下载别人的更新 |
| `git status` | — | 看看当前什么状态 |
| `git log` | — | 查看提交历史 |

---

## 八、总结：一句话理解

> **`git add` + `git commit` = 在你的电脑上存个档**  
> **`git push` = 把这个存档上传到 GitHub 云端**  
> **`git remote add` = 告诉 Git 云端地址是什么**（只需做一次）

你现在仓库已经配好，只需：
```bash
git push -u AI_Algorithm main
```
就能把本地代码推送到 https://github.com/judy66995/AI_Algorithm 。
