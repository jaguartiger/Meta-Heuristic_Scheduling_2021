'''绘图程序，如甘特图、每代最优解、历代最优解'''

import matplotlib.pyplot as plt
import numpy as np
import xlutils.copy as xc
import xlwt,xlrd

# 第n代后（下面代码是第7代后）每代最优解record_hifi变量绘图
def sinline(record_hifi):
    plt.plot([i for i in range(7,len(record_hifi))],record_hifi[7:],linewidth=0.8,marker='1',label='每代最优解') # marker='1'
    # plt.plot([range(7,500)],22.7,linewidth=0.8,label='启发式算法最优解')
    plt.legend()
    plt.show()


# 每代最优解record_hifi和历代最优解record_fi的对比绘图
def dueline(record_hifi, record_fi):
    plt.rcParams['figure.dpi'] = 800 # 设置图片的分辨率为800dpi
    plt.rcParams['figure.figsize'] = (15.0, 5.0)   #长度和高度
    plt.plot([i for i in range(len(record_hifi))],record_hifi,linewidth=1,label='每代最优解') # marker='1'
    plt.plot([i for i in range(len(record_fi))],record_fi,linewidth=1,label='历代最优解')  #  range(7,len(record_fi))],re_fi[7:],marker='1',color='gray',
    plt.legend(loc='upper right', fontsize='small',frameon=False)
    plt.show()


# 绘制甘特图程序
# 10、绘制解的甘特图

# ax=plt.gca() # 返回对象ax用于设置下一行的属性
# [ax.spines[i].set_visible(False) for i in ["top","right"]] # 不显示上方和右侧的边框线
# 关于plt.gca()和其字典属性，在网页https://www.cnblogs.com/franknihao/p/9259723.html中


def hoisting_gatt(sol,tt): # 此处只是备份，出现在主控程序中，因为内部调用函数fitcalu。输入参数为历史最优somin[0]、工时矩阵task_wt
    sma,fma=fitcalu(sol)
    plt.rcParams['figure.dpi'] = 1000  # 设置图片的分辨率为800dpi
    plt.rcParams['figure.figsize'] = (17.0, 5.0)  # 长度和高度
    colorset = ['#00CD66', '#F4A460', '#00CED1', '#ff3366', '#58ACFA', '#D358F7', '#BDBDBD', '#58FAF4', '#F6CEE3',
                '#FFFF00', '#BFFF00', '#B45F04']
    #           1-绿色，2-橙色（原金色#FFD700），3-暗宝石绿，4-红色，5-湖蓝，6-淡紫，7-灰色，8-青色，9-粉色，10-明黄，11-嫩芽绿，12-棕色

    """甘特图
    sol 解字典
    tt  工序的工时
    sma 每个产品工序的开工时间
    """
    for i in range(1,len(sol)+1):
        for j in range(len(sol[i])):
            if tt[sol[i][j][0]][sol[i][j][1]]!=0:
                plt.barh(i,tt[sol[i][j][0]][sol[i][j][1]],left=sma[sol[i][j][0]][sol[i][j][1]],color=colorset[sol[i][j][0]])
                plt.text(sma[sol[i][j][0]][sol[i][j][1]],i-0.34,'%.1f \n%.1f \nP%s'%(sma[sol[i][j][0]][sol[i][j][1]],tt[sol[i][j][0]][sol[i][j][1]],sol[i][j][0]),color="black",size=8) # 文字的位置与文字的内容
                # 上面一行是文字，参数依次为：文字横向位置、纵向位置、文字内容（可用\n换行）、文字颜色、文字大小
                #     plt.yticks(np.arange(len(sol)+1),np.arange(0,len(sol)+1)) 跟下面一行一模一样
    plt.yticks(np.arange(len(sol)+1)) # y轴刻度从0到几
    plt.show()

def set_style(name, height, bold=False):  # 将数据写到外部excel的字体格式函数，作为sheet.write（）的第四个参数
    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 为样式创建字体
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style



def output(record_hifi, record_fi, somin,date,i):  # date和i是用来命名sheet的信息，date是字符串，i是整数
    exi = xlrd.open_workbook('C:/Users/Jaguar/Desktop/Scheduling_Output.xls', 'w+b')
    new_exi = xc.copy(exi)
    nesheet = new_exi.add_sheet(date+'调度运算'+str(i))
    for ind, ite in enumerate(['每代最优解', '历代最优解', '最优调度方案机器', '班组顺序', '次优调度方案机器','班组顺序' ]):
        nesheet.write(0, ind, ite, set_style('Times New Roman', 200, False))  # 写入表头

    for i0, j0 in enumerate(record_hifi):
        nesheet.write(i0 + 1, 0, j0, set_style('Times New Roman', 200, False))

    for i1, j1 in enumerate(record_fi):
        nesheet.write(i1 + 1, 1, j1, set_style('Times New Roman', 200, False))

    for i2, j2 in enumerate(somin[0]):
        nesheet.write( i2+1, 2, j2, set_style('Times New Roman', 200, False))
        nesheet.write(i2 + 1, 3, str(somin[0][j2]), set_style('Times New Roman', 200, False))

    for i3, j3 in enumerate(somin[1]):
        nesheet.write( i3+1, 4, j3, set_style('Times New Roman', 200, False))
        nesheet.write(i3 + 1, 5, str(somin[1][j3]), set_style('Times New Roman', 200, False))

    new_exi.save('C:/Users/Jaguar/Desktop/Scheduling_Output.xls')
