import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline,PchipInterpolator
from scipy.optimize import root_scalar

# -----------------------------
# 参数
# -----------------------------
n0 = 5e18
a = 0.5
dn = 0.3*n0
ncrit = 1.24e18

# 探测点
r = np.array([0,0.05,0.1,0.15,0.2,0.3,0.4,0.5])

# -----------------------------
# 密度函数
# -----------------------------
def ne(r):
    return n0*(1-(r/a)**2)+dn*np.sin(5*np.pi*r/a)

# 采样数据
y = ne(r)

# -----------------------------
# 分段线性插值
# -----------------------------
def linear_interp(x_nodes,y_nodes,x):

    for i in range(len(x_nodes)-1):

        if x_nodes[i] <= x <= x_nodes[i+1]:

            x0,x1 = x_nodes[i],x_nodes[i+1]
            y0,y1 = y_nodes[i],y_nodes[i+1]

            return y0+(y1-y0)*(x-x0)/(x1-x0)

# -----------------------------
# Hermite插值
# -----------------------------
def numerical_derivative(f,x,h=1e-5):

    return (f(x+h)-f(x-h))/(2*h)

dy = numerical_derivative(ne,r)

def hermite_segment(x0,x1,y0,y1,dy0,dy1,x):

    h=x1-x0
    t=(x-x0)/h

    h00=(1+2*t)*(1-t)**2
    h10=t*(1-t)**2
    h01=t**2*(3-2*t)
    h11=t**2*(t-1)

    return h00*y0+h10*h*dy0+h01*y1+h11*h*dy1

def hermite_interp(x_nodes,y_nodes,dy_nodes,x):

    for i in range(len(x_nodes)-1):

        if x_nodes[i] <= x <= x_nodes[i+1]:

            return hermite_segment(
                x_nodes[i],
                x_nodes[i+1],
                y_nodes[i],
                y_nodes[i+1],
                dy_nodes[i],
                dy_nodes[i+1],
                x
            )

# -----------------------------
# 三次样条
# -----------------------------
spline = CubicSpline(r,y)

# -----------------------------
# 绘图
# -----------------------------
r_plot = np.linspace(0,a,400)

y_true = ne(r_plot)
y_linear = [linear_interp(r,y,x) for x in r_plot]
y_hermite = [hermite_interp(r,y,dy,x) for x in r_plot]
y_spline = spline(r_plot)

plt.figure(figsize=(8,5))

plt.plot(r_plot,y_true,'--',label="True function")
plt.plot(r_plot,y_linear,label="Linear")
plt.plot(r_plot,y_hermite,label="Hermite")
plt.plot(r_plot,y_spline,label="Cubic Spline")

plt.scatter(r,y,color='red',label="data")

plt.axhline(ncrit,color='k',linestyle=':')

plt.xlabel("r")
plt.ylabel("n_e(r)")
plt.legend()
plt.grid()
plt.show()

# -----------------------------
# 截止层求解
# -----------------------------
def f_linear(x):
    return linear_interp(r,y,x)-ncrit

def f_hermite(x):
    return hermite_interp(r,y,dy,x)-ncrit

def f_spline(x):
    return spline(x)-ncrit

root_linear = root_scalar(f_linear,bracket=[0,a]).root
root_hermite = root_scalar(f_hermite,bracket=[0,a]).root
root_spline = root_scalar(f_spline,bracket=[0,a]).root

print("Linear cutoff r =",root_linear)
print("Hermite cutoff r =",root_hermite)
print("Spline cutoff r =",root_spline)
