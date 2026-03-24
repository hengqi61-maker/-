import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import CubicSpline#导入使用库
def f(x):
    return 100/(1+((x-500)/5)**2)
x = np.linspace(480,520,11)#采样离散点
y = f(x)
line = CubicSpline(x,y)
x_plot = np.linspace(450,550,200)
y_linear = line(x_plot)
plt.plot(x_plot,y_linear,label="nihe")
plt.plot(x_plot,f(x_plot),label="f(x)")
plt.scatter(x,y,color="red",label="data points")
plt.legend()
plt.grid()
plt.show()
d_spline = line.derivative()
point=d_spline.roots()
print("导数为0的位置",point)

