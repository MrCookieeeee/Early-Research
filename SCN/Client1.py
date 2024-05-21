import socket
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.linalg import lu_factor, lu_solve


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

    def connect_to_server(self):
        self.client_socket.connect((self.host, self.port))

    def send_data(self, w, b, beta, n, loss):
        data = pickle.dumps((w, b, beta, n, loss))
        self.client_socket.sendall(data)

    def receive_data(self):
        data = self.client_socket.recv(1024)
        w, b, beta = pickle.loads(data)
        return w, b, beta

    def close_connection(self):
        self.client_socket.close()




# initialize netport
server_host = '127.0.0.1'
server_port = 12345
client = Client(server_host, server_port)


# Load data
n = 800                   # Sample  size
data = np.load("./data/dataset1.npz", allow_pickle=True)
Xtrain = data['Xtrain']   # 800*1
Ttrain = data['Ttrain']   # 800*1
Xtest = data['Xtest']
Ttest = data['Ttest']

# Initialize parameters
input_dimension  = 1
output_dimension = 1
Hidden_Layer_Weight = np.matrix([])          # Hidden layer weights
Hidden_Layer_Bias   = np.matrix([])          # Bias
beta = np.matrix([])                         # Output weights
ErrorPlot = []                               # ErrorPlot


# Set maximum iterations and tolerance
C_max = 20                                          # Maximum candidates
Lambdas = [100, 160, 170, 180, 190, 200]            # Random weight range
R = [0.9, 0.99, 0.999, 0.9999, 0.99999, 0.999999]   # Learning parameters
residual = Ttrain                                   # Residual error
Error = np.sqrt(np.sum(np.square(residual)) / n)    # Current error

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def toExcel(data):
    df = pd.DataFrame(data)
    df.to_excel('./test_excel.xlsx', index=False)

def printSize(data):
    print(data.shape)

# Set random seed
np.random.seed(0)
progress_bar = tqdm(total=300, desc="Progress", unit="iteration")

# Training loop
# while j <= L_max and Error > tol:
cnt = 0
while True:
    progress_bar.update(1)
    Record_weight = np.matrix([])  # Candidate weights satisfying inequality constraint
    Record_bias = np.matrix([])  # Candidate biases satisfying inequality constraint
    Record_xi = np.matrix([])  # Collect different correlation coefficient values xi_j
    I = np.matrix([])  # Save the index of the neuron with the maximum correlation coefficient

    # Iterate over Lambdas
    for lambda_u in Lambdas:
        Candi_wight = lambda_u * (2 * np.random.rand(input_dimension, C_max) - 1)  # Candidate weights, 1*20
        Candi_bias = lambda_u * (2 * np.random.rand(input_dimension, C_max) - 1)  # Candidate biases, 1*20
        Candi_wight = np.matrix(Candi_wight)
        Candi_bias = np.matrix(Candi_bias)
        Curr_node_output = sigmoid(Xtrain @ Candi_wight + Candi_bias)       # Current hidden node output for the given candidate, 800*20

        for learning_rate in R:
            for c in range(C_max):
                hc = Curr_node_output[:, c]      # hc->size = 800*1
                xi = np.zeros((1, output_dimension))
                for i in range(output_dimension):
                    residual_i = residual[:, i]  # eq->size = 800*1
                    xi[i] = ((residual_i.T @ hc) ** 2) / (hc.T @ hc) - (1 - learning_rate) * (residual_i.T @ residual_i)
                sum_xi = np.sum(xi)
                if np.min(xi) > 0:  # if xi>0, we record eligible candidate elements, which are in column c
                    Record_xi = np.concatenate((Record_xi, np.matrix(sum_xi)), axis=1)  # [[]]used to define a 2D array with one row and one column
                    Record_weight = np.concatenate((Record_weight, Candi_wight[:, c]), axis=1)  # axis=1 for concatenating columns
                    Record_bias = np.concatenate((Record_bias, Candi_bias[:, c]), axis=1)

            if Record_xi.shape[1] >= 1:  # break learning_rate loop
                break
        if Record_xi.shape[1] >= 1:  # break lambda_u loop
            break

    if Record_xi.shape[1] >= 1:  # column of Record_xi implies whethere there is eligible w&b
        # Sort in descending order and get the ORIGINAL indices
        sorted_indices = np.argsort(Record_xi, axis=1)[:, ::-1]
        Hidden_Layer_Weight = np.concatenate((Hidden_Layer_Weight, Record_weight[:, sorted_indices[0, 0]]), axis=1)  # Appending the best candidate weight
        Hidden_Layer_Bias = np.concatenate((Hidden_Layer_Bias, Record_bias[:, sorted_indices[0, 0]]), axis=1)  # Appending the best candidate bias
    else:
        continue


    # Calculating the output Hj based on the obtained W, B
    Hj = sigmoid(Xtrain @ Hidden_Layer_Weight + Hidden_Layer_Bias)
    """
    it's worth mention that the dimension of Hj changes with the increase of hidden nodes, when max_L is 100, 
    dimension of Hj changes from 800*1 to 800*100, every column represents the output of 800 input calculated by a hidden node 
    """
    # NJ论文输出，使用Cholesky分解降低运算复杂度
    I1 = np.eye((Hj.T @ Hj).shape[0])  # I1 represents the unit matrix of the same type as (Hj'*Hj)
    C = 0.001
    A = Hj.T @ Hj + I1 / C  # Get A matrix for calculation

    # solve A*beta = b(Hj.T * Ttrain)
    lu, piv = lu_factor(A)
    b = Hj.T * Ttrain
    beta = lu_solve((lu, piv), b)


    # pass w, b, beta, n(SampleSize), loss to Server
    Weight_last_element = Hidden_Layer_Weight[0, -1]
    Bias_last_element   = Hidden_Layer_Bias[0, -1]
    beta_last_element   = beta[-1]

    try:
        client.send_data(Weight_last_element, Bias_last_element, beta_last_element, n, Error)
    except ConnectionError as e:
        print("senddddddddddddddd")
        break


    """
    Server handle new parameters
    """
    update_w = 0.0
    update_b = 0.0
    update_beta = 0.0
    try:
        update_w, update_b, update_beta = client.receive_data()
    except ConnectionError as e:
        print("receiveeeeeeeeeeeeeeee")
        break

    # if update_w == 0 & update_b == 0:
    #     break

    Hidden_Layer_Weight[0, -1] = update_w
    Hidden_Layer_Bias[0, -1]   = update_b
    beta[-1]                   = update_beta


    # use new w, b, beta to firstly update Hj, and secondly calculate residual
    # 这里是不是应该用测试集啊啊啊啊啊啊啊啊
    Hj = sigmoid(Xtest @ Hidden_Layer_Weight + Hidden_Layer_Bias)

    # calculate current output Y
    Y = np.asarray(Hj @ beta)
    residual = Ttest - Y  # New residual error
    Error = np.sqrt(np.sum(np.sum(residual ** 2) / Y.size))  # Calculate new error from residual error
    ErrorPlot.append(Error)  # Append error to the array



last_x = len(ErrorPlot) - 1
last_y = ErrorPlot[-1]
last_y = round(last_y, 6)
plt.scatter(last_x, last_y, color='blue', s=50, label='Last point')  # 标注最后一个数据点
plt.text(last_x, last_y, f'({last_x}, {last_y})', fontsize=10, ha='right', va='bottom')  # 添加文本标签
plt.legend()  # 显示图例

ErrorPlot = np.array(ErrorPlot)
plt.plot(ErrorPlot), plt.xlabel('Iteration'), plt.ylabel('Error'), plt.title('Client1 ErrorTrain Curve'), plt.show()
