import time

import pandas as pd

year = "2011"
month = "01"
day = "01"


def label():
    data = pd.read_excel("../step1.1_dataclean/AR_mid_result.xlsx")
    time_columns = data["Publication Date"]
    border = time.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
    # drop the former index from last processing
    #data.drop(["Unnamed: 0"], axis=1, inplace=True)
    Label_1 = 0
    Label_2 = 0
    for i in range(len(time_columns)):
        _time = time.strptime(str(time_columns[i]), "%Y-%m-%d")
        if _time > border:
            data.loc[i, "label"] = "2"
            Label_2 = Label_2 + 1
        else:
            data.loc[i, "label"] = "1"
            Label_1 = Label_1 + 1
    print(f"label1:{Label_1}, label2:{Label_2}")
    data.drop("Publication Date", axis=1, inplace=True)
    data.to_excel("./label_result.xlsx")
    return data


