import pickle
import matplotlib.pyplot as plt
import networkx as ntx
import networkx as nx
import pandas as pd
from tqdm import trange

# 跑完这个函数耗时14分钟

def main():
    top_n = 3 # top3社群

    with open('../step1_dataclean/step1.2_community_depart/top3.pkl', 'rb') as f:
        loaded_list = pickle.load(f)

    for t in trange(top_n):   # 进行top_n次循环，对top_n个社群进行主路径分析
        G = ntx.DiGraph()
        nodes = loaded_list[t]

        plt.rcParams.update({
            'figure.figsize': (30, 30)
        })
        data = pd.read_excel('../step1_dataclean/step1.2_community_depart/label_result.xlsx')
        CP = data["CP"]
        PN = data["Publication Number"]
        CP_list = []

        for i in CP:
            CP_list.append(i.split("'")[1::2])  # 原来的CP内容是一整串以string出现的，现在转换成可操作的二维数组
        # print(CP_list[1][1]) WO2016040376

        # 把数据添加到网络
        for i in range(len(PN)):
            if PN[i] in nodes:
                G.add_node(PN[i])  # node 是我们想要研究的社群，只有社群里的结点才加入
            else:
                continue
            for j in range(len(CP_list[i])):
                if PN[i] == CP_list[i][j]:
                    continue
                G.add_edge(CP_list[i][j], PN[i])

        weights = dict(G.degree())  # 边权 = 边两个点的度数之和
        for u, v in G.edges():
            G.edges[u, v]['weight'] = weights[u] + weights[v]

        # 在一个社群中找到网络中找度数前3大的结点
        max_degree_nodes = get_high_degree_nodes(G, 3)

        for i in range(3):
            path = extract_main_path(G.copy(), max_degree_nodes[i], data)
            sorted_path = sort_date(path)
            save_path(sorted_path, i, t)
            #visualize_main_path(sorted_path, data, max_degree_nodes[i], i, t)    # 暂时注释掉

def save_path(path ,num , t):
    df = pd.read_excel("abstract.xlsx")
    selected_data_list = []
    for element in path:
        matching_rows = df[df['Publication Number'] == element]
        selected_data = matching_rows[['Publication Number', 'Abstract']]
        selected_data_list.append(selected_data)
    total_data = pd.concat(selected_data_list)
    total_data.index = range(len(total_data))
    total_data.to_excel(f"./top3_community/SPC_community_{t+1}/Abstract{num+1}.xlsx", index=False)



def sort_date(path):
    data = pd.read_excel("../step1_dataclean/step1.1_dataclean/AR_mid_result.xlsx")

    PN_Date = []
    for element in path:
        date = str(data[data["Publication Number"] == str(element)]["Publication Date"]).split(" ")
        date1 = date[4]
        date2 = date1.split("\n")[0]     # 这几行是拿到element对应的时间的，透明使用即可
        PN_Date.append((element,date2))  # PN_Date[0] -> ('CN107554425', '2018-01-09')

    sorted_PN_Date = sorted(PN_Date, key=lambda x: x[1])
    result = []
    for node in sorted_PN_Date:
        result.append(node[0])
    return result

def label_mark(G, data, max_node) -> list:
    result = []
    for node in G:
        # 拿到node对应的label编号，透明使用即可
        label = str(data[data["Publication Number"] == str(node)]["label"]).split(' ')
        label_tmp = label[4][0]
        if node == max_node:
            result.append('black')
            continue
        if str(label_tmp) == "1":
            result.append("blue")
        else:
            result.append("red")
    return result

def visualize_main_path(path_list, data, max_degree_node, num, t):
    """
    1.路径可视化
    2.保存到 top3_community_{t}/SPC_community_{num}中， t表示这是第几个社群， num表示这是该社群的第几条主路经

    参数：
        - path_list：一条list[]形式的路径。
        - data：label_result结果。
        - max_degree_node：度数最大的结点之一，主路经围绕它展开。
        - num：该社群的第几条主路经。
        - t：第t个社群。

    返回值：
        - 无。
    """

    G = ntx.DiGraph()

    for i in range(len(path_list) - 1):
        source = path_list[i]
        target = path_list[i + 1]
        G.add_edge(source, target)
    pos = ntx.spiral_layout(G)
    ntx.draw(G, pos=pos, node_color=label_mark(G, data, max_degree_node), with_labels=True)
    plt.savefig(f"./top3_community/SPC_community_{t+1}/main_path{num+1}.png")
    plt.show()



def get_high_degree_nodes(G, k):
    """
    返回 networkx 中度数比较大的点列表。

    参数：
        - G：networkx 图形对象。
        - k：int，要返回的前k个最高度数的节点。

    返回值：
        - 一个包含前k个最高度数节点的列表。
    """
    degrees = dict(G.degree())
    sorted_nodes = sorted(degrees, key=degrees.get, reverse=True)
    return sorted_nodes[:k]




def extract_main_path(G, max_degree_node, data):
    """
    提取主路经。

    参数：
        - G：networkx 图形对象。
        - max_out_degree_node：度最大的几个结点之一。
        - data：label_result结果。

    返回值：
        - 一条包含max_out_degree_node的主路经， list[]的形式。
    """
    starts = find_start_nodes(G, max_degree_node)  # 开始结点是用max_out结点向前迭代找出来的

    ends = find_end_nodes(G, data)                     # 结束结点是在全图中找出出度最小且label为2的

    mid = max_degree_node

    #print(starts, ends)

    # 找到主路经分两步 1.找mid到end 2.找start到mid 再把这些路合起来，也就是以max_degree_node为中心，向前向后找
    paths_back = []
    for end in ends:
        try:
            path = nx.dijkstra_path(G.copy(), mid, end)
            paths_back.append(path)
        except Exception as e:
            print(e)        # 这里会报错，no path to xx，表示这两点之间不可达，不影响程序

    paths_forward = []
    for start in starts:
        try:
            path = nx.dijkstra_path(G.copy(), start, mid)
            paths_forward.append(path)
        except Exception as e:
            print(e)

    print("dij finish~~~")

    # 以spc为指标，找前后路径中的主路经
    # 后向
    max_B_path = []
    max_B_degree = 0
    for path in paths_back:
        if calculate_spc_weight(G, path) >= max_B_degree:
            max_B_path = path
            max_B_degree = calculate_spc_weight(G, path)

    #前向
    max_F_path = []
    max_F_degree = 0
    for path in paths_forward:
        if calculate_spc_weight(G, path) >= max_F_degree:
            max_F_path = path
            max_F_degree = calculate_spc_weight(G, path)

    Final_path = max_F_path + max_B_path
    return Final_path


def calculate_spc_weight(G, path):
    weight = 1
    for i in range(len(path) - 1):
        edge_data = G.get_edge_data(path[i], path[i + 1])  # get_edge_data函数返回两个点的边权信息
        weight *= edge_data['weight']
    return weight



def find_end_nodes(G, data):
    """
        寻找有资格作为结束点的结点。
        1.出度最小
        2.label值为2

        参数：
            - G：networkx 图形对象， 有向图。
            - data：label_result结果。
    """
    # 第一步，找到度数最小的结点们
    min_nodes = []
    degrees = dict(G.out_degree())   #注意这里要使用出度
    sorted_nodes = sorted(degrees, key=degrees.get, reverse=False)
    minn = degrees[sorted_nodes[0]]  #升序排序后，找到node的最小值
    for nodes in G:
        if degrees[nodes] == minn:
            min_nodes.append(nodes)

    # 第二步， 在度数最小的结点中， label为2的（处在第二个生命周期），才有资格作终点
    ends = []
    for node in min_nodes:
        tmp = data[data["Publication Number"] == str(node)]  # 在label_result中找到min_nodes们
        label_tmp = tmp.values[0][2]
        if str(label_tmp) == "1":  # 如果它们的标签值为1
            continue
        else:                      # 如果它们的标签值为2(对于AR的label_result，只有1和2两个值)
            ends.append(node)
    return ends



def find_start_nodes(G, node):
    """
        寻找给定节点所在链条的起始节点列表。

        参数：
            - G：networkx 图形对象， 有向图。
            - node：给定节点。
    """

    start_nodes = []  # 起始节点列表
    visited = set()  # 记录已经访问的节点

    # 递归查找起始节点，
    def dfs(curr_node):
        # 如果当前节点已经访问过，直接返回
        if curr_node in visited:
            return
        visited.add(curr_node)

        # 如果当前节点没有入边，将其添加到起始节点列表中
        if G.in_degree(curr_node) == 0:
            start_nodes.append(curr_node)

        # 对于这个结点所有的父结点，继续执行dfs
        for start_node in G.predecessors(curr_node):  #predecessors函数返回到这个点有边的点
            dfs(start_node)

    dfs(node)
    return start_nodes






if __name__ == '__main__':
    main()
