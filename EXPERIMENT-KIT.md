# AI GitHub 代码决策能力实验 - 实验材料包

> 本实验用于测试 ChatGPT 通过不同路径访问 GitHub 代码并做出技术决策的能力。

---

## 📦 第一部分：准备测试仓库

### 步骤 1：把本地仓库推送到 GitHub

请依次执行以下命令，把 `ai-github-test-repo` 推送到你的 GitHub：

```bash
# 进入仓库目录
cd ai-github-test-repo

# 初始化 git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Task Manager API with intentional bugs"

# 在 GitHub 上新建一个公开仓库（名字建议：ai-github-test-repo）
# 然后把本地仓库关联并推送
git remote add origin https://github.com/yujian777555/ai-github-test-repo.git
git branch -M main
git push -u origin main
```

> ⚠️ 注意：请把 `yujian777555` 替换为你的实际 GitHub 用户名！

### 步骤 2：确认仓库可访问

推送完成后，在浏览器打开：
```
https://github.com/yujian777555/ai-github-test-repo
```

确认所有文件都已上传。

---

## 🧪 第二部分：3 组实验提示词

### 实验设计原则

- **同一批问题**、**同一仓库**、**不同接入路径**
- 记录每条路径的完整输出（包括 ChatGPT 的思考过程）
- 比较三条路径的答案质量和差异

---

### 🔧 路径 A：Shell 沙箱（gh / git CLI）

把下面整段文字复制给 ChatGPT：

---

**【路径 A 提示词 - 直接复制发送给 ChatGPT】**

```
我要测试你通过命令行访问 GitHub 的能力。请按以下步骤执行：

1. 在你的隔离 Linux 环境中，安装 GitHub CLI：
   curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
   chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null
   apt update && apt install gh -y

2. 使用 git clone 克隆这个仓库：
   git clone https://github.com/yujian777555/ai-github-test-repo.git /tmp/test-repo

3. 读取以下所有文件的内容，并把完整内容展示出来：
   - /tmp/test-repo/main.py
   - /tmp/test-repo/auth.py
   - /tmp/test-repo/database.py
   - /tmp/test-repo/config.py
   - /tmp/test-repo/utils.py

4. 基于你读取到的全部代码，回答以下问题：

   【L1 基础理解】
   a) 这个项目的功能是什么？技术栈是什么？
   b) main.py 里定义了哪些路由/端点？

   【L2 依赖追踪】
   c) 当用户调用 POST /tasks 创建任务时，数据流经过哪些文件和函数？
   d) auth.py 里的 authenticate_user 被哪些文件调用？

   【L3 代码审查】
   e) 找出 auth.py 中所有安全问题，按严重程度排序
   f) 找出 database.py 中所有安全问题，按严重程度排序
   g) 找出 config.py 中所有安全问题

   【L4 Bug 诊断】
   h) 如果我在 POST /tasks 时传入 title = "'; DROP TABLE tasks; --"，会发生什么？解释原因并指出涉及的文件和代码行
   i) main.py 中的 rate_limit_middleware 真的能限流吗？请分析并说明原因

   【L5 架构决策】
   j) 假设我要把数据库从 SQLite 换成 PostgreSQL，需要修改哪些文件？给出迁移步骤
   k) 这个项目的代码质量整体如何？如果满分 10 分你打几分？为什么？

请把每一步的命令执行过程和最终回答都完整展示出来。
```

---

### 🔌 路径 B：GitHub Connector（工具调用）

把下面整段文字复制给 ChatGPT：

---

**【路径 B 提示词 - 直接复制发送给 ChatGPT】**

```
我要测试你通过 GitHub Connector 访问代码的能力。请使用你的工具调用能力：

1. 连接到 GitHub 仓库：yujian777555/ai-github-test-repo

2. 读取以下所有文件的完整内容：
   - main.py
   - auth.py
   - database.py
   - config.py
   - utils.py

3. 基于你读取到的全部代码，回答以下问题：

   【L1 基础理解】
   a) 这个项目的功能是什么？技术栈是什么？
   b) main.py 里定义了哪些路由/端点？

   【L2 依赖追踪】
   c) 当用户调用 POST /tasks 创建任务时，数据流经过哪些文件和函数？
   d) auth.py 里的 authenticate_user 被哪些文件调用？

   【L3 代码审查】
   e) 找出 auth.py 中所有安全问题，按严重程度排序
   f) 找出 database.py 中所有安全问题，按严重程度排序
   g) 找出 config.py 中所有安全问题

   【L4 Bug 诊断】
   h) 如果我在 POST /tasks 时传入 title = "'; DROP TABLE tasks; --"，会发生什么？解释原因并指出涉及的文件和代码行
   i) main.py 中的 rate_limit_middleware 真的能限流吗？请分析并说明原因

   【L5 架构决策】
   j) 假设我要把数据库从 SQLite 换成 PostgreSQL，需要修改哪些文件？给出迁移步骤
   k) 这个项目的代码质量整体如何？如果满分 10 分你打几分？为什么？

请展示你调用了哪些工具、传了什么参数、收到了什么返回，以及你的最终回答。
```

---

### 🌐 路径 C：Web URL 抓取

把下面整段文字复制给 ChatGPT：

---

**【路径 C 提示词 - 直接复制发送给 ChatGPT】**

```
我要测试你通过直接访问 URL 读取 GitHub 代码的能力。请直接打开以下 URL 并读取完整内容：

1. https://raw.githubusercontent.com/yujian777555/ai-github-test-repo/main/main.py
2. https://raw.githubusercontent.com/yujian777555/ai-github-test-repo/main/auth.py
3. https://raw.githubusercontent.com/yujian777555/ai-github-test-repo/main/database.py
4. https://raw.githubusercontent.com/yujian777555/ai-github-test-repo/main/config.py
5. https://raw.githubusercontent.com/yujian777555/ai-github-test-repo/main/utils.py

基于你读取到的全部代码，回答以下问题：

【L1 基础理解】
a) 这个项目的功能是什么？技术栈是什么？
b) main.py 里定义了哪些路由/端点？

【L2 依赖追踪】
c) 当用户调用 POST /tasks 创建任务时，数据流经过哪些文件和函数？
d) auth.py 里的 authenticate_user 被哪些文件调用？

【L3 代码审查】
e) 找出 auth.py 中所有安全问题，按严重程度排序
f) 找出 database.py 中所有安全问题，按严重程度排序
g) 找出 config.py 中所有安全问题

【L4 Bug 诊断】
h) 如果我在 POST /tasks 时传入 title = "'; DROP TABLE tasks; --"，会发生什么？解释原因并指出涉及的文件和代码行
i) main.py 中的 rate_limit_middleware 真的能限流吗？请分析并说明原因

【L5 架构决策】
j) 假设我要把数据库从 SQLite 换成 PostgreSQL，需要修改哪些文件？给出迁移步骤
k) 这个项目的代码质量整体如何？如果满分 10 分你打几分？为什么？

请展示你访问的每个 URL 的内容摘要，以及你的最终回答。
```

---

## 📋 第三部分：记录模板

请为每条路径创建如下记录：

```
### 路径 [A/B/C] 记录

**能否成功读取全部文件？** 是 / 否 / 部分
**读取耗时：** ___ 秒
**回答问题数量：** __ / 11

---

**问题 a) 回答：**
[粘贴 ChatGPT 的回答]

**问题 b) 回答：**
[粘贴 ChatGPT 的回答]

...（依此类推）

---

**我的观察：**
[你对这条路径表现的观察]

**路径特有行为：**
[这条路径特有的成功/失败/异常行为]
```

---

## ✅ 第四部分：实验执行清单

- [ ] 推送仓库到 GitHub
- [ ] 确认仓库公开可访问
- [ ] 执行路径 A 实验并保存结果
- [ ] 执行路径 B 实验并保存结果
- [ ] 执行路径 C 实验并保存结果
- [ ] 把 3 组结果发给 Kimi 做对比评分

---

## 🎯 预期答案参考（用于人工核对）

本项目故意埋了以下 bug/问题：

### auth.py
1. **硬编码密钥** `SECRET_KEY`（高危）
2. **明文存储密码**（高危）
3. **使用 MD5 哈希**（高危）
4. **无恒定时间比较**（中危）

### database.py
1. **SQL 注入**（create_task, get_task, list_tasks, update_task）（高危）
2. **无软删除**（高危 - 数据丢失风险）
3. **无索引**（性能问题）
4. **无迁移机制**（维护问题）

### config.py
1. **Debug 模式常开**（中危）
2. **硬编码 API 密钥和数据库密码**（高危）
3. **无环境变量配置**（运维问题）

### main.py
1. **可变全局状态**（竞态条件）
2. **无输入长度验证**
3. **日志泄露敏感信息**
4. **admin 接口无鉴权**
5. **限流中间件无效**
6. **无授权检查**

### utils.py
1. **无效输入清理**
2. **日志直接打印到 stdout**
3. **分页无负数检查**
4. **无日志轮转**

---

> 📎 完成实验后，把 3 组 ChatGPT 的回答复制保存为文件，发回给我，我来帮你做专业评分和对比分析！
