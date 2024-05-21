import socket
import threading
import pickle
import matplotlib.pyplot as plt
max_Client = 3
sum_n = 2000
reinforce_study = 1

class ClientHandler(threading.Thread):
    def __init__(self, client_socket, client_address):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address

    def run(self):
        print(f"Accepted connection from {self.client_address}")

    def receive_data(self):
        data = self.client_socket.recv(1024)
        w, b, beta, n, loss = pickle.loads(data)
        return w, b, beta, n, loss


    def send_data(self, w, b, beta):
        data = pickle.dumps((w, b, beta))
        self.client_socket.sendall(data)

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.arrays = [[] for _ in range(max_Client)]    # store ultimate weight


    def cal_weight(self, temp_arrays):
        n1 = temp_arrays[0][3]
        n2 = temp_arrays[1][3]
        n3 = temp_arrays[2][3]
        loss1 = temp_arrays[0][4]
        loss2 = temp_arrays[1][4]
        loss3 = temp_arrays[2][4]
        #print(n1, n2, n3, loss1, loss2, loss3)             # n1=400 n3=800
        sum_loss = 1 / loss1 + 1 / loss2 + 1 / loss3
        # 计算归一化后的值
        norm_loss1 = (1 / loss1) / sum_loss
        norm_loss2 = (1 / loss2) / sum_loss
        norm_loss3 = (1 / loss3) / sum_loss

        n1 = n1 * norm_loss1
        n2 = n2 * norm_loss2
        n3 = n3 * norm_loss3

        sum_n = n1 + n2 + n3
        theta1 = n1 / sum_n
        theta2 = n2 / sum_n
        theta3 = n3 / sum_n
        # print(str(theta1) + " " + str(theta2) + " " + str(theta3))
        return theta1, theta2, theta3


    def draw(self):
        for i in range(3):
            plt.plot(self.arrays[i], label=f'Line {i + 1}')  # 给每条曲线设置标签，例如 Line 1, Line 2, Line 3

        # 添加图例
        plt.legend()

        # 添加标题和轴标签
        plt.title('Plot of Arrays')
        plt.xlabel('Index')
        plt.ylabel('Value')

        # 显示图形
        plt.show()


    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        Client_count = 0
        while Client_count < max_Client:
            client_socket, client_address = self.server_socket.accept()
            client_handler = ClientHandler(client_socket, client_address)
            client_handler.start()
            self.clients.append(client_handler)
            Client_count += 1


        print("Connected to all Client, Let's train")
        flag = 1
        times = 1
        Lmax = 300
        Tolerance = 0.01
        while times <= Lmax and flag:
            max_loss = 0
            sum_w = 0
            sum_b = 0
            sum_beta = 0
            temp_arrays = [[] for _ in range(max_Client)]
            for i in range(max_Client):
                w, b, beta, n, loss = self.clients[i].receive_data()
                if reinforce_study == 0:
                    sum_w += n * w / sum_n
                    sum_b += n * b / sum_n
                    sum_beta += n * beta / sum_n
                else:
                    temp_arrays[i].append(w)
                    temp_arrays[i].append(b)
                    temp_arrays[i].append(beta)
                    temp_arrays[i].append(n)
                    temp_arrays[i].append(loss)

                max_loss = max(loss, max_loss)
            if max_loss < Tolerance:
                print("loss is OK so break while-------------------------")
                print(max_loss)
                flag = 0

            if reinforce_study == 0:
                new_w = sum_w
                new_b = sum_b
                new_beta = sum_beta
            else:
                theta1, theta2, theta3 = self.cal_weight(temp_arrays)   # theta1-3 are the ultimate weight
                if times == 1:
                    self.arrays[0].append(theta1*0.1)
                    self.arrays[1].append(theta2*0.1)
                    self.arrays[2].append(theta3*0.1)
                else:
                    tem_theta1 = self.arrays[0][times-2] * theta1*0.1
                    tem_theta2 = self.arrays[1][times-2] * theta2*0.1
                    tem_theta3 = self.arrays[2][times-2] * theta3*0.1
                    sum_theta = tem_theta1 + tem_theta2 + tem_theta3
                    self.arrays[0].append(tem_theta1 / sum_theta)
                    self.arrays[1].append(tem_theta2 / sum_theta)
                    self.arrays[2].append(tem_theta3 / sum_theta)

                w1 = temp_arrays[0][0]
                w2 = temp_arrays[1][0]
                w3 = temp_arrays[2][0]
                b1 = temp_arrays[0][1]
                b2 = temp_arrays[1][1]
                b3 = temp_arrays[2][1]
                beta1 = temp_arrays[0][2]
                beta2 = temp_arrays[1][2]
                beta3 = temp_arrays[2][2]

                theta1 = self.arrays[0][times-1]
                theta2 = self.arrays[1][times-1]
                theta3 = self.arrays[2][times-1]

                # print(theta1, theta2, theta3)

                new_w = w1 * theta1 + w2 * theta2 + w3 * theta3
                new_b = b1 * theta1 + b2 * theta2 + b3 * theta3
                new_beta = beta1 * theta1 + beta2 * theta2 + beta3 * theta3


            for i in range(max_Client):
                self.clients[i].send_data(new_w, new_b, new_beta)

            times += 1

        self.draw()

        # 走出while循环，训练结束
        for i in range(max_Client):
            self.clients[i].send_data(0, 0, 0)


def main():
    server_host = '127.0.0.1'
    server_port = 12345

    server = Server(server_host, server_port)
    server.start()

if __name__ == "__main__":
    main()
