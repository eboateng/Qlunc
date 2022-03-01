# -*- coding: utf-8 -*-

"""
Created on Mon Feb 21 08:45:23 2022

@author: fcosta

"""


import numpy as np
import math
import pdb
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import cm
# from Utils import Qlunc_Help_standAlone as SA

GUM    = 1
MC     = 1

#%% Define inputs
Hh          = 125
alpha       = np.array([.001]) # shear exponent
N           = np.round(50000) #number of points for the MC simulation
Vh          = 8.5
rho         = np.linspace(1000,1000,250)
theta       = np.linspace(0,50,250)
psi         = np.linspace(13,13,250)
stdv_rho    = 0/100     #in percentage
stdv_theta  = 0.6/100 #in percentage
stdv_psi    = 0/100     #in percentage
rho_noisy   = []
theta_noisy = []
psi_noisy   = []
for ind_noise in range(len(rho)):
    # rho_noisy.append(np.random.normal(rho[ind_noise],stdv_rho,N))
    # theta_noisy.append(np.random.normal(theta[ind_noise],stdv_theta,N))
    # psi_noisy.append(np.random.normal(psi[ind_noise],stdv_psi,N))
    rho_noisy.append(np.random.normal(rho[ind_noise],stdv_rho*rho[ind_noise],N))
    theta_noisy.append(np.random.normal(theta[ind_noise],stdv_theta*theta[ind_noise],N))
    psi_noisy.append(np.random.normal(psi[ind_noise],stdv_psi*psi[ind_noise],N))

# Weighting fucntion
pulsed     = 1
truncation = 1 # N° of Zr to truncate the WF
tau_meas=265e-9
tau=165e-9
c_l=3e8

# Impulse for the pulse

#%% MONTECARLO METHOD
# Define inputs
if MC==1:

    # Homogeneous flow
    
    # Calculate radial speed
    Vrad_homo = []
    Vrad_homo=([Vh*np.cos(np.radians(theta_noisy[ind_theta]))*np.cos(np.radians(psi_noisy[ind_theta])) for ind_theta in range (len(theta_noisy))])

    # simulation to get reconstructed Vh from the simulated points
    Vh_rec_homo_MC=[]
    for index_vrad in range(len(theta)):      
        Vh_rec_homo_MC.append(Vrad_homo[index_vrad]/(math.cos(np.deg2rad(psi[index_vrad]))*math.cos(np.deg2rad(theta[index_vrad]))))
    
    # Uncertainty
    U_Vh_homo,U_Vrad_homo_MC=[],[]
    # U_Vh_homo.append([np.std(Vh_rec_homo_MC[ind_stdv]) for ind_stdv in range(len(Vh_rec_homo_MC))])
    U_Vrad_homo_MC.append([np.std(Vrad_homo[ind_stdv])  for ind_stdv in range(len(Vrad_homo))])
    
    # Including shear model
    U_Vh_PL,U_Vrad_S_MC=[],[]
    # Calculate the hights
    H0 = [np.multiply(rho[ind_mul],np.sin(np.deg2rad(theta[ind_mul]))) for ind_mul in range(len(theta_noisy)) ] # Original heights
    H  = [np.multiply(rho_noisy[ind_mul],np.sin(np.deg2rad(theta_noisy[ind_mul]))) for ind_mul in range(len(theta_noisy))] # Noisy heights
      
#####################################################
    # Power Law model        
    # Calculate radial speed
    # if pulsed =1:


    # Rayleigh_length = (c_l*tau_meas)/(2*math.erf(np.sqrt(np.log(2))*(tau_meas)/(tau)))/2
    # Trun_val        = truncation* Rayleigh_length
    # offset          = 100

    # rho_lorentz,rho_lorentz1,rho_noisy_lorentz = [],[],[]
    # H_lorentz,H_lorentz_sorted      = [],[]
    # for vec_rho in range(len(rho)):
    #     rho_lorentz.append(np.linspace(rho_noisy[vec_rho]-Trun_val,rho_noisy[vec_rho]+Trun_val,1001))
        
    #     H_lorentz.append(rho_lorentz[vec_rho]*np.sin(np.radians(theta[vec_rho]))) # heights within the probe volume for each noisy point
    #     rho_loren=np.transpose(rho_lorentz)
        
    #     # for vec_rho2 in range(len(rho_lorentz[0])):
    #     #     H_lorentz.append(rho_lorentz[vec_rho][vec_rho2]*np.sin(np.radians(theta[vec_rho]))) # heights within the probe volume for each noisy point
    #     H_lorentz_sorted.append(np.sort(np.transpose(H_lorentz[vec_rho])))
    #     # pdb.set_trace()
    # rho_lorentz=rho_lorentz[0]
    # WeightingFunction=[]
    # offset = 100
    # focus_distance = 0
    # z=np.linspace(-Trun_val,Trun_val,1001)
    
    # for ind_z in z:        
    #     WeightingFunction.append((1/(tau_meas*c_l))*(math.erf((4*np.sqrt(np.log(2))*(ind_z-focus_distance)/((c_l*tau)))+(np.sqrt(np.log(2)))*tau_meas/tau)-math.erf((4*np.sqrt(np.log(2))*(ind_z-focus_distance)/((c_l*tau)))-(np.sqrt(np.log(2)))*tau_meas/tau)))        
###########################################################
    # fig,ax=plt.subplots(), ax.plot(z,WeightingFunction)
    # fig,axs0=plt.subplots(), axs0.hist(WeightingFunction/z)
    Vrad_PL,Vh_rec_shear,Vrad_PL_PB = [],[],[]
    
    for ind_npoints in range(len(rho)):
        Vrad_PL.append (Vh*(np.cos(np.radians(psi_noisy[ind_npoints]))*np.cos(np.radians(theta_noisy[ind_npoints])))*(((Hh+np.sin(np.radians(theta_noisy[ind_npoints]))*rho_noisy[ind_npoints])/Hh)**alpha[0]))

        # for ind_pointsPB in range(len(H_lorentz)):
        #     Vrad_PL_PB.append(Vh*(np.cos(np.radians(psi_noisy[ind_npoints]))*np.cos(np.radians(theta_noisy[ind_npoints])))*(((np.sin(np.radians(theta_noisy[ind_npoints]))*rho_noisy[ind_npoints])/(np.sin(np.radians(theta[ind_npoints]))*rho[ind_npoints]))**alpha[0]))
        #     pdb.set_trace()
        # Vh_rec_shear.append(np.divide(Vrad_PL[ind_npoints],(math.cos(np.deg2rad(theta[ind_npoints])))) )
      
    # Uncertainty
    U_Vrad_S_MC.append([np.nanstd(Vrad_PL[ind_stdv]) for ind_stdv in range(len(Vrad_PL))])           
    # U_Vh_PL.append([np.std(Vh_rec_shear[ind_stdv])*Vh for ind_stdv in range(len(Vh_rec_shear))])
    # g=np.digitize(WeightingFunction,np.linspace(np.min(WeightingFunction),np.max(WeightingFunction),500))

#%% GUM METHOD

if GUM==1:
   
    # Homogeneous flow
    U_Vrad_homo_GUM,U_Vrad_theta,U_Vrad_psi,U_Vh,U_Vrad_range=[],[],[],[],[]
    U_Vrad_theta.append([Vh*np.cos(np.radians(psi[ind_u]))*np.sin(np.radians(theta[ind_u]))*np.radians(stdv_theta*theta[ind_u]) for ind_u in range(len(theta))])
    U_Vrad_psi.append([Vh*np.cos(np.radians(theta[ind_u]))*np.sin(np.radians(psi[ind_u]))*np.radians(stdv_psi*psi[ind_u]) for ind_u in range(len(theta))])   
    U_Vrad_homo_GUM.append([np.sqrt((U_Vrad_theta[0][ind_u])**2+(U_Vrad_psi[0][ind_u])**2) for ind_u in range(len(theta))])
    
    # Including shear:
    U_Vrad_sh_theta,U_Vrad_sh_psi,U_Vh_sh,U_Vrad_S_GUM,U_Vrad_sh_range= [],[],[],[],[]       
    for ind_alpha in range(len(alpha)):
        # U_Vrad_sh_theta.append([Vh*(((np.sin(np.radians(theta_noisy[ind_u]))*rho_noisy[ind_u])/(np.sin(np.radians(theta[ind_u]))*rho[ind_u]))**alpha[ind_alpha])*np.cos(np.radians(psi[ind_u]))*np.cos(np.radians(theta[ind_u]))*np.radians(stdv_theta*theta[ind_u])*abs((alpha[ind_alpha]/math.tan(np.radians(theta[ind_u])))-np.tan(np.radians(theta[ind_u])) ) for ind_u in range(len(theta))])

        U_Vrad_sh_theta.append([Vh*(((Hh+np.sin(np.radians(theta_noisy[ind_u]))*rho_noisy[ind_u])/Hh)**alpha[ind_alpha])*np.cos(np.radians(psi[ind_u]))*np.cos(np.radians(theta[ind_u]))*np.radians(stdv_theta*theta[ind_u])*abs((alpha[ind_alpha]*(rho[ind_u]*np.cos(np.radians(theta[ind_u]))/(Hh+rho[ind_u]*np.sin(np.radians(theta[ind_u])))))-np.tan(np.radians(theta[ind_u])) ) for ind_u in range(len(theta))])
        U_Vrad_sh_psi.append([Vh*(((np.sin(np.radians(theta_noisy[ind_u]))*rho_noisy[ind_u])/(np.sin(np.radians(theta[ind_u]))*rho[ind_u]))**alpha[ind_alpha])*np.cos(np.radians(theta[ind_u]))*np.sin(np.radians(psi[ind_u]))*np.radians(stdv_psi*psi[ind_u]) for ind_u in range(len(psi))])            
        U_Vrad_sh_range.append([Vh*alpha[ind_alpha]*(1/rho[ind_u])*np.cos(np.radians(theta[ind_u]))*np.cos(np.radians(psi[ind_u]))*(stdv_rho*rho[ind_u]) for ind_u in range(len(rho))])
        U_Vrad_S_GUM.append([np.sqrt((np.mean(U_Vrad_sh_theta[ind_alpha][ind_u]))**2+(np.mean(U_Vrad_sh_psi[ind_alpha][ind_u]))**2+(np.mean(U_Vrad_sh_range[ind_alpha][ind_u]))**2) for ind_u in range(len(rho)) ])
            
       
#%% Plot errors
# pdb.set_trace()
if GUM==1 and MC==0:
    # color=iter(cm.rainbow(np.linspace(0,1,len(alpha))))   
    # fig,ax1= plt.subplots()  
    # ax1.plot(theta,U_Vh[0],'b-',label='U Uniform flow GUM')
    # for ind_a in range(len(alpha)):
    #     c=next(color)
    #     ax1.plot(theta,U_Vh_sh[ind_a],'r-.',label='U Shear GUM (\u03B1 = {})'.format(alpha[ind_a]),c=c)
    
    # ax1.set_xlabel('theta [°]',fontsize=25)
    # ax1.set_ylabel('U [%]',fontsize=25)
    
    # plt.title('Uncertainty in horizontal velocity (GUM)',fontsize=29)
    # ax1.legend()
    # ax1.grid(axis='both')
    
    color=iter(cm.rainbow(np.linspace(0,1,len(alpha))))
    fig,ax2 = plt.subplots()  
    ax2.plot(theta,U_Vrad_homo_GUM[0],'b-',label='U Uniform flow GUM')
    for ind_a in range(len(alpha)):
        c=next(color)
        ax2.plot(theta,U_Vrad_S_GUM[ind_a],'r-.',label='U Shear GUM (\u03B1 = {})'.format(alpha[ind_a]),c=c)
    
    ax2.set_xlabel('theta [°]',fontsize=25)
    ax2.set_ylabel('U [%]',fontsize=25)
    plt.title('Uncertainty in radial velocity (GUM)',fontsize=29)
    ax2.legend()
    ax2.grid(axis='both')
elif MC==1 and GUM==0:
    fig,ax1=plt.subplots()
    # for ind_al in range(len(alpha0)):
    # pdb.set_trace()
    # ax1.plot(theta,U_Vh_homo[0],'x-b' ,label='U Uniform flow')
    # ax1.plot(theta,U_Vh_PL[0],'+-r' ,label='U shear')
    # ax1.legend()
    # ax1.set_xlabel('Theta [°]')
    # ax1.set_ylabel('Uncertainty [%]')
    # ax1.grid(axis='both')
    # plt.title('Vh Uncertainty')
    # pdb.set_trace()
    # fig,ax2=plt.subplots()
    # ax2.plot(pointZ,U_Vrad_homo[0],'-b' ,label='U_homo')
    # ax2.plot(pointZ,U_Vrad_PL[0],'-r' ,label='U_shear')
    # ax2.legend()
    # ax2.set_xlabel('Height [m]')
    # ax2.set_ylabel('Uncertainty')
    # ax2.grid(axis='both')
    # plt.title('Vrad Uncertainty')
    
    fig,ax2=plt.subplots()
    ax2.plot(theta,U_Vrad_homo[0],'x-b' ,label='U Uniform flow (MC)')
    ax2.plot(theta,U_Vrad_PL[0],'+-r' ,label='U shear (MC)')
    ax2.legend()
    ax2.set_xlabel('Theta [°]')
    ax2.set_ylabel('Uncertainty [m/s]')
    ax2.grid(axis='both')
    plt.title('Vrad Uncertainty')
if MC==1 and GUM==1:
    # fig,ax1=plt.subplots()
    # color=iter(cm.rainbow(np.linspace(0,1,len(alpha))))   

    # ax1.plot(theta,U_Vh_homo[0],'x-b' ,label='U uniform MC')
    # ax1.plot(theta,U_Vh_PL[0],'+-r' ,label='U shear MC')
    # ax1.plot(theta,U_Vh[0],'b-',label='Uniform flow')
    # for ind_a in range(len(alpha)):
    #     c=next(color)
    #     ax1.plot(theta,U_Vh_sh[ind_a],'r-.',label='U Shear GUM ({})'.format(alpha[ind_a]),c=c)
    
    # ax1.legend()
    # ax1.set_xlabel('Theta [°]')
    # ax1.set_ylabel('Uncertainty [%]')
    # ax1.grid(axis='both')
    # plt.title('Vh Uncertainty')
    # pdb.set_trace()
    # fig,ax2=plt.subplots()
    # ax2.plot(pointZ,U_Vrad_homo[0],'-b' ,label='U_homo')
    # ax2.plot(pointZ,U_Vrad_PL[0],'-r' ,label='U_shear')
    # ax2.legend()
    # ax2.set_xlabel('Height [m]')
    # ax2.set_ylabel('Uncertainty')
    # ax2.grid(axis='both')
    # plt.title('Vrad Uncertainty')
    
    #Plot Uncertainty in Vrad with theta
    fig,ax2=plt.subplots()
    ax2.plot(theta,U_Vrad_homo_GUM[0],'b-',label='U Uniform flow GUM')
    color=iter(cm.rainbow(np.linspace(0,1,len(alpha))))   
    for ind_a in range(len(alpha)):
        c=next(color)
        ax2.plot(theta,U_Vrad_S_GUM[ind_a],'-',label='U Shear GUM  (\u03B1 = {})'.format(alpha[ind_a]),c=c)    
    ax2.plot(theta,U_Vrad_homo_MC[0],'ob' , markerfacecolor=(1, 1, 0, 0.5),label='U uniform MC')
    ax2.plot(theta,U_Vrad_S_MC[0],'or' , markerfacecolor=(1, 1, 0, 0.5),label='U shear MC')
    ax2.legend()
    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    textstr = '\n'.join((
    r'$\rho=%.2f$' % (rho[0], ),
    r'$\psi=%.2f$' % (psi[0], ),
    r'N={}'.format(N, ),
    r'Hh={}'.format(Hh, )))
    
    # place a text box in upper left in axes coords
    ax2.text(0.05, 0.95, textstr, transform=ax2.transAxes, fontsize=14,horizontalalignment='left',verticalalignment='top', bbox=props)
    ax2.set_xlabel('Theta [°]',fontsize=25)
    ax2.set_ylabel('Uncertainty [m/s]',fontsize=25)
    ax2.grid(axis='both')
    plt.title('Vrad Uncertainty',fontsize=30)
    plt.show()


    #Plot Uncertainty in Vrad with psi
    fig,ax3=plt.subplots()
    ax3.plot(psi,U_Vrad_homo_GUM[0],'b-',label='U Uniform flow GUM')
    color=iter(cm.rainbow(np.linspace(0,1,len(alpha))))   
    for ind_a in range(len(alpha)):
        c=next(color)
        ax3.plot(psi,U_Vrad_S_GUM[ind_a],'r-',label='U Shear GUM  (\u03B1 = {})'.format(alpha[ind_a]),c=c)
    ax3.plot(psi,U_Vrad_homo_MC[0],'ob' , markerfacecolor=(1, 1, 0, 0.5),label='U uniform MC')
    ax3.plot(psi,U_Vrad_S_MC[0],'or' , markerfacecolor=(1, 1, 0, 0.5),label='U shear MC')
    ax3.legend()
    ax3.set_xlabel('Psi [°]',fontsize=25)
    ax3.set_ylabel('Uncertainty [m/s]',fontsize=25)
    ax3.grid(axis='both')
    plt.title('Vrad Uncertainty',fontsize=30)
    
    #Plot Uncertainty in Vrad with rho
    fig,ax4=plt.subplots()
    ax4.plot(rho,U_Vrad_homo_GUM[0],'b-',label='U Uniform flow GUM')
    color=iter(cm.rainbow(np.linspace(0,1,len(alpha))))   
    for ind_a in range(len(alpha)):
        c=next(color)
        ax4.plot(rho,U_Vrad_S_GUM[ind_a],'r-',label='U Shear GUM  (\u03B1 = {})'.format(alpha[ind_a]),c=c)
    ax4.plot(rho,U_Vrad_homo_MC[0],'ob' , markerfacecolor=(1, 1, 0, 0.5),label='U uniform MC')
    ax4.plot(rho,U_Vrad_S_MC[0],'or' , markerfacecolor=(1, 1, 0, 0.5),label='U shear MC')
    ax4.legend()
    ax4.set_xlabel('rho [m]',fontsize=25)
    ax4.set_ylabel('Uncertainty [m/s]',fontsize=25)
    ax4.grid(axis='both')
    plt.title('Vrad Uncertainty',fontsize=30)
   
    # Histogram
    # plt.figure()
    # plt.hist(Vrad_PL[0],21)
    # plt.title('Histogram Radial velocity',fontsize=30)
    # plt.xlabel('Vrad [m/s]',fontsize=25)
    # plt.ylabel('Occurrences [-]',fontsize=25)
    
    
    # fig,axs5 = plt.subplots()  
    # axs5=plt.axes(projection='3d')
    # axs5.plot(theta, psi,U_Vrad_S_MC[0])