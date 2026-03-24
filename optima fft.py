import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, fftshift

# -------------------------
# 1. 参数
# -------------------------
dt = 0.001
t = np.arange(-5, 5, dt)
f0 = 5  # 中心频率

sigma = 0.5   # 高斯宽度
tau = 0.5     # 寿命（洛伦兹）

# -------------------------
# 2. 定义时域信号
# -------------------------
# 高斯包络
E_gauss = np.exp(-t**2/(2*sigma**2)) * np.cos(2*np.pi*f0*t)

# 指数衰减（洛伦兹来源）
E_lorentz = np.exp(-np.abs(t)/(2*tau)) * np.cos(2*np.pi*f0*t)

# 组合信号（Voigt来源）
E_voigt = np.exp(-t**2/(2*sigma**2)) * np.exp(-np.abs(t)/(2*tau)) * np.cos(2*np.pi*f0*t)

# -------------------------
# 3. FFT函数
# -------------------------
def compute_fft(signal):
    F = fft(signal)
    freq = fftfreq(len(signal), dt)
    return fftshift(freq), fftshift(np.abs(F))

freq, G = compute_fft(E_gauss)
_, L = compute_fft(E_lorentz)
_, V = compute_fft(E_voigt)

# 归一化
G /= np.max(G)
L /= np.max(L)
V /= np.max(V)

# -------------------------
# 4. 绘图
# -------------------------
plt.figure(figsize=(12,6))

# 时域
plt.subplot(1,2,1)
plt.plot(t, E_gauss, label="Gaussian (time)")
plt.plot(t, E_lorentz, label="Exponential (time)")
plt.plot(t, E_voigt, label="Product (Voigt source)", linewidth=2)
plt.title("Time Domain")
plt.xlabel("t")
plt.legend()
plt.grid()

# 频域
plt.subplot(1,2,2)
plt.plot(freq, G, label="Gaussian spectrum")
plt.plot(freq, L, label="Lorentzian spectrum")
plt.plot(freq, V, label="Voigt (convolution result)", linewidth=2)
plt.xlim(0, 15)
plt.title("Frequency Domain")
plt.xlabel("Frequency")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
