import os
import ROOT
from ROOT import *
C=TCanvas("canvas","",0,0,800,800)
#ROOT.gStyle.SetFrameLineWidth(3)
#ROOT.gStyle.SetLineWidth(3)
ROOT.gStyle.SetOptStat(0)

#File= TFile('T1tttt_limit_scan_smooth10_horn_0p1.root','r')
#File= TFile('NewSMOOTH_Feb20/lmit_scan_postCWR_4_B0_0p1_smooth10_cmb.root','r')
#File= TFile('T1tttt_limit_scan_smooth10_B0p1.root','r')
File= TFile('lmit_scan_postCWR_4_B0_0p1_smooth10_cmb.root','r')

H2= File.Get("T1ttttObservedExcludedXsec")
for i in range(H2.GetNbinsX()):
    for j in range (H2.GetNbinsY()):
        if H2.GetBinContent(i,j) > 0 and H2.GetBinContent(i,j) < 1:
            H2.SetBinContent(i,j,.1)
        if H2.GetBinContent(i,j) > 0 and H2.GetBinContent(i,j) > 1:
            H2.SetBinContent(i,j,2)
H2.GetXaxis().SetTitle('m_{LQ} [Gev]')
H2.GetYaxis().SetTitle('m_{DM} [Gev]')
H2.GetYaxis().SetRangeUser(300,800)
H2.GetZaxis().SetTitle(0)
H2.Draw('COLZ')
C.SaveAs('_smooth10_horn_0p1_current.pdf')


#File= TFile('T1tttt_limit_scan_smooth10_B0p5.root','r')
#File= TFile('NewSMOOTH_Feb20/lmit_scan_postCWR_4_B0_0p5_smooth10_cmb.root','r')
#File= TFile('T1tttt_limit_scan_smooth10_horn_0p5.root','r')
File= TFile('lmit_scan_postCWR_4_B0_0p5_smooth10_cmb.root','r')
H2= File.Get("T1ttttObservedExcludedXsec")
for i in range(H2.GetNbinsX()):
    for j in range (H2.GetNbinsY()):
        if H2.GetBinContent(i,j) > 0 and H2.GetBinContent(i,j) < 1:
            H2.SetBinContent(i,j,.1)
        if H2.GetBinContent(i,j) > 0 and H2.GetBinContent(i,j) > 1:
            H2.SetBinContent(i,j,2)
H2.GetXaxis().SetTitle('m_{LQ} [Gev]')
H2.GetYaxis().SetTitle('m_{DM} [Gev]')
H2.GetYaxis().SetRangeUser(300,800)
H2.GetZaxis().SetTitle(0)
H2.Draw('COLZ')
C.SaveAs('_smooth10_horn_0p5_current.pdf')