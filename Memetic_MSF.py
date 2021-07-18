'''2021.7.15创建，将jupyter notebook中的混合元启发式算法程序“Memetic+Heuristic混合算法-12.27-与PC同步”导入进来'''

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import random,numpy as np
from random import shuffle,choice
import sys
sys.setrecursionlimit(1000000)
import copy,math
from Function import oss, lunpan, pj_pre, pj_ri, idcro, idcheck, pj_ne
from Drawing import hoisting_gatt, sinline, dueline, output  # 当__main__函数运行完之后，在python console运行这些函数，绘图或将计算数据导出到excel


colorset=['#00CD66','#F4A460','#00CED1','#ff3366','#58ACFA','#D358F7','#BDBDBD','#58FAF4','#F6CEE3','#FFFF00','#BFFF00','#B45F04']
#           1-绿色，2-橙色（原金色#FFD700），3-暗宝石绿，4-红色，5-湖蓝，6-淡紫，7-灰色，8-青色，9-粉色，10-明黄，11-嫩芽绿，12-棕色
import matplotlib.pyplot as plt

'''第一部分，初始化种群，初始个体schedule_wt是12个产品5道工序在7个工作队完成的初始顺序'''
t1 = [0.9, 3, 2.7, 1.5, 1, 9.1]
t2 = [1.4, 2.5, 0, 0.6, 0.5, 5]
t3 = [1.2, 1.9, 2.4, 1.8, 1.2, 8.5]
t4 = [0.5, 3.5, 1.3, 1.2, 1.5, 8]
t5 = [0, 2.8, 1.9, 0.9, 0.8, 6.4]
t6 = [2, 3.6, 3.3, 2.1, 2.1, 13.1]
t7 = [1.5, 1.5, 0.9, 0.6, 0.5, 5]
t8 = [0.7, 0.8, 1.2, 2.3, 1.3, 6.3]
t9 = [1.8, 2.2, 2.6, 0.8, 1.1, 8.5]
t10 = [0, 1.1, 0, 0.7, 0.6, 2.4]
t11 = [1.6, 2.9, 2, 1.3, 1.8, 9.6]
t12 = [2.1, 3.7, 3, 1.6, 2.2, 12.6]
task_wt = np.array([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12])  # 产品工序工时矩阵

job_st = np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

zerowt = {2: [(9, 2), (1, 2)], 4: [(4, 0), (9, 0)]}  # 工时为0的工序全安排在对应机器的最早位置

# 生成调度方案每台机器二进制编码的基准方案：


solution=[]  # 种群list，每一个元素都是一个schedule_wt个体解

bi_bench = {}

if 1==1:  # if下的种群是完全随机解
# 以下第27行至第46行是生成完全随机初始解的代码，班组分配方案job_to_wt已经事先确定了
    job_to_wt=np.array([[5, 3, 3, 5, 7],   # 第27行
    [4, 1, 1, 4, 7],
    [5, 3, 1, 3, 6],
    [4, 2, 1, 3, 6],
    [5, 2, 1, 2, 7],
    [4, 2, 1, 2, 7],
    [4, 3, 2, 4, 6],
    [5, 1, 3, 3, 6],
    [5, 3, 1, 2, 6],
    [5, 2, 2, 5, 6],
    [5, 2, 2, 3, 6],
    [5, 2, 1, 4, 7]])  # 机器分配方案

    schedule_wt={}  # 初始解，从机器分配方案中得到每台机器的工序列表,字典的键是机器号（1-7），
    for i in range(1,8):  # tsw是一个tuple,有两个元素，各是一维向量，第一个元素是job编号（0-11），第二个元素是工序号（0-4）,表示
        tsw=np.where(job_to_wt==i)  # 矩阵job_to_wt中字典键（i，代表对应班组wt）出现的行列位置，即该班组要完成的（产品、工序）
        schedule_wt[i]=[]
        for j in range(len(tsw[0])):
            schedule_wt[i].append((tsw[0][j],tsw[1][j]))  #比如1号wt的op为：schedule_wt[1]=[(1, 1), (1, 2), (2, 2), (3, 2), (4, 2),...]

    for m in schedule_wt: # 2021.7.17添加，先从个体解中删除掉工时为0的工序
        for mi in schedule_wt[m]:
            if task_wt[mi[0]][mi[1]]==0:
                schedule_wt[m].remove(mi)
    if sum([len(schedule_wt[mz]) for mz in schedule_wt])>=57: # 2021.7.17添加，检验是否成功删除
        print('初始解个体错了')

    bi_bench=schedule_wt
    for i in range(100):  # 先把初始schedule_wt复制为种群中的每一个个体
        solution.append(schedule_wt.copy())
    for js in solution:
        for m in range(1,8):
            js[m]=schedule_wt[m].copy() # 这一步非常关键，必须对每一个List都用copy()创建，仅有上面循环的copy不够
            shuffle(js[m])
# 第46行
else:  # else进一步分为两部分，if是完全随机初始种群，只使用启发式最优解的班组分配方案；else中有5个是启发式算法最优解，剩余95个是全随机解
# 以下schedule_wt是启发式算法求出的结果，schedule_wt是个体解，用于元启发式算法还要把工时为0的工序zerowt添加到启发式算法得出的schedule_wt中
    schedule_wt = {1: [(3, 1), (10, 1), (2, 2), (8, 1), (11, 2), (4, 1)],
                   2: [(9, 1), (5, 1), (2, 1), (6, 2), (11, 1), (1, 1), (8, 2), (0, 3), (4, 3)],
                   3: [(9, 3), (7, 1), (7, 2), (3, 2), (6, 1), (5, 2), (10, 2), (0, 1), (0, 2), (4, 2)],
                   4: [(3, 0), (7, 0), (0, 0), (1, 0), (10, 0), (8, 0), (7, 3), (5, 3), (10, 3), (11, 3)],
                   5: [(5, 0), (2, 0), (6, 0), (3, 3), (11, 0), (6, 3), (2, 3), (1, 3), (8, 3)],
                   6: [(9, 4), (6, 4), (2, 4), (10, 4), (8, 4), (0, 4)],
                   7: [(3, 4), (7, 4), (5, 4), (1, 4), (11, 4), (4, 4)]}
    # 前95个解都随机打散，只保留最后5个解是启发式算法的最优解
    bi_bench=schedule_wt
    for i in range(100):  # 先把初始schedule_wt复制为种群中的每一个个体
        solution.append(schedule_wt.copy())
    if 3==3:    # 2021.7.18 再增加一个逻辑，使用启发式算法解，If部分是只使用班组分配方案的完全随机初始种群，else部分是有5个初始个体为启发式算法解,剩余
        for js in solution:           # 95个解为使用相同班组分配方案的随机解
            for m in range(1, 8):
                js[m] = schedule_wt[m].copy()  # 这一步非常关键，必须对每一个List都用copy()创建，仅有上面循环的copy不够
                shuffle(js[m])
    else:
        for js in solution[0:95]:  # 12.21修改，前95个解需要打乱
            for m in range(1, 8):
                js[m] = schedule_wt[m].copy()  # 这一步非常关键，必须对每一个List都用copy()创建，仅有上面循环的copy不够
                shuffle(js[m])
        for js in solution[95:100]:  # 12.21修改，后5个解是启发式算法的最优解
            for m in range(1, 8):
                js[m] = schedule_wt[m].copy()  # 这一步非常关键，必须对每一个List都用copy()创建，仅有上面循环的copy不够

lent = [0, len(bi_bench[1]), len(bi_bench[2]), len(bi_bench[3]), len(bi_bench[4]), len(bi_bench[5]), len(bi_bench[6]),
        len(bi_bench[7])]  # 用在交叉变异函数中作为global变量，为1-7台机器的工序任务数量

'''第二部分，计算个体和种群适应度函数，因为有global变量，所以必须在主函数文件中定义'''

def fitcalu(schedule_w):  # 添加全局变量zerowt，从第376行开始修改
    global zerowt
    global job_st   # 12.21 添加，更规范
    global task_wt  # 12.21 添加，更规范
    jobstart=np.array(job_st-1,dtype=np.float)
    jobfinish=jobstart.copy()
    pwt=['wt',0,0,0,0,0,0,0] # 从index第1到第7个元素，代表对应wt的当前可安排工序
    c=0 # 计算次数，最后输出
    zerot=copy.deepcopy(zerowt) # 第376行，12.22 必须要深度复制，否则会更改全局zerowt
    schedule_wt=copy.deepcopy(schedule_w) # 12.22 也必须要深度复制，因为只有计算适应度时才需要添加工时为0的工序，所以不能更改外部的解
    for w in zerot:
        if w in schedule_wt.keys():
            zerot[w].extend(schedule_wt[w])
            schedule_wt[w]=zerot[w].copy()
    while min(jobstart.flat)==-1:   # 计算终止条件，开工时间矩阵没有-1了
        for i in range(1,8):
            c+=1 # 每部分计算完之后，都检索紧右工序是否工时为0，如果是，就赋值自己的开工、完工时间
            if pwt[i]!=len(schedule_wt[i]):
#                 print(f'机器号{i}  任务序号{pwt[i]}')
                if task_wt[schedule_wt[i][pwt[i]][0]][schedule_wt[i][pwt[i]][1]]==0: # 12.22 新增 工时为0的工序，开工完工时间都是0
                    jobstart[schedule_wt[i][pwt[i]][0]][schedule_wt[i][pwt[i]][1]]=0
                    jobfinish[schedule_wt[i][pwt[i]][0]][schedule_wt[i][pwt[i]][1]]=0
                    pwt[i]+=1
                elif schedule_wt[i][pwt[i]][1]==0 and pwt[i]==0:  # 如果机器的第一个工序也是该产品的第一个工序
                    jobstart[schedule_wt[i][pwt[i]][0]][schedule_wt[i][pwt[i]][1]]=0
                    jobfinish[schedule_wt[i][pwt[i]][0]][schedule_wt[i][pwt[i]][1]]=task_wt[schedule_wt[i][pwt[i]][0]][schedule_wt[i][pwt[i]][1]]
                    pwt[i]+=1
                elif pwt[i]==0 and jobstart[schedule_wt[i][pwt[i]][0]][schedule_wt[i][pwt[i]][1]-1]!=-1 and task_wt[schedule_wt[i][pwt[i]][0]][schedule_wt[i][pwt[i]][1]-1]==0:
                    # 12.22新增，当当前工序是产品的第0工序，且同产品上一工序的工时为0
                    a12=schedule_wt[i][pwt[i]][0]
                    b12=schedule_wt[i][pwt[i]][1]
                    pwin=schedule_wt[i][pwt[i]][1]-1
                    while True:
                        pwin-=1
                        if pwin==-1: # 说明该产品schedule_wt[i][pwt[i]][1]工序前的所有工序工时都为0
                            jobstart[a12][b12]=0
                            jobfinish[a12][b12]=task_wt[a12][b12]
                            pwt[i]+=1
                            break
                        elif task_wt[a12][pwin]==0:
                            pass
                        elif task_wt[a12][pwin]!=0 and jobstart[a12][pwin]==-1:
                            break # ***** 极其非常重要，遇到同产品前面工序虽然工时不为0，但该工序还未开始
                        elif task_wt[a12][pwin]!=0 and jobstart[a12][pwin]!=-1:
                            jobstart[a12][b12]=jobstart[a12][pwin]+task_wt[a12][pwin]
                            jobfinish[a12][b12]=jobstart[a12][b12]+task_wt[a12][b12]
                            pwt[i]+=1
                            break
                elif pwt[i]==0 and jobstart[schedule_wt[i][pwt[i]][0]][schedule_wt[i][pwt[i]][1]-1]!=-1 and task_wt[schedule_wt[i][pwt[i]][0]][schedule_wt[i][pwt[i]][1]-1]!=0:
                    # 12.22 跟上面的elif是一对，增加了一个条件：同产品上一工序工时不为0
                    a1=schedule_wt[i][pwt[i]][0]
                    b1=schedule_wt[i][pwt[i]][1]
                    jobstart[a1][b1]=jobstart[a1][b1-1]+task_wt[a1][b1-1]
                    jobfinish[a1][b1]=jobstart[a1][b1]+task_wt[a1][b1]
                    pwt[i]+=1
                elif pwt[i]!=0 and schedule_wt[i][pwt[i]][1]==0:
                    a2=schedule_wt[i][pwt[i]][0]
                    b2=schedule_wt[i][pwt[i]][1]
                    a3=schedule_wt[i][pwt[i]-1][0]
                    b3=schedule_wt[i][pwt[i]-1][1]
                    jobstart[a2][b2]=jobstart[a3][b3]+task_wt[a3][b3]
                    jobfinish[a2][b2]=jobstart[a2][b2]+task_wt[a2][b2]
                    pwt[i]+=1
                elif jobstart[schedule_wt[i][pwt[i]][0]][schedule_wt[i][pwt[i]][1]-1]!=-1 and task_wt[schedule_wt[i][pwt[i]][0]][schedule_wt[i][pwt[i]][1]-1]==0:
                    # 12.22 新增，普通情况，当同产品上一工序工时为0
                    a7=schedule_wt[i][pwt[i]][0]
                    b7=schedule_wt[i][pwt[i]][1]
                    a8=schedule_wt[i][pwt[i]-1][0]
                    b8=schedule_wt[i][pwt[i]-1][1]
                    pb7=schedule_wt[i][pwt[i]][1]-1
                    while True:
                        pb7-=1
                        if pb7==-1:
                            jobstart[a7][b7]=jobstart[a8][b8]+task_wt[a8][b8]
                            jobfinish[a7][b7]=jobstart[a7][b7]+task_wt[a7][b7]
                            pwt[i]+=1
                            break
                        elif task_wt[a7][pb7]==0:
                            pass
                        elif task_wt[a7][pb7]!=0 and jobstart[a7][pb7]!=-1:
                            jobstart[a7][b7]=max(jobstart[a7][pb7]+task_wt[a7][pb7],jobstart[a8][b8]+task_wt[a8][b8])
                            jobfinish[a7][b7]=jobstart[a7][b7]+task_wt[a7][b7]
                            pwt[i]+=1
                            break
                        elif task_wt[a7][pb7]!=0 and jobstart[a7][pb7]==-1:
                            break
                elif jobstart[schedule_wt[i][pwt[i]][0]][schedule_wt[i][pwt[i]][1]-1]!=-1 and task_wt[schedule_wt[i][pwt[i]][0]][schedule_wt[i][pwt[i]][1]-1]!=0:
                    # 12.22 跟上面的elif是一对，增加了一个条件：同产品上一工序工时不为0
                    a4=schedule_wt[i][pwt[i]][0]
                    b4=schedule_wt[i][pwt[i]][1]-1
                    a5=schedule_wt[i][pwt[i]-1][0]
                    b5=schedule_wt[i][pwt[i]-1][1]
                    jobstart[a4][b4+1]=max(jobstart[a4][b4]+task_wt[a4][b4],jobstart[a5][b5]+task_wt[a5][b5])
                    jobfinish[a4][b4+1]=jobstart[a4][b4+1]+task_wt[a4][b4+1]
                    pwt[i]+=1
                else:
                    pass
#     print(c)  10.27 程序验证正确，取消打印。但可以作为变量返回，从而分析计算的时间复杂度
    return jobstart,jobfinish

def fitness_calu(solut):  # 最终计算解schedule_wt的开工时间矩阵和完工时间矩阵,输入参数是解除死锁之后的种群list
    solu_start=[] # 种群中每一个解的开工时间list，长度即种群规模100
    solu_fit=[]   # 种群中每一个解的完工时间list，长度即种群规模100
#     cin=0
    for sch in solut:
#         cin+=1
#         print(cin)
        jbst,jbfi=fitcalu(sch)
        solu_start.append(jbst)
        solu_fit.append(jbfi)
    return solu_start,solu_fit # 返回种群的开工时间矩阵和完工时间矩阵


'''第三部分，一个变异辅助函数和交叉变异函数'''

def backin(sol, xxma, xr):  # 因为用到了fitcalu，所以 backin函数必须出现在主函数中
    sma, fma = fitcalu(sol)

    #     po=np.where(fma==max(fma.flat))
    # 注意，只对本问题有特殊性，因为是1-5台机器，所以下一工序不会超出边界，即sol[xxma][xr][1]+1最多是4
    # ***** 极其非常重要的一个关键，就是下面if条件中or的运用
    if pj_ri(fma, sol, xxma, xr + 1) != 0 and fma[sol[xxma][xr + 1][0]][pj_pre(fma, sol, xxma, xr + 1)] < \
            sma[sol[xxma][xr][0]][sol[xxma][xr][1]] \
            and pj_ne(fma, sol, xxma, xr) != 5 and pj_ne(fma, sol, xxma, xr + 1) != 5 and fma[sol[xxma][xr][0]][
        sol[xxma][xr][1]] < sma[sol[xxma][xr][0]][pj_ne(fma, sol, xxma, xr)] or \
            pj_ne(fma, sol, xxma, xr) == 5 and pj_ne(fma, sol, xxma, xr + 1) != 5 and pj_ri(fma, sol, xxma,
                                                                                            xr + 1) != 0 and \
            fma[sol[xxma][xr + 1][0]][pj_pre(fma, sol, xxma, xr + 1)] < sma[sol[xxma][xr][0]][sol[xxma][xr][1]]:
        jiqn = 0  # 用于记录右边产品下一工序所在的机器
        prin = 0  # 用于记录右边产品下一工序在机器上的顺序
        for keyy, itemm in sol.items():
            if (sol[xxma][xr + 1][0], pj_ne(fma, sol, xxma, xr + 1)) in itemm:
                jiqn = keyy
                prin = itemm.index((sol[xxma][xr + 1][0], pj_ne(fma, sol, xxma, xr + 1)))
                break
        if prin == 0 and pj_ri(fma, sol, jiqn, prin + 1) != 0:
            # and \fma[sol[jiqn][prin+1][0]][sol[jiqn][prin+1][1]-1] > fma[sol[xxma][xr+1][0]][sol[xxma][xr+1][1]]: 12.20取消了这个条件
            # 当产品是所在机器jipn的第一道工序时，且prin+1不是该产品的第0工序，就直接交换
            sol[xxma][xr], sol[xxma][xr + 1] = sol[xxma][xr + 1], sol[xxma][xr]
            rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
            sol = rsol[0][0]
            sma, fma = fitcalu(sol)
        elif prin != (len(sol[jiqn]) - 1) and prin != 0 and pj_ri(fma, sol, jiqn, prin + 1) != 0 and \
                fma[sol[jiqn][prin + 1][0]][pj_pre(fma, sol, jiqn, prin + 1)] > fma[sol[xxma][xr + 1][0]][
            sol[xxma][xr + 1][1]] and \
                (sma[sol[jiqn][prin][0]][sol[jiqn][prin][1]] - fma[sol[jiqn][prin - 1][0]][sol[jiqn][prin - 1][1]]) >= \
                task_wt[sol[xxma][xr][0]][sol[xxma][xr][1]]:
            # 在产品不是机器的第一个工序且右边产品不是第0工序的前提下，当产品前的间隙大于[xxma][xr]本产品工序(第0工序)时间，
            # 并且右边产品工序的上一工序完工时间比本产品的上一工序（[xxma][xr+1]）完工时间更晚
            sol[xxma][xr], sol[xxma][xr + 1] = sol[xxma][xr + 1], sol[xxma][xr]
            rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
            sol = rsol[0][0]
            sma, fma = fitcalu(sol)
        elif prin == (len(sol[jiqn]) - 1) and (
                sma[sol[jiqn][prin][0]][sol[jiqn][prin][1]] - fma[sol[jiqn][prin - 1][0]][sol[jiqn][prin - 1][1]]) >= \
                task_wt[sol[xxma][xr][0]][sol[xxma][xr][1]]:
            sol[xxma][xr], sol[xxma][xr + 1] = sol[xxma][xr + 1], sol[xxma][xr]
            rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
            sol = rsol[0][0]
            sma, fma = fitcalu(sol)
        elif prin == (len(sol[jiqn]) - 1) and (
                sma[sol[jiqn][prin][0]][sol[jiqn][prin][1]] - fma[sol[jiqn][prin - 1][0]][sol[jiqn][prin - 1][1]]) < \
                task_wt[sol[xxma][xr][0]][sol[xxma][xr][1]]:
            interval = (sma[sol[jiqn][prin][0]][sol[jiqn][prin][1]] - fma[sol[jiqn][prin - 1][0]][
                sol[jiqn][prin - 1][1]]) / task_wt[sol[xxma][xr][0]][sol[xxma][xr][1]]
            if random.random() < interval * 0.9:
                sol[xxma][xr], sol[xxma][xr + 1] = sol[xxma][xr + 1], sol[xxma][xr]
                rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                sol = rsol[0][0]
                sma, fma = fitcalu(sol)
        elif prin != (len(sol[jiqn]) - 1) and prin != 0 and pj_ri(fma, sol, jiqn, prin + 1) != 0 and \
                fma[sol[jiqn][prin + 1][0]][pj_pre(fma, sol, jiqn, prin + 1)] > fma[sol[xxma][xr + 1][0]][
            sol[xxma][xr + 1][1]] and (
                sma[sol[jiqn][prin][0]][sol[jiqn][prin][1]] - fma[sol[jiqn][prin - 1][0]][sol[jiqn][prin - 1][1]]) < \
                task_wt[sol[xxma][xr][0]][sol[xxma][xr][1]]:
            interval = (sma[sol[jiqn][prin][0]][sol[jiqn][prin][1]] - fma[sol[jiqn][prin - 1][0]][
                sol[jiqn][prin - 1][1]]) / task_wt[sol[xxma][xr][0]][sol[xxma][xr][1]]
            if random.random() < interval * 0.9:
                sol[xxma][xr], sol[xxma][xr + 1] = sol[xxma][xr + 1], sol[xxma][xr]
                rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                sol = rsol[0][0]
                sma, fma = fitcalu(sol)

def cromut(cso, mf, avg):  # 交叉变异函数，输入为种群，返回为交叉变异后的种群。mf为历代至今的最优解，即从历代hi5中选出的最优解
    global bi_bench
    global lent
    # 1、交叉程序
    cro_cso = []  # 交叉变异后的种群，解的数量为100
    #     ocso=oss(cso) 不需要了，因为调用交叉变异函数之前，在轮盘赌选择之前，种群已解锁， 12.28添加，先解锁，为了计算适应度来计算交叉概率
    #     cso=ocso[0]   不需要了，因为调用交叉变异函数之前，在轮盘赌选择之前，种群已解锁，12.28添加，解锁后的种群
    for i in range(len(cso) // 2):  # 12.21修改，原先是50，这样更通用，注意//商是整数，而/结果是小数，不能用于for循环
        parents = random.sample(cso, 2)  # random.sample(li,n)从li中随机取出n个不同元素，返回结果是长度为n的list
        fa = copy.deepcopy(parents[0])  # 父亲解，10.29增加.copy()  ****** 10.30改为deepcopy深度复制
        ma = copy.deepcopy(parents[1])  # 母亲解，10.29增加.copy()  ****** 10.30改为deepcopy深度复制
        faa, fab = fitcalu(fa)  # 12.28添加，为了计算交叉概率
        maa, mab = fitcalu(ma)  # 12.28添加，为了计算交叉概率
        minb = min(max(fab.flat), max(mab.flat))  # 两个解适应度最小的那个
        pcro = None
        if minb <= avg:
            pcro = 1.2 / (1 + math.exp(0.3 * (avg - minb)))  # 12.28 交叉的概率，当minb比平均值越小，交叉概率越小，当minb比平均值越大，交叉概率越大
        else:
            pcro = 1.2 / (1 + math.exp(0.6 * (avg - minb)))
        if random.random() < pcro:  # 如果交叉的话
            a1 = random.choice([1, 2, 3, 4, 5])
            a2 = random.choice([6, 7])
            crp1 = random.randint(1, lent[a1] - 1)  # 确定交叉点1，交叉的时候，更换处理长链
            fa1 = fa[a1][0:crp1]
            fa2 = fa[a1][crp1:]
            ma1 = ma[a1][0:crp1]
            ma2 = ma[a1][crp1:]
            crp2 = random.randint(1, lent[a2] - 1)  # 确定交叉点2，交叉的时候，更换处理长链
            fat1 = fa[a2][0:crp2]
            fat2 = fa[a2][crp2:]
            mat1 = ma[a2][0:crp2]
            mat2 = ma[a2][crp2:]
            if len(fa1) >= len(fa2):
                indfa = []
                indma = []
                for j in range(len(fa1)):
                    if fa1[j] in ma1:
                        pass
                    else:
                        indfa.append(j)
                    if ma1[j] in fa1:
                        pass
                    else:
                        indma.append(j)
                for ij in range(len(indfa)):  # 处理交叉的染色体不一致的情况
                    fa1[indfa[ij]], ma1[indma[ij]] = ma1[indma[ij]], fa1[indfa[ij]]
            else:
                indfa1 = []
                indma1 = []
                for jj in range(len(fa2)):
                    if fa2[jj] in ma2:
                        pass
                    else:
                        indfa1.append(jj)
                    if ma2[jj] in fa2:
                        pass
                    else:
                        indma1.append(jj)
                for ijj in range(len(indfa1)):  # 处理交叉的染色体不一致的情况
                    fa2[indfa1[ijj]], ma2[indma1[ijj]] = ma2[indma1[ijj]], fa2[indfa1[ijj]]
            fa1.extend(ma2)  # 10.29修改，之前的fa[a1]=fa1.extend(ma2)，实际上fa[a1]=None
            fa[a1] = fa1
            ma1.extend(fa2)  # 10.29修改，之前的ma[a1]=ma1.extend(fa2)，实际上ma[a1]=None
            ma[a1] = ma1
            # 至此完成机器a1的单点交叉，接下来进行机器a2的单点交叉：
            #         crp2=random.randint(1,lent[a2]-1)  # 确定交叉点2，交叉的时候，更换处理长链
            #         fat1=fa[a2][0:crp2]
            #         fat2=fa[a2][crp2:]
            #         mat1=ma[a2][0:crp2]
            #         mat2=ma[a2][crp2:]
            if len(fat1) >= len(fat2):
                indfat = []
                indmat = []
                for jt in range(len(fat1)):
                    if fat1[jt] in mat1:
                        pass
                    else:
                        indfat.append(jt)
                    if mat1[jt] in fat1:
                        pass
                    else:
                        indmat.append(jt)
                for ijt in range(len(indfat)):  # 处理交叉的染色体不一致的情况
                    fat1[indfat[ijt]], mat1[indmat[ijt]] = mat1[indmat[ijt]], fat1[indfat[ijt]]
            else:
                indfat1 = []
                indmat1 = []
                for jjt in range(len(fat2)):
                    if fat2[jjt] in mat2:
                        pass
                    else:
                        indfat1.append(jjt)
                    if mat2[jjt] in fat2:
                        pass
                    else:
                        indmat1.append(jjt)
                for ijjt in range(len(indfat1)):  # 处理交叉的染色体不一致的情况
                    fat2[indfat1[ijjt]], mat2[indmat1[ijjt]] = mat2[indmat1[ijjt]], fat2[indfat1[ijjt]]
            fat1.extend(mat2)  # 10.29修改，之前的fa[a2]=fat1.extend(mat2)，实际上fa[a2]=None
            fa[a2] = fat1
            mat1.extend(fat2)  # 10.29修改，之前的ma[a2]=mat1.extend(fat2)，实际上ma[a2]=None
            ma[a2] = mat1
            cro_cso.append(fa)
            cro_cso.append(ma)
        else:  # 12.28 如果不满足交叉概率，就不交叉，直接将随机选出的两个解添加到输出结果cro_cso中
            cro_cso.append(fa)
            cro_cso.append(ma)

    # 2、变异程序，每个解的每台机器，随机选出两个产品工序，如果随机数小于交叉概率，就交换两个产品工序

    cro_csox = oss(cro_cso)  # 12.5新增，非常重要，由于下面的变异需要计算种群适应度，所以必须先在这里对交叉后的种群解锁
    cro_cso = cro_csox[0]  # 12.5新增，非常重要，由于下面的变异需要计算种群适应度，所以必须先在这里对交叉后的种群解锁
    for sol in cro_cso:
        #         print('开始第',cro_cso.index(sol),'个解')
        sma, fma = fitcalu(sol)  # 求解sol的开工时间矩阵sma和完工时间矩阵fma
        #         print('初始计算适应度完成')
        prom = None  # 变异概率
        fma_va = max(fma.flat)
        if fma_va <= avg:
            prom = 2 / (1 + math.exp(0.3 * (avg - fma_va)))  # 12.28 变异概率，只有当解更优时，才降低变异概率，当解比平均解更差，一定变异
        else:
            prom = 1
        if random.random() < prom:  # 如果变异的话

            # 主动修复：由于最后一个工序的机器只生产最后一个工序，所以尽一切可能地消除间隙，只要消除就一定能缩短总工时
            for xmai in [6, 7]:  #
                for ppr in range(len(sol[xmai]) - 1):
                    if ppr == 0:
                        if fma[sol[xmai][1][0]][pj_pre(fma, sol, xmai, 1)] < sma[sol[xmai][0][0]][
                            4]:  # 如果后面产品工序的前一工序完工时间更早，就交换
                            sol[xmai][0], sol[xmai][1] = sol[xmai][1], sol[xmai][0]
                            rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                            sol = rsol[0][0]
                            #                         sma,fma=fitcalu(rsol[0][0])
                            sma, fma = fitcalu(sol)  # *** 很重要，一定要再计算一遍求解sol的开工时间矩阵sma和完工时间矩阵fma
                    else:
                        if fma[sol[xmai][ppr - 1][0]][4] < sma[sol[xmai][ppr][0]][4]:  # 说明在当前产品工序ppr前有间隙
                            if fma[sol[xmai][ppr + 1][0]][pj_pre(fma, sol, xmai, ppr + 1)] < sma[sol[xmai][ppr][0]][4]:
                                sol[xmai][ppr], sol[xmai][ppr + 1] = sol[xmai][ppr + 1], sol[xmai][ppr]
                                rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                                sol = rsol[0][0]
                                sma, fma = fitcalu(sol)  # *** 很重要，每次交换完之后都要再计算一遍，求sol的开工时间矩阵sma和完工时间矩阵fma
            # 第二类变异，更复杂一些，先寻找间隙、记录，然后根据权重或者知识指导来交换间隙右边的两个相邻工序
            for xxma in range(1, 6):
                for xr in range(len(sol[xxma]) - 1):
                    if xr == 0:  # 对于机器的第一道工序
                        if pj_ri(fma, sol, xxma, xr) != 0:  # 只有当该工序不是第0道工序
                            if pj_ri(fma, sol, xxma, 1) == 0:  # 如果右边的产品工序是第0个工序，那么就直接交换
                                sol[xxma][0], sol[xxma][1] = sol[xxma][1], sol[xxma][0]
                                rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                                sol = rsol[0][0]
                                sma, fma = fitcalu(sol)
                            elif pj_ri(fma, sol, xxma, 1) != 0 and fma[sol[xxma][1][0]][pj_pre(fma, sol, xxma, 1)] < \
                                    sma[sol[xxma][0][0]][sol[xxma][0][1]] \
                                    and sma[sol[xxma][0][0]][sol[xxma][0][1]] - fma[sol[xxma][1][0]][
                                pj_pre(fma, sol, xxma, 1)] >= task_wt[sol[xxma][1][0]][sol[xxma][1][1]]:
                                sol[xxma][0], sol[xxma][1] = sol[xxma][1], sol[xxma][0]
                                rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                                sol = rsol[0][0]
                                sma, fma = fitcalu(sol)  # 如果第二个产品工序不是第0个工序，但是满足交换条件，就交换
                            elif pj_ri(fma, sol, xxma, 1) != 0 and fma[sol[xxma][1][0]][pj_pre(fma, sol, xxma, 1)] < \
                                    sma[sol[xxma][0][0]][sol[xxma][0][1]] \
                                    and sma[sol[xxma][0][0]][sol[xxma][0][1]] - fma[sol[xxma][1][0]][
                                pj_pre(fma, sol, xxma, 1)] < task_wt[sol[xxma][1][0]][sol[xxma][1][1]]:
                                # 如果不满足直接交换条件，就将上一工序完工时间差记录下来
                                interva1 = (sma[sol[xxma][0][0]][sol[xxma][0][1]] - fma[sol[xxma][1][0]][
                                    pj_pre(fma, sol, xxma, 1)]) / task_wt[sol[xxma][1][0]][sol[xxma][1][1]]
                                if random.random() < interva1 * 0.7:
                                    sol[xxma][0], sol[xxma][1] = sol[xxma][1], sol[xxma][0]
                                    rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                                    sol = rsol[0][0]
                                    sma, fma = fitcalu(sol)
                                backin(sol, xxma, xr)  # 12.24添加，然后再判断是否满足后向交换

                    else:
                        if pj_ri(fma, sol, xxma, xr) == 0:  # *** 如果是产品的第0道工序，自身没有间隙，根据后续间隙来判断是否直接交换
                            backin(sol, xxma, xr)  # 后向交换判断
                        else:
                            if fma[sol[xxma][xr - 1][0]][sol[xxma][xr - 1][1]] < sma[sol[xxma][xr][0]][
                                sol[xxma][xr][1]] and pj_ri(fma, sol, xxma, xr + 1) == 0:
                                # 如果前面有间隙，且右边是产品的第0道工序，就直接交换
                                sol[xxma][xr], sol[xxma][xr + 1] = sol[xxma][xr + 1], sol[xxma][xr]
                                rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                                sol = rsol[0][0]
                                sma, fma = fitcalu(sol)
                            elif fma[sol[xxma][xr - 1][0]][sol[xxma][xr - 1][1]] < sma[sol[xxma][xr][0]][
                                sol[xxma][xr][1]] and \
                                    pj_ri(fma, sol, xxma, xr + 1) != 0 and fma[sol[xxma][xr + 1][0]][
                                pj_pre(fma, sol, xxma, xr + 1)] < sma[sol[xxma][xr][0]][sol[xxma][xr][1]] and \
                                    min(sma[sol[xxma][xr][0]][sol[xxma][xr][1]] - fma[sol[xxma][xr - 1][0]][
                                        sol[xxma][xr - 1][1]],
                                        sma[sol[xxma][xr][0]][sol[xxma][xr][1]] - fma[sol[xxma][xr + 1][0]][
                                            pj_pre(fma, sol, xxma, xr + 1)]) >= task_wt[sol[xxma][xr + 1][0]][
                                sol[xxma][xr + 1][1]]:
                                # 如果前面有间隙，右边不是产品的第0道工序但满足直接交换条件，就直接交换
                                sol[xxma][xr], sol[xxma][xr + 1] = sol[xxma][xr + 1], sol[xxma][xr]
                                rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                                sol = rsol[0][0]
                                sma, fma = fitcalu(sol)
                            elif fma[sol[xxma][xr - 1][0]][sol[xxma][xr - 1][1]] < sma[sol[xxma][xr][0]][
                                sol[xxma][xr][1]] and \
                                    pj_ri(fma, sol, xxma, xr + 1) != 0 and fma[sol[xxma][xr + 1][0]][
                                pj_pre(fma, sol, xxma, xr + 1)] < sma[sol[xxma][xr][0]][sol[xxma][xr][1]] and \
                                    min(sma[sol[xxma][xr][0]][sol[xxma][xr][1]] - fma[sol[xxma][xr - 1][0]][
                                        sol[xxma][xr - 1][1]],
                                        sma[sol[xxma][xr][0]][sol[xxma][xr][1]] - fma[sol[xxma][xr + 1][0]][
                                            pj_pre(fma, sol, xxma, xr + 1)]) < task_wt[sol[xxma][xr + 1][0]][
                                sol[xxma][xr + 1][1]]:
                                interva2 = min(sma[sol[xxma][xr][0]][sol[xxma][xr][1]] - fma[sol[xxma][xr - 1][0]][
                                    sol[xxma][xr - 1][1]],
                                               sma[sol[xxma][xr][0]][sol[xxma][xr][1]] - fma[sol[xxma][xr + 1][0]][
                                                   pj_pre(fma, sol, xxma, xr + 1)]) / task_wt[sol[xxma][xr + 1][0]][
                                               sol[xxma][xr + 1][1]]
                                if random.random() < interva2 * 0.7:
                                    sol[xxma][xr], sol[xxma][xr + 1] = sol[xxma][xr + 1], sol[xxma][xr]
                                    rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                                    sol = rsol[0][0]
                                    sma, fma = fitcalu(sol)  # 如果第二个产品工序不是第0个工序，但是满足交换条件，就交换
                                # 如果前面有间隙，右边不是产品的第0道工序且不满足直接交换条件，就记录在interval
                                backin(sol, xxma, xr)  # 12.24添加，然后判断后向交换情况
                            elif fma[sol[xxma][xr - 1][0]][sol[xxma][xr - 1][1]] == sma[sol[xxma][xr][0]][
                                sol[xxma][xr][1]] and \
                                    pj_ri(fma, sol, xxma, xr + 1) != 0 and fma[sol[xxma][xr + 1][0]][
                                pj_pre(fma, sol, xxma, xr + 1)] <= sma[sol[xxma][xr][0]][sol[xxma][xr][1]]:
                                backin(sol, xxma, xr)  # 整个elif都是12.24新添加，如果没有间隙，但交换后xr+1能按相同时间开工，就判断后向交换
                            else:  # 右边工序的上一工序完成时间更晚，如果交换会更糟，就不交换
                                pass
                                # 以下模块是再对剩余的潜在交换产品工序进行处理，只交换间隙最大的产品工序
            #         inte_ma={} # 键是机器，值是最大的间隙值
            #         inte_ma_inde={} # 键是机器，值是最大间隙值所在的index
            #         hamm_d=0  # 在此记录变异的机器，如果该机器已发生变异，那么后面的知识指导变异就要排除这台机器
            #         for kim,vim in interval.items():
            #             inte_ma[kim]=max(vim)
            #             inte_ma_inde[kim]=vim.index(max(vim))
            #         for kinm,vinm in inte_ma.items():
            #             if max(inte_ma.values())==vinm:
            #                 if random.random()<mutrt1:  # 并且变异概率为mutrt
            #                     hamm_d=kinm
            #                     sol[kinm][inte_ma_inde[kinm]],sol[kinm][inte_ma_inde[kinm]+1]=sol[kinm][inte_ma_inde[kinm]+1],sol[kinm][inte_ma_inde[kinm]]
            #                 break

            # 12.29 将关键路径工序变异从第一个位置移到此位置
            po = np.where(fma == max(fma.flat))  # 求完工时间矩阵最后一个完工任务的产品号工序号，po是一个tuple，有两个元素，分别是行号向量和列号向量

            # 12.25作废，由更精确的下面模块取代。以下是第一类变异，对调度方案最后一个产品工序，将该产品的第一道工序置于最先开始
            #         for key,value in sol.items( ):
            #             if (po[0][0],0) in value:
            #                 while value.index((po[0][0],0))!=0:
            #                     indmu=value.index((po[0][0],0))
            #                     if random.random()<0.5:
            #                         sol[key][indmu-1],sol[key][indmu]=sol[key][indmu],sol[key][indmu-1]
            #                     if random.random()<0.8:
            #                         break
            #                 break
            #         rsol=oss([sol])  # 交换后，先解锁，然后再计算适应度
            #         sol=rsol[0][0]
            #         sma,fma=fitcalu(sol)  # *** 注意，这里也要重新计算一遍

            # 第301行，12.25创建的第一类变异，至第426行，是关键路径工序处理模块
            p0 = po[0][0]  # 最后完工工序的产品
            p1 = po[1][0]  # 最后完工工序的工序
            p2 = p1 - 1  # 最后完工产品工序的上一工序号
            pini = None  # 产品p0的第一个工序（工时不为0）
            pini_e = None  # 在下一个while中用来判断是否直到产品的第0个工序，仍然找不到可调整缩短的工序
            for i in range(task_wt.shape[1] - 1):  # 找到产品p0的实际第一个工序的序号pini
                if task_wt[p0][i] != 0:
                    pini = i
                    break
            p0m = []  # 12.26添加，记录最后完工产品p0的所有前面无间隙工序，用于第395行新增的条件
            while True:  # 本循环的目的，就是要找到最后完工产品p0从最后一个工序p1开始，第一个前面没有间隙（上一工序完工时间不等于本工序开工时间）的工序
                if fma[p0][p2] != 0 and fma[p0][p1] != 0:
                    if sma[p0][p1] > fma[p0][p2] and p2 != pini:
                        p0m.append(p1)
                        p1 -= 1
                        p2 -= 1
                    elif sma[p0][p1] == fma[p0][p2] and p2 == pini:
                        pini_e = 1
                        break
                    elif sma[p0][p1] > fma[p0][p2] and p2 == pini:
                        p0m.append(p1)
                        break
                    else:
                        p1 -= 1
                        p2 -= 1
                elif fma[p0][p2] == 0 and fma[p0][p1] != 0:
                    p2 -= 1
                elif fma[p0][p2] != 0 and fma[p0][p1] == 0:
                    p1 -= 1
                else:
                    p1 -= 1
                    p2 -= 1
            # 上述while结束后的p1，就是需要通过自身与紧左工序交换（当p1不为最后一个工序时）或者让紧左工序利用左侧空隙（当p1是最后一个工序时必须采用，当p1不是最后一个工序时也可以采用）
            p0m.sort()  # 最初的p0m是从大到小排列，不能用，需要将其按从小到大排列
            kpm = 0
            lpm = 0
            llpm = 0
            if len(p0m) != 0:  # 如果len(p0m)==0的话，说明就是 pini_e的情况，即最后完工的产品0只有第一个工序（工时非0）前面才没有间隙
                kpm = [key for key, value in sol.items() if (p0, p0m[-1]) in value][0]  # 最后一个工序所在的机器
                lpm = sol[kpm].index((p0, p0m[-1]))  # 需要处理的p1工序在机器kpm上的index
                llpm = lpm - 1  # 紧临的左侧工序
            if len(p0m) == 0 and pini_e == 1:  # 此时，产品p0的第一个工序p2/pini需要交换到前面
                kpm1 = [key for key, value in sol.items() if (p0, p2) in value][0]  # 最后一个工序所在的机器
                lpm1 = sol[kpm1].index((p0, p2))  # 需要处理的p1工序在机器kpm上的index
                if lpm1 != 0:  # 保证不在机器的第一道工序
                    lpm1_p = random.randint(0, lpm1 - 1)
                    sol[kpm1][lpm1_p], sol[kpm1][lpm1] = sol[kpm1][lpm1], sol[kpm1][lpm1_p]
                    rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                    sol = rsol[0][0]
                    sma, fma = fitcalu(sol)  # *** 注意，这里也要重新计算一遍
            elif p0m[-1] == po[1][0]:  # 说明产品p0的最后一个工序前面没有间隙，需要通过紧临左侧工序填补左侧空袭，通过有空隙左侧工序的前道工序交换
                while True:  # 目的是找到p1左侧前面没有间隙的工序llpm，好在解sol不存在工时为0的工序
                    if llpm == 0:  # 说明一直到机器kpm的第一道工序，前面才有间隙
                        break
                    elif sma[sol[kpm][llpm][0]][sol[kpm][llpm][1]] > fma[sol[kpm][llpm - 1][0]][sol[kpm][llpm - 1][1]]:
                        break
                    else:
                        llpm -= 1
                lp0 = sol[kpm][llpm][0]  # 需要缩短间隙的产品号
                lp1 = sol[kpm][llpm][1] - 1  # 需要缩短间隙的产品工序号
                while fma[sol[kpm][llpm][0]][lp1] == 0:  # 确保lp1是产品lp0的sol[kpm][llpm][1]工序的上一工时非零工序
                    lp1 -= 1
                lp2 = lp1 - 1  # lp1的上一工序
                lpini = None  # 产品lp0的第一个工序（工时不为0）
                lpini_e = None  # 说明产品lp0只有第一个工序lpini才能交换
                for j in range(task_wt.shape[1] - 1):
                    if task_wt[lp0][j] != 0:
                        lpini = j
                        break
                while True:
                    if fma[lp0][lp1] != 0 and fma[lp0][lp2] != 0:
                        if sma[lp0][lp1] > fma[lp0][lp2]:
                            break
                        elif sma[lp0][lp1] == fma[lp0][lp2] and lp2 == lpini:
                            lpini_e = 1
                            break
                        else:
                            lp1 -= 1
                            lp2 -= 1
                    elif fma[lp0][lp1] == 0 and fma[lp0][lp2] == 0:
                        lp1 -= 1
                        lp2 -= 1
                    elif fma[lp0][lp1] != 0 and fma[lp0][lp2] == 0:
                        lp2 -= 1
                    elif fma[lp0][lp1] == 0 and fma[lp0][lp2] != 0:
                        lp1 -= 1
                if lpini_e == 1:
                    kpm3 = [key for key, value in sol.items() if (lp0, lp2) in value][0]
                    lpm3 = sol[kpm3].index((lp0, lp2))
                    if lpm3 != 0:  # 12.30添加，更稳妥一点
                        sol[kpm3][lpm3], sol[kpm3][lpm3 - 1] = sol[kpm3][lpm3 - 1], sol[kpm3][lpm3]
                        rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                        sol = rsol[0][0]
                        sma, fma = fitcalu(sol)  # *** 注意，这里也要重新计算一遍
                else:
                    kpm4 = [key for key, value in sol.items() if (lp0, lp1) in value][0]
                    lpm4 = sol[kpm4].index((lp0, lp1))
                    if sol[kpm4][lpm4 - 1][0] != p0:  # 第395行，12.26添加的条件，可能紧左工序是最后完工产品p0的工序，此时只能交换p0的前面无间隙工序
                        sol[kpm4][lpm4], sol[kpm4][lpm4 - 1] = sol[kpm4][lpm4 - 1], sol[kpm4][lpm4]
                        rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                        sol = rsol[0][0]
                        sma, fma = fitcalu(sol)  # *** 注意，这里也要重新计算一遍
                    else:
                        p00 = None
                        if p0m[0] > sol[kpm4][lpm4 - 1][1]:
                            p00 = pini
                        else:
                            for i in p0m:
                                if i == sol[kpm4][lpm4 - 1][1]:
                                    p00 = i
                                    break
                                elif i > sol[kpm4][lpm4 - 1][1]:
                                    p00 = p0m[p0m.index(i) - 1]
                                    break
                        kpm5 = [key for key, value in sol.items() if (p0, p00) in value][0]
                        lpm5 = sol[kpm5].index((p0, p00))
                        if lpm5 != 0:  # 仅仅适用于当p00==pini的情况，因为其它p0m的工序不可能是相应机器的第一道工序
                            sol[kpm5][lpm5], sol[kpm5][lpm5 - 1] = sol[kpm5][lpm5 - 1], sol[kpm5][lpm5]
                            rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                            sol = rsol[0][0]
                            sma, fma = fitcalu(sol)

            else:  # 说明p1不是最后一个工序，且p2不是第一个工序，所以要通过交换p1与其左侧工序或者通过左侧工序前移
                kpm2 = [key for key, value in sol.items() if (p0, p1) in value][0]
                lpm2 = sol[kpm2].index((p0, p1))
                sol[kpm2][lpm2], sol[kpm2][lpm2 - 1] = sol[kpm2][lpm2 - 1], sol[kpm2][lpm2]
                rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                sol = rsol[0][0]
                sma, fma = fitcalu(sol)  # 第426行，第一类变异，关键路径工序处理模块结束

            # 以下模块是文化算法，用状况知识，即历代最优解指导变异（局部搜索）
            # 1.1 首先将当前解和历代最优解mf转化为二进制型
            bi_sol = {}  # 调度方案/解sol的二进制表示型
            bi_mf = {}  # 历代最优解mf的二进制表示型
            for ibi in bi_bench:
                bi_sol[ibi] = []
                bi_mf[ibi] = []
                for jbi in bi_bench[ibi]:
                    for qbi in bi_bench[ibi][bi_bench[ibi].index(jbi) + 1:]:
                        if sol[ibi].index(jbi) < sol[ibi].index(qbi):
                            bi_sol[ibi].append(1)
                        if sol[ibi].index(jbi) > sol[ibi].index(qbi):
                            bi_sol[ibi].append(0)
                        if mf[ibi].index(jbi) < mf[ibi].index(qbi):
                            bi_mf[ibi].append(1)
                        if mf[ibi].index(jbi) > mf[ibi].index(qbi):
                            bi_mf[ibi].append(0)
            # 1.2 然后计算当前解和历代解海明距离最大的染色体，并找到不一样且间隙最大的基因，进行变异
            calhai_bi = {}  # 当前解与历代最优解海明距离字典，键是机器，值是机器对应染色体的海明距离
            for smm in range(1, 6):
                calhai_bi[smm] = 0
                for isc in range(len(bi_mf[smm])):
                    if bi_mf[smm][isc] != bi_sol[smm][isc]:
                        calhai_bi[smm] += 1
            hmma = 0  # 海明距离最大的机器
            for ck, cv in calhai_bi.items():
                if cv == max(calhai_bi.values()):
                    hmma = ck
                    break
            lde = random.randint(0, len(sol[hmma]) - 2)
            if random.random() < 0.7:
                sol[hmma][lde], sol[hmma][lde + 1] = sol[hmma][lde + 1], sol[hmma][lde]

    return cro_cso  # 返回经过交叉、变异后的种群

def mut1(cro_cso, mf):
    global bi_bench
    global lent
    mutrt1 = 0.5  # 变异概率
    mutrt2 = 0.8  # 第二种变异概率

    cro_csox = oss(cro_cso)  # 单独把变异函数拿出来并迭代运行需要
    cro_cso = cro_csox[0]  # 单独把变异函数拿出来并迭代运行需要

    for sol in cro_cso:
        #         print('开始第',cro_cso.index(sol),'个解')
        sma, fma = fitcalu(sol)  # 求解sol的开工时间矩阵sma和完工时间矩阵fma
        #         print('初始计算适应度完成')
        po = np.where(fma == max(fma.flat))  # 求完工时间矩阵最后一个完工任务的产品号工序号，po是一个tuple，有两个元素，分别是行号向量和列号向量

        # 12.25作废，由更精确的下面模块取代。以下是第一类变异，对调度方案最后一个产品工序，将该产品的第一道工序置于最先开始
        #         for key,value in sol.items( ):
        #             if (po[0][0],0) in value:
        #                 while value.index((po[0][0],0))!=0:
        #                     indmu=value.index((po[0][0],0))
        #                     if random.random()<0.5:
        #                         sol[key][indmu-1],sol[key][indmu]=sol[key][indmu],sol[key][indmu-1]
        #                     if random.random()<0.8:
        #                         break
        #                 break
        #         rsol=oss([sol])  # 交换后，先解锁，然后再计算适应度
        #         sol=rsol[0][0]
        #         sma,fma=fitcalu(sol)  # *** 注意，这里也要重新计算一遍

        # 第301行，12.25创建的第一类变异，至第426行，是关键路径工序处理模块
        p0 = po[0][0]  # 最后完工工序的产品
        p1 = po[1][0]  # 最后完工工序的工序
        p2 = p1 - 1  # 最后完工产品工序的上一工序号
        pini = None  # 产品p0的第一个工序（工时不为0）
        pini_e = None  # 在下一个while中用来判断是否直到产品的第0个工序，仍然找不到可调整缩短的工序
        for i in range(task_wt.shape[1] - 1):  # 找到产品p0的实际第一个工序的序号pini
            if task_wt[p0][i] != 0:
                pini = i
                break
        p0m = []  # 12.26添加，记录最后完工产品p0的所有前面无间隙工序，用于第395行新增的条件
        while True:  # 本循环的目的，就是要找到最后完工产品p0从最后一个工序p1开始，第一个前面没有间隙（上一工序完工时间不等于本工序开工时间）的工序
            if fma[p0][p2] != 0 and fma[p0][p1] != 0:
                if sma[p0][p1] > fma[p0][p2] and p2 != pini:
                    p0m.append(p1)
                    p1 -= 1
                    p2 -= 1
                elif sma[p0][p1] == fma[p0][p2] and p2 == pini:
                    pini_e = 1
                    break
                elif sma[p0][p1] > fma[p0][p2] and p2 == pini:
                    p0m.append(p1)
                    break
                else:
                    p1 -= 1
                    p2 -= 1
            elif fma[p0][p2] == 0 and fma[p0][p1] != 0:
                p2 -= 1
            elif fma[p0][p2] != 0 and fma[p0][p1] == 0:
                p1 -= 1
            else:
                p1 -= 1
                p2 -= 1
        p0m.sort()
        # 上述while结束后的p1，就是需要通过自身与紧左工序交换（当p1不为最后一个工序时）或者让紧左工序利用左侧空隙（当p1是最后一个工序时必须采用，当p1不是最后一个工序时也可以采用）
        kpm = 0
        lpm = 0
        llpm = 0
        if len(p0m) != 0:
            kpm = [key for key, value in sol.items() if (p0, p0m[-1]) in value][0]  # 最后一个工序所在的机器
            lpm = sol[kpm].index((p0, p0m[-1]))  # 需要处理的p1工序在机器kpm上的index
            llpm = lpm - 1  # 紧临的左侧工序
        if len(p0m) == 0 and pini_e == 1:  # 此时，产品p0的第一个工序p2/pini需要交换到前面
            kpm1 = [key for key, value in sol.items() if (p0, p2) in value][0]  # 最后一个工序所在的机器
            lpm1 = sol[kpm1].index((p0, p2))  # 需要处理的p1工序在机器kpm上的index
            if lpm1 != 0:  # 保证不在机器的第一道工序
                lpm1_p = random.randint(0, lpm1 - 1)
                sol[kpm1][lpm1_p], sol[kpm1][lpm1] = sol[kpm1][lpm1], sol[kpm1][lpm1_p]
                rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                sol = rsol[0][0]
                sma, fma = fitcalu(sol)  # *** 注意，这里也要重新计算一遍
        elif p0m[-1] == po[1][0]:  # 说明产品p0的最后一个工序前面没有间隙，需要通过紧临左侧工序填补左侧空袭，通过有空隙左侧工序的前道工序交换
            while True:  # 目的是找到p1左侧前面没有间隙的工序llpm，好在解sol不存在工时为0的工序
                if llpm == 0:  # 说明一直到机器kpm的第一道工序，前面才有间隙
                    break
                elif sma[sol[kpm][llpm][0]][sol[kpm][llpm][1]] > fma[sol[kpm][llpm - 1][0]][sol[kpm][llpm - 1][1]]:
                    break
                else:
                    llpm -= 1
            lp0 = sol[kpm][llpm][0]  # 需要缩短间隙的产品号
            lp1 = sol[kpm][llpm][1] - 1  # 需要缩短间隙的产品工序号
            while fma[sol[kpm][llpm][0]][lp1] == 0:  # 确保lp1是产品lp0的sol[kpm][llpm][1]工序的上一工时非零工序
                lp1 -= 1
            lp2 = lp1 - 1  # lp1的上一工序
            lpini = None  # 产品lp0的第一个工序（工时不为0）
            lpini_e = None  # 说明产品lp0只有第一个工序lpini才能交换
            for j in range(task_wt.shape[1] - 1):
                if task_wt[lp0][j] != 0:
                    lpini = j
                    break
            while True:
                if fma[lp0][lp1] != 0 and fma[lp0][lp2] != 0:
                    if sma[lp0][lp1] > fma[lp0][lp2]:
                        break
                    elif sma[lp0][lp1] == fma[lp0][lp2] and lp2 == lpini:
                        lpini_e = 1
                        break
                    else:
                        lp1 -= 1
                        lp2 -= 1
                elif fma[lp0][lp1] == 0 and fma[lp0][lp2] == 0:
                    lp1 -= 1
                    lp2 -= 1
                elif fma[lp0][lp1] != 0 and fma[lp0][lp2] == 0:
                    lp2 -= 1
                elif fma[lp0][lp1] == 0 and fma[lp0][lp2] != 0:
                    lp1 -= 1
            if lpini_e == 1:
                kpm3 = [key for key, value in sol.items() if (lp0, lp2) in value][0]
                lpm3 = sol[kpm3].index((lp0, lp2))
                sol[kpm3][lpm3], sol[kpm3][lpm3 - 1] = sol[kpm3][lpm3 - 1], sol[kpm3][lpm3]
                rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                sol = rsol[0][0]
                sma, fma = fitcalu(sol)  # *** 注意，这里也要重新计算一遍
            else:
                kpm4 = [key for key, value in sol.items() if (lp0, lp1) in value][0]
                lpm4 = sol[kpm4].index((lp0, lp1))
                if sol[kpm4][lpm4 - 1][0] != p0:  # 第395行，12.26添加的条件，可能紧左工序是最后完工产品p0的工序，此时只能交换p0的前面无间隙工序
                    sol[kpm4][lpm4], sol[kpm4][lpm4 - 1] = sol[kpm4][lpm4 - 1], sol[kpm4][lpm4]
                    rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                    sol = rsol[0][0]
                    sma, fma = fitcalu(sol)  # *** 注意，这里也要重新计算一遍
                else:
                    p00 = None
                    if p0m[0] > sol[kpm4][lpm4 - 1][1]:
                        p00 = pini
                    else:
                        for i in p0m:
                            if i == sol[kpm4][lpm4 - 1][1]:
                                p00 = i
                                break
                            elif i > sol[kpm4][lpm4 - 1][1]:
                                p00 = p0m[p0m.index(i) - 1]
                                break
                    kpm5 = [key for key, value in sol.items() if (p0, p00) in value][0]
                    lpm5 = sol[kpm5].index((p0, p00))
                    if lpm5 != 0:  # 仅仅适用于当p00==pini的情况，因为其它p0m的工序不可能是相应机器的第一道工序
                        sol[kpm5][lpm5], sol[kpm5][lpm5 - 1] = sol[kpm5][lpm5 - 1], sol[kpm5][lpm5]
                        rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                        sol = rsol[0][0]
                        sma, fma = fitcalu(sol)

        else:  # 说明p1不是最后一个工序，且p2不是第一个工序，所以要通过交换p1与其左侧工序或者通过左侧工序前移
            kpm2 = [key for key, value in sol.items() if (p0, p1) in value][0]
            lpm2 = sol[kpm2].index((p0, p1))
            sol[kpm2][lpm2], sol[kpm2][lpm2 - 1] = sol[kpm2][lpm2 - 1], sol[kpm2][lpm2]
            rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
            sol = rsol[0][0]
            sma, fma = fitcalu(sol)  # 第426行，第一类变异，关键路径工序处理模块结束

        # 主动修复：由于最后一个工序的机器只生产最后一个工序，所以尽一切可能地消除间隙，只要消除就一定能缩短总工时
        for xmai in [6, 7]:  #
            for ppr in range(len(sol[xmai]) - 1):
                if ppr == 0:
                    if fma[sol[xmai][1][0]][pj_pre(fma, sol, xmai, 1)] < sma[sol[xmai][0][0]][
                        4]:  # 如果后面产品工序的前一工序完工时间更早，就交换
                        sol[xmai][0], sol[xmai][1] = sol[xmai][1], sol[xmai][0]
                        rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                        sol = rsol[0][0]
                        #                         sma,fma=fitcalu(rsol[0][0])
                        sma, fma = fitcalu(sol)  # *** 很重要，一定要再计算一遍求解sol的开工时间矩阵sma和完工时间矩阵fma
                else:
                    if fma[sol[xmai][ppr - 1][0]][4] < sma[sol[xmai][ppr][0]][4]:  # 说明在当前产品工序ppr前有间隙
                        if fma[sol[xmai][ppr + 1][0]][pj_pre(fma, sol, xmai, ppr + 1)] < sma[sol[xmai][ppr][0]][4]:
                            sol[xmai][ppr], sol[xmai][ppr + 1] = sol[xmai][ppr + 1], sol[xmai][ppr]
                            rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                            sol = rsol[0][0]
                            sma, fma = fitcalu(sol)  # *** 很重要，每次交换完之后都要再计算一遍，求sol的开工时间矩阵sma和完工时间矩阵fma
        # 第二类变异，更复杂一些，先寻找间隙、记录，然后根据权重或者知识指导来交换间隙右边的两个相邻工序
        for xxma in range(1, 6):
            for xr in range(len(sol[xxma]) - 1):
                if xr == 0:  # 对于机器的第一道工序
                    if pj_ri(fma, sol, xxma, xr) != 0:  # 只有当该工序不是第0道工序
                        if pj_ri(fma, sol, xxma, 1) == 0:  # 如果右边的产品工序是第0个工序，那么就直接交换
                            sol[xxma][0], sol[xxma][1] = sol[xxma][1], sol[xxma][0]
                            rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                            sol = rsol[0][0]
                            sma, fma = fitcalu(sol)
                        elif pj_ri(fma, sol, xxma, 1) != 0 and fma[sol[xxma][1][0]][pj_pre(fma, sol, xxma, 1)] < \
                                sma[sol[xxma][0][0]][sol[xxma][0][1]] \
                                and sma[sol[xxma][0][0]][sol[xxma][0][1]] - fma[sol[xxma][1][0]][
                            pj_pre(fma, sol, xxma, 1)] >= task_wt[sol[xxma][1][0]][sol[xxma][1][1]]:
                            sol[xxma][0], sol[xxma][1] = sol[xxma][1], sol[xxma][0]
                            rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                            sol = rsol[0][0]
                            sma, fma = fitcalu(sol)  # 如果第二个产品工序不是第0个工序，但是满足交换条件，就交换
                        elif pj_ri(fma, sol, xxma, 1) != 0 and fma[sol[xxma][1][0]][pj_pre(fma, sol, xxma, 1)] < \
                                sma[sol[xxma][0][0]][sol[xxma][0][1]] \
                                and sma[sol[xxma][0][0]][sol[xxma][0][1]] - fma[sol[xxma][1][0]][
                            pj_pre(fma, sol, xxma, 1)] < task_wt[sol[xxma][1][0]][sol[xxma][1][1]]:
                            # 如果不满足直接交换条件，就将上一工序完工时间差记录下来
                            interva1 = (sma[sol[xxma][0][0]][sol[xxma][0][1]] - fma[sol[xxma][1][0]][
                                pj_pre(fma, sol, xxma, 1)]) / task_wt[sol[xxma][1][0]][sol[xxma][1][1]]
                            if random.random() < interva1 * 0.7:
                                sol[xxma][0], sol[xxma][1] = sol[xxma][1], sol[xxma][0]
                                rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                                sol = rsol[0][0]
                                sma, fma = fitcalu(sol)
                            backin(sol, xxma, xr)  # 12.24添加，然后再判断是否满足后向交换

                else:
                    if pj_ri(fma, sol, xxma, xr) == 0:  # *** 如果是产品的第0道工序，自身没有间隙，根据后续间隙来判断是否直接交换
                        backin(sol, xxma, xr)  # 后向交换判断
                    else:
                        if fma[sol[xxma][xr - 1][0]][sol[xxma][xr - 1][1]] < sma[sol[xxma][xr][0]][
                            sol[xxma][xr][1]] and pj_ri(fma, sol, xxma, xr + 1) == 0:
                            # 如果前面有间隙，且右边是产品的第0道工序，就直接交换
                            sol[xxma][xr], sol[xxma][xr + 1] = sol[xxma][xr + 1], sol[xxma][xr]
                            rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                            sol = rsol[0][0]
                            sma, fma = fitcalu(sol)
                        elif fma[sol[xxma][xr - 1][0]][sol[xxma][xr - 1][1]] < sma[sol[xxma][xr][0]][
                            sol[xxma][xr][1]] and \
                                pj_ri(fma, sol, xxma, xr + 1) != 0 and fma[sol[xxma][xr + 1][0]][
                            pj_pre(fma, sol, xxma, xr + 1)] < sma[sol[xxma][xr][0]][sol[xxma][xr][1]] and \
                                min(sma[sol[xxma][xr][0]][sol[xxma][xr][1]] - fma[sol[xxma][xr - 1][0]][
                                    sol[xxma][xr - 1][1]],
                                    sma[sol[xxma][xr][0]][sol[xxma][xr][1]] - fma[sol[xxma][xr + 1][0]][
                                        pj_pre(fma, sol, xxma, xr + 1)]) >= task_wt[sol[xxma][xr + 1][0]][
                            sol[xxma][xr + 1][1]]:
                            # 如果前面有间隙，右边不是产品的第0道工序但满足直接交换条件，就直接交换
                            sol[xxma][xr], sol[xxma][xr + 1] = sol[xxma][xr + 1], sol[xxma][xr]
                            rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                            sol = rsol[0][0]
                            sma, fma = fitcalu(sol)
                        elif fma[sol[xxma][xr - 1][0]][sol[xxma][xr - 1][1]] < sma[sol[xxma][xr][0]][
                            sol[xxma][xr][1]] and \
                                pj_ri(fma, sol, xxma, xr + 1) != 0 and fma[sol[xxma][xr + 1][0]][
                            pj_pre(fma, sol, xxma, xr + 1)] < sma[sol[xxma][xr][0]][sol[xxma][xr][1]] and \
                                min(sma[sol[xxma][xr][0]][sol[xxma][xr][1]] - fma[sol[xxma][xr - 1][0]][
                                    sol[xxma][xr - 1][1]],
                                    sma[sol[xxma][xr][0]][sol[xxma][xr][1]] - fma[sol[xxma][xr + 1][0]][
                                        pj_pre(fma, sol, xxma, xr + 1)]) < task_wt[sol[xxma][xr + 1][0]][
                            sol[xxma][xr + 1][1]]:
                            interva2 = min(sma[sol[xxma][xr][0]][sol[xxma][xr][1]] - fma[sol[xxma][xr - 1][0]][
                                sol[xxma][xr - 1][1]],
                                           sma[sol[xxma][xr][0]][sol[xxma][xr][1]] - fma[sol[xxma][xr + 1][0]][
                                               pj_pre(fma, sol, xxma, xr + 1)]) / task_wt[sol[xxma][xr + 1][0]][
                                           sol[xxma][xr + 1][1]]
                            if random.random() < interva2 * 0.7:
                                sol[xxma][xr], sol[xxma][xr + 1] = sol[xxma][xr + 1], sol[xxma][xr]
                                rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                                sol = rsol[0][0]
                                sma, fma = fitcalu(sol)  # 如果第二个产品工序不是第0个工序，但是满足交换条件，就交换
                            # 如果前面有间隙，右边不是产品的第0道工序且不满足直接交换条件，就记录在interval
                            backin(sol, xxma, xr)  # 12.24添加，然后判断后向交换情况
                        elif fma[sol[xxma][xr - 1][0]][sol[xxma][xr - 1][1]] == sma[sol[xxma][xr][0]][
                            sol[xxma][xr][1]] and \
                                pj_ri(fma, sol, xxma, xr + 1) != 0 and fma[sol[xxma][xr + 1][0]][
                            pj_pre(fma, sol, xxma, xr + 1)] <= sma[sol[xxma][xr][0]][sol[xxma][xr][1]]:
                            backin(sol, xxma, xr)  # 整个elif都是12.24新添加，如果没有间隙，但交换后xr+1能按相同时间开工，就判断后向交换
                        else:  # 右边工序的上一工序完成时间更晚，如果交换会更糟，就不交换
                            pass
                            # 以下模块是再对剩余的潜在交换产品工序进行处理，只交换间隙最大的产品工序
        #         inte_ma={} # 键是机器，值是最大的间隙值
        #         inte_ma_inde={} # 键是机器，值是最大间隙值所在的index
        #         hamm_d=0  # 在此记录变异的机器，如果该机器已发生变异，那么后面的知识指导变异就要排除这台机器
        #         for kim,vim in interval.items():
        #             inte_ma[kim]=max(vim)
        #             inte_ma_inde[kim]=vim.index(max(vim))
        #         for kinm,vinm in inte_ma.items():
        #             if max(inte_ma.values())==vinm:
        #                 if random.random()<mutrt1:  # 并且变异概率为mutrt
        #                     hamm_d=kinm
        #                     sol[kinm][inte_ma_inde[kinm]],sol[kinm][inte_ma_inde[kinm]+1]=sol[kinm][inte_ma_inde[kinm]+1],sol[kinm][inte_ma_inde[kinm]]
        #                 break

        # 以下模块是文化算法，用状况知识，即历代最优解指导变异（局部搜索）
        # 1.1 首先将当前解和历代最优解mf转化为二进制型
        bi_sol = {}  # 调度方案/解sol的二进制表示型
        bi_mf = {}  # 历代最优解mf的二进制表示型
        for ibi in bi_bench:
            bi_sol[ibi] = []
            bi_mf[ibi] = []
            for jbi in bi_bench[ibi]:
                for qbi in bi_bench[ibi][bi_bench[ibi].index(jbi) + 1:]:
                    if sol[ibi].index(jbi) < sol[ibi].index(qbi):
                        bi_sol[ibi].append(1)
                    if sol[ibi].index(jbi) > sol[ibi].index(qbi):
                        bi_sol[ibi].append(0)
                    if mf[ibi].index(jbi) < mf[ibi].index(qbi):
                        bi_mf[ibi].append(1)
                    if mf[ibi].index(jbi) > mf[ibi].index(qbi):
                        bi_mf[ibi].append(0)
        # 1.2 然后计算当前解和历代解海明距离最大的染色体，并找到不一样且间隙最大的基因，进行变异
        calhai_bi = {}  # 当前解与历代最优解海明距离字典，键是机器，值是机器对应染色体的海明距离
        for smm in range(1, 6):
            calhai_bi[smm] = 0
            for isc in range(len(bi_mf[smm])):
                if bi_mf[smm][isc] != bi_sol[smm][isc]:
                    calhai_bi[smm] += 1
        hmma = 0  # 海明距离最大的机器
        for ck, cv in calhai_bi.items():
            if cv == max(calhai_bi.values()):
                hmma = ck
                break
        lde = random.randint(0, len(sol[hmma]) - 2)
        if random.random() < mutrt2:
            sol[hmma][lde], sol[hmma][lde + 1] = sol[hmma][lde + 1], sol[hmma][lde]

    return cro_cso  # 返回经过交叉、变异后的种群

def mut2(cro_cso, mf):  # 第二个变异函数mut2，比mut1好用，先变异前向间隙后向间隙，再变异关键路径工序
    global bi_bench
    global lent
    mutrt1 = 0.5  # 变异概率
    mutrt2 = 0.8  # 第二种变异概率

    cro_csox = oss(cro_cso)  # 单独把变异函数拿出来并迭代运行需要
    cro_cso = cro_csox[0]  # 单独把变异函数拿出来并迭代运行需要

    for sol in cro_cso:
        #         print('开始第',cro_cso.index(sol),'个解')

        sma, fma = fitcalu(sol)
        # 主动修复：由于最后一个工序的机器只生产最后一个工序，所以尽一切可能地消除间隙，只要消除就一定能缩短总工时
        for xmai in [6, 7]:  #
            for ppr in range(len(sol[xmai]) - 1):
                if ppr == 0:
                    if fma[sol[xmai][1][0]][pj_pre(fma, sol, xmai, 1)] < sma[sol[xmai][0][0]][
                        4]:  # 如果后面产品工序的前一工序完工时间更早，就交换
                        sol[xmai][0], sol[xmai][1] = sol[xmai][1], sol[xmai][0]
                        rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                        sol = rsol[0][0]
                        #                         sma,fma=fitcalu(rsol[0][0])
                        sma, fma = fitcalu(sol)  # *** 很重要，一定要再计算一遍求解sol的开工时间矩阵sma和完工时间矩阵fma
                else:
                    if fma[sol[xmai][ppr - 1][0]][4] < sma[sol[xmai][ppr][0]][4]:  # 说明在当前产品工序ppr前有间隙
                        if fma[sol[xmai][ppr + 1][0]][pj_pre(fma, sol, xmai, ppr + 1)] < sma[sol[xmai][ppr][0]][4]:
                            sol[xmai][ppr], sol[xmai][ppr + 1] = sol[xmai][ppr + 1], sol[xmai][ppr]
                            rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                            sol = rsol[0][0]
                            sma, fma = fitcalu(sol)  # *** 很重要，每次交换完之后都要再计算一遍，求sol的开工时间矩阵sma和完工时间矩阵fma
        # 第二类变异，更复杂一些，先寻找间隙、记录，然后根据权重或者知识指导来交换间隙右边的两个相邻工序
        for xxma in range(1, 6):
            for xr in range(len(sol[xxma]) - 1):
                if xr == 0:  # 对于机器的第一道工序
                    if pj_ri(fma, sol, xxma, xr) != 0:  # 只有当该工序不是第0道工序
                        if pj_ri(fma, sol, xxma, 1) == 0:  # 如果右边的产品工序是第0个工序，那么就直接交换
                            sol[xxma][0], sol[xxma][1] = sol[xxma][1], sol[xxma][0]
                            rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                            sol = rsol[0][0]
                            sma, fma = fitcalu(sol)
                        elif pj_ri(fma, sol, xxma, 1) != 0 and fma[sol[xxma][1][0]][pj_pre(fma, sol, xxma, 1)] < \
                                sma[sol[xxma][0][0]][sol[xxma][0][1]] \
                                and sma[sol[xxma][0][0]][sol[xxma][0][1]] - fma[sol[xxma][1][0]][
                            pj_pre(fma, sol, xxma, 1)] >= task_wt[sol[xxma][1][0]][sol[xxma][1][1]]:
                            sol[xxma][0], sol[xxma][1] = sol[xxma][1], sol[xxma][0]
                            rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                            sol = rsol[0][0]
                            sma, fma = fitcalu(sol)  # 如果第二个产品工序不是第0个工序，但是满足交换条件，就交换
                        elif pj_ri(fma, sol, xxma, 1) != 0 and fma[sol[xxma][1][0]][pj_pre(fma, sol, xxma, 1)] < \
                                sma[sol[xxma][0][0]][sol[xxma][0][1]] \
                                and sma[sol[xxma][0][0]][sol[xxma][0][1]] - fma[sol[xxma][1][0]][
                            pj_pre(fma, sol, xxma, 1)] < task_wt[sol[xxma][1][0]][sol[xxma][1][1]]:
                            # 如果不满足直接交换条件，就将上一工序完工时间差记录下来
                            interva1 = (sma[sol[xxma][0][0]][sol[xxma][0][1]] - fma[sol[xxma][1][0]][
                                pj_pre(fma, sol, xxma, 1)]) / task_wt[sol[xxma][1][0]][sol[xxma][1][1]]
                            if random.random() < interva1 * 0.7:
                                sol[xxma][0], sol[xxma][1] = sol[xxma][1], sol[xxma][0]
                                rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                                sol = rsol[0][0]
                                sma, fma = fitcalu(sol)
                            backin(sol, xxma, xr)  # 12.24添加，然后再判断是否满足后向交换

                else:
                    if pj_ri(fma, sol, xxma, xr) == 0:  # *** 如果是产品的第0道工序，自身没有间隙，根据后续间隙来判断是否直接交换
                        backin(sol, xxma, xr)  # 后向交换判断
                    else:
                        if fma[sol[xxma][xr - 1][0]][sol[xxma][xr - 1][1]] < sma[sol[xxma][xr][0]][
                            sol[xxma][xr][1]] and pj_ri(fma, sol, xxma, xr + 1) == 0:
                            # 如果前面有间隙，且右边是产品的第0道工序，就直接交换
                            sol[xxma][xr], sol[xxma][xr + 1] = sol[xxma][xr + 1], sol[xxma][xr]
                            rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                            sol = rsol[0][0]
                            sma, fma = fitcalu(sol)
                        elif fma[sol[xxma][xr - 1][0]][sol[xxma][xr - 1][1]] < sma[sol[xxma][xr][0]][
                            sol[xxma][xr][1]] and \
                                pj_ri(fma, sol, xxma, xr + 1) != 0 and fma[sol[xxma][xr + 1][0]][
                            pj_pre(fma, sol, xxma, xr + 1)] < sma[sol[xxma][xr][0]][sol[xxma][xr][1]] and \
                                min(sma[sol[xxma][xr][0]][sol[xxma][xr][1]] - fma[sol[xxma][xr - 1][0]][
                                    sol[xxma][xr - 1][1]],
                                    sma[sol[xxma][xr][0]][sol[xxma][xr][1]] - fma[sol[xxma][xr + 1][0]][
                                        pj_pre(fma, sol, xxma, xr + 1)]) >= task_wt[sol[xxma][xr + 1][0]][
                            sol[xxma][xr + 1][1]]:
                            # 如果前面有间隙，右边不是产品的第0道工序但满足直接交换条件，就直接交换
                            sol[xxma][xr], sol[xxma][xr + 1] = sol[xxma][xr + 1], sol[xxma][xr]
                            rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                            sol = rsol[0][0]
                            sma, fma = fitcalu(sol)
                        elif fma[sol[xxma][xr - 1][0]][sol[xxma][xr - 1][1]] < sma[sol[xxma][xr][0]][
                            sol[xxma][xr][1]] and \
                                pj_ri(fma, sol, xxma, xr + 1) != 0 and fma[sol[xxma][xr + 1][0]][
                            pj_pre(fma, sol, xxma, xr + 1)] < sma[sol[xxma][xr][0]][sol[xxma][xr][1]] and \
                                min(sma[sol[xxma][xr][0]][sol[xxma][xr][1]] - fma[sol[xxma][xr - 1][0]][
                                    sol[xxma][xr - 1][1]],
                                    sma[sol[xxma][xr][0]][sol[xxma][xr][1]] - fma[sol[xxma][xr + 1][0]][
                                        pj_pre(fma, sol, xxma, xr + 1)]) < task_wt[sol[xxma][xr + 1][0]][
                            sol[xxma][xr + 1][1]]:
                            interva2 = min(sma[sol[xxma][xr][0]][sol[xxma][xr][1]] - fma[sol[xxma][xr - 1][0]][
                                sol[xxma][xr - 1][1]],
                                           sma[sol[xxma][xr][0]][sol[xxma][xr][1]] - fma[sol[xxma][xr + 1][0]][
                                               pj_pre(fma, sol, xxma, xr + 1)]) / task_wt[sol[xxma][xr + 1][0]][
                                           sol[xxma][xr + 1][1]]
                            if random.random() < interva2 * 0.7:
                                sol[xxma][xr], sol[xxma][xr + 1] = sol[xxma][xr + 1], sol[xxma][xr]
                                rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                                sol = rsol[0][0]
                                sma, fma = fitcalu(sol)  # 如果第二个产品工序不是第0个工序，但是满足交换条件，就交换
                            # 如果前面有间隙，右边不是产品的第0道工序且不满足直接交换条件，就记录在interval
                            backin(sol, xxma, xr)  # 12.24添加，然后判断后向交换情况
                        elif fma[sol[xxma][xr - 1][0]][sol[xxma][xr - 1][1]] == sma[sol[xxma][xr][0]][
                            sol[xxma][xr][1]] and \
                                pj_ri(fma, sol, xxma, xr + 1) != 0 and fma[sol[xxma][xr + 1][0]][
                            pj_pre(fma, sol, xxma, xr + 1)] <= sma[sol[xxma][xr][0]][sol[xxma][xr][1]]:
                            backin(sol, xxma, xr)  # 整个elif都是12.24新添加，如果没有间隙，但交换后xr+1能按相同时间开工，就判断后向交换
                        else:  # 右边工序的上一工序完成时间更晚，如果交换会更糟，就不交换
                            pass

        sma, fma = fitcalu(sol)  # 求解sol的开工时间矩阵sma和完工时间矩阵fma
        #         print('初始计算适应度完成')
        po = np.where(fma == max(fma.flat))  # 求完工时间矩阵最后一个完工任务的产品号工序号，po是一个tuple，有两个元素，分别是行号向量和列号向量

        # 第301行，12.25创建的第一类变异，至第426行，是关键路径工序处理模块
        p0 = po[0][0]  # 最后完工工序的产品
        p1 = po[1][0]  # 最后完工工序的工序
        p2 = p1 - 1  # 最后完工产品工序的上一工序号
        pini = None  # 产品p0的第一个工序（工时不为0）
        pini_e = None  # 在下一个while中用来判断是否直到产品的第0个工序，仍然找不到可调整缩短的工序
        for i in range(task_wt.shape[1] - 1):  # 找到产品p0的实际第一个工序的序号pini
            if task_wt[p0][i] != 0:
                pini = i
                break
        p0m = []  # 12.26添加，记录最后完工产品p0的所有前面无间隙工序，用于第395行新增的条件
        while True:  # 本循环的目的，就是要找到最后完工产品p0从最后一个工序p1开始，第一个前面没有间隙（上一工序完工时间不等于本工序开工时间）的工序
            if fma[p0][p2] != 0 and fma[p0][p1] != 0:
                if sma[p0][p1] > fma[p0][p2] and p2 != pini:
                    p0m.append(p1)
                    p1 -= 1
                    p2 -= 1
                elif sma[p0][p1] == fma[p0][p2] and p2 == pini:
                    pini_e = 1
                    break
                elif sma[p0][p1] > fma[p0][p2] and p2 == pini:
                    p0m.append(p1)
                    break
                else:
                    p1 -= 1
                    p2 -= 1
            elif fma[p0][p2] == 0 and fma[p0][p1] != 0:
                p2 -= 1
            elif fma[p0][p2] != 0 and fma[p0][p1] == 0:
                p1 -= 1
            else:
                p1 -= 1
                p2 -= 1
        # 上述while结束后的p1，就是需要通过自身与紧左工序交换（当p1不为最后一个工序时）或者让紧左工序利用左侧空隙（当p1是最后一个工序时必须采用，当p1不是最后一个工序时也可以采用）
        p0m.sort()  # 最初得到的p0m是从大到小排列，因此需要对其从小到大排列
        kpm = 0
        lpm = 0
        llpm = 0
        if len(p0m) != 0:
            kpm = [key for key, value in sol.items() if (p0, p0m[-1]) in value][0]  # 最后一个工序所在的机器
            lpm = sol[kpm].index((p0, p0m[-1]))  # 需要处理的p1工序在机器kpm上的index
            llpm = lpm - 1  # 紧临的左侧工序
        if len(p0m) == 0 and pini_e == 1:  # 此时，产品p0的第一个工序p2/pini需要交换到前面
            kpm1 = [key for key, value in sol.items() if (p0, p2) in value][0]  # 最后一个工序所在的机器
            lpm1 = sol[kpm1].index((p0, p2))  # 需要处理的p1工序在机器kpm上的index
            if lpm1 != 0:  # 保证不在机器的第一道工序
                lpm1_p = random.randint(0, lpm1 - 1)
                sol[kpm1][lpm1_p], sol[kpm1][lpm1] = sol[kpm1][lpm1], sol[kpm1][lpm1_p]
                rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                sol = rsol[0][0]
                sma, fma = fitcalu(sol)  # *** 注意，这里也要重新计算一遍
        elif p0m[-1] == po[1][0]:  # 说明产品p0的最后一个工序前面没有间隙，需要通过紧临左侧工序填补左侧空袭，通过有空隙左侧工序的前道工序交换
            while True:  # 目的是找到p1左侧前面没有间隙的工序llpm，好在解sol不存在工时为0的工序
                if llpm == 0:  # 说明一直到机器kpm的第一道工序，前面才有间隙
                    break
                elif sma[sol[kpm][llpm][0]][sol[kpm][llpm][1]] > fma[sol[kpm][llpm - 1][0]][sol[kpm][llpm - 1][1]]:
                    break
                else:
                    llpm -= 1
            lp0 = sol[kpm][llpm][0]  # 需要缩短间隙的产品号
            lp1 = sol[kpm][llpm][1] - 1  # 需要缩短间隙的产品工序号
            while fma[sol[kpm][llpm][0]][lp1] == 0:  # 确保lp1是产品lp0的sol[kpm][llpm][1]工序的上一工时非零工序
                lp1 -= 1
            lp2 = lp1 - 1  # lp1的上一工序
            lpini = None  # 产品lp0的第一个工序（工时不为0）
            lpini_e = None  # 说明产品lp0只有第一个工序lpini才能交换
            for j in range(task_wt.shape[1] - 1):
                if task_wt[lp0][j] != 0:
                    lpini = j
                    break
            while True:
                if fma[lp0][lp1] != 0 and fma[lp0][lp2] != 0:
                    if sma[lp0][lp1] > fma[lp0][lp2]:
                        break
                    elif sma[lp0][lp1] == fma[lp0][lp2] and lp2 == lpini:
                        lpini_e = 1
                        break
                    else:
                        lp1 -= 1
                        lp2 -= 1
                elif fma[lp0][lp1] == 0 and fma[lp0][lp2] == 0:
                    lp1 -= 1
                    lp2 -= 1
                elif fma[lp0][lp1] != 0 and fma[lp0][lp2] == 0:
                    lp2 -= 1
                elif fma[lp0][lp1] == 0 and fma[lp0][lp2] != 0:
                    lp1 -= 1
            if lpini_e == 1:
                kpm3 = [key for key, value in sol.items() if (lp0, lp2) in value][0]
                lpm3 = sol[kpm3].index((lp0, lp2))
                sol[kpm3][lpm3], sol[kpm3][lpm3 - 1] = sol[kpm3][lpm3 - 1], sol[kpm3][lpm3]
                rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                sol = rsol[0][0]
                sma, fma = fitcalu(sol)  # *** 注意，这里也要重新计算一遍
            else:
                kpm4 = [key for key, value in sol.items() if (lp0, lp1) in value][0]
                lpm4 = sol[kpm4].index((lp0, lp1))
                if sol[kpm4][lpm4 - 1][0] != p0:  # 第395行，12.26添加的条件，可能紧左工序是最后完工产品p0的工序，此时只能交换p0的前面无间隙工序
                    sol[kpm4][lpm4], sol[kpm4][lpm4 - 1] = sol[kpm4][lpm4 - 1], sol[kpm4][lpm4]
                    rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                    sol = rsol[0][0]
                    sma, fma = fitcalu(sol)  # *** 注意，这里也要重新计算一遍
                else:
                    p00 = None
                    if p0m[0] > sol[kpm4][lpm4 - 1][1]:
                        p00 = pini
                    else:
                        for i in p0m:
                            if i == sol[kpm4][lpm4 - 1][1]:
                                p00 = i
                                break
                            elif i > sol[kpm4][lpm4 - 1][1]:
                                p00 = p0m[p0m.index(i) - 1]
                                break
                    kpm5 = [key for key, value in sol.items() if (p0, p00) in value][0]
                    lpm5 = sol[kpm5].index((p0, p00))
                    if lpm5 != 0:  # 仅仅适用于当p00==pini的情况，因为其它p0m的工序不可能是相应机器的第一道工序
                        sol[kpm5][lpm5], sol[kpm5][lpm5 - 1] = sol[kpm5][lpm5 - 1], sol[kpm5][lpm5]
                        rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
                        sol = rsol[0][0]
                        sma, fma = fitcalu(sol)

        else:  # 说明p1不是最后一个工序，且p2不是第一个工序，所以要通过交换p1与其左侧工序或者通过左侧工序前移
            kpm2 = [key for key, value in sol.items() if (p0, p1) in value][0]
            lpm2 = sol[kpm2].index((p0, p1))
            sol[kpm2][lpm2], sol[kpm2][lpm2 - 1] = sol[kpm2][lpm2 - 1], sol[kpm2][lpm2]
            rsol = oss([sol])  # 交换后，先解锁，然后再计算适应度
            sol = rsol[0][0]
            sma, fma = fitcalu(sol)  # 第426行，第一类变异，关键路径工序处理模块结束

        # 以下模块是文化算法，用状况知识，即历代最优解指导变异（局部搜索）
        # 1.1 首先将当前解和历代最优解mf转化为二进制型
        bi_sol = {}  # 调度方案/解sol的二进制表示型
        bi_mf = {}  # 历代最优解mf的二进制表示型
        for ibi in bi_bench:
            bi_sol[ibi] = []
            bi_mf[ibi] = []
            for jbi in bi_bench[ibi]:
                for qbi in bi_bench[ibi][bi_bench[ibi].index(jbi) + 1:]:
                    if sol[ibi].index(jbi) < sol[ibi].index(qbi):
                        bi_sol[ibi].append(1)
                    if sol[ibi].index(jbi) > sol[ibi].index(qbi):
                        bi_sol[ibi].append(0)
                    if mf[ibi].index(jbi) < mf[ibi].index(qbi):
                        bi_mf[ibi].append(1)
                    if mf[ibi].index(jbi) > mf[ibi].index(qbi):
                        bi_mf[ibi].append(0)
        # 1.2 然后计算当前解和历代解海明距离最大的染色体，并找到不一样且间隙最大的基因，进行变异
        calhai_bi = {}  # 当前解与历代最优解海明距离字典，键是机器，值是机器对应染色体的海明距离
        for smm in range(1, 6):
            calhai_bi[smm] = 0
            for isc in range(len(bi_mf[smm])):
                if bi_mf[smm][isc] != bi_sol[smm][isc]:
                    calhai_bi[smm] += 1
        hmma = 0  # 海明距离最大的机器
        for ck, cv in calhai_bi.items():
            if cv == max(calhai_bi.values()):
                hmma = ck
                break
        lde = random.randint(0, len(sol[hmma]) - 2)
        if random.random() < mutrt2:
            sol[hmma][lde], sol[hmma][lde + 1] = sol[hmma][lde + 1], sol[hmma][lde]

    return cro_cso  # 返回经过交叉、变异后的种群


'''第四部分，迭代计算主函数'''
if __name__=="__main__":
    # 6、遗传算法的第一次计算，对初始种群solution解锁、计算适应度、轮盘赌选择、交叉变异得到第二代种群cro_cso
    # al=oss(solution) # 第706行，al[0]就是解锁后的种群，全部可以计算适应度，al[1]是空的话，len(al[0])=100
    # # ***** 注意，此时al[0]==solution，这就说明字典的关联性。10.30补充，本质是id(al[0])==id(solution)
    #
    # k,b=fitness_calu(al[0]) # k、b分别是种群的开工时间、完工时间矩阵，b[i]-k[i]==task_wt，len(k)==len(b)==100
    #
    # cso,csofit,hi5,hifit5=lunpan(al[0],b)  # 轮盘赌选出100个新的种群cso以及每个解的完工时间csofit，种群中最优的
    # # 前五个解hi5、前5个最优解的完工时间hifit5。cso中的解有可能包括了hi5的5个解，因此，本代种群最优秀的前5个解
    # # 也有机会参与后面的交叉、变异操作
    # avg=sum(csofit)/len(csofit)
    # cro_cso=cromut(cso,hi5[0],avg) # 第715行，第一次交叉变异，得到交叉变异后的种群cro_cso

    # 2021.7.18增加if-else结构，if部分是混合元启发式算法，else部分是纯变异模块体
    if 1==2:
        i=0
        cro_cso = solution # 第719行和第720行可以替代上面的第706至第715行
        hifit5 = [70, 75]  # 第720行

        # fimin=[22,22]   最终前两个最优解的适应度,12.20修改，为bi_bench解的适应度
        fimin=[hifit5[0],hifit5[1]] # 12.28修改，替代上一行，最初是初始种群前两个最优解的目标函数值
        somin=[bi_bench,bi_bench] # 最终前两个最优解，12.20修改，不能为0，改为bi_bench
        record_fi=[]
        record_hifi=[] # 记录每一代最优解的目标函数值
        num_cso=[] # 记录每一代轮盘赌选出的不同个体数
        while i<500:
            i+=1
            print('开始第',i,'次')
            bl=oss(cro_cso)  # 第二次迭代，解锁，得到解锁后的种群bl[0]
            k1,b1=fitness_calu(bl[0])  # 计算第二代种群的适应度
            csoo,csofito,hio5,hifito5=lunpan(bl[0],b1)
            num_cso.append(len(idcro(csoo)))
            record_hifi.append(hifito5[0])
            idcheck(csoo)
        #     st,ft=fitcalu(hio5[0])
        #     max(ft.flat)
        #     hifito5[0]
            if hifito5[0]<fimin[0]:
                fimin.remove(fimin[0])
                fimin.insert(0,hifito5[0])
                somin.remove(somin[0])
                somin.insert(0,hio5[0])
            if hifito5[1]<fimin[1]:
                fimin.remove(fimin[1])
                fimin.insert(1,hifito5[1])
                somin.remove(somin[1])
                somin.insert(1,hio5[1])
            avg=sum(csofito)/len(csofito) # 12.28新增，当前种群解的平均值
            cro_csoo=cromut(csoo,somin[0],avg)
            idcheck(cro_csoo)
            cro_cso=cro_csoo
            record_fi.append(fimin[0])

    else:  # 使用纯变异模块进行迭代，可以选择用mut1或mut2
        cc = solution
        ic = 0 # 迭代次数

        fimin = [75, 75]  # 12.28修改，替代上一行，最初是初始种群前两个最优解的目标函数值
        somin = [bi_bench, bi_bench]  # 最终前两个最优解，12.20修改，不能为0，改为bi_bench
        record_fi = []
        record_hifi = []  # 每一代种群中的最优解的目标函数

        num_cso = []  # 记录每一代轮盘赌选出的不同个体数
        while ic < 500:
            ic += 1
            print('开始第', ic, '次')
            occ = oss(cc)  # 第二次迭代，解锁，得到解锁后的种群bl[0]
            occa, occb = fitness_calu(occ[0])  # 计算第二代种群的适应度

            csoo, csofito, hio5, hifito5 = lunpan(occ[0], occb)
            num_cso.append(len(idcro(csoo)))
            record_hifi.append(hifito5[0])

            if hifito5[0] < fimin[0]:
                fimin.remove(fimin[0])
                fimin.insert(0, hifito5[0])
                somin.remove(somin[0])
                somin.insert(0, hio5[0])
            if hifito5[1] < fimin[1]:
                fimin.remove(fimin[1])
                fimin.insert(1, hifito5[1])
                somin.remove(somin[1])
                somin.insert(1, hio5[1])

            if fimin[0] < 21:
                print(fimin)
                break
            cc = mut2(csoo, bi_bench)
            idcheck(cc)
            record_fi.append(fimin[0])
        print('目标函数最小值：', fimin[0])
        print('第一次变异后解的目标函数值：', record_hifi[1])
        print('目标函数最大值：', max(record_hifi))
        print('解的目标函数平均值：', sum(record_hifi) / len(record_hifi))

# 当__main__函数运行完之后，在python console运行Drawing.py中的函数，绘图或将计算数据导出到excel，如output(record_hifi,record_fi,somin,'7.18',1)