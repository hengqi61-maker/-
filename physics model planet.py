import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline#导入使用库
x1 = np.random.uniform(0, 0.5*np.pi, 5)
x2 = np.random.uniform(0.5*np.pi,2*np.pi,5)
x = np.sort(np.concatenate((x1,x2)))#采样点（实际中应该是两个对应的数据都是测量的）


def f(x):
    return (2*(1+0.3*np.cos(x))/(1-0.09)-1)**0.5
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
coef_newton=newton_divided_diff(x,f(x))
x_plot=np.linspace(0,6,100)
y_newton=[newton_interpolation(x, coef_newton, xi) for xi in x_plot]
def df(x):
    h = 1e-5
    return (f(x + h) - f(x - h)) / (2 * h)
y = f(x)
dy = df(x)
def hermite_segment(x0, x1, y0, y1, dy0, dy1, x):
    h = x1 - x0
    t = (x - x0) / h
    h00 = (1 + 2 * t) * (1 - t) ** 2
    h10 = t * (1 - t) ** 2
    h01 = t ** 2 * (3 - 2 * t)
    h11 = t ** 2 * (t - 1)
    return h00 * y0 + h10 * h * dy0 + h01 * y1 + h11 * h * dy1
def piecewise_hermite(x_nodes, y_nodes, dy_nodes, x):
    n = len(x_nodes)
    for i in range(n - 1):
        if x_nodes[i] <= x <= x_nodes[i + 1]:
            return hermite_segment(
                x_nodes[i],
                x_nodes[i + 1],
                y_nodes[i],
                y_nodes[i + 1],
                dy_nodes[i],
                dy_nodes[i + 1],
                x
            )
y_hermite = [piecewise_hermite(x, y, dy, xi) for xi in x_plot]
line = CubicSpline(x,f(x))
y_linear = line(x_plot)
plt.figure(figsize=(8,5))
plt.plot(x_plot,y_newton,label="newton")#newton插值
plt.plot(x_plot,y_hermite,label="Cubic Hermite Interpolation")#分段三次插值
plt.plot(x_plot,y_linear,label="CubicSpline")#样条插值
plt.plot(x_plot,f(x_plot),'--',label="True Function")#原函数
plt.scatter(x,f(x),color="red",label="data points")
plt.legend()
plt.grid()
plt.xlabel("x")
plt.ylabel("y")
plt.title("Interpolation Comparison")
plt.show()
