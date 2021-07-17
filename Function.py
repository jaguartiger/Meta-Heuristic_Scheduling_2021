'''MSF文件中用到的函数'''

import random,numpy as np

import copy


'''1、选择函数群'''

# 12.17创建，用来计算最终的种群cro_c中，有多少个不同的解，返回是种群中所有不同解构成的列表scheu
def idcro(cro_c):
    scheu = copy.deepcopy(cro_c)
    for i in range(1, len(cro_c)):
        for j in range(0, i):
            if cro_c[i] == cro_c[j]:
                del scheu[j]
                scheu.insert(j, 0)
    for m in scheu[0:]:
        if m == 0:
            scheu.remove(m)
    return scheu


# 12.17创建，计算种群有多少不重复的目标函数值，输入为最后的种群cro_cs,返回为不重复的种群目标函数值集合sfitl，集合中元素是数
def idfit(cro_cs):
    a, b = fitness_calu(cro_cs)
    fitl = []
    for i in b:
        fitl.append(max(i.flat))
    sfitl = set(fitl)
    return sfitl


# 10.30添加：检查种群中是否有id相同的解、相同键的值的id相同的解
def idcheck(solution):
    for i in range(len(solution) - 1):
        for j in range(i + 1, len(solution)):
            if id(solution[i]) == id(solution[j]):
                print('解的id一样：', i, '＋', j)
            for q in range(1, 8):
                if id(solution[i][q]) == id(solution[j][q]):
                    print('解中相同键的值id一样：', i, '＋', j, 'id：', q)


def match(solut, solu_fit):  # 锦标赛筛选法，输入为种群和对应种群中每个解的完工时间矩阵
    cso = []
    maxfit = []
    csofit = []
    for j in solu_fit:
        maxfit.append(max(j.flat))
    inde = [i for i in range(100)]
    for i in range(100):
        i1 = random.choice(inde)
        i2 = random.choice(inde)
        if maxfit[i1] >= maxfit[i2]:
            cso.append(solut[i2])
            csofit.append(maxfit[i2])
        else:
            cso.append(solut[i1])
            csofit.append(maxfit[i1])
    return cso, csofit


def lunpan(solut, solu_fi):  # 轮盘赌，输入为种群和对应种群中每个解的完工时间矩阵
    hi5 = []  # 本代种群中最优的前五个个体
    hifit5 = []  # 本代种群中最优的前五个个体的完工时间
    cso = []
    maxfi = []
    csofit = []
    for j in solu_fi:
        maxfi.append(max(j.flat))
    fmax = max(maxfi) + 2
    wmaxfi = [fmax - ii for ii in maxfi]  # 每个解的权重
    summaxfi = sum(wmaxfi)
    pmaxfi = [jj / summaxfi for jj in wmaxfi]  # 每个解的概率
    spmaxfi = []
    for ire in range(len(pmaxfi)):  # *** 很重要，10.27修改，原先的错误在于，pmaxfi种会有相同元素，第二次及
        spmaxfi.append(sum(pmaxfi[0:ire + 1]))  # 以上次数遇到后，pmaxfi.index()实际上还是第一次的
    #     spmaxfi=[ sum(pmaxfi[0:pmaxfi.index(so)+1]) for so in pmaxfi ]
    for i in range(len(solut)):
        ra = random.random()
        mid = len(spmaxfi) // 2
        lr = 0
        rr = len(spmaxfi)
        while True:
            if ra <= spmaxfi[0]:
                cso.append(copy.deepcopy(solut[0]))  # ******* 10.30修改，用deepcopy深度复制，确保值的id也不同
                csofit.append(maxfi[0])
                break
            elif mid < (len(spmaxfi) - 1) and ra >= spmaxfi[mid] and ra <= spmaxfi[mid + 1]:
                cso.append(copy.deepcopy(solut[mid]))
                csofit.append(maxfi[mid])
                break
            elif ra <= spmaxfi[mid] and ra >= spmaxfi[mid - 1]:
                cso.append(copy.deepcopy(solut[mid - 1]))
                csofit.append(maxfi[mid - 1])
                break
            elif ra == spmaxfi[mid] and mid == (len(spmaxfi) - 1):  # 10.27新增，只真针对当ra==1这一种极特殊情况
                #             elif mid==len(spmaxfi)-1: 10.26新增，达到边界条件,后来又删了，因为最后一个元素为1，ra必小于
                print(ra)  # ra必为1
                cso.append(copy.deepcopy(solut[mid]))
                csofit.append(maxfi[mid])
                break
            elif ra < spmaxfi[mid] and ra < spmaxfi[mid - 1]:
                rr = mid
                mid = (lr + rr) // 2
            elif ra > spmaxfi[mid] and ra > spmaxfi[mid + 1]:
                lr = mid
                mid = (lr + rr) // 2
    sormaxfi = sorted(maxfi)
    for q in range(5):
        hi5.append(copy.deepcopy(solut[maxfi.index(sormaxfi[q])]))
        hifit5.append(maxfi[maxfi.index(sormaxfi[q])])
    return cso, csofit, hi5, hifit5  # 返回为筛选出的种群cso、cso中每个解的完工时间csofit、前5个最优解hi5、前5个最优解的完工时间hifit5


'''2、变异模块辅助函数群'''

# 以下四个函数是12.24创建，前三个函数用于在函数cromut的变异模块处理工时为0的工序，最后一个函数backin是后向交换处理函数
def pj_pre(fma, sol, xxma, xr):  # 用来返回相同产品上一工序的序号，排除工时为0的工序，如果返回0，就以fma[sol[xxma][xr][0]][0]=0作为上一工序
    inx = sol[xxma][xr][1] - 1  # 序完工时间约束，是一样的
    while True:
        if inx == -1:  # 说明xr实际上是产品的第0工序，但在本函数pj_pre所处的变异模块环境中，一般外层的if已经用pj_ri排除了xr是产品第0工序
            return 0
        elif fma[sol[xxma][xr][0]][inx] == 0:
            inx -= 1
        else:
            return inx


def pj_ne(fma, sol, xxma, xr):  # 用来返回相同产品下一工序的序号，排除工时为0的工序，如果返回5，说明自身xr就已经是产品的最后一道工序了
    inm = sol[xxma][xr][1] + 1
    while True:
        if inm == 5:
            return 5
        elif fma[sol[xxma][xr][0]][inm] == 0:
            inm += 1
        else:
            return inm


def pj_ri(fma, sol, xxma, xr):  # 用来判断本工序是否是本产品的第一道工序，如果返回0，且sol[xxma][xr][1]!=0，那说明sol[xxma][xr][1]
    if sol[xxma][xr][1] == 0:  # 就是产品的第0道工序。如果不是产品的第0工序，就返回自身sol[xxma][xr][1]
        return 0
    else:
        if fma[sol[xxma][xr][0]][sol[xxma][xr][1] - 1] != 0:
            return sol[xxma][xr][1]
        else:
            inxr = sol[xxma][xr][1] - 1
            while True:
                inxr -= 1
                if inxr == -1:  # 说明sol[xxma][xr]实际上就是该产品的第0工序
                    return 0
                elif fma[sol[xxma][xr][0]][inxr] == 0:
                    pass
                elif fma[sol[xxma][xr][0]][inxr] != 0:
                    return sol[xxma][xr][1]


def backin(sol, xxma, xr):  # 这里只是备份，直接出现在主函数文件中，因为调用fitcalu，而fitcalu由于使用global变量必须出现在主函数文件中
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


''' 3、计算适应度函数群——注意：因为有global变量，所以这两个函数都在主函数文件中定义 '''

#12.22重大修改，输入的参数是不包含工时为0的工序的解，首先在本函数内部为解添加工时为0的工序
def fitcalu(schedule_w):  # 由于需要全局变量，所以复制代码在Memetic_MSF文件中，不import。添加全局变量zerowt，从第376行开始修改
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


'''4、排序函数群'''

# 极其非常重要，对每个死锁的最短死锁链按长度进行由大到小排序，输入是cc，输出是bcc
def _merge(a,b) -> list:
    """Merge two sorted list"""
    c = []
    while len(a) > 0 and len(b) > 0:
        if a[0][4]> b[0][4]:
            c.append(a[0])
            a.remove(a[0])
        else:
            c.append(b[0])
            b.remove(b[0])
    if len(a) == 0:
        c += b
    else:
        c += a
    return c
# 最终的排序函数，调用前一个函数
def _merge_sorted(nums) -> list:
    # Won't sort in place
    if len(nums) <= 1:
        return nums
# 分治策略，将list一分为二：
    m = len(nums) // 2
    a = _merge_sorted(nums[:m])
    b = _merge_sorted(nums[m:])
    return _merge(a, b)

# 用来对单一死锁的子死锁链进行长度由小到大排序
def smerge(a,b) -> list:
    """Merge two sorted list"""
    c = []
    while len(a) > 0 and len(b) > 0:
        if a[0][3]< b[0][3]:
            c.append(a[0])
            a.remove(a[0])
        else:
            c.append(b[0])
            b.remove(b[0])
    if len(a) == 0:
        c += b
    else:
        c += a
    return c
# 最终的排序函数，调用前一个函数
def smerge_sorted(nums) -> list:
    # Won't sort in place
    if len(nums) <= 1:
        return nums
# 分治策略，将list一分为二：
    m = len(nums) // 2
    a = smerge_sorted(nums[:m])
    b = smerge_sorted(nums[m:])
    return smerge(a, b)


'''5、第一类死锁检查、解锁函数群'''

# 10.18 函数群2：解开第二类死锁
# 要注意，由于是可重入生产，当一台机器有相同产品的工序生产时，必须要前一工序先生产
# 否则会自己产生死锁。计算调度方案的适应度之前，首先要解除死锁
# 9.1 本cell是第一类死锁（同一机器有两个相同产品的前后工序、两对产品的死锁）的三个处理解除函数
def sisuo(solution):  # 查找并解除死锁的函数，输入为种群list,返回经过处理后的种群
    for schedul_wt in solution:
        qi = 1
        while schedul_wt[4][0][1] != 0 and schedul_wt[5][0][1] != 0:  # 如果整个解中都没有启动工序，也是死锁
            schedul_wt[4][0], schedul_wt[4][qi] = schedul_wt[4][qi], schedul_wt[4][0]
            schedul_wt[5][0], schedul_wt[5][qi] = schedul_wt[5][qi], schedul_wt[5][0]
            qi += 1  # 调整完之后，不用担心后面的解锁程序会破坏，因为一旦第一道工序是某产品0工序，那么该绝不构成死锁，所以不会被检出与顺序交换
        for i in range(1, 7):
            for j in range(len(schedul_wt[i]) - 1):  # 第i台机器的每一个任务，从j开始
                for f in range(j + 1, len(schedul_wt[i])):  # 第i台机器每一个j任务后的任务
                    if schedul_wt[i][j][0] != schedul_wt[i][f][0]:  # 不是同一产品的工序对
                        for q in range(i + 1, 8):  # 第q(i+1)台机器
                            for m in range(len(schedul_wt[q]) - 1):  # 第q(i+1)台机器的每一个任务m
                                for n in range(m + 1, len(schedul_wt[q])):  # 第q台机器的m后的任务
                                    if schedul_wt[i][j][0] == schedul_wt[q][n][0] and schedul_wt[i][f][0] == \
                                            schedul_wt[q][m][0]:
                                        if schedul_wt[i][j][1] > schedul_wt[q][n][1] and schedul_wt[q][m][1] > \
                                                schedul_wt[i][f][1]:  # 就是死锁
                                            #                                             print(f'解{solution.index(schedul_wt)}出现死锁，位于机器{i}和机器{q} \n\
                                            #                                             {schedul_wt[i][j]}——{schedul_wt[i][f]}和{schedul_wt[q][m]}——{schedul_wt[q][n]}')
                                            if f - j > n - m:  # 哪条链短，就交换哪条链上的两个死锁工序
                                                schedul_wt[q][m], schedul_wt[q][n] = schedul_wt[q][n], schedul_wt[q][m]
                                            else:
                                                schedul_wt[i][j], schedul_wt[i][f] = schedul_wt[i][f], schedul_wt[i][j]
                    else:  # 找出每个解的1-6台机器的任务序列中，相同产品的任务，解除死锁
                        if schedul_wt[i][j][1] > schedul_wt[i][f][1]:  # 如果后面的工序先开始，就是死锁，就要交换
                            schedul_wt[i][j], schedul_wt[i][f] = schedul_wt[i][f], schedul_wt[i][j]
        for j7 in range(len(schedul_wt[7]) - 1):  # 单独检查最后一台机器的任务序列中，相同产品的任务，解除死锁
            for f7 in range(j7 + 1, len(schedul_wt[7])):
                if schedul_wt[7][j7][0] == schedul_wt[7][f7][0]:
                    if schedul_wt[7][j7][1] > schedul_wt[7][f7][1]:
                        schedul_wt[7][j7], schedul_wt[7][f7] = schedul_wt[7][f7], schedul_wt[7][j7]
    return solution  # 返回的是经过第一轮死锁处理的种群


def detsisuo(soluti):  # 检测种群中的每个解是否还有死锁，输入为种群list，返回为判断结果，3有死锁，1无死锁
    for schedul_wt in soluti:
        for i in range(1, 7):
            for j in range(len(schedul_wt[i]) - 1):  # 第i台机器的每一个任务，从j开始
                for f in range(j + 1, len(schedul_wt[i])):  # 第i台机器每一个j任务后的任务
                    if schedul_wt[i][j][0] != schedul_wt[i][f][0]:  # 不是同一产品的工序对
                        for q in range(i + 1, 8):  # 第q(i+1)台机器
                            for m in range(len(schedul_wt[q]) - 1):  # 第q(i+1)台机器的每一个任务m
                                for n in range(m + 1, len(schedul_wt[q])):  # 第q台机器的m后的任务
                                    if schedul_wt[i][j][0] == schedul_wt[q][n][0] and schedul_wt[i][f][0] == schedul_wt[q][m][0]:
                                        if schedul_wt[i][j][1] > schedul_wt[q][n][1] and schedul_wt[q][m][1] > \
                                                schedul_wt[i][f][1]:
                                            #                                             print(f'解{soluti.index(schedul_wt)}出现死锁，位于机器{i}和机器{q} \n\
                                            #                                             {schedul_wt[i][j]}——{schedul_wt[i][f]}和{schedul_wt[q][m]}——{schedul_wt[q][n]}')
                                            return 3  # 只要出现死锁，就返回3
                    else:
                        if schedul_wt[i][j][1] > schedul_wt[i][f][1]:
                            #                             print(f'出现第二种死锁，解{soluti.index(schedul_wt)}，位于机器{i}  \n\
                            #                             {schedul_wt[i][j]}——{schedul_wt[i][f]}')
                            return 3
        for j7 in range(len(schedul_wt[7]) - 1):  # 单独检查最后一台机器的任务序列中，相同产品的任务，解除死锁
            for f7 in range(j7 + 1, len(schedul_wt[7])):
                if schedul_wt[7][j7][0] == schedul_wt[7][f7][0]:
                    if schedul_wt[7][j7][1] > schedul_wt[7][f7][1]:
                        #                         print(f'出现第二种死锁，解{soluti.index(schedul_wt)}，位于机器7  \n\
                        #                             {schedul_wt[i][j]}——{schedul_wt[i][f]}')
                        return 3
    return 1  # 如果返回1，说明没有死锁


def opensisuo(solu):  # 调用了上一cell的sisuo()、detsisuo()函数。输入为种群，输出为解除死锁后的种群
    a = detsisuo(solu)
    if a == 1:
        return solu
    else:
        temm = solu
        i = 0
        while a == 3 and i < 100:
            temm = sisuo(temm)
            a = detsisuo(temm)
            i += 1  # 记录解除了多少次死锁
        if a == 1:
            #             print(f'运行了{i}次才解除死锁') 10.27 程序验证正确，所以取消打印
            return temm
        else:
            print('fuck up')  # 运行了100次解除死锁函数sisuo()都无法将种群中的死锁彻底解除
            return 404


        # 6-2、解的第二类死锁解除函数


'''6-1、第二类死锁检查函数群'''

def detectsisuo(sche):  # 对没有第一类死锁的解，检出更复杂的其余类型死锁
    inli_all={}
    for i in range(1,6):        # 第一台机器。从原来
        for j in range(len(sche[i])-1):  # 第一台机器第一个工序
            if sche[i][j][1]!=0:
                for q in range(j+1,len(sche[i])):  # 第一台机器第二个工序
                    a=i
                    b=q
                    if sche[a][b][0]!=sche[i][j][0] and sche[a][b][1]!=4: # 执行innersisuo前先要判断的，满足才执行
                        inli=innersisuo(sche,a,q,i,j)
                        if len(inli)!=0:
                            inli_all[((i,j),(a,b))]=inli
    return inli_all   # 返回详细的死锁链

# 极其非常重要，以下是2020.2.8更新的优化后的函数，详见日志，当遇到非死锁时，所在机器均不被后续检索了，激活非死锁的elif，
# 一个是引入新参数wt标记非死锁机器wt并在非死锁的elif更新，另一个是非死锁的elif结尾是break
def innersisuo(sche,a,b,i,j,midd=[],wt=None): # a为机器号，b为机器上的顺序号。i,j为最初的启动机器号和机器上的顺序号。2.8增加wt=None
    inlis=[]
    gi=0
    wtz=wt # 2.8增加,当后面遇到非死锁的elif,更新，否则其余时候传递给递归调用innersisuo的elif
    for c in range(sche[a][b][1]+1,4):
        if c!=gi and (c+1)!=gi and (c+2)!=gi:# 如果某台机器有多个产品che[a][b][0]的工序，直接处理，然后在for c循环就跳过
            for w in range(i+1,6): # 因为a之前机器中的死锁工序完全重合，如果有的话，在前面机器就能检出来，不必重复
                if w!=a and w!=wt: # 因为上一行从range(a+1,8)改成了range(i+1,6)，所以要增加这个限制条件，以降低计算量。2.8增加w!=wt
                    if (sche[a][b][0],c) in sche[w] and sche[w].index((sche[a][b][0],c))<len(sche[w])-1:
                        te=0
                        tec=[]
                        for z in range(sche[w].index((sche[a][b][0],c))+1,len(sche[w])):
                            middrou=[] # 这个是记录寻找路径的关键
#                             if sche[w][z]==(4,1):
#                                 print('找到了')
#                                 print(sche[w][z])
                            if sche[w][z][0]==sche[i][j][0] and sche[w][z][1]<sche[i][j][1]:
        #                         print(f'遇到死锁，终点为机器{w},第{z}个任务')
                                inlis.extend(midd)
                                inlis.append((w,sche[w].index((sche[a][b][0],c)))) # 新增记录搜索路径
                                inlis.append((w,z,'lock'))
                                break # 不需要推进机器的后续工序了，即使后面还有死锁，那么跟此处的死锁完全重合，只是后面不一样
        #    不能return,还要检查相同产品的剩余工序                  return inlis
        #                     elif sche[w][z][0]==sche[i][j][0] and sche[w][z][1]>sche[i][j][1]:
        #                         pass
                            elif sche[w][z][0]!=sche[i][j][0] and sche[w][z][0]!=sche[a][b][0] and sche[w][z][1]!=4:
        #                         inlis.append((w,sche[w].index((sche[a][b][0],c))))
        #                         inlis.append((w,z))
                                if te==1:
#                                     if sche[w][z]==(2,1):
#                                         print('找到了1')
#                                         print(sche[w][z])
                                    middrou.extend(midd)
                                    middrou.append((w,sche[w].index((sche[a][b][0],c))))
                                    for tem in tec:
                                        middrou.append(tem)
                                    middrou.append((w,z))
                                    if len(middrou)-5>len(set(middrou)): # ***** 10.20增加漏洞解除程序
#                                         print('异常1')
                                        return inlis   # 如果有第二类死锁，这里返回，后面会检出
                                    inlis.extend(innersisuo(sche,w,z,i,j,middrou,wtz))  # 从w,z开始，替代a,b，重复执行innersisuo
                                else:
#                                     if sche[w][z]==(2,1) and sche[a][b]==(6,0):
#                                         print('找到了2')
#                                         print(sche[w][z])
                                    middrou.extend(midd)
                                    middrou.append((w,sche[w].index((sche[a][b][0],c))))
                                    middrou.append((w,z))
                                    if len(middrou)-5>len(set(middrou)): # ***** 10.20增加漏洞解除程序
#                                         print('异常2')
                                        return inlis   # 如果有第二类死锁，这里返回，后面会检出
                                    inlis.extend(innersisuo(sche,w,z,i,j,middrou,wtz))  # 从w,z开始，替代a,b，重复执行innersisuo
                            elif sche[w][z][0]==sche[i][j][0] and sche[w][z][1]>sche[i][j][1]: # 就是sche[w][z][0]==sche[i][j][0] and sche[w][z][1]>sche[i][j][1]
                                wtz=w  # 2.8 记录非死锁的机器，在上一个elif里传给函数innersisuo，以后跳过该机器
                                break  # 2.8 这一步，是限制本次不在继续搜索非死锁后面的工序了
    #                             if te==1:        ***** 10.27 极其非常重要，将上一行取消,这种情况将在最后的else里一并跳过
    #                                 for tem in tec:
    #                                     middrou=[]
    #                                     middrou.extend(midd)
    #                                     middrou.append((tem[0],tem[1]))
    #                                     for tt in range(tem[1]+1,len(sche[w])):
    #                                     middrou.append((tem[0],tem[1]))
    #                                     inlis.extend(innersisuo(sche,tem[0],tem[1],i,j,middrou))
#                                 return inlis  ***** 10.27 极其非常重要，将本行及所属的elif取消
                            elif sche[w][z][0]==sche[a][b][0]: # 就是sche[w][z][0]==sche[a][b][0]，先记录下，然后跳过
                                te=1
                                gi=sche[w][z][1]
                                tec.append((w,z))
                                pass
                            else: # 只剩sche[w][z][1]==4,直接跳过
                                pass
                        break # 如果找到的话，就不用迭代机器了，只迭代初始产品（a，b）的下一工序
                    elif (sche[a][b][0],c) in sche[w] and sche[w].index((sche[a][b][0],c))==len(sche[w])-1:
                        break
    return inlis # 这意味着，要么同产品后序所有工序都不在后续机器中，或者同产品后续工序都在对应机器的最后一个工序


'''6-2、第二类死锁解锁函数群'''

def n2sisuo(af, qq):  # af是qq中的第二类死锁，qq是解，返回值为解开第二类死锁后的qq
    key_list = []
    for key, value in af.items():
        k = []
        for ke in key:
            k.append(ke)
        for va in value:
            k.append(va)
        key_list.append(k)
    key_po = []
    for m in key_list:
        i = 0
        sscm = []
        while i < len(m):
            ssc = [m[i]]
            #     for i in range(len(m)):
            j = i + 1
            while m[i][0] == m[j][0]:
                ssc.append(m[j])
                j += 1
                if j == len(m):
                    break
            i = j
            sscm.append(ssc)
        key_po.append(sscm)
    aa = {}
    for i in range(len(key_po)):
        aa[i] = key_po[i]

    bb = {}  # 多个死锁的死锁的起点链，单独拿出来，这种情况下只改起点链，该死锁的全部死锁就都解开了
    bb_sp = {}  # 很重要，多个死锁死锁每个死锁的一个死锁链，用来取代bb中的起点链，注意，bb_sp中的每个死锁链都要解开
    for j in range(len(aa)):
        cou = 0
        for q in aa[j]:
            if q[-1][-1] == 'lock':
                cou += 1
        if cou > 1:
            bb[j] = aa[j][0]
            #         bb_sp[(j,aa[j][0][0][0],aa[j][0][0][1],aa[j][0][-1][1],aa[j][0][-1][1]-aa[j][0][0][1])]=[aa[j][1]]
            bb_sp[j] = [[j, aa[j][1][0][0], aa[j][1][0][1], aa[j][1][-1][1], aa[j][1][-1][1] - aa[j][1][0][1]]]
            for q in range(2, len(aa[j]) - 1):
                if aa[j][q][-1][-1] == 'lock':
                    bb_sp[j].append([j, aa[j][q + 1][0][0], aa[j][q + 1][0][1], aa[j][q + 1][-1][1],
                                     aa[j][q + 1][-1][1] - aa[j][q + 1][0][1]])
    if bb != None:  # 把bb中的死锁从aa中剔除
        for i in bb.keys():
            usl = aa.pop(i)  # 此时，aa中的死锁全都是一个,usl是从aa中剔除的bb中的死锁

    cc = []  # cc就是所有要解的死锁链，cc中的元素个数就是死锁的个数
    for i in aa:
        sic = []
        resi = []
        for j in aa[i]:
            resi.append([j[0][0], j[0][1], j[-1][1], j[-1][1] - j[0][1]])
        resii = smerge_sorted(resi)
        cc.append([i, resii[0][0], resii[0][1], resii[0][2], resii[0][3], resii[1:]])
    for i in bb:
        cc.append([i, bb[i][0][0], bb[i][0][1], bb[i][-1][1], bb[i][-1][1] - bb[i][0][1]])
    bcc = _merge_sorted(cc)
    bb_spp = {}  # 是bb_sp的去掉重复的死锁链
    for i in bb_sp:  # 删除bb_sp中重复的死锁链，直接将list变成集合set就可以了
        bb_spm = []
        for ij in bb_sp[i]:
            bb_spm.append(tuple(ij))
        bb_spm = set(bb_spm)
        bb_spmn = []
        for im in bb_spm:
            bb_spmn.append(list(im))
        bb_spp[i] = bb_spmn
    bccl = [i for i in bcc if len(i) == 5]
    # [bcc.remove(i) for i in bccl]
    accl = [i for i in bcc if len(i) > 5]
    repla = []  # 第320行创建，每一个必须要解开的死锁链
    con_num = 0  # ***** 控制变量，如果遇到最复杂的情况无法处理，就终止迭代，输出bcc，将该解删除掉
    con_num_i = None
    sp_bcc = bcc.copy()  # 10.29添加，用于第400行报错时输出
    sp_bccl = bccl.copy()  # 10.29添加，用于第400行报错时输出
    while (len(bcc)) > 0:
        if con_num == 1:
            print('特别复杂的死锁')
            print(con_num_i)  # 输出具体的死锁,key_po的键
            break
        if len(bcc) == 1:
            qq[bcc[0][1]][bcc[0][2]], qq[bcc[0][1]][bcc[0][3]] = qq[bcc[0][1]][bcc[0][3]], qq[bcc[0][1]][bcc[0][2]]
            break
        else:
            if bcc[0] in accl:  # 1 如果bcc[i]是accl中的死锁处理
                #                 if bcc[0]!=accl[0]: *** 10.20将条件从bcc[0]==accl[0]改为bcc[0] in accl
                #                     return (bcc,accl) ***** 但是后来修改了后面的accl[1:]为accl[0:]，就不需要这个判断了
                if len(bccl) != 0:  # 1.1 处理bccl中死锁的关系
                    cou1 = 0
                    while cou1 == 0:  # 只要bcc[i]最短死锁链与bccl中死锁的死锁链有交错，就更新bcc[i]的死锁链
                        cou1 = 1  # 注意，更新完之后，仍要再依照bccl的死锁链核对
                        for q in bccl:
                            if bcc[0][1] == q[1] and bcc[0][3] == q[2]:  # 把与bccl有交错的accl中的最短死锁链改成第二死锁链
                                bcc[0][1], bcc[0][2], bcc[0][3], bcc[0][4] = bcc[0][5][0]
                                bcc[0][5].remove(bcc[0][5][0])
                                ac_b = bcc[0].copy()  # *** 10.20新添加，需要同时更新accl
                                accl.remove(accl[0])
                                accl.insert(0, ac_b)
                                cou1 = 0
                                break
                            elif bcc[0][1] == q[1] and bcc[0][2] == q[3]:  # 把与bccl有交错的accl中的最短死锁链改成第二死锁链
                                bcc[0][1], bcc[0][2], bcc[0][3], bcc[0][4] = bcc[0][5][0]
                                bcc[0][5].remove(bcc[0][5][0])
                                ac_c = bcc[0].copy()  # *** 10.20新添加，需要同时更新accl
                                accl.remove(accl[0])
                                accl.insert(0, ac_c)
                                cou1 = 0
                                break
                    for n in bccl[0:]:  # 确定不会与bccl的死锁链有交错，就查找可被同时消除的bccl中的死锁
                        if bcc[0][1] == n[1] and bcc[0][2] == n[2] and bcc[0][3] >= n[3]:
                            bcc.remove(n)
                            bccl.remove(n)
                        elif bcc[0][1] == n[1] and bcc[0][2] < n[2] and bcc[0][3] == n[3]:
                            bcc.remove(n)
                            bccl.remove(n)
                if len(accl) > 1:  # 1.2 处理与accl中其它死锁的关系
                    p2 = None
                    while True:
                        coun = 0
                        #                     z1=None
                        for p in accl[0:]:  # accl[0]必定是bcc[i]
                            if p != bcc[0] and bcc[0][1] == p[1] and bcc[0][3] == p[2]:
                                coun += 1
                                p2 = accl.index(p)
                            elif p != bcc[0] and bcc[0][1] == p[1] and bcc[0][2] == p[3]:
                                coun += 1
                                p2 = accl.index(p)
                        if coun > 1:  # 如果bcc[0]与超过一个accl中的其它死锁的最短死锁链交错，就更新bcc[0]的最短死锁链
                            bcc[0][1], bcc[0][2], bcc[0][3], bcc[0][4] = bcc[0][5][0]
                            bcc[0][5].remove(bcc[0][5][0])  # 53行，***** bcc[i] 更新了最短死锁链，需要从头开始分析，递归
                            ac_b1 = bcc[0].copy()  # *** 10.20新添加，需要同时更新accl
                            accl.remove(accl[0])
                            accl.insert(0, ac_b1)
                        elif coun == 1:  # 如果只有一个accl死锁的最短死锁链交错，则更新该死锁的最短死锁链
                            accl_d = accl[p2].copy()  # *** 10.20新添加，需要同时更新bcc
                            p3 = bcc.index(accl_d)  # *** 10.20新添加，需要同时更新bcc
                            accl[p2][1], accl[p2][2], accl[p2][3], accl[p2][4] = accl[p2][5][0]
                            accl[p2][5].remove(accl[p2][5][0])
                            bcc.remove(accl_d)  # *** 10.20新添加，需要同时更新bcc
                            bcc.insert(p3, accl[p2])  # *** 10.20新添加，需要同时更新bcc
                            for o in accl[0:]:  # ***** 10.16 很重要，经过测试，即使在循环中有accl元素被删除，但仍可以
                                if o != bcc[0]:
                                    if bcc[0][1] == o[1] and bcc[0][2] == o[2] and bcc[0][3] >= o[3]:
                                        accl.remove(o)
                                        bcc.remove(o)
                                    elif bcc[0][1] == o[1] and bcc[0][2] < o[2] and bcc[0][3] == o[3]:
                                        accl.remove(o)
                                        bcc.remove(o)
                                    else:  # 处理其它死锁链
                                        for o5 in o[5]:
                                            if bcc[0][1] == o5[0] and bcc[0][2] == o5[1] and bcc[0][3] >= o5[2]:
                                                accl.remove(o)
                                                bcc.remove(o)
                                                break
                                            elif bcc[0][1] == o5[0] and bcc[0][3] == o5[2] and bcc[0][2] < o5[1]:
                                                accl.remove(o)
                                                bcc.remove(o)
                                                break
                                            elif bcc[0][1] == o5[0] and bcc[0][2] == o5[1] and bcc[0][3] < o5[1]:
                                                o_del = o.copy()
                                                bcc.remove(o_del)
                                                o[5].remove(o5)  # 10.16 增加，不需要z1了
                                                bcc.append(o)
                                            elif bcc[0][1] == o5[0] and bcc[0][3] == o5[2] and bcc[0][2] > o5[1]:
                                                o_del = o.copy()
                                                bcc.remove(o_del)
                                                o[5].remove(o5)  # 10.16 增加，不需要z1了
                                                bcc.append(o)
                                            elif bcc[0][1] == o5[0] and bcc[0][2] == o5[2]:
                                                o_del = o.copy()
                                                bcc.remove(o_del)
                                                o[5].remove(o5)  # 10.16 增加，不需要z1了
                                                bcc.append(o)
                                            elif bcc[0][1] == o5[0] and bcc[0][3] == o5[1]:
                                                o_del = o.copy()
                                                bcc.remove(o_del)
                                                o[5].remove(o5)  # 10.16 增加，不需要z1了
                                                bcc.append(o)
                            break  # 只有这样才算可以终止对其它死锁的检索，完成对bcc[i]的解锁
                        else:  # coun==0，将accl中被bcc[0]同时解开的其它死锁删除
                            for oo in accl[0:]:  # ***** 10.16 很重要，经过测试，即使在循环中有accl元素被删除，但仍可以
                                if oo != bcc[0]:
                                    if bcc[0][1] == oo[1] and bcc[0][2] == oo[2] and bcc[0][3] >= oo[3]:
                                        accl.remove(oo)
                                        bcc.remove(oo)
                                    elif bcc[0][1] == oo[1] and bcc[0][2] < oo[2] and bcc[0][3] == oo[3]:
                                        accl.remove(oo)
                                        bcc.remove(oo)
                                    else:
                                        for oo5 in oo[5][0:]:
                                            if bcc[0][1] == oo5[0] and bcc[0][2] == oo5[1] and bcc[0][3] >= oo5[2]:
                                                accl.remove(oo)
                                                bcc.remove(oo)
                                                break
                                            elif bcc[0][1] == oo5[0] and bcc[0][3] == oo5[2] and bcc[0][2] < oo5[1]:
                                                accl.remove(oo)
                                                bcc.remove(oo)
                                                break
                                            elif bcc[0][1] == oo5[0] and bcc[0][2] == oo5[1] and bcc[0][3] < oo5[2]:
                                                oo_del = oo.copy()
                                                bcc.remove(oo_del)
                                                oo[5].remove(oo5)  # 10.16 增加，不需要z1了
                                                bcc.append(oo)
                                            elif bcc[0][1] == oo5[0] and bcc[0][3] == oo5[2] and bcc[0][2] > oo5[1]:
                                                oo_del = oo.copy()
                                                bcc.remove(oo_del)
                                                oo[5].remove(oo5)  # 10.16 增加，不需要z1了
                                                bcc.append(oo)
                                            elif bcc[0][1] == oo5[0] and bcc[0][2] == oo5[2]:
                                                oo_del = oo.copy()
                                                bcc.remove(oo_del)
                                                oo[5].remove(oo5)  # 10.16 增加，不需要z1了
                                                bcc.append(oo)
                                            elif bcc[0][1] == oo5[0] and bcc[0][3] == oo5[1]:
                                                oo_del = oo.copy()
                                                bcc.remove(oo_del)
                                                oo[5].remove(oo5)  # 10.16 增加，不需要z1了
                                                bcc.append(oo)
                            break
                qq[bcc[0][1]][bcc[0][2]], qq[bcc[0][1]][bcc[0][3]] = qq[bcc[0][1]][bcc[0][3]], qq[bcc[0][1]][
                    bcc[0][2]]  # 最后，是交换bbc[i]的最短死锁链
                accl.remove(bcc[0])
                bcc.remove(bcc[0])
            # 至此完成对单一死锁（accl中元素）的解锁
            elif bcc[0] in repla:  # 第320行，repla是每一个必须要解开的死锁链
                for b_c_l in bccl[0:]:
                    if bcc[0][1] == b_c_l[1] and bcc[0][2] == b_c_l[3]:
                        con_num = 1
                        con_num_i = key_po[bcc[0][0]]  # 无解的死锁链
                        break
                    elif bcc[0][1] == b_c_l[1] and bcc[0][3] == b_c_l[2]:
                        con_num = 1
                        con_num_i = key_po[bcc[0][0]]  # 无解的死锁链
                        break
                    elif bcc[0][1] == b_c_l[1] and bcc[0][2] == b_c_l[2]:
                        bcc.remove(b_c_l)
                        bccl.remove(b_c_l)
                    elif bcc[0][1] == b_c_l[1] and bcc[0][3] == b_c_l[3]:
                        bcc.remove(b_c_l)
                        bccl.remove(b_c_l)
                if con_num == 1:
                    break
                else:  # 然后解除accl中的死锁
                    for a_c_l in accl[0:]:
                        m_ar = 0
                        if a_c_l[1] == bcc[0][1] and bcc[0][2] == a_c_l[2]:
                            accl.remove(a_c_l)
                            bcc.remove(a_c_l)
                            m_ar = 1
                        elif a_c_l[1] == bcc[0][1] and bcc[0][3] == a_c_l[3]:
                            accl.remove(a_c_l)
                            bcc.remove(a_c_l)
                            m_ar = 1
                        elif a_c_l[1] == bcc[0][1] and bcc[0][3] == a_c_l[2]:
                            a_c_l_del = a_c_l.copy()
                            bcc.remove(a_c_l_del)
                            a_c_l[1], a_c_l[2], a_c_l[3], a_c_l[4] = a_c_l[5][0]
                            a_c_l[5].remove(a_c_l[5][0])
                            bcc.append(a_c_l)
                        elif a_c_l[1] == bcc[0][1] and bcc[0][2] == a_c_l[3]:
                            a_c_l_del = a_c_l.copy()
                            bcc.remove(a_c_l_del)
                            a_c_l[1], a_c_l[2], a_c_l[3], a_c_l[4] = a_c_l[5][0]
                            a_c_l[5].remove(a_c_l[5][0])
                            bcc.append(a_c_l)
                        if m_ar == 0:
                            for a_c_l5 in a_c_l[5][0:]:
                                if a_c_l5[0] == bcc[0][1] and a_c_l5[1] == bcc[0][2] and a_c_l5[2] <= bcc[0][3]:
                                    accl.remove(a_c_l)
                                    bcc.remove(a_c_l)
                                    break
                                elif a_c_l5[0] == bcc[0][1] and a_c_l5[1] == bcc[0][2] and a_c_l5[2] > bcc[0][3]:
                                    a_c_l5_del = a_c_l.copy()
                                    bcc.remove(a_c_l5_del)
                                    a_c_l[5].remove(a_c_l5)
                                    bcc.append(a_c_l)
                                elif a_c_l5[0] == bcc[0][1] and a_c_l5[2] == bcc[0][3] and a_c_l5[1] > bcc[0][2]:
                                    accl.remove(a_c_l)
                                    bcc.remove(a_c_l)
                                    break
                                elif a_c_l5[0] == bcc[0][1] and a_c_l5[2] == bcc[0][3] and a_c_l5[1] < bcc[0][2]:
                                    a_c_l5_del = a_c_l.copy()
                                    bcc.remove(a_c_l5_del)
                                    a_c_l[5].remove(a_c_l5)
                                    bcc.append(a_c_l)
                                elif a_c_l5[0] == bcc[0][1] and a_c_l5[1] == bcc[0][3]:
                                    a_c_l5_del = a_c_l.copy()
                                    bcc.remove(a_c_l5_del)
                                    a_c_l[5].remove(a_c_l5)
                                    bcc.append(a_c_l)
                                elif a_c_l5[0] == bcc[0][1] and a_c_l5[2] == bcc[0][2]:
                                    a_c_l5_del = a_c_l.copy()
                                    bcc.remove(a_c_l5_del)
                                    a_c_l[5].remove(a_c_l5)
                                    bcc.append(a_c_l)
                    qq[bcc[0][1]][bcc[0][2]], qq[bcc[0][1]][bcc[0][3]] = qq[bcc[0][1]][bcc[0][3]], qq[bcc[0][1]][
                        bcc[0][2]]  # 最后，是交换bbc[i]的最短死锁链
                    repla.remove(bcc[0])
                    bcc.remove(bcc[0])
            else:  # 2 当bcc[0]是bccl中的死锁，就按照另一套规则解锁
                if bcc[0] not in bccl:  # 10.29 添加，为解决第400行的bcc[0]不在bccl中的问题
                    print('sp_bcc=', sp_bcc)  # 10.29添加，用于第400行报错时输出
                    print('sp_bccl=', sp_bccl)  # 10.29添加，用于第400行报错时输出
                    print(bcc[0])
                    print(bccl)
                if len(bccl) > 1:  # 2.1 对bccl中的死锁进行处理
                    coub = 0  # 记录有几个交错
                    zc1 = []  # 左侧交错的bccl中死锁
                    zc2 = []  # 右侧交错的bccl中死锁
                    zs1 = []  # 左侧覆盖的bccl中死锁
                    zs2 = []  # 右侧覆盖的bccl中死锁
                    for e in bccl[1:]:
                        if bcc[0][1] == e[1] and bcc[0][2] == e[2] and bcc[0][3] >= e[3]:
                            zs1.append(e)  # 先不能消除，因为还要看交错死锁情况，有可能会根据交错死锁情况来调整
                        elif bcc[0][1] == e[1] and bcc[0][3] == e[3] and bcc[0][2] < e[2]:
                            zs2.append(e)  # 先不能消除，因为还要看交错死锁情况，有可能会根据交错死锁情况来调整
                        elif bcc[0][1] == e[1] and bcc[0][2] == e[3]:
                            coub += 1
                            zc1.append(e)
                        elif bcc[0][1] == e[1] and bcc[0][3] == e[2]:
                            coub += 1
                            zc2.append(e)
                    # ***** 这里隐含一个重要问题，交错交换的死锁，还应该再跟bccl中其它死锁确认有没有交错关系，即传递交错
                    # 而且这种传递交错不会出现在coub>1中，因为传递交错的死锁与bcc[i]没有共享工序。目前，本算法不能处理传递
                    # 交错死锁，只能在最开始的时候检索并处理，处理方式是解除其它机器上的死锁链，使得所有机器都不出现传递交
                    # 错死锁。
                    if coub == 1:  # 2.1.1第二复杂的部分
                        if len(zc1) == 1:  # —2.1.1.1-1处理同时解开的bccl中的死锁
                            for bcl1 in bccl[1:]:
                                if bcl1 != zc1[0] and zc1[0][1] == bcl1[1] and zc1[0][2] == bcl1[2]:
                                    bcc.remove(bcl1)
                                    bccl.remove(bcl1)
                                elif bcl1 != bcc[0] and bcc[0][1] == bcl1[1] and bcc[0][3] == bcl1[3]:
                                    bcc.remove(bcl1)
                                    bccl.remove(bcl1)
                                    # 2.1.1.2-1处理同时解开的accl中的死锁
                            for acla in accl[0:]:
                                mar3 = 0
                                if bcc[0][1] == acla[1] and zc1[0][2] == acla[2]:
                                    accl.remove(acla)
                                    bcc.remove(acla)
                                    mar3 = 1
                                elif bcc[0][1] == acla[1] and bcc[0][3] == acla[3]:
                                    accl.remove(acla)
                                    bcc.remove(acla)
                                    mar3 = 1
                                elif bcc[0][1] == acla[1] and zc1[0][2] == acla[3]:
                                    acla_del = acla.copy()
                                    bcc.remove(acla_del)
                                    acla[1], acla[2], acla[3], acla[4] = acla[5][0]
                                    acla[5].remove(acla[5][0])
                                    bcc.append(acla)
                                elif bcc[0][1] == acla[1] and bcc[0][3] == acla[2]:
                                    acla_del = acla.copy()
                                    bcc.remove(acla_del)
                                    acla[1], acla[2], acla[3], acla[4] = acla[5][0]
                                    acla[5].remove(acla[5][0])
                                    bcc.append(acla)
                                if mar3 == 0:
                                    for acla5 in acla[5][0:]:
                                        if bcc[0][1] == acla5[0] and zc1[0][2] == acla5[1] and bcc[0][3] >= acla5[2]:
                                            accl.remove(acla)
                                            bcc.remove(acla)
                                            break
                                        elif bcc[0][1] == acla5[0] and bcc[0][3] == acla5[2] and zc1[0][2] < acla5[1]:
                                            accl.remove(acla)
                                            bcc.remove(acla)
                                            break
                                        elif bcc[0][1] == acla5[0] and zc1[0][2] == acla5[2]:
                                            acla5_del = acla.copy()
                                            bcc.remove(acla5_del)
                                            acla[5].remove(acla5)
                                            bcc.append(acla)
                                        elif bcc[0][1] == acla5[0] and bcc[0][3] == acla5[1]:
                                            acla5_del = acla.copy()
                                            bcc.remove(acla5_del)
                                            acla[5].remove(acla5)
                                            bcc.append(acla)
                                        elif bcc[0][1] == acla5[0] and zc1[0][2] == acla5[1] and bcc[0][3] < acla5[2]:
                                            acla5_del = acla.copy()
                                            bcc.remove(acla5_del)
                                            acla[5].remove(acla5)  # *** 10.16新增加，不是交错死锁链，但已不能用了
                                            bcc.append(acla)
                                        elif bcc[0][1] == acla5[0] and bcc[0][3] == acla5[2] and zc1[0][2] > acla5[1]:
                                            acla5_del = acla.copy()
                                            bcc.remove(acla5_del)
                                            acla[5].remove(acla5)  # *** 10.16新增加，不是交错死锁链，但已不能用了
                                            bcc.append(acla)

                            # 最后是交换删除死锁，交换完之后，同时消除bccl中的两个交错死锁 zc1[0][2],bcc[i][3]=bcc[i][3],zc1[0][2]
                            qq[bcc[0][1]][zc1[0][2]], qq[bcc[0][1]][bcc[0][3]] = qq[bcc[0][1]][bcc[0][3]], \
                                                                                 qq[bcc[0][1]][
                                                                                     zc1[0][2]]  # 最后，是交换bbc[i]的最短死锁链
                            bccl.remove(bcc[0])  # 10.29 第400行，有可能出错
                            bccl.remove(zc1[0])
                            bcc.remove(bcc[0])
                            bcc.remove(zc1[0])
                        else:  # 交错死锁在zc2中
                            if zc2[0] not in bccl:
                                print('FUCK！ zc2[0] 不在 bccl')
                            else:
                                print('zc2[0] 在 bccl中')
                            for bcl2 in bccl[1:]:  # —2.1.1.1-2处理同时解开的bccl中的死锁
                                if bcl2 != zc2[0] and zc2[0][1] == bcl2[1] and zc2[0][3] == bcl2[3]:
                                    bcc.remove(bcl2)
                                    bccl.remove(bcl2)
                                elif bcl2 != zc2[0] and bcc[0][1] == bcl2[1] and bcc[0][2] == bcl2[
                                    2]:  # 12.5新增条件bcl2!=zc2[0]，虽然多余
                                    bcc.remove(bcl2)
                                    bccl.remove(bcl2)
                                    # 2.1.1.2-2处理同时解开的accl中的死锁
                            if zc2[0] not in bccl[1:]:
                                print('现在就已经不在了')
                            for accla in accl[0:]:
                                mar7 = 0
                                if bcc[0][1] == accla[1] and zc2[0][3] == accla[3]:
                                    accl.remove(accla)
                                    bcc.remove(accla)
                                    mar7 = 1
                                elif bcc[0][1] == accla[1] and bcc[0][2] == accla[2]:
                                    accl.remove(accla)
                                    bcc.remove(accla)
                                    mar7 = 1
                                elif bcc[0][1] == accla[1] and zc2[0][3] == accla[2]:
                                    accla_del = accla.copy()
                                    bcc.remove(accla_del)
                                    accla[1], accla[2], accla[3], accla[4] = accla[5][0]
                                    accla[5].remove(accla[5][0])
                                    bcc.append(accla)
                                elif bcc[0][1] == accla[1] and bcc[0][2] == accla[3]:
                                    accla_del = accla.copy()
                                    bcc.remove(accla_del)
                                    accla[1], accla[2], accla[3], accla[4] = accla[5][0]
                                    accla[5].remove(accla[5][0])
                                    bcc.append(accla)
                                if mar7 == 0:
                                    for accla5 in accla[5][0:]:
                                        if bcc[0][1] == accla5[0] and zc2[0][3] == accla5[2] and bcc[0][2] <= accla5[1]:
                                            accl.remove(accla)
                                            bcc.remove(accla)
                                            break
                                        elif bcc[0][1] == accla5[0] and bcc[0][2] == accla5[1] and zc2[0][3] > accla5[
                                            2]:
                                            accl.remove(accla)
                                            bcc.remove(accla)
                                            break
                                        elif bcc[0][1] == accla5[0] and zc2[0][3] == accla5[1]:
                                            accla5_del = accla.copy()
                                            bcc.remove(accla5_del)
                                            accla[5].remove(accla5)
                                            bcc.append(accla)
                                        elif bcc[0][1] == accla5[0] and bcc[0][2] == accla5[2]:
                                            accla5_del = accla.copy()
                                            bcc.remove(accla5_del)
                                            accla[5].remove(accla5)
                                            bcc.append(accla)
                                        elif bcc[0][1] == accla5[0] and zc2[0][3] == accla5[2] and bcc[0][2] > accla5[
                                            1]:
                                            accla5_del = accla.copy()
                                            bcc.remove(accla5_del)
                                            accla[5].remove(accla5)  # *** 10.16新增加，不是交错死锁链，但已不能用了
                                            bcc.append(accla)
                                        elif bcc[0][1] == accla5[0] and bcc[0][2] == accla5[1] and zc2[0][3] < accla5[
                                            2]:
                                            accla5_del = accla.copy()
                                            bcc.remove(accla5_del)
                                            accla[5].remove(accla5)  # *** 10.16新增加，不是交错死锁链，但已不能用了
                                            bcc.append(accla)
                            # zc1[0][3],bcc[i][2]=bcc[i][2],zc1[0][3]
                            qq[bcc[0][1]][zc2[0][3]], qq[bcc[0][1]][bcc[0][2]] = qq[bcc[0][1]][bcc[0][2]], \
                                                                                 qq[bcc[0][1]][
                                                                                     zc2[0][3]]  # 最后，是交换bbc[i]的最短死锁链
                            bccl.remove(bcc[0])
                            bccl.remove(zc2[0])
                            bcc.remove(bcc[0])
                            bcc.remove(zc2[0])
                    elif coub > 1:  # 2.1.2————最复杂的部分
                        if len(zc1) == 0:  # 意味着交错死锁全在zc2中，相对好办，只需要交换zc2中最大的那个，
                            # 交换之后删除这两个死锁即可，就不会有问题。zc2中最大的那个就是zc2[0]
                            for b22 in bccl[0:]:  # —2.1.2.1-1 处理同时解开的bccl中的死锁
                                if b22 != zc2[0] and b22[1] == zc2[0][1] and b22[3] == zc2[0][3]:
                                    bcc.remove(b22)
                                    bccl.remove(b22)
                                elif b22 != bcc[0] and bcc[0][1] == b22[1] and bcc[0][2] == b22[2]:
                                    bcc.remove(b22)
                                    bccl.remove(b22)
                            for a22 in accl[0:]:  # —2.1.2.2-1 处理同时解开的accl中的死锁
                                mar22 = 0
                                if bcc[0][1] == a22[1] and zc2[0][3] == a22[3]:
                                    accl.remove(a22)
                                    bcc.remove(a22)
                                    mar22 = 1
                                elif bcc[0][1] == a22[1] and bcc[0][2] == a22[2]:
                                    accl.remove(a22)
                                    bcc.remove(a22)
                                    mar22 = 1
                                elif bcc[0][1] == a22[1] and zc2[0][3] == a22[2]:
                                    a22_del = a22.copy()
                                    bcc.remove(a22_del)
                                    a22[1], a22[2], a22[3], a22[4] = a22[5][0]
                                    a22[5].remove(a22[5][0])
                                    bcc.append(a22)
                                elif bcc[0][1] == a22[1] and bcc[0][2] == a22[3]:
                                    a22_del = a22.copy()
                                    bcc.remove(a22_del)
                                    a22[1], a22[2], a22[3], a22[4] = a22[5][0]
                                    a22[5].remove(a22[5][0])
                                    bcc.append(a22)
                                if mar22 == 0:
                                    for a25 in a22[5][0:]:
                                        if bcc[0][1] == a25[0] and zc2[0][3] == a25[2] and bcc[0][2] <= a25[1]:
                                            accl.remove(a22)
                                            bcc.remove(a22)
                                            break
                                        elif bcc[0][1] == a25[0] and bcc[0][2] == a25[1] and zc2[0][3] > a25[2]:
                                            accl.remove(a22)
                                            bcc.remove(a22)
                                            break
                                        elif bcc[0][1] == a25[0] and zc2[0][3] == a25[1]:
                                            a25_del = a22.copy()
                                            bcc.remove(a25_del)
                                            a22[5].remove(a25)
                                            bcc.append(a22)
                                        elif bcc[0][1] == a25[0] and bcc[0][2] == a25[2]:
                                            a25_del = a22.copy()
                                            bcc.remove(a25_del)
                                            a22[5].remove(a25)
                                            bcc.append(a22)
                                        elif bcc[0][1] == a25[0] and zc2[0][3] == a25[2] and bcc[0][2] > a25[1]:
                                            a25_del = a22.copy()
                                            bcc.remove(a25_del)
                                            a22[5].remove(a25)  # *** 10.16新增加，不是交错死锁链，但已不能用了
                                            bcc.append(a22)
                                        elif bcc[0][1] == a25[0] and bcc[0][2] == a25[1] and zc2[0][3] < a25[2]:
                                            a25_del = a22.copy()
                                            bcc.remove(a25_del)
                                            a22[5].remove(a25)  # *** 10.16新增加，不是交错死锁链，但已不能用了
                                            bcc.append(a22)
                            qq[bcc[0][1]][zc2[0][3]], qq[bcc[0][1]][bcc[0][2]] = qq[bcc[0][1]][bcc[0][2]], \
                                                                                 qq[bcc[0][1]][
                                                                                     zc2[0][3]]  # 最后，是交换bbc[i]的最短死锁链
                            bccl.remove(bcc[0])
                            bccl.remove(zc2[0])
                            bcc.remove(bcc[0])
                            bcc.remove(zc2[0])
                        elif len(zc2) == 0:  # 意味着交错死锁全在zc1中,bcc[i]只需与zc1中最大的那个交错死锁交换
                            for b31 in bccl[0:]:  # —2.1.2.1-2 处理同时解开的bccl中的死锁
                                if b31 != zc1[0] and zc1[0][1] == b31[1] and zc1[0][2] == b31[2]:
                                    bcc.remove(b31)
                                    bccl.remove(b31)
                                elif b31 != bcc[0] and bcc[0][1] == b31[1] and bcc[0][3] == b31[3]:
                                    bcc.remove(b31)
                                    bccl.remove(b31)
                                    # 2.1.2.2-2处理同时解开的accl中的死锁
                            for aacla in accl[0:]:
                                ma3 = 0
                                if bcc[0][1] == aacla[1] and zc1[0][2] == aacla[2]:
                                    accl.remove(aacla)
                                    bcc.remove(aacla)
                                    ma3 = 1
                                elif bcc[0][1] == aacla[1] and bcc[0][3] == aacla[3]:
                                    accl.remove(aacla)
                                    bcc.remove(aacla)
                                    ma3 = 1
                                elif bcc[0][1] == aacla[1] and zc1[0][2] == aacla[3]:
                                    aacla_del = aacla.copy()
                                    bcc.remove(aacla_del)
                                    aacla[1], aacla[2], aacla[3], aacla[4] = aacla[5][0]
                                    aacla[5].remove(aacla[5][0])
                                    bcc.append(aacla)
                                elif bcc[0][1] == aacla[1] and bcc[0][3] == aacla[2]:
                                    aacla_del = aacla.copy()
                                    bcc.remove(aacla_del)
                                    aacla[1], aacla[2], aacla[3], aacla[4] = aacla[5][0]
                                    aacla[5].remove(aacla[5][0])
                                    bcc.append(aacla)
                                if ma3 == 0:
                                    for ala5 in aacla[5][0:]:
                                        if bcc[0][1] == ala5[0] and zc1[0][2] == ala5[1] and bcc[0][3] >= ala5[2]:
                                            accl.remove(aacla)
                                            bcc.remove(aacla)
                                            break
                                        elif bcc[0][1] == ala5[0] and bcc[0][3] == ala5[2] and zc1[0][2] < ala5[1]:
                                            accl.remove(aacla)
                                            bcc.remove(aacla)
                                            break
                                        elif bcc[0][1] == ala5[0] and zc1[0][2] == ala5[2]:
                                            ala5_del = aacla.copy()
                                            bcc.remove(ala5_del)
                                            aacla[5].remove(ala5)
                                            bcc.append(aacla)
                                        elif bcc[0][1] == ala5[0] and bcc[0][3] == ala5[1]:
                                            ala5_del = aacla.copy()
                                            bcc.remove(ala5_del)
                                            aacla[5].remove(ala5)
                                            bcc.append(aacla)
                                        elif bcc[0][1] == ala5[0] and zc1[0][2] == ala5[1] and bcc[0][3] < ala5[2]:
                                            ala5_del = aacla.copy()
                                            bcc.remove(ala5_del)
                                            aacla[5].remove(ala5)  # *** 10.16新增加，不是交错死锁链，但已不能用了
                                            bcc.append(aacla)
                                        elif bcc[0][1] == ala5[0] and bcc[0][3] == ala5[2] and zc1[0][2] > ala5[1]:
                                            ala5_del = aacla.copy()
                                            bcc.remove(ala5_del)
                                            aacla[5].remove(ala5)  # *** 10.16新增加，不是交错死锁链，但已不能用了
                                            bcc.append(aacla)
                            # 最后是交换删除死锁，交换完之后，同时消除bccl中的两个交错死锁 zc1[0][2],bcc[i][3]=bcc[i][3],zc1[0][2]
                            qq[bcc[0][1]][zc1[0][2]], qq[bcc[0][1]][bcc[0][3]] = qq[bcc[0][1]][bcc[0][3]], \
                                                                                 qq[bcc[0][1]][
                                                                                     zc1[0][2]]  # 最后，是交换bbc[i]的最短死锁链
                            bccl.remove(bcc[0])
                            bccl.remove(zc1[0])
                            bcc.remove(bcc[0])
                            bcc.remove(zc1[0])

                        else:  # 意味着zc1和zc2中都有交错死锁,将bcc[i]删除，然后解除对应的bb_sp中的所有死锁链
                            repla.extend(bb_spp[bcc[0][0]])  # 第 320行，bb_spp{6: [[6，3, 4, 7, 3]]}
                            for repli in bb_spp[bcc[0][0]]:
                                bcc.append(repli)
                            bcc.remove(bcc[0])
                            bccl.remove(
                                bcc[0])  # ***** 用bb_spp的所有子死锁链来替代bcc[0]，bb_spp是必须要解开的死锁链

                    elif coub == 0:  # 2.1.3bccl中没有交错死锁链需要处理
                        for acl in accl[0:]:
                            mar0 = 0
                            if bcc[0][1] == acl[1] and bcc[0][2] == acl[2]:  # 不需要 and bcc[i][3]>=acl[3]:
                                accl.remove(acl)
                                bcc.remove(acl)
                                mar0 = 1
                            elif bcc[0][1] == acl[1] and bcc[0][3] == acl[3]:  # 不需要and bcc[i][2]<acl[2]:
                                accl.remove(acl)
                                bcc.remove(acl)
                                mar0 = 1
                            elif bcc[0][1] == acl[1] and bcc[0][2] == acl[3]:
                                acl_del = acl.copy()  # 10.16增加，也要将bcc中的acl更新
                                bcc.remove(acl_del)  # 10.16增加，也要将bcc中的acl更新
                                acl[1], acl[2], acl[3], acl[4] = acl[5][0]
                                acl[5].remove(acl[5][0])
                                bcc.append(acl)  # 10.16增加，也要将bcc中的acl更新
                            elif bcc[0][1] == acl[1] and bcc[0][3] == acl[2]:
                                acl_del = acl.copy()  # 10.16增加，也要将bcc中的acl更新
                                bcc.remove(acl_del)  # 10.16增加，也要将bcc中的acl更新
                                acl[1], acl[2], acl[3], acl[4] = acl[5][0]
                                acl[5].remove(acl[5][0])
                                bcc.append(acl)  # 10.16增加，也要将bcc中的acl更新
                            if mar0 == 0:
                                for acl5 in acl[5][0:]:
                                    if bcc[0][1] == acl5[0] and bcc[0][2] == acl5[1] and bcc[0][3] >= acl5[2]:
                                        accl.remove(acl)
                                        bcc.remove(acl)
                                        break
                                    elif bcc[0][1] == acl5[0] and bcc[0][3] == acl5[2] and bcc[0][2] < acl5[1]:
                                        accl.remove(acl)
                                        bcc.remove(acl)
                                        break
                                    elif bcc[0][1] == acl5[0] and bcc[0][2] == acl5[2]:
                                        acl5_del = acl.copy()
                                        bcc.remove(acl5_del)
                                        acl[5].remove(acl5)
                                        bcc.append(acl)
                                    elif bcc[0][1] == acl5[0] and bcc[0][3] == acl5[1]:
                                        acl5_del = acl.copy()
                                        bcc.remove(acl5_del)
                                        acl[5].remove(acl5)
                                        bcc.append(acl)
                                    elif bcc[0][1] == acl5[0] and bcc[0][2] == acl5[1] and bcc[0][3] < acl5[2]:
                                        acl5_del = acl.copy()
                                        bcc.remove(acl5_del)
                                        acl[5].remove(acl5)  # *** 10.16新增加，不是交错死锁链，但已不能用了
                                        bcc.append(acl)
                                    elif bcc[0][1] == acl5[0] and bcc[0][3] == acl5[2] and bcc[0][2] > acl5[1]:
                                        acl5_del = acl.copy()
                                        bcc.remove(acl5_del)
                                        acl[5].remove(acl5)  # *** 10.16新增加，不是交错死锁链，但已不能用了
                                        bcc.append(acl)
                        # 然后再删除bccl中共同解开的死锁
                        for zs1i in zs1:
                            bcc.remove(zs1i)
                            bccl.remove(zs1i)
                        for zs2i in zs2:
                            bcc.remove(zs2i)
                            bccl.remove(zs2i)
                        qq[bcc[0][1]][bcc[0][2]], qq[bcc[0][1]][bcc[0][3]] = qq[bcc[0][1]][bcc[0][3]], qq[bcc[0][1]][
                            bcc[0][2]]  # 最后，是交换bbc[i]的最短死锁链
                        bccl.remove(bcc[0])
                        bcc.remove(bcc[0])

                elif len(bccl) == 1:  # 2.2 bccl中只有一个死锁，就对accl中的死锁进行处理,更新交错的死锁链，删除同时解开的死锁
                    for w in accl[0:]:  # ***** 10.20修改上面条件从else:到elif len(bccl)==1:
                        mar1 = 0
                        if bcc[0][1] == w[1] and bcc[0][2] == w[2]:  # 不需要and bcc[0][3]>=accl[w][3]:
                            accl.remove(w)
                            bcc.remove(w)
                            mar1 = 1
                        elif bcc[0][1] == w[1] and bcc[0][3] == w[3]:  # and bcc[i][2]<accl[w][2]
                            accl.remove(w)
                            bcc.remove(w)
                            mar1 = 1
                        elif bcc[0][1] == w[1] and bcc[0][2] == w[3]:
                            w_del = w.copy()  # 10.16增加，也要将bcc中的acl更新
                            bcc.remove(w_del)  # 10.16增加，也要将bcc中的acl更新
                            w[1], w[2], w[3], w[4] = w[5][0]
                            w[5].remove(w[5][0])
                            bcc.append(w)
                        elif bcc[0][1] == w[1] and bcc[0][3] == w[2]:
                            w_del = w.copy()  # 10.16增加，也要将bcc中的acl更新
                            bcc.remove(w_del)  # 10.16增加，也要将bcc中的acl更新
                            w[1], w[2], w[3], w[4] = w[5][0]
                            w[5].remove(w[5][0])
                            bcc.append(w)
                        if mar1 == 0:  # 如果死锁并未删除
                            for x in w[5][0:]:
                                if bcc[0][1] == x[0] and bcc[0][2] <= x[1] and bcc[0][3] == x[2]:
                                    accl.remove(w)
                                    bcc.remove(w)
                                    break
                                elif bcc[0][1] == x[0] and bcc[0][2] == x[1] and bcc[0][3] > x[2]:
                                    accl.remove(w)
                                    bcc.remove(w)
                                    break
                                elif bcc[0][1] == x[0] and bcc[0][2] == x[2]:
                                    x_del = w.copy()
                                    bcc.remove(x_del)
                                    w[5].remove(x)
                                    bcc.append(w)
                                elif bcc[0][1] == x[0] and bcc[0][3] == x[1]:
                                    x_del = w.copy()
                                    bcc.remove(x_del)
                                    w[5].remove(x)
                                    bcc.append(w)
                                elif bcc[0][1] == x[0] and bcc[0][2] > x[1] and bcc[0][3] == x[2]:
                                    x_del = w.copy()
                                    bcc.remove(x_del)
                                    w[5].remove(x)
                                    bcc.append(w)
                                elif bcc[0][1] == x[0] and bcc[0][2] == x[1] and bcc[0][3] < x[2]:
                                    x_del = w.copy()
                                    bcc.remove(x_del)
                                    w[5].remove(x)
                                    bcc.append(w)
                    qq[bcc[0][1]][bcc[0][2]], qq[bcc[0][1]][bcc[0][3]] = qq[bcc[0][1]][bcc[0][3]], qq[bcc[0][1]][
                        bcc[0][2]]  # 最后，是交换bbc[i]的最短死锁链
                    bccl.remove(bcc[0])
                    bcc.remove(bcc[0])
        bcc = _merge_sorted(bcc)
        accl = _merge_sorted(accl)
    if con_num_i == None:
        #         return qq 不用返回解，因为解qq已经解开死锁了
        return 'OK'
    else:
        return con_num_i


# ***** 极其非常重要，在计算解的适应度时又发现一个问题，检查第二类死锁的程序，并不能检查出第一类死锁中的最
# 简单情况，即一台机器上，相同产品后面工序先开工，而且即使这类死锁存在，也不影响解锁程序。而在解锁的过程中，
# 却会产生新的这类死锁，从而无法计算解的适应度。为此，在函数oss中还要增加每个解在完成第二类死锁解锁后、对此
# 类死锁的判断、解除，再次迭代——最终的修改极为简单，增加了第15行
def oss(solu):  # 最终解锁函数，输入为要解锁的种群
    osolu = opensisuo(solu)  # 解除种群的第一类死锁
    superc = []  # 有超级复杂死锁的解，被从种群中删除，然后记录在superc中
    for qq in osolu[0:]:  # 对种群中的每一个解qq
        spqq = qq.copy()  # 10.29添加，当出现特别复杂的死锁，或者解锁算法出问题时，用于输出该解
        while True:
            af = detectsisuo(qq)  # 检出qq中的第二类死锁af
            if af == {}:  # 如果qq中没有第二类死锁，就直接跳过该qq，进入下一个osolu中的解，这样节约时间
                break
            oqq = n2sisuo(af, qq)  # 解除qq中的第二类死锁
            qql = opensisuo([qq])  # 第15行，解决新问题的关键   10.29再修改，移动到第27行
            #             qq=qql[0]  10.26修改，极其非常重要，必须将再次解除第一类死锁的结果赋予qq 10.29再修改，移到27行
            #  ******* 经过10.31对变量id的认识与验证，原先做法也没错，因为qql[0]==qq，即id(qql[0])==id(qq)
            if oqq != 'OK':
                #             ind=osolu.index(qq)
                #             qqq=osolu[ind+1]
                osolu.remove(qq)  # 如果qq中有超级复杂的死锁，直接将qq从种群中删除
                superc.append(spqq)  # 记录有超级死锁的解,注意，这个是原始的解，而此时的qq是已经处理过的解
                break  # 注意，删除掉有超复杂死锁的解后，跳出while循环，对下一osolu中的解进行解锁
            #             osolu.insert(ind,qqq)
            else:
                #                 qql=opensisuo([qq]) # 第15行，解决新问题的关键
                #                 qq=qql[0] # 10.26 修改，极其非常重要，必须要将再次解除第一类死锁的结果赋予qq
                if detectsisuo(qql[0]) == {}:  # 又检查一遍，说明qq中的第二类死锁确实已被解除了
                    qq = qql[0]
                    break
                else:
                    qq = qql[0]
    return (osolu, superc)  # 如果解锁成功，返回tuple，第一个元素是解锁后的种群，第二个元素是[]或被删除的解


'''7、纯遗传算法的交叉变异函数群'''


def cro(cso,avg):  # 纯交叉函数，输入为种群，返回为交叉后的种群。

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


    for sol in cro_cso:
        #         print('开始第',cro_cso.index(sol),'个解')
        sma, fma = fitcalu(sol)  # 求解sol的开工时间矩阵sma和完工时间矩阵fma
        #         print('初始计算适应度完成')
        prom = None  # 变异概率
        fma_va = max(fma.flat)
        if fma_va <= avg:
            prom = 2 / (1 + math.exp(0.3 * (avg - fma_va)))  # 12.28 变异概率，只有当解更优时，才降低变异概率，当解比平均解更差，一定变异
        else:
            prom = 0.9  # 如果解很差，就提高变异概率
        if random.random() < prom:  # 如果变异的话
            mano1=random.choice([1,2,3,4,5])
            mano2=random.choice([6,7])
            cronu1=random.sample(list(range(len(sol[mano1]))),2)
            cronu2 = random.sample(list(range(len(sol[mano2]))), 2)
            sol[mano1][cronu1[0]],sol[mano1][cronu1[1]]=sol[mano1][cronu1[1]],sol[mano1][cronu1[0]]
            sol[mano2][cronu2[0]], sol[mano2][cronu2[1]] = sol[mano2][cronu2[1]], sol[mano2][cronu2[0]]

    return cro_cso  # 返回交叉变异后的种群



    # for i in range(len(cso) // 2):
    #     parents = random.sample(cso, 2)  # random.sample(li,n)从li中随机取出n个不同元素，返回结果是长度为n的list
    #     fa = copy.deepcopy(parents[0])  # 父亲解，10.29增加.copy()  ****** 10.30改为deepcopy深度复制
    #     ma = copy.deepcopy(parents[1])  # 母亲解，10.29增加.copy()  ****** 10.30改为deepcopy深度复制
    #     a1 = random.choice([1, 2, 3, 4, 5])
    #     a2 = random.choice([6, 7])
    #     crp1 = random.randint(1, lent[a1] - 1)  # 确定交叉点1，交叉的时候，更换处理长链
    #     fa1 = fa[a1][0:crp1]
    #     fa2 = fa[a1][crp1:]
    #     ma1 = ma[a1][0:crp1]
    #     ma2 = ma[a1][crp1:]
    #     crp2 = random.randint(1, lent[a2] - 1)  # 确定交叉点2，交叉的时候，更换处理长链
    #     fat1 = fa[a2][0:crp2]
    #     fat2 = fa[a2][crp2:]
    #     mat1 = ma[a2][0:crp2]
    #     mat2 = ma[a2][crp2:]
    #     if len(fa1) >= len(fa2):
    #         indfa = []
    #         indma = []
    #         for j in range(len(fa1)):
    #             if fa1[j] in ma1:
    #                 pass
    #             else:
    #                 indfa.append(j)
    #             if ma1[j] in fa1:
    #                 pass
    #             else:
    #                 indma.append(j)
    #         for ij in range(len(indfa)):  # 处理交叉的染色体不一致的情况
    #             fa1[indfa[ij]], ma1[indma[ij]] = ma1[indma[ij]], fa1[indfa[ij]]
    #     else:
    #         indfa1 = []
    #         indma1 = []
    #         for jj in range(len(fa2)):
    #             if fa2[jj] in ma2:
    #                 pass
    #             else:
    #                 indfa1.append(jj)
    #             if ma2[jj] in fa2:
    #                 pass
    #             else:
    #                 indma1.append(jj)
    #         for ijj in range(len(indfa1)):  # 处理交叉的染色体不一致的情况
    #             fa2[indfa1[ijj]], ma2[indma1[ijj]] = ma2[indma1[ijj]], fa2[indfa1[ijj]]
    #     fa1.extend(ma2)  # 10.29修改，之前的fa[a1]=fa1.extend(ma2)，实际上fa[a1]=None
    #     fa[a1] = fa1
    #     ma1.extend(fa2)  # 10.29修改，之前的ma[a1]=ma1.extend(fa2)，实际上ma[a1]=None
    #     ma[a1] = ma1
    #     # 至此完成机器a1的单点交叉，接下来进行机器a2的单点交叉：
    #     #         crp2=random.randint(1,lent[a2]-1)  # 确定交叉点2，交叉的时候，更换处理长链
    #     #         fat1=fa[a2][0:crp2]
    #     #         fat2=fa[a2][crp2:]
    #     #         mat1=ma[a2][0:crp2]
    #     #         mat2=ma[a2][crp2:]
    #     if len(fat1) >= len(fat2):
    #         indfat = []
    #         indmat = []
    #         for jt in range(len(fat1)):
    #             if fat1[jt] in mat1:
    #                 pass
    #             else:
    #                 indfat.append(jt)
    #             if mat1[jt] in fat1:
    #                 pass
    #             else:
    #                 indmat.append(jt)
    #         for ijt in range(len(indfat)):  # 处理交叉的染色体不一致的情况
    #             fat1[indfat[ijt]], mat1[indmat[ijt]] = mat1[indmat[ijt]], fat1[indfat[ijt]]
    #     else:
    #         indfat1 = []
    #         indmat1 = []
    #         for jjt in range(len(fat2)):
    #             if fat2[jjt] in mat2:
    #                 pass
    #             else:
    #                 indfat1.append(jjt)
    #             if mat2[jjt] in fat2:
    #                 pass
    #             else:
    #                 indmat1.append(jjt)
    #         for ijjt in range(len(indfat1)):  # 处理交叉的染色体不一致的情况
    #             fat2[indfat1[ijjt]], mat2[indmat1[ijjt]] = mat2[indmat1[ijjt]], fat2[indfat1[ijjt]]
    #     fat1.extend(mat2)  # 10.29修改，之前的fa[a2]=fat1.extend(mat2)，实际上fa[a2]=None
    #     fa[a2] = fat1
    #     mat1.extend(fat2)  # 10.29修改，之前的ma[a2]=mat1.extend(fat2)，实际上ma[a2]=None
    #     ma[a2] = mat1
    #     cro_cso.append(fa)
    #     cro_cso.append(ma)

