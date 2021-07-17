'''2021.7.16创建，求解机器分配方案的遗传算法，由遗传“算法1-机器分配”复制而来
总共有五部分：外部库导入、初始解与初始种群、计算适应度、轮盘赌选择、交叉变异操作'''

# 运行1，初始化
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import random,numpy as np

# 运行2，创建基本变量
# 两阶段，每一个解都由若干子染色体组成，每次父母解的交叉，都是对应相同子染色体交叉
# 第一阶段，为产品工序分配机器，每个产品是一个染色体，基因是工序，基因的值是该工序
# 可安排的机器，可以通过选择、交叉、变异，产生新的机器安排方案，适应度为机器的负荷
# 的方差
# JSP调度解的编码，每个机器是一个染色体，染色体上每个基因是一个产品工序，基因按该机器
# 上的工序先后顺序排列，基因的值就是产品工序号

ts1=[0,0,0,0,0]
ts2=[0,0,0,0,0]
ts3=[0,0,0,0,0]
ts4=[0,0,0,0,0]
ts5=[0,0,0,0,0]
ts6=[0,0,0,0,0]
ts7=[0,0,0,0,0]
ts8=[0,0,0,0,0]
ts9=[0,0,0,0,0]
ts10=[0,0,0,0,0]
ts11=[0,0,0,0,0]
ts12=[0,0,0,0,0]
task_wt=np.array([ts1,ts2,ts3,ts4,ts5,ts6,ts7,ts8,ts9,ts10,ts11,ts12]) # 个体解，12个产品就是12个染色体

# 每个工序基因可选择的机器编号：
# wt_pro={'wt1':[2,3],'wt2_1':[2,3,4],'wt2_2':[2,3,4],'wt3_1':[1,4],'wt3_2':[1,4],'wt4_1':[5],'wt4_2':[5]}
# wt1=1,wt2_1=2,wt2_2=3,wt3_1=4,wt3_2=5,wt4_1=6,wt4_2=7
s1=[4,5]
s2=[1,2,3]
s3=[1,2,3]
s4=[2,3,4,5]
s5=[6,7]   # 专用资源，也是瓶颈资源
sid=[s1,s2,s3,s4,s5]


# 运行3，创建初始种群并计算种群中每个解的适应度
# 种群规模为20，种群是一个List，list中的每个元素就是一个解task_wt,生成初始种群
solution_wt=[]   # 种群，是一个list
for i in range(20):
    a=task_wt.copy() # 2021.7.16需要增加.copy()
    for j in a:
        for m in range(len(j)):
            j[m]=random.choice(sid[m])
    solution_wt.append(a)

# 计算初始种群的适应度并选择出交叉的父代。适应度为机器负荷的方差
wt_load_var=[]  # 每个解的方差list，
for i in range(len(solution_wt)):
    wt_count=np.bincount(solution_wt[i].flat)  # 极其非常重要，统计矩阵numpy array中元素数量，见网页https://segmentfault.com/q/1010000016716175
    wt_load_var.append(np.var(wt_count[1:8]))    # 计算方差,见网页https://blog.csdn.net/qq_38826019/article/details/82875407

# 因为是最小化问题，需要对适应度进行变换：
wt_fitness=[]  # 适应度list
for i in range(len(wt_load_var)):
    wt_fitness.append(max(wt_load_var)-wt_load_var[i]+0.1)

# 函数版本，计算种群适应度，输入参数为种群，返回制为种群的适应度

def calcufitness(solution_wt):
    wt_load_var=[] # 种群中每个解的方差list
    wt_fitness=[]  # 种群中每个解的适应度list
    for i in range(len(solution_wt)):
        wt_count=np.bincount(solution_wt[i].flat)  # 极其非常重要，统计矩阵numpy array中元素数量，见网页https://segmentfault.com/q/1010000016716175
        wt_load_var.append(np.var(wt_count[1:8]))    # 计算方差,见网页https://blog.csdn.net/qq_38826019/article/details/82875407

    # 因为是最小化问题，需要对适应度进行变换：
    wt_fitness=[]  # 适应度list
    for i in range(len(wt_load_var)):
        wt_fitness.append(max(wt_load_var)-wt_load_var[i]+0.1)
    return wt_fitness


# 运行4，轮盘赌，根据适应度的概率选出新种群
# sort_wtloadvar=sorted(wt_load_var.items(),key=lambda x:x[1]) #方差按升序排序后的字典
# 如果采用轮盘赌策略，就不需要上面的排序了，以下为轮盘赌选择策略：
load_propre=[]  # list 长度为种群数量20，每个元素为对应解的适应度比例，即为选择概率
loadsum=sum(wt_fitness) # 种群适应度之和
for i in wt_fitness:
    load_propre.append(i/loadsum)
loadcumsum=[]  # 种群的概率累加list
for i in range(len(load_propre)):
    loadcumsum.append(sum(load_propre[0:i+1]))

for i in range(20): #转20次轮盘，每次选出一个解
    r=random.random()
    for j in loadcumsum:
        if r<j:
            solution_wt[i]=solution_wt[loadcumsum.index(j)]
            break

# 函数版本
def lunpan(solution,wt_fit):  # 参数是种群,种群的适应度list,返回制是选择之后的种群
    load_propre=[]
    loadsum=sum(wt_fit)
    for i in wt_fit:
        load_propre.append(i/loadsum)
    loadcumsum=[]  # 种群的概率累加list
    for i in range(len(load_propre)):
        loadcumsum.append(sum(load_propre[0:i+1]))
    for i in range(20): #转20次轮盘，每次选出一个解
        r=random.random()
        for j in loadcumsum:
            if r<j:
                solution[i]=solution[loadcumsum.index(j)].copy()
                break
    return solution


# 运行5，对种群进行交叉操作
# 引进交叉概率，先选出一对染色体，然后取随机数如果大于交叉概率，就直接将这对染色体复制给
# 种群，小于交叉概率才交叉。但《详解》案例中不是随机抽取交叉染色体队，而是遍历所有种群个体
for i in range(10):  # 选出10对父代的解
    swt1 = random.choice(solution_wt)  # 从种群中随机选出一个父代解
    swt2 = random.choice(solution_wt)  # 从种群中随机选出另一个父代解
    pc = 0.7  # 交叉概率，设定得比较高
    pcr = random.random()  # pcr小于pc就进行交叉操作
    if swt1.tolist() == swt2.tolist():  # 如果选出的是同一对染色体，就不进行交叉，直接用swt1=swt2更新种群
        solution_wt[i] = swt1  # ——————要验证，这样对不对，可以用list给矩阵的一行赋值
        solution_wt[i + 1] = swt2  # 用一行的矩阵元素给矩阵赋值可以吗
    elif swt1.tolist() != swt2.tolist() and pcr < pc:
        for j in range(12):  # 对于父代解中12条子染色体的其中一条
            crossr = random.randint(1, 4)  # 随机选择交叉的位点，[1,4]之间的任意整数
            dna1_1 = swt1[j][0:crossr].tolist()  # 在交叉点切出的染色体前一片段list
            dna1_2 = swt1[j][crossr:].tolist()  # 在交叉点切出的染色体后一片段list
            dna2_1 = swt2[j][0:crossr].tolist()
            dna2_2 = swt2[j][crossr:].tolist()
            dna1_1.extend(dna2_2)  # 得到的子染色体1，就是dna1_1
            dna2_1.extend(dna1_2)  # 得到的子染色体2，就是dna2_1
            swt1[j] = dna1_1  # 将dna1_1这个list赋值给解的相应行，即更新子染色体
            swt2[j] = dna2_1  # 将dna2_1这个list赋值给解的相应行，即更新子染色体
    else:  # 如果选出的两个解不同但是随机数大于交叉概率，就不交叉，直接复制
        solution_wt[i] = swt1
        solution_wt[i + 1] = swt2
pm = 0.6  # 变异概率为0.6，如果随机数小于0.6就变异，如果大于0.6就不变异
for i in solution_wt:
    pmr = random.random()
    mup = []  # 十个变异点，每个变异点是一个二元list为矩阵中的行和列。mup=[[3,2],[7,0]]
    if pmr < 0.6:  # 有十个变异点，在每个解的12*5个基因中
        for j in range(10):
            point = [random.randint(0, 11), random.randint(0, 4)]
            mup.append(point)
        for q in mup:  # 按照mup中的十个变异基因，对解i执行变异
            i[q[0]][q[1]] = random.choice(sid[q[1]])


# 函数版本,输入参数是选择之后的解，返回值是交叉变异之后的解
def wtcromu(solution_wt):
    for i in range(10):  # 选出10对父代的解
        swt1 = random.choice(solution_wt)  # 从种群中随机选出一个父代解
        swt2 = random.choice(solution_wt)  # 从种群中随机选出另一个父代解
        pc = 0.7  # 交叉概率，设定得比较高
        pcr = random.random()  # pcr小于pc就进行交叉操作
        if swt1.tolist() == swt2.tolist():  # 如果选出的是同一对染色体，就不进行交叉，直接用swt1=swt2更新种群
            solution_wt[i] = swt1  # ——————要验证，这样对不对，可以用list给矩阵的一行赋值
            solution_wt[i + 1] = swt2  # 用一行的矩阵元素给矩阵赋值可以吗
        elif swt1.tolist() != swt2.tolist() and pcr < pc:
            for j in range(12):  # 对于父代解中12条子染色体的其中一条
                crossr = random.randint(1, 4)  # 随机选择交叉的位点，[1,4]之间的任意整数
                dna1_1 = swt1[j][0:crossr].tolist()  # 在交叉点切出的染色体前一片段list
                dna1_2 = swt1[j][crossr:].tolist()  # 在交叉点切出的染色体后一片段list
                dna2_1 = swt2[j][0:crossr].tolist()
                dna2_2 = swt2[j][crossr:].tolist()
                dna1_1.extend(dna2_2)  # 得到的子染色体1，就是dna1_1
                dna2_1.extend(dna1_2)  # 得到的子染色体2，就是dna2_1
                swt1[j] = dna1_1  # 将dna1_1这个list赋值给解的相应行，即更新子染色体
                swt2[j] = dna2_1  # 将dna2_1这个list赋值给解的相应行，即更新子染色体
        else:  # 如果选出的两个解不同但是随机数大于交叉概率，就不交叉，直接复制
            solution_wt[i] = swt1
            solution_wt[i + 1] = swt2
    # 以下是变异部分
    pm = 0.6  # 变异概率为0.6，如果随机数小于0.6就变异，如果大于0.6就不变异
    for i in solution_wt:
        pmr = random.random()
        mup = []  # 十个变异点，每个变异点是一个二元list为矩阵中的行和列。mup=[[3,2],[7,0]]
        if pmr < 0.6:  # 有十个变异点，在每个解的12*5个基因中
            for j in range(10):
                point = [random.randint(0, 11), random.randint(0, 4)]
                mup.append(point)
            for q in mup:  # 按照mup中的十个变异基因，对解i执行变异
                i[q[0]][q[1]] = random.choice(sid[q[1]])
    return solution_wt
