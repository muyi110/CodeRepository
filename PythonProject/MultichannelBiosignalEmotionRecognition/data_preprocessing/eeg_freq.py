import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

a = np.loadtxt("../data_analysis/samples/s06/trial_9.csv", delimiter=',', skiprows=0, dtype=np.float32)
a_eeg = a[0,128*3:128*5]
a_eeg_fft = np.fft.fft(a_eeg) # 整体 FFT 变化
x = np.linspace(0, 128//2, 2*128//2)

b_theta, a_theta = signal.butter(6, [0.0625, 0.109375], "bandpass") # 4-7Hz
b_alpha, a_alpha = signal.butter(6, [0.125, 0.203125], "bandpass") # 8-13Hz
b_beta, a_beta = signal.butter(6, [0.21875, 0.46875], "bandpass") # 14-30Hz
b_gamma, a_gamma = signal.butter(6, 0.484375, "highpass") # 31-50Hz

theta = signal.filtfilt(b_theta, a_theta, a_eeg)
alpha = signal.filtfilt(b_alpha, a_alpha, a_eeg)
beta = signal.filtfilt(b_beta, a_beta, a_eeg)
gamma = signal.filtfilt(b_gamma, a_gamma, a_eeg)

theta_fft = np.fft.fft(theta)
alpha_fft = np.fft.fft(alpha)
beta_fft = np.fft.fft(beta)
gamma_fft = np.fft.fft(gamma)

finall = theta+alpha+beta+gamma
finall_fft = np.fft.fft(finall)

plt.subplot(231)
plt.plot(x, np.abs(a_eeg_fft[:1*128]))
plt.grid()
plt.subplot(232)
plt.plot(x, np.abs(theta_fft[:1*128]))
plt.grid()
plt.title("theta")
plt.subplot(233)
plt.plot(x, np.abs(alpha_fft[:1*128]))
plt.grid()
plt.title("alpha")
plt.subplot(234)
plt.plot(x, np.abs(beta_fft[:1*128]))
plt.grid()
plt.title("beta")
plt.subplot(235)
plt.plot(x, np.abs(gamma_fft[:1*128]))
plt.grid()
plt.title("gamma")
plt.subplot(236)
plt.plot(x, np.abs(finall_fft[:1*128]))
plt.grid()
plt.show()
