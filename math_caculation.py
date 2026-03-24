import numpy as np
def f(x):
    return np.sin(x)
x_nodes = np.array([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
y_nodes = f(x_nodes)
x = 0.8
def lagrange_interpolation(x_nodes, y_nodes, x):
    n = len(x_nodes)
    result = 0
    for i in range(n):
        term = y_nodes[i]
        for j in range(n):
            if j != i:
                term *= (x - x_nodes[j]) / (x_nodes[i] - x_nodes[j])
        result += term
    return result
def newton_divided_diff(x_nodes, y_nodes):#获取Newton interpolation系数
    n = len(x_nodes)
    coef = np.copy(y_nodes)
    for j in range(1, n):
        coef[j:n] = (coef[j:n] - coef[j-1:n-1]) / (x_nodes[j:n] - x_nodes[0:n-j])
    return coef
def newton_interpolation(x_nodes, coef, x):#构建插值函数
    n = len(coef)
    result = coef[n-1]
    for i in range(n-2, -1, -1):
        result = result * (x - x_nodes[i]) + coef[i]
    return result
lagrange_result = lagrange_interpolation(x_nodes, y_nodes, x)
coef = newton_divided_diff(x_nodes, y_nodes)
newton_result = newton_interpolation(x_nodes, coef, x)
true_value = np.sin(x)
print("Lagrange结果:", lagrange_result)
print("Newton结果:", newton_result)
print("真实值:", true_value)

print("Lagrange误差:", abs(lagrange_result - true_value))
print("Newton误差:", abs(newton_result - true_value))
# 新增节点 π/6
def divided_difference_table(x, y):
    n = len(x)
    # 创建差商表
    table = np.zeros((n, n))
    # 第一列放函数值
    table[:,0] = y
    # 计算差商
    for j in range(1, n):
        for i in range(n-j):
            table[i][j] = (table[i+1][j-1] - table[i][j-1]) / (x[i+j] - x[i])
    return table
table = divided_difference_table(x_nodes, y_nodes)
print("差商表：")
print(table)
x_new = np.append(x_nodes, np.pi/6)
y_new = np.sin(x_new)
coef_new = newton_divided_diff(x_new, y_new)
newton_new_result = newton_interpolation(x_new, coef_new, x)
print("\n新增节点 π/6 后 Newton结果:", newton_new_result)
lagrange_new_result = lagrange_interpolation(x_new, y_new, x)
print("\n新增节点 π/6 后 lagrange结果:", lagrange_new_result)
