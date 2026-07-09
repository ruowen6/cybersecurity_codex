Information and threats > general >> first concept
# 笔记区
## 网络攻击 总论
破坏系统的integrity-完整性，来达成攻击目的。
破坏的后果就是，被破坏的软件/系统的任务无法完成，lack of availability ==》 拒绝服务，达成不了原定的服务，denial of service
那我们就把这样的攻击方法称为attack vector = 向量
多个向量组成array，向量也有方向
一堆不同的attack vector就可以进行Distributed DoS攻击 ==》 DDoS
## def of security
confidentiality, integrity and availability
机密性，完整性，可用性
当信息享有上面这三大核心性质，并达到期望水平，那这个信息就是安全的
recall刚才我们讨论过的，integrity和availability有一定关联，那么剩下的机密性就很好理解很好记忆了。
## NOTE
材料也提醒我们去看 Maps & Lists这个文档。


# MCQ区
## Q1
What is required of an attack to be regarded as a cyber attack?
1. The target relies on an electronic information system.
1. The attack happens on behalf of a nation state.
1. The target suffers a substantial loss.
1. The attacker is not acting alone but in a large coherent group.
### 思路和正确答案
我选了1，
理由：
个人也可以是黑客所以2和4错误；
网络攻击也有可能失败，但是失败与否不影响网络攻击行为本身是不是一个攻击，所以3错误

## Q2
Denial of service is a term
1. for a specific attack where the attacker modifies the responses from a www server to display HTTP 404.
1. used of any situations where the user or a process is not granted the service he, she or it would be authorized to get.
1. that refers to a service not being able to operate because of malicious requests.
1. used mainly of such situations where a cracked service has been taken down for repair by administrators.
### 思路和正确答案
我选3，
理由：
DoS是通过攻击使得被攻击对象无法达成服务，造成“拒绝服务”的表现。因此也可能是其她的状态码，所以1错误；
选项2看起来不够全面，因为这个场景也可能出现在一些其她的错误中，比如开发者自己没有调好用户权限，所以2错误；
4不正确，同样是太片面了，只是可能的其中一种情况，没有讲到DoS的本质。综合来看我选3

## Q3
What makes a denial of service attack (DoS) a distributed DoS?
1. There are many hackers working in consort to gain access to the attacked service.
1. The attacked server spreads the unavailability to a large community of other servers and services.
1. The whole farm of load-balancing and resilience-providing computers are attacked to make the service unavailable.
1. The attacking traffic comes to the server from several computers simultaneously.
### 思路和正确答案
我选3，
理由：
不一定要很多个黑客，一个黑客也可以，关键是看有没有不同的attack vector，所以1错；
选项2看起来是指有很多个受害者，但实际上DDoS的重点是很多不同方向的攻击向量，distributed的是攻击不是受害者，所以2错；
3和4其实我不确定，看起来都有可能对；
我认为4更可疑一点，因为可能不需要很多台电脑同时攻击，一台电脑也可以做到
#### 正确答案
正确答案是4，那为什么3错呢？


## Q4
The term attack vector
1. is just a more fancy way of referring to a particular attack that has happened.
1. refers to the attacker's point of view to the chain of protections that implement the defence-in-depth approach.
1. refers to the method of an attack - one that happened or is possible.
1. refers to the combination of all vulnerabilities that exist in a particular information system.
### 思路和正确答案
我选3，
理由：
攻击vector不强调是否已经发生过，所以1错；
我不记得attack vec和defence有什么关系所以我认为2错；
我认为attack vec的重点是attack，和信息系统的脆弱性是不同维度，所以4错

## Q5
Confidentiality is one of the three basic goals ("C-I-A") of information security,
1. but it is hardly ever as important as integrity.
1. and it is nearly always more important than availability.
1. but it is usually not sufficient without integrity and availability.
1. and lack of confidentiality would lead to similar problems as lack of either integrity or availability.
### 思路和正确答案
我选3，
理由：
CIA三个都重要，没有谁特别不重要，不然把这些东西列出来干嘛？所以1和2错，3看起来正确；
其实3和4我不确定，
但是逻辑推理来说，如果三个维度都重要，那么缺少任意一方导致的问题都会是较为独特的，不然为什么有三个独立维度呢？就好像linear independent一样，如果矩阵缺乏其中一行不影响rank，那么那一行肯定不是independent的

## 答案
13433


# 贡献区