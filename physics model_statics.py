import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline#导入使用库
x=np.array([0,0.1 ,0.3 ,0.5 ,0.7 ,0.9 ,1.0])#采样点（实际中应该是两个对应的数据都是测量的）
def f(x):
    return 300+50*x+1000/(200*np.pi**2)*np.sin(np.pi*x)


def linear_interp(x_nodes, y_nodes, x_val):#分段线性插值
    for i in range(len(x_nodes)-1):
        if x_nodes[i] <= x_val <= x_nodes[i+1]:
            x0,x1 = x_nodes[i],x_nodes[i+1]
            y0,y1 = y_nodes[i],y_nodes[i+1]
            return y0 + (y1-y0)*(x_val-x0)/(x1-x0)
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
x_plot = np.linspace(0, 1, 100)
def linear_derivative(x_nodes, y_nodes, x_val):#线性插值求导，也就是线性求导
    for i in range(len(x_nodes) - 1):

        if x_nodes[i] <= x_val <= x_nodes[i + 1]:
            return (y_nodes[i + 1] - y_nodes[i]) / (x_nodes[i + 1] - x_nodes[i])
dy_linear=[linear_derivative(x,y,xi) for xi in x_plot]#获取线性插值的导函数

def hermite_derivative(x0, x1, y0, y1, dy0, dy1, x):
    h = x1 - x0
    t = (x - x0) / h
    dh00 = 6 * t * (t - 1)
    dh10 = 1 - 4 * t + 3 * t ** 2
    dh01 = 6 * t * (1 - t)
    dh11 = 3 * t ** 2 - 2 * t
    return (dh00 * y0 + dh10 * h * dy0 + dh01 * y1 + dh11 * h * dy1) / h
def piecewise_hermite_derivative(x_nodes,y_nodes,dy_nodes,x):

    n=len(x_nodes)

    for i in range(n-1):

        if x_nodes[i] <= x <= x_nodes[i+1]:

            return hermite_derivative(
                x_nodes[i],
                x_nodes[i+1],
                y_nodes[i],
                y_nodes[i+1],
                dy_nodes[i],
                dy_nodes[i+1],
                x
            )
dy_hermite=[piecewise_hermite_derivative(x,y,dy,xi) for xi in x_plot]#hermit插值导函数获取

spline = CubicSpline(x,f(x))

dspline = spline.derivative()
dy_spline = dspline(x_plot)

y_linear_interp = [linear_interp(x, y, xi) for xi in x_plot]#线性插值
y_hermite = [piecewise_hermite(x, y, dy, xi) for xi in x_plot]#hermit插值
line = CubicSpline(x,f(x))#样条插值
y_linear = line(x_plot)
plt.figure(figsize=(8,5))
plt.plot(x_plot,y_linear_interp,label="linear_interp")#linear_interp插值
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



dy_linear=[linear_derivative(x,y,xi) for xi in x_plot]

dy_hermite=[piecewise_hermite_derivative(x,y,dy,xi) for xi in x_plot]

dspline=line.derivative()
dy_spline=dspline(x_plot)

plt.figure(figsize=(8,5))

plt.plot(x_plot,dy_linear,label="linear derivative")

plt.plot(x_plot,dy_hermite,label="Hermite derivative")

plt.plot(x_plot,dy_spline,label="Spline derivative")

plt.legend()
plt.grid()
plt.show()
