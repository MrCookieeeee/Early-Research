import pandas
import xlrd
import xlwt
from tqdm import trange
import seaborn as sns
import matplotlib.pyplot as plt


def get_Abstract():
    data = pandas.read_csv('AR/AR.csv', encoding='latin', error_bad_lines=False)
    result = data[["Publication Number", "Abstract"]]
    result.to_excel('AR/abstract.xlsx',encoding='utf-8')


def preprocess():   #找到前引和后引
    data = pandas.read_csv('AR/AR.csv', encoding='latin1', error_bad_lines=False)
    result = data[["Publication Number", "Publication Date", "Forward Citations", "Backward Citations"]]
    result.to_excel("AR/AR_MID.xlsx")

def readFile():
    xls_Data = xlrd.open_workbook('AR/AR_MID.xlsx')  # MID主要存放前后引
    table = xls_Data.sheets()[0]  # 读取sheet1的面板数据，不加这个0好像也没关系
    index = table.row_values(0, start_colx=0, end_colx=None) # 提取第0行数据，即索引作为list

    date_index = 0  # PD是哪一列
    for i in index:
        if "Publication Date" == i:
            break
        date_index = date_index + 1

    date_data = table.col_values(date_index, start_rowx=1, end_rowx=None)# 提取出PD列的所有数据
    length = len(date_data)
    date = [] #存放每个时间的年-月-日分割
    for m in trange(length): # trange 两个作用：1.int型的length不可迭代，转化为可迭代 2.添加可视化进度条
        i = str(date_data[m]).strip()
        res = [i[0:4], i[5:7], i[8:10]]
        date.append(res)
    data_of_mon_year = process(date)
    return data_of_mon_year




def process(raw: list) -> dict: # 收集每年中每个月的数据量
    data = {}
    for i in raw:
        keys = data.keys()
        if i[0] in keys: #i[0]代表年
            data[ i[0] ][ i[1] ] += 1
        else: #不存在同年份的，创建，并给该年份的每个月赋初值0
            data[i[0]] = {"01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0,
                          "11": 0, "12": 0}
            data[ i[0] ][ i[1] ] += 1

    sorted_data = dict(sorted(data.items(), reverse=True)) #对data的第一个元素（年份），降序排序
    print(sorted_data)
    return sorted_data


def write(data :dict):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet("result")
    for i in range(1, 13):
        worksheet.write(0, i, str(i) + "月")# 月份写在第0行开始，1，2，3...直到12
    keys = data.keys()
    count_years = 1 #控制写第几行

    for year in keys:
        worksheet.write(count_years, 0, str(year))# 年份写在第0列
        for i in range(1, 13):
            month = ""
            if i < 10:
                month = "0" + str(i)
            else:
                month = str(i)
            worksheet.write(count_years, i, str(data[str(year)][month]))
        count_years += 1



    workbook.save("./result/count_result.xls")








#get_Abstract()
#preprocess()
#readFile()
#write(readFile())  #直接调用这个生成结果excel
