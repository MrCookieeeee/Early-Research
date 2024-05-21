def cal_weight(temp_arrays):
    n1 = temp_arrays[0][3]
    n2 = temp_arrays[1][3]
    n3 = temp_arrays[2][3]
    loss1 = temp_arrays[0][4]
    loss2 = temp_arrays[1][4]
    loss3 = temp_arrays[2][4]
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
    return theta1, theta2, theta3


temp_arrays = [[] for _ in range(3)]

temp_arrays[0].append(0)
temp_arrays[0].append(0)
temp_arrays[0].append(0)
temp_arrays[0].append(20)
temp_arrays[0].append(0.1)

temp_arrays[1].append(0)
temp_arrays[1].append(0)
temp_arrays[1].append(0)
temp_arrays[1].append(30)
temp_arrays[1].append(0.2)

temp_arrays[2].append(0)
temp_arrays[2].append(0)
temp_arrays[2].append(0)
temp_arrays[2].append(40)
temp_arrays[2].append(0.3)

theta1, theta2, theta3 = cal_weight(temp_arrays)
print(theta1)
print(theta2)
print(theta3)
