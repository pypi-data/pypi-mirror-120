import punpy
import numpy as np
import matplotlib.pyplot as plt

# your measurement function
def calibrate(L0,gains,dark):
   return (L0-dark)*gains

def make_plots_L1(L1,L1_ur=None,L1_us=None,L1_ut=None,L1_corr=None):
  if L1_corr is not None:
    fig,(ax1,ax2) = plt.subplots(1,2,figsize=(10,5))
  else:
    fig,ax1 = plt.subplots(1,figsize=(5,5))

  ax1.plot(wavs,L1,"o")
  if L1_ur is not None:
    ax1.errorbar(wavs,L1,yerr=L1_ur,label="random uncertainty",capsize=5)
  if L1_us is not None:
    ax1.errorbar(wavs,L1,yerr=L1_us,label="systematic uncertainty",capsize=5)
  if L1_ut is not None:
    ax1.errorbar(wavs,L1,yerr=L1_ut,label="total uncertainty",capsize=5)
  ax1.legend()
  ax1.set_xlabel("wavelength (nm)")
  ax1.set_ylabel("radiance")
  ax1.set_title("L1 uncertainties")
  if L1_corr is not None:
    ax2.set_title("L1 correlation")
    cov_plot=ax2.imshow(L1_corr)
    plt.colorbar(cov_plot,ax=ax2)
  plt.show()

# your data
wavs = np.array([350,450,550,650,750])
L0 = np.array([0.43,0.8,0.7,0.65,0.9])
dark = np.array([0.05,0.03,0.04,0.05,0.06])
gains = np.array([23,26,28,29,31])

# your uncertainties
L0_ur = L0*0.05  # 5% random uncertainty
L0_us = np.ones(5)*0.03  # systematic uncertainty of 0.03
                         # (common between bands)
gains_ur = np.array([0.5,0.7,0.6,0.4,0.1])  # random uncertainty
gains_us = np.array([0.1,0.2,0.1,0.4,0.3])  # systematic uncertainty
# (different for each band but fully correlated)
dark_ur = np.array([0.01,0.002,0.006,0.002,0.015])  # random uncertainty

prop=punpy.MCPropagation(10000)
L1=calibrate(L0,gains,dark)

corr_var=np.array([[1,0,1],[0,1,0],[1,0,1]])



# prop=punpy.MCPropagation(10000)
# L1=calibrate(L0,gains,dark)
# L1_ur=prop.propagate_random(calibrate,[L0,gains,dark],
#       [L0_ur,gains_ur,dark_ur])
# L1_us=prop.propagate_systematic(calibrate,[L0,gains,dark],
#       [L0_us,gains_us,np.zeros(5)])
# L1_ut=(L1_ur**2+L1_us**2)**0.5
# L1_cov=punpy.convert_corr_to_cov(np.eye(len(L1_ur)),L1_ur)+\
#        punpy.convert_corr_to_cov(np.ones((len(L1_us),len(L1_us))),L1_ur)
#
# print("L1:    ",L1)
# print("L1_ur: ",L1_ur)
# print("L1_us: ",L1_us)
# print("L1_ut: ",L1_ut)
# print("L1_cov:\n",L1_cov)

# your data
wavs = np.array([350,450,550,650,750])

L0 = np.tile([0.43,0.8,0.7,0.65,0.9],(50,100,1)).T
#L0 = L0 + 0.01*np.random.normal(0.0,0.05,L0.shape)

dark = np.tile([0.05,0.03,0.04,0.05,0.06],(50,100,1)).T
gains = np.tile([23,26,28,29,31],(50,100,1)).T

# your uncertainties
L0_ur = L0*0.05  # 5% random uncertainty
L0_us = np.ones((5,100,50))*0.03  # systematic uncertainty of 0.03
                         # (common between bands)

gains_ur = np.tile(np.array([0.5,0.7,0.6,0.4,0.1]),(50,100,1)).T  # random uncertainty
gains_us = np.tile(np.array([0.1,0.2,0.1,0.4,0.3]),(50,100,1)).T  # systematic uncertainty
# (different for each band but fully correlated)
dark_ur = np.tile(np.array([0.01,0.002,0.006,0.002,0.015]),(50,100,1)).T  # random uncertainty

prop=punpy.MCPropagation(1000,)
# L1=calibrate(L0,gains,dark)
# # L1_ur=prop.propagate_random(calibrate,[L0,gains,dark],
# #        [L0_ur,gains_ur,dark_ur],repeat_dims=[1])
# L1_us=prop.propagate_systematic(calibrate,[L0,gains,dark],
#       [L0_us,gains_us,None],repeat_dims=[1])
# # L1_ut=(L1_ur**2+L1_us**2)**0.5
#
#
# def make_plots_L1_image(wavs,L1,L1_u=None,c_range=[0,0.1]):
#     fig,axs = plt.subplots(1,len(wavs),figsize=(20,5))
#
#     for i,ax in enumerate(axs):
#         ax.set_xlabel("x_pix")
#         ax.set_ylabel("y_pix")
#         ax.set_title("%s nm uncertainties"%(wavs[i]))
#         im_plot = ax.imshow(L1_u[i]/L1[i],vmin=c_range[0],vmax=c_range[1])
#
#     plt.colorbar(im_plot)
#     plt.show()
#
# make_plots_L1_image(wavs,L1,L1_us)

L1_us=prop.propagate_systematic(calibrate,[L0,gains,dark],
      [L0_us,None,None],corr_between=corr_var)
print(L1_us)
L1_ut=prop.propagate_systematic(calibrate,[L0,gains,dark],
      [L0_us,gains_us,L0_us])
L1_ur=prop.propagate_systematic(calibrate,[L0,gains,dark],
      [None,gains_us,None],corr_between=corr_var)
# L1_ut=(L1_ur**2+L1_us**2)**0.5
# L1_cov=punpy.convert_corr_to_cov(np.eye(len(L1_ur)),L1_ur)+\
#        punpy.convert_corr_to_cov(np.ones((len(L1_us),len(L1_us))),L1_us)
# L1_corr=punpy.correlation_from_covariance(L1_cov)
make_plots_L1(L1,L1_ur,L1_us,L1_ut)
