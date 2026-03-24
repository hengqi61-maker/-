import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline#样条插值
x = np.array([0,1,2,3,4,5])
y = np.array([0,0.8,1.2,1.0,0.5,0])
def linear_interp(x_nodes, y_nodes, x_val):#分段线性插值
    for i in range(len(x_nodes)-1):
        if x_nodes[i] <= x_val <= x_nodes[i+1]:
            x0,x1 = x_nodes[i],x_nodes[i+1]
            y0,y1 = y_nodes[i],y_nodes[i+1]
            return y0 + (y1-y0)*(x_val-x0)/(x1-x0)
x0 = 2.5
#x_plot = np.linspace(-1, 1, 400)
linear_result = linear_interp(x,y,x0)
#y = [linear_interp(x, y, xi) for xi in x_plot]
print("线性插值:",linear_result)
spline = CubicSpline(x,y,bc_type='natural')#直接调用函数库，对已知函数进行拟合得到拟合后的函数
spline_result = spline(x0)#在函数上找点
print("样条插值:",spline_result)
x_plot = np.linspace(0,5,400)
y_linear = [linear_interp(x,y,i) for i in x_plot]
y_spline = spline(x_plot)
plt.figure(figsize=(8,5))
plt.plot(x_plot,y_linear,label="Piecewise Linear")#线性插值
plt.plot(x_plot,y_spline,label="Cubic Spline")#样条插值
plt.scatter(x,y,color="red",label="data points")
plt.legend()
plt.grid()
plt.xlabel("x")
plt.ylabel("y")
plt.title("Interpolation Comparison")
plt.show()
slopes = np.diff(y)/np.diff(x)#线性插值的导数就是点上的导数
print("线性各段导数:",slopes)
spline_derivative = spline.derivative()#调用样条插值函数
print("样条导数在2.5:", spline_derivative(2.5))


