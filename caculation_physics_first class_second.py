import numpy as np
import matplotlib.pyplot as plt
def f(x):
    return 1/(1+25*x**2)
n=20
i=np.linspace(0, n, n)
x_i = x_i = np.cos((2*i + 1) / (2*n + 2) * np.pi)
y_i=f(x_i)
x_nodes = np.linspace(-1, 1, n)
y_nodes = f(x_nodes)
def lagrange_interpolation(x_nodes, y_nodes, x):#拉格朗日插值函数
    n = len(x_nodes)
    result = 0
    for i in range(n):
        term = y_nodes[i]
        for j in range(n):
            if j != i:
                term *= (x - x_nodes[j]) / (x_nodes[i] - x_nodes[j])
        result += term
    return result
x_plot = np.linspace(-1, 1, 400)#绘图点
y_true = f(x_plot)
y_lagrange = [lagrange_interpolation(x_nodes, y_nodes, xi) for xi in x_plot]#插值得到的函数的函数值
import sympy as sp
x_sym = sp.symbols('x')
def get_lagrange_expr(x_nodes, y_nodes):#把插值得到的函数以数学多项式形式展开
    n = len(x_nodes)
    poly = 0
    for i in range(n):
        # 构建基函数 L_i(x)
        term = y_nodes[i]
        for j in range(n):
            if j != i:
                term *= (x_sym - x_nodes[j]) / (x_nodes[i] - x_nodes[j])
        poly += term
    return sp.expand(poly) # 展开多项式
equation = get_lagrange_expr(x_nodes, y_nodes)
print("插值多项式方程为：")
sp.pprint(equation)
plt.figure(figsize=(8,5))#下面纯画图
plt.subplot(1, 2, 1)
plt.plot(x_plot, y_true, label="Original function")
plt.plot(x_plot, y_lagrange, "--", label="Lagrange interpolation")

plt.title("Lagrange Interpolation of Runge Function")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
y_true_new = f(x_plot)
y_lagrange_new = [lagrange_interpolation(x_i, y_i, xi) for xi in x_plot]
plt.subplot(1, 2, 2)
plt.plot(x_plot, y_lagrange_new, "--", label="Lagrange interpolation_chebyshev")
plt.plot(x_plot,y_true_new,color="green",label="true line_2")
plt.legend()
plt.grid(True)
plt.show()
# 将列表转换为 numpy 数组以便进行减法运算
y_lagrange_arr = np.array(y_lagrange)
y_lagrange_new_arr = np.array(y_lagrange_new)

# 计算绝对误差
error_equidistant = np.abs(y_true - y_lagrange_arr)
error_chebyshev = np.abs(y_true - y_lagrange_new_arr)

# 获取最大误差
max_err_eq = np.max(error_equidistant)
max_err_cheb = np.max(error_chebyshev)

print("-" * 30)
print(f"等距节点插值 (n={n}) 的最大误差: {max_err_eq:.6e}")
print(f"Chebyshev 节点插值 (n={n}) 的最大误差: {max_err_cheb:.6e}")
print("-" * 30)