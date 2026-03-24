import numpy as np
import matplotlib.pyplot as plt
def central_diff(x, h):
    return (f(x + h) - f(x - h)) / (2 * h)
def f(x):
    return np.exp(x)
h = np.logspace(-15, 0, 50)

error=[]
error = np.abs(central_diff(1, h) - np.e)

plt.loglog(h, error)
plt.xlabel("h")
plt.ylabel("error")

idx = np.argmin(error)
h_min = h[idx]

plt.scatter(h_min, error[idx], label="actual min")#实际最优步长
h_opt = 1e-5
plt.scatter(h_opt, np.interp(h_opt, h, error), label="theoretical")#理论直接描点
plt.legend()
plt.show()
