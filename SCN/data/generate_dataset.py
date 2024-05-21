import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

def generate_dataset1():
    # Generating training data
    num1 = 800
    Xtrain = np.random.rand(num1, 1)
    Ttrain = 0.2 * np.exp(-(10 * Xtrain - 4) ** 2) + 0.5 * np.exp(-(80 * Xtrain - 40) ** 2) + 0.3 * np.exp(
        -(80 * Xtrain - 20) ** 2)

    # Generating test data
    Xtest = np.linspace(0, 1, num1).reshape(-1, 1)
    Ttest = 0.2 * np.exp(-(10 * Xtest - 4) ** 2) + 0.5 * np.exp(-(80 * Xtest - 40) ** 2) + 0.3 * np.exp(
        -(80 * Xtest - 20) ** 2)

    # Plotting the test data
    plt.plot(Ttest)
    # plt.plot(Ttrain)
    plt.show()

    # Saving the dataset
    np.savez("./dataset1.npz", Xtrain=Xtrain, Ttrain=Ttrain, Xtest=Xtest, Ttest=Ttest)


def generate_dataset2():
    # Generating training data
    num2 = 600
    Xtrain = np.random.rand(num2, 1)
    Ttrain = 0.2 * np.exp(-(10 * Xtrain - 4) ** 2) + 0.5 * np.exp(-(80 * Xtrain - 40) ** 2) + 0.3 * np.exp(
        -(80 * Xtrain - 20) ** 2)

    # 添加错误点
    num_errors = 200
    error_indices = np.random.choice(num2, num_errors, replace=False)      # 随机选择200个索引
    error_magnitude = np.random.uniform(-10, 10, (num_errors,1))         # 在指定范围内生成随机数作为错误幅度
    Ttrain[error_indices] += error_magnitude                               # 在选定的索引处添加错误

    # print(Ttrain[error_indices].shape)   200x1
    # print(error_magnitude.shape)         200x1



    # noise_level = 1.9  # 噪声水平
    # Ttrain = Ttrain + np.random.normal(0, noise_level, Ttrain.shape)

    # Generating test data
    Xtest = np.linspace(0, 1, num2).reshape(-1, 1)
    Ttest = 0.2 * np.exp(-(10 * Xtest - 4) ** 2) + 0.5 * np.exp(-(80 * Xtest - 40) ** 2) + 0.3 * np.exp(
        -(80 * Xtest - 20) ** 2)

    # Plotting the test data
    plt.plot(Ttrain)
    plt.show()

    # Saving the dataset
    np.savez("./dataset2.npz", Xtrain=Xtrain, Ttrain=Ttrain, Xtest=Xtest, Ttest=Ttest)


def generate_dataset3():
    # Generating training data
    num3 = 600
    Xtrain = np.random.rand(num3, 1)
    Ttrain = 0.2 * np.exp(-(10 * Xtrain - 4) ** 2) + 0.5 * np.exp(-(80 * Xtrain - 40) ** 2) + 0.3 * np.exp(
        -(80 * Xtrain - 20) ** 2)

    # 添加错误点
    num_errors = 100
    error_indices = np.random.choice(num3, num_errors, replace=False)  # 随机选择200个索引
    error_magnitude = np.random.uniform(-10, 10, (num_errors, 1))  # 在指定范围内生成随机数作为错误幅度
    Ttrain[error_indices] += error_magnitude  # 在选定的索引处添加错误

    # noise_level = 0.99  # 噪声水平
    # Ttrain = Ttrain + np.random.normal(0, noise_level, Ttrain.shape)

    # Generating test data
    Xtest = np.linspace(0, 1, num3).reshape(-1, 1)
    Ttest = 0.2 * np.exp(-(10 * Xtest - 4) ** 2) + 0.5 * np.exp(-(80 * Xtest - 40) ** 2) + 0.3 * np.exp(
        -(80 * Xtest - 20) ** 2)

    # Plotting the test data
    plt.plot(Ttrain)
    plt.show()

    # Saving the dataset
    np.savez("./dataset3.npz", Xtrain=Xtrain, Ttrain=Ttrain, Xtest=Xtest, Ttest=Ttest)


def generate_dataset_all():
    # Generating training data
    num1 = 800
    Xtrain = np.random.rand(num1, 1)
    Ttrain = 0.2 * np.exp(-(10 * Xtrain - 4) ** 2) + 0.5 * np.exp(-(80 * Xtrain - 40) ** 2) + 0.3 * np.exp(
        -(80 * Xtrain - 20) ** 2)

    # Generating test data
    Xtest = np.linspace(0, 1, num1).reshape(-1, 1)
    Ttest = 0.2 * np.exp(-(10 * Xtest - 4) ** 2) + 0.5 * np.exp(-(80 * Xtest - 40) ** 2) + 0.3 * np.exp(
        -(80 * Xtest - 20) ** 2)


    # 产生第二组数据
    num2 = 600
    Xtrain_2 = Xtrain[:num2]
    Ttrain_2 = Ttrain[:num2]

    num_errors_2 = 50
    error_indices = np.random.choice(num2, num_errors_2, replace=False)  # 随机选择200个索引
    error_magnitude = np.random.uniform(-10, 10, (num_errors_2, 1))      # 在指定范围内生成随机数作为错误幅度
    Ttrain_2[error_indices] += error_magnitude                           # 在选定的索引处添加错误

    Xtest_2 = Xtest[:num2]
    Ttest_2 = Ttest[:num2]


    # 产生第三组数据
    num3 = 600
    Xtrain_3 = Xtrain[:num3]
    Ttrain_3 = Ttrain[:num3]
    num_errors_3 = 100
    error_indices = np.random.choice(num3, num_errors_3, replace=False)  # 随机选择200个索引
    error_magnitude = np.random.uniform(-10, 10, (num_errors_3, 1))      # 在指定范围内生成随机数作为错误幅度
    Ttrain_3[error_indices] += error_magnitude                           # 在选定的索引处添加错误

    Xtest_3 = Xtest[:num3]
    Ttest_3 = Ttest[:num3]

    # plt.plot(Ttest)
    # plt.plot(Ttrain)
    # plt.show()

    # Saving the dataset
    np.savez("./dataset1.npz", Xtrain=Xtrain, Ttrain=Ttrain, Xtest=Xtest, Ttest=Ttest)
    np.savez("./dataset2.npz", Xtrain=Xtrain_2, Ttrain=Ttrain_2, Xtest=Xtest_2, Ttest=Ttest_2)
    np.savez("./dataset2.npz", Xtrain=Xtrain_3, Ttrain=Ttrain_3, Xtest=Xtest_3, Ttest=Ttest_3)


#generate_dataset1()
#generate_dataset2()
#generate_dataset3()
generate_dataset_all()



