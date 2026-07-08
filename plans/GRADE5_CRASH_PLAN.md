# Cyber Security 1 Grade 5 冲刺总计划

当前日期：2026-07-08
目标期限：最迟 2026-07-30 前参加并通过 Exam 3
目标成绩：grade 5，即总 grade points >= 70，且必须通过 Exam 3

## 0. 先说风险

最大阻塞不是学习量，而是行政链路：

- Exam 1 前必须有 Maso id=700 self-evaluation approved。
- 当前 self-evaluation 还没有 approved。
- 你给出的背景是老师 2026-06-27 到 2026-07-26 放假，不处理邮件。我在项目文件中没有找到这条假期信息，所以本计划把它作为外部约束使用。
- 因此 2026-07-08 到 2026-07-26 期间不能依赖老师审批。真实 Exam 1 很可能最早只能在 2026-07-27 晚上或之后开始。
- Self-evaluation 不应太早提交。它本来就是对 G1-G3 和 C1-C6 掌握情况的总结，应该在 Exam 1 Maso pages 大致学完之后再写，才真实有效。
- Exam 3 由老师批改，第二/第三次 attempt 必须等前一次批改完。7/27-7/31 的窗口非常窄，grade 5 是否能在 7/31 前完全落地，取决于老师能否及时 approve self-evaluation 和批改 Exam 3。

策略：7/9-7/26 做完所有可控准备；self-evaluation 在 Exam 1 Maso 第一轮完成后再定稿并提交；7/27-7/31 只执行考试和少量补强，不再大规模学习。

## 1. 已读取材料结论

### 课程与考试

来源：`CybSec1-v12.2.pdf`、`CybSecMaps-v4.5.pdf`、`general/GradeCalc.xlsx`、`general/schedule.xlsx`。

- 成绩由 Exam 1、Exam 2、Exam 3、Harpo exercises 四部分组成。
- 总分线：30/40/50/60/70 分对应 grade 1/2/3/4/5。
- Exam 1 必须先通过，Exam 2 必须在 Exam 1 后，Exam 3 必须在 Exam 2 后。
- Exam 1 通过后不能再考，所以不要低分侥幸通过。
- Harpo points 必须在用于结课的 Exam 2 或 Exam 3 attempt 之前完成，否则对该 attempt 的最终成绩无效。
- GradeCalc 确认：Harpo 和 Exam 3 直接进入 grade points；Exam 1 和 Exam 2 是 exam points - 12，未过及格线则该部分为 0。
- `schedule.xlsx` 在 40h/week 输入下把官方 8 周计划压缩成约 78.5h；示例路径是 Harpo 22.5、exam total 52、总分 74.5，达到 grade 5。

### Maso HTML 状态

来源：`maso/maso_exam1.html`、`maso/maso_exam2.html`。

- `maso_exam1.html` 包含 34 个 material links，其中 id=700 是 Self-evaluation，另外 33 个是 Exam 1 pages。
- `maso_exam2.html` 包含 84 个 material links，对应 Exam 2 pages。
- 两个 HTML 都是 folded/tree view 页面，只包含标题、material id、贡献/Q 状态；树页本身没有实际 MCQ 题干、选项、正文或输入框。
- 但这些 material links 是有效入口。真正的学习方式是逐个打开 `materiaali.php?id=...` 页面，在具体 material page 中阅读知识点和 MCQ。
- 具体 MCQ 的正确答案可通过鼠标悬浮在题目上显示；我已验证，答案也出现在题目 HTML 的 `title` 属性里，例如 `<li class="tehtavarivi" title="3. correct option...">`。每页学习时必须记录：题干、选项、hover/title 正确答案、为什么正确、为什么其他选项错。
- folded tree 文件中 `<form>`、`<input>`、`textarea` 数量均为 0，所以不能只靠树页复习所有 MCQ。
- HTML 中有 immersive-translate 插件注入标记，说明它们是浏览器保存的树页，不是完整学习页快照。

Maso 页面访问和保存方式：

1. 从 `maso_exam1.html` 或 `maso_exam2.html` 的 links 逐个打开具体 material page，例如 `materiaali.php?id=701`。
2. 确认页面出现三块内容：top topics、middle MCQ、bottom input/contribution/comment。
3. 对每道 MCQ 用鼠标 hover 题目，或从 HTML 的 `title` 属性读取正确答案。不要只背答案，要写 reasoning。
4. 展开页面上所有折叠、Q/comment、show/hide 内容。
5. 每个 material page 同时保存两份：
   - `Save Page As -> Webpage, Complete`，命名为 `maso/pages/id_701_First_concepts.html`。
   - `Print -> Save as PDF`，命名为 `maso/pages/id_701_First_concepts.pdf`。
6. 如果浏览器保存 HTML 后没有 frame 内容，右键每个 frame 单独保存，或优先保留 PDF 作为可读备份。

## 2. Harpo 规则确认

来源：`harpo/general/` 下 PDF、`CybSec1-v12.2.pdf`。

### Automatic exercises

- 共 25 个 automatic exercises。
- 当前 profile 显示 automatic exercises 是 0.00 points。
- Cookie & VPN 允许无限尝试，最高 1 point。
- CISSP 是最后一个 exercise，最高 2 points。
- 其他 automatic exercises 最高 1 point，通常前 2 次通过给满分；之后按 4/7/12 attempts 的 schedule 递减。
- 除 review 类 exercise 外，通常必须所有答案正确才得分。
- `Send answers` 和 `Reload` 都算一次 attempt，所以提交前必须先把答案准备完整。
- Exam 3 small essay 会优先从 10 个带星 automatic exercises 出题，条件是该 exercise 得分 >= 5/6。
- Harpo 不应该在没有学到对应内容时提前提交。7/9 只读规则、题型和相关 Maso/Maps 基础，不做会消耗 attempt 的提交。主要提交窗口放在周五/周六/周日，集中注意力，先准备草稿和计算过程，再一次性提交。

会触发 Exam 3 small essay 池的 10 个 starred exercises：

- Checksum
- Networking
- Operating systems
- Password
- Elementary hacking
- Secure email
- Cryptoslots 1
- Cryptoslots 2
- Crypto algorithms 1
- Crypto algorithms 2

其他 automatic exercises：

- Cookie & VPN
- Calculations
- Programming
- Certificate
- Encryption
- Signature
- Symmetric ciphering
- Mind maps 1
- Mind maps 2
- ENISA: Social media to APT
- NIST SP: Systems Security Eng.
- NIST SP: Access control models
- Jewels
- Principles and problems
- CISSP

### Specials

- Availability：0-1 point。需要密码管理器、云存储/备份、文件传输方案，并写 report 通过文件传输发给老师。老师审批，所以 7/26 前不能依赖得分，但可以先完成报告。
- Contributions：0-2 points。Maso contribution 从第 4 个 approved 开始每个 1/6 point，到第 15 个满 2 points。必须帮助其他学生理解页面概念或题目，不能只是答案、链接或复制粘贴；必须有来源；不能重复别人内容；AI 生成内容受严格限制。
- News tweets：0-3 points。新闻最多一天旧；每天只计最后一条；需要覆盖 4 个 topic types 和 4 个 source types，不含 Other；8 条合格得 1 point，之后每 2 条加 0.5 point，到 16 条得 3 points。
- Survey：0-3 points。先完成自己的 mobile security questionnaire，再找两个不住在芬兰且不是 TAU ITC 学生的人完成；一共 3 份才是满分路径。
- Essays：0-3 points。必须先通过 Exam 1 才能开始。Stage 1 两个不同 ontology category 的问题描述；Stage 2 按老师反馈提交 prompt 和 AI response，最多 1 point；Stage 3 按老师反馈编辑并加入 scientific reference，最多 2 points。由于老师假期和 7/30 截止，本计划不把 Essays 当作 grade 5 基线分数。

## 3. Grade 5 分数策略

基线目标：

- Harpo：22.5-25 points。
- Exam 1：26+/32，等价约 14+ grade points。
- Exam 2：32+/52，等价 20+ grade points。
- Exam 3：13+/20。

可接受组合：

- 理想：Harpo 25 + Exam1 14 + Exam2 20 + Exam3 13 = 72。
- 官方示例：Harpo 22.5 + exam total 52 = 74.5。
- 风险线：Harpo 20 + Exam1 14 + Exam2 20 + Exam3 12 = 66，只能 grade 4。

结论：Harpo 不是附加题，是 grade 5 安全垫。7/9-7/26 的主要任务是把 Harpo、Maso、Exam 3 essay 框架提前完成。

## 4. 2026-07-09 到 2026-07-30 总节奏

### Phase A：7/9-7/12，本周启动，27h

目标：

- 建立 Exam 1 的 33 page / 90 concept 框架。
- 逐个打开 Exam 1 Maso material pages，阅读知识点和 MCQ，并用 hover/title 记录正确答案。
- 在 Exam 1 Maso 第一轮大致完成后，再起草 self-evaluation。
- 先准备第一批 Harpo automatic exercises，不急着提交：Cookie & VPN、Checksum、Calculations、Networking、Operating systems、Programming、Password。
- 周五只有 3h+2h，所以周五主要做 Maso/Exam 1 和 Harpo checklist；Harpo 实际提交主要集中在周六/周日，避免无准备试错影响分数。
- 开始 News，每天 1 条。
- 做完 Exam1Sample 第一轮，答案必须能解释为什么对/错。

完成标准：

- `maso/SELF_EVALUATION_DRAFT.md` 不要求 7/12 前提交；只要求在学完大部分 Exam 1 Maso 后完成真实初稿。
- `notes/` 有每日笔记。
- `maso/pages/` 至少保存或摘录 24 个左右 Exam 1 material pages；若能完成 33 个则进入优秀线。
- `maso/` 中每个已学页面必须记录 MCQ hover/title 答案和 reasoning。
- Exam1Sample 至少完成 24 题第一轮解释；32 题完整完成是优秀线。
- Harpo 至少完成 3-5 个 automatic exercise 的准备稿；实际提交只做有把握的题，目标周末拿到 3 个左右满分或接近满分。
- News 至少 4 条，尽量覆盖不同 topic/source。

### Phase B：7/13-7/19，主学习周，至少 40h

目标：

- 完成所有 Exam 1 pages 和 90 concepts。
- 完成至少 50% Exam 2 pages。
- Harpo starred exercises 优先拿到 >=5/6。
- 完成 Exam2Sample 第一轮。
- Exam 3 big essay 选定 1 个主选题 + 2 个备用，并写 1 页英文大纲。

完成标准：

- Exam 1 自测稳定 28+/32；最低不能低于 26/32。
- Exam 2 sample 至少完成 52 题第一轮解释。
- Starred exercises 至少 7 个 >=5/6。
- News 累计 11 条以上。
- Contributions 草稿累计 10-15 条，等老师回来后再等审批。

### Phase C：7/20-7/26，封闭冲刺周，至少 40h

目标：

- 完成全部 117 Maso material pages 的保存与复习。
- 完成 Harpo automatic exercises 的高价值部分，目标 automatic 18-20+ points。
- News 累计 16 条，拿满 3 points 路径。
- Survey 完成 3 份。
- Availability report 完成并准备提交。
- Exam 3 big essay 能在 30-35 分钟内写出有结构的答案。
- 10 个 spare small essay 全部有 120-180 词英文答案框架。

完成标准：

- Exam 1 mock：连续两次 28+/32。
- Exam 2 mock/sample：连续两次 34+/52 或至少稳定 32+/52。
- Exam 3：1 个 big essay 完整手写/打字演练 3 次；small essay 每天 7 题抽测。
- 7/26 晚上只剩审批/考试执行，不剩大块学习债。

### Phase D：7/27-7/31，考试执行窗口

前提：self-evaluation approved。

预测最快路线：

- 7/27 晚：Exam 1。若当场分数低于 26/32 且还没 final，宁可清空/放弃，不要低分通过。
- 7/28：Exam 2。目标 32+/52。
- 7/29-7/31：Exam 3 first attempt，越早越好。目标 13+/20。

说明：

- 这条路线只在 self-evaluation 7/27 获批时成立。
- 如果 7/29 无法约 Exam 3，则 7/30 或 7/31 是后续窗口，但不能再留太多学习债。

如果 self-evaluation 7/27 仍未 approved：

- 每天早晚检查 Maso/Harpo 状态。
- 不反复发邮件催老师；准备好简短礼貌提醒，只在 7/27 或之后需要时发送。
- 继续做 Exam 2/3 和 Harpo，等待批准。
- 现实判断：若 7/28 仍不能开始 Exam 1，7/30 前完成 grade 5 的概率会显著下降。

## 5. 每日工作流

公司 2h：

1. 按当天计划完成 reading / Maso / Harpo / sample questions。
2. 在 `notes/YYYY-MM-DD.md` 写概念笔记。
3. 在 `maso/YYYY-MM-DD.md` 写 MCQ 理由和错题。
4. 在 `harpo/YYYY-MM-DD.md` 记录 exercise attempt、得分、失败原因。
5. 下班前 push 到 GitHub。

晚上回家：

1. 告诉 Codex 今天公司阶段完成了哪些文件和任务。
2. Codex review notes/answers。
3. Codex 生成 `quick_tests/YYYY-MM-DD.md`。
4. 你完成 quick test。
5. Codex 根据错误生成当晚 2h todo list。
6. 晚上完成后再次 review。
7. Codex 生成第二天计划。

每天结束必须有：

- `notes/YYYY-MM-DD.md`
- `maso/YYYY-MM-DD.md`
- `harpo/YYYY-MM-DD.md`
- `exam3/YYYY-MM-DD.md`
- `reviews/YYYY-MM-DD.md`
- `quick_tests/YYYY-MM-DD.md`

## 5.1 动态调整机制

每天、每周、每阶段结束后都要根据真实执行情况调整下一步计划。记录位置：

- `tracking/PROGRESS_LOG.md`
- `tracking/DAILY_REVIEW_TEMPLATE.md`
- `tracking/ADAPTIVE_STUDY_GUIDELINES.md`

每次 review 必须回答：

- 计划完成率大约是多少。
- 是时间不够、概念不懂、恐惧/拖延、工具问题，还是计划过载。
- 下一天要保留什么、删掉什么、顺延什么。
- 哪些地方值得肯定。
- 哪些地方需要注意和改进。

## 6. Self-evaluation 提交策略

提交位置：Maso id=700。

提交时间：不要在 7/9 过早提交。先完成 Exam 1 Maso pages 的第一轮学习，再写真实总结。目标是在 7/13-7/19 形成初稿，7/24-7/26 定稿并提交，让 7/27 有机会被审批。

语气要求：

- 简短真实。
- 不要复制 self-evaluation 页面上的课程目标和 core content 原文。
- 用 G1/G2/G3 和 C1-C6 明确引用。
- 分别评价每个 learning objective 和每个 core content。
- 可以写 strengths、interesting topics、以前已清楚的主题、Exam 1 前还要补的主题。
- 承认薄弱点，但说明已经知道如何继续补。
- 注意：被接受后其他登录用户也能看到；如果后续编辑，需要重新审批。

草稿文件：`maso/SELF_EVALUATION_DRAFT.md`。

## 7. 当前优先级

1. 7/9 开始逐个访问 Maso Exam 1 material pages，记录知识点、MCQ、hover/title 正确答案和 reasoning。
2. 7/9 开始 News，每天 1 条，不间断到 7/24 或 7/25 达到 16 条。
3. 7/9-7/12 把 Exam 1 核心读完第一轮，不追求完美，追求覆盖。
4. 7/10-7/12 集中做 Harpo，但只提交已经准备充分的 exercises，避免低价值随机尝试。
5. Self-evaluation 等 Exam 1 Maso 第一轮完成后再写，目标 7/13-7/19 初稿，7/24-7/26 定稿提交。
6. 7/13 起并行 Exam 2 和 Exam 3，不等 Exam 1 批准后才开始。
