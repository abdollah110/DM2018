import os
import ROOT
from ROOT import *

file=TFile('mumujj_betaVsMass.root','r')
Plot_LQ2_observed= file.Get('beta_vs_m_lljj_observed')


x = Plot_LQ2_observed.GetX()
y = Plot_LQ2_observed.GetY()


for i in range (0,200):
    print i, x[i], y[i]


