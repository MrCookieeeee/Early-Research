import numpy as np
import pandas
import pandas as pd
from tqdm import trange



def main():
    data = pd.read_excel("AR/AR_MID.xlsx")
    result = data[["Publication Number", "Publication Date"]]
    result = result.reindex(columns=result.columns.tolist() + ["CP", "label"])  #给result 加了两行
    result[['CP', 'label']] = result[['CP', 'label']].astype('object')          #把选中的两行转换成 object 格式
    refer = result.copy()


    F_citations = data["Forward Citations"]
    B_citations = data["Backward Citations"]



    length = len(B_citations)
    # 循环处理前后引用  只要某专利的前后引用包含另一个专利， 并且， 这个专利在我们的列表中，我们就把这个专利放到CP中
    for i in trange(length):
        # 处理前引用
        tmpB:list[str] = str(B_citations[i]).split("| ")
        tmpB_1 = []
        for j in tmpB:                 # tmp       ['US20150312560 A', 'US20150312561 B']
            tmpB_2 = j.split(" ")      # tmp_2     ['US20150312560' ,'A']
            tmpB_1.append(tmpB_2[0])    #tmp_2[0]  US20150312560
        afterB = cleaner(tmpB_1, data["Publication Number"])


        # 处理后引用
        tmpF: list[str] = str(F_citations[i]).split("| ")
        tmpF_1 = []
        for j in tmpF:  # tmp       ['US20150312560 A', 'US20150312561 B']
            tmpF_2 = j.split(" ")  # tmp_2     ['US20150312560' ,'A']
            tmpF_1.append(tmpF_2[0])  # tmp_2[0]  US20150312560

        #print(tmpF_1)
        afterF = cleaner(tmpF_1, data["Publication Number"])
        #print(afterF)

        # 结果塞入CP
        result.at[i, 'CP'] = pd.array([])
        result.at[i, 'CP'] = pd.array(list(set(list(result.at[i, "CP"]) + afterB + afterF)))  # 将前面收集的after列表塞入该行的CP中
        result.at[i, 'CP'] = list(result.at[i, 'CP']) # 这行不能少，不然就是ArrayList的乱七八糟信息


    CP_rows = result["CP"]
    for i in range(len(CP_rows)):
        tmp = pd.isna(CP_rows[i]) # isna 返回bool值，判断对应的行是否为空值
        if type(tmp) == np.ndarray:
            if len(tmp) == 0:
                result.drop(i, axis=0, inplace=True)
    result.index = range(len(result)) # 把第一条专利，从0开始编号，如果去掉，excel会从第一行（PN那一行）开始标注

    result.to_excel("AR/AR_mid_result.xlsx", index=False)



def cleaner(raw: list, data_0: pandas.Series) -> list: # 判断raw内元素是不是在data_0内，返回所有在data_0内的raw元素（不重复）
    data = data_0.tolist()
    res = []
    for i in raw:
        if i in data:
            res.append(i)
    res = list(set(res))  #set函数 去重
    return res

main()