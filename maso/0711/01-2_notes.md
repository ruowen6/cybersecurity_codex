我已核对 `maso/0709/01-2_victims_attackers.md`。这一页核心不是技术细节，而是：**攻击者类型、受害者不确定性、社会传播、身份相关攻击**。

**你需要记住的知识点**

1. **脚本小子（script kiddie）**
脚本小子不是重点看年龄，而是看攻击方式：他们通常使用别人写好的工具或脚本（scripts/tools），技术理解可能不深。  
从防守者角度看，关键不是“他们很弱所以不危险”，而是他们的行为可能很模式化、可预测，因为很多人使用相似工具。  
不要把 script kiddie 理解成“未成年人”或“学徒”。

2. **受害者（victim）**
受害者不能像攻击者一样清楚分类。攻击者可以叫 script kiddie、identity thief、social engineer、phisher、industrial spy、criminal group、botnet operator，但受害者可能是任何人。  
尤其是非定向攻击（non-targeted attack）中，普通用户也会中招。社交媒体（social media）会放大这个问题，因为转发和分享（forwarding/sharing）会让风险扩散。

3. **身份盗用（identity theft）**
身份盗用是恶意使用他人的身份识别数据（identifying data）。重点是“使用别人的身份数据”，不一定要求已经造成金钱损失，也不等于单纯把别人账号锁住。  
它通常是有恶意意图（malicious intent）的，不要把 accidental confusion 当成 identity theft。

4. **社会工程学（social engineering）**
社会工程学的核心是影响人，让人违反自己的安全策略或正常判断（influencing people to act against security policy）。  
它比 phishing 更宽。Phishing 通常是用伪装邮件、消息或网站骗取信息；social engineering 包括 phishing，也包括套近乎、翻垃圾、观察密码输入、冒充权威等。  
做题时看到多个例子都对，要选覆盖范围最广的定义。

5. **钓鱼攻击（phishing）**
钓鱼是社会工程的一种，通常通过伪装成可信来源（masquerading as trusted source）来骗取敏感信息（sensitive information），例如密码、银行卡信息、登录凭据。  
不要把 phishing 等同于所有 social engineering。

6. **冒充（impersonation）**
冒充不是“新身份被分配”，也不是“身份被没收”。重点是：受害者或系统被欺骗，以为自己正在和某个合法对象交流（acting as if in contact with someone else）。  
它可以发生在人对人，也可以发生在人对系统、系统对系统。

7. **用户转发传播的实体（user-forwarded entities）**
这页强调：很多东西主要靠人转发传播，而不是靠程序自动复制。你要区分它们的性质和风险：

- 垃圾信息（spam）：大量不请自来的消息，可能带广告、诈骗、恶意链接。
- 谣言/骗局警告（hoax）：错误或误导性信息，风险在于误导人、浪费注意力、诱导错误行为。
- 勒索软件（ransomware）：程序（program/malware），会让数据不可访问并索要赎金，是直接计算风险。
- 模因病毒（meme virus）：不是计算机病毒（not a computer virus），更像通过人传播的观念、笑话、内容模式。
- 尼日利亚信（Nigerian letter）：预付款诈骗（advance-fee fraud），不一定真的来自 Nigeria。
- 喷子（troll）：是人（person），不是数字实体本身；风险通常是扰乱讨论、诱导冲突、污染信息环境。

这道题不要背数字。判断流程是：  
先问它是人、程序、消息还是内容；再问它是否主要靠用户转发；最后问它是否是直接的 computing risk。

**做这页 MCQ 的 reasoning 模板**

遇到定义题时先写：

“这个概念的本质是____，不是____。”

例如：

- script kiddie 的本质是使用他人工具，不是年龄。
- identity theft 的本质是恶意使用他人身份数据，不是单纯账号被锁。
- social engineering 的本质是操纵人违反安全策略，不只是 phishing。
- impersonation 的本质是让对方误以为正在接触另一个合法对象。

**你可以背的 5 句话**

- 脚本小子（script kiddie）主要特征是使用别人写好的脚本或工具。
- 身份盗用（identity theft）是恶意使用他人的身份识别数据。
- 社会工程学（social engineering）是影响人违反安全策略的艺术。
- 钓鱼（phishing）是社会工程的一种，但社会工程不只包括钓鱼。
- 冒充（impersonation）是让人或系统误以为正在和合法对象交互。

现在最重要任务：回到 `maso/0709/01-2_victims_attackers.md`，用上面这些知识先自己答 Q1-Q6，不看答案。  
今天主要看：`maso/0709/01-2_victims_attackers.md`。  
参考文件：`plans/2026-07-11.md` 和 `exams/Exam1Sample_topic_map.md`，现在不要打开太久。