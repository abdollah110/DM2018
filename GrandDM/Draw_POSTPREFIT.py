#!/usr/bin/env python
import ROOT
import re
from array import array
import ROOT as rt

def add_lumi():
    lowX=0.67
    lowY=0.82
    lumi  = ROOT.TPaveText(lowX, lowY+0.04, lowX+0.30, lowY+0.14, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.06)
    lumi.SetTextFont (   42 )
#    lumi.AddText("41.5 fb^{-1} (13 TeV)")
    lumi.AddText("77.4 fb^{-1} (13 TeV)")
    return lumi

def add_CMS():
    lowX=0.21
    lowY=0.70
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(61)
    lumi.SetTextSize(0.08)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("CMS")
    return lumi

def add_Preliminary():
    lowX=0.21
    lowY=0.63
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(52)
    lumi.SetTextSize(0.06)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("Preliminary")
    return lumi

def make_legend():
    output = ROOT.TLegend(0.38, 0.5, 0.92, 0.85, "", "brNDC")
    output.SetLineWidth(0)
    output.SetLineStyle(0)
    output.SetFillStyle(0)
    output.SetBorderSize(0)
    output.SetTextFont(62)
    output.SetNColumns(2)
    
    return output

#["postfit_shapes.root","Codex__mj_1_13TeV_prefit","#it{M}_{LQ} [GeV]","#mu j ",2000,"Codex_","RH W 3TeV",100],
def MakePlot(FileName,categoriy,HistName,Xaxis,MaxRange,sig,sigLeg,sigLeg2,XSection, Status):
    ROOT.gStyle.SetFrameLineWidth(3)
    ROOT.gStyle.SetLineWidth(3)
    ROOT.gStyle.SetOptStat(0)
#    ROOT.gStyle.SetErrorX(0.0001);
    RB_=1

    c=ROOT.TCanvas("canvas","",0,0,600,600)
    c.cd()

    file=ROOT.TFile(FileName,"r")

    adapt=ROOT.gROOT.GetColor(12)
    new_idx=ROOT.gROOT.GetListOfColors().GetSize() + 1
#    trans=ROOT.TColor(new_idx, adapt.GetRed(), adapt.GetGreen(),adapt.GetBlue(), "",0.5)

#    categories=["MuTau_DiJet","MuTau_JetBJet"]
#    ncat=

    Data=file.Get(categoriy).Get("data_obs")
    Data.Rebin(RB_)
    
    ## print Data table for HEPDATA EXO-17-015
    for bin in range(Data.GetNbinsX()):

        xbin= bin+1
        LowEdge=int(Data.GetBinLowEdge(xbin))
        endEdge=int(Data.GetBinLowEdge(xbin)+Data.GetBinWidth(xbin))
        data_val= int(round(file.Get(categoriy).Get("data_obs").GetBinContent(xbin)))
        bkg_val=file.Get(categoriy).Get("TotalBkg").GetBinContent(xbin)
        bkg_val_err=file.Get(categoriy).Get("TotalBkg").GetBinError(xbin)
        Signal_val=file.Get(categoriy.replace('postfit','prefit')).Get(sig)
#        Signal_val.Scale( 1.391115 * 2)  # CS x BR  1000_400_440  // factor of 2 is added as we consider the full doublet
        Signal_val_=Signal_val.GetBinContent(xbin)*1.391115 * 2
        print "[(%d, %d), %d, (%0.1f,    %0.1f),%0.1f],"%(LowEdge,endEdge,data_val,bkg_val,bkg_val_err,Signal_val_)
    
    
    QCD=file.Get(categoriy).Get("QCD")
    QCD.Rebin(RB_)

    W=file.Get(categoriy).Get("W")
    W.Rebin(RB_)

    TT=file.Get(categoriy).Get("TT")
    TT.Rebin(RB_)

    SingleT=file.Get(categoriy).Get("SingleTop")
    SingleT.Rebin(RB_)
    
    VV=file.Get(categoriy).Get("VV")
    VV.Rebin(RB_)

    DYS=file.Get(categoriy).Get("ZTT")
    DYS.Rebin(RB_)

    Signal=file.Get(categoriy.replace('postfit','prefit')).Get(sig)
    Signal.Scale( 1.391115 * 2)  # CS x BR  1000_400_440  // factor of 2 is added as we consider the full doublet 
    Signal.Rebin(RB_)
    #    Signal.SetFillStyle(0.)
    Signal.SetLineStyle(11)
    Signal.SetLineWidth(3)
    Signal.SetLineColor(4)
    Signal.SetMarkerColor(4)
    Signal.SetLineStyle(8)

#    Signal.SetLineColor(ROOT.TColor.GetColor(108, 226, 354))
#    Signal.SetMarkerColor(ROOT.TColor.GetColor(108, 226, 354))
    #    Signal.SetLineColor(kBlue)
    


#    ##### Garwood Method to assign error bar to bins with zero content https://twiki.cern.ch/twiki/bin/view/CMS/PoissonErrorBars
#    ALLSample=[Data]
#    for sample in ALLSample:
#        for ibin in range(sample.GetXaxis().GetNbins()):
#            if sample.GetBinContent(ibin)==0:
#                #                sample.SetBinErrorUp(ibin, 1.8)
#                sample.SetBinErrorOption(rt.TH1.kPoisson)
##                sample.GetBinError(ibin,1.8)
#                print "sample.GetBinErrorLow( ",ibin," )", sample.GetBinErrorLow(ibin)
#                print "sample.GetBinErrorUp( ",ibin," )", sample.GetBinErrorUp(ibin)


##### chnage binning content
    ALLSample=[Data,QCD,W,TT,SingleT,Signal,VV,DYS]
    for sample in ALLSample:
        for ibin in range(sample.GetXaxis().GetNbins()):
#            print ibin+1, sample.GetBinWidth(ibin+1)

            sample.SetBinContent(ibin+1,1.0*sample.GetBinContent(ibin+1)/sample.GetBinWidth(ibin+1))
            sample.SetBinError(ibin+1,1.0*sample.GetBinError(ibin+1)/sample.GetBinWidth(ibin+1))

            if sample==Data and sample.GetBinContent(ibin+1)==0: #https://twiki.cern.ch/twiki/bin/view/CMS/PoissonErrorBars
                sample.SetBinError(ibin+1,1.0*1.8/sample.GetBinWidth(ibin+1))
    

    

    Data.GetXaxis().SetTitle("")
    Data.GetXaxis().SetTitleSize(0)
    Data.GetXaxis().SetNdivisions(505)
    Data.GetYaxis().SetLabelFont(42)
    Data.GetYaxis().SetLabelOffset(0.01)
    Data.GetYaxis().SetLabelSize(0.06)
    Data.GetYaxis().SetTitleSize(0.075)
    Data.GetYaxis().SetTitleOffset(1.04)
    Data.SetTitle("")
    Data.GetYaxis().SetTitle("Events / GeV")



    QCD.SetFillColor(ROOT.TColor.GetColor(408, 106, 154))
    W.SetFillColor(ROOT.TColor.GetColor(200, 2, 285))
    TT.SetFillColor(ROOT.TColor.GetColor(208, 376, 124))
    SingleT.SetFillColor(ROOT.TColor.GetColor(150, 132, 232))
    VV.SetFillColor(ROOT.TColor.GetColor(200, 282, 232))
    DYS.SetFillColor(ROOT.TColor.GetColor(108, 226, 354))


#    for i in range(Data.GetNbinsX()):
#        if i > 8 : Data.SetBinContent(i+1,0)
#        if i > 8 : Data.SetBinError(i+1,0)


    ######  Add OverFlow Bin
#    QCD.SetBinContent(18,QCD.Integral(18,20))
#    W.SetBinContent(18,W.Integral(18,20))
#    TT.SetBinContent(18,TT.Integral(18,20))
#    SingleT.SetBinContent(18,SingleT.Integral(18,20))
#    VV.SetBinContent(18,VV.Integral(18,20))
#    DYS.SetBinContent(18,DYS.Integral(18,20))
#    Data.SetBinContent(18,Data.Integral(18,20))
#    Signal.SetBinContent(18,Signal.Integral(18,20))




    Data.SetMarkerStyle(20)
    Data.SetMarkerSize(1)
    QCD.SetLineColor(ROOT.kBlack)
    W.SetLineColor(ROOT.kBlack)
    TT.SetLineColor(ROOT.kBlack)
    DYS.SetLineColor(ROOT.kBlack)
    VV.SetLineColor(ROOT.kBlack)
    SingleT.SetLineColor(ROOT.kBlack)
    Data.SetLineColor(ROOT.kBlack)
    Data.SetLineWidth(2)

    stack=ROOT.THStack("stack","stack")
    

    stack.Add(VV)
    stack.Add(DYS)
    stack.Add(QCD)
    stack.Add(SingleT)
    stack.Add(TT)
    stack.Add(W)
#    stack.Add(Signal)

    errorBand = QCD.Clone()
    errorBand.Add(W)
    errorBand.Add(TT)
    errorBand.Add(VV)
    errorBand.Add(SingleT)
    errorBand.Add(DYS)
    errorBand.SetMarkerSize(0)
    errorBand.SetFillColor(16)
    errorBand.SetFillStyle(3001)
    errorBand.SetLineWidth(1)

    pad1 = ROOT.TPad("pad1","pad1",0,0.35,1,1)
    
    pad1.Draw()
    pad1.cd()
#    if Status == "LOG" : pad1.SetLogy() ; pad1.SetLogx()
    if Status == "LOG" : pad1.SetLogy()
    
    pad1.SetFillColor(0)
    pad1.SetBorderMode(0)
    pad1.SetBorderSize(10)
    pad1.SetTickx(1)
    pad1.SetTicky(1)
    pad1.SetLeftMargin(0.18)
    pad1.SetRightMargin(0.05)
    pad1.SetTopMargin(0.122)
    pad1.SetBottomMargin(0.026)
    pad1.SetFrameFillStyle(0)
    pad1.SetFrameLineStyle(0)
    pad1.SetFrameLineWidth(3)
    pad1.SetFrameBorderMode(0)
    pad1.SetFrameBorderSize(10)

    Data.GetXaxis().SetLabelSize(0)
    
    if Status == "LOG" :Data.SetMaximum(Data.GetMaximum()*2000); Data.SetMinimum(0.001)
#    if Status == "LOG" :Data.SetMaximum(999); Data.SetMinimum(0.01)
    if Status=="Normal": Data.SetMaximum(Data.GetMaximum()*2) ;  Data.SetMinimum(0)


    Data.GetXaxis().SetRangeUser(0,MaxRange)
    
    Data.SetBinErrorOption(rt.TH1.kPoisson)
    Data.Draw("ex0")
    stack.Draw("histsame")
    errorBand.Draw("e2same")
    Data.Draw("ex0same")
    Signal.Draw("histsame")
#    Signal.Draw("histsame")



########################################################
#Adding Extra signal
    Signal2=Signal.Clone()
    Signal2.Scale(2.836/1.391)
#    Signal2.SetLineStyle(11)
    Signal2.SetLineWidth(3)
    Signal2.SetLineStyle(2)
    Signal2.SetLineColor(2)
    Signal2.SetMarkerColor(2)
    Signal2.Draw("histsame")
    
    legende=make_legend()
    legende.AddEntry(Data,"Observed","elp")

    legende.AddEntry(Signal,sigLeg,"l")
    legende.AddEntry(W,"W+jets","f")
    legende.AddEntry(Signal2,sigLeg2,"l")
    legende.AddEntry(TT,"t#bar{t}","f")
    legende.AddEntry(SingleT,"Single top","f")
    legende.AddEntry(QCD,"QCD multijet","f")
    legende.AddEntry(DYS,"Z+jets ","f")
    legende.AddEntry(VV,"Diboson","f")
    legende.AddEntry(errorBand,"Total uncertainty","f")

    legende.Draw()

    l1=add_lumi()
    l1.Draw("same")
    l2=add_CMS()
    l2.Draw("same")
    l3=add_Preliminary()
#    l3.Draw("same")

    pad1.RedrawAxis()

    categ  = ROOT.TPaveText(0.21, 0.48+0.013, 0.43, 0.68+0.155, "NDC")
    categ.SetBorderSize(   0 )
    categ.SetFillStyle(    0 )
    categ.SetTextAlign(   12 )
    categ.SetTextSize ( 0.07 )
    categ.SetTextColor(    1 )
#    categ.SetTextFont (   41 )
    #       if i==1 or i==3:
#    categ.AddText('|#eta_{#mu} < 2.0|')
    #       else :
    #        categ.AddText("SS")
    categ.Draw()

    c.cd()
    pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.35);
#    if Status == "LOG" : pad2.SetLogx()
#    pad2.GetXaxis().SetRangeUser(200,5000)
    pad2.SetTopMargin(0.05);
    pad2.SetBottomMargin(0.35);
    pad2.SetLeftMargin(0.18);
    pad2.SetRightMargin(0.05);
    pad2.SetTickx(1)
    pad2.SetTicky(1)
    pad2.SetFrameLineWidth(3)
#    pad2.SetGridx()
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()
    
    h1=errorBand.Clone()
 
    
    h1.SetMinimum(0.1)
    h1.SetMarkerStyle(20)

    h3=Data.Clone()


    h3.Sumw2()
    h1.Sumw2()
    
    
    h1.SetStats(0)
    h3.SetStats(0)
    h1.SetTitle("")
    
    h1.Divide(errorBand)
    #######  set the bin errors to zero befive divinig data to that
    errorBandZeroErr=errorBand.Clone()
    for ibin in range(errorBandZeroErr.GetXaxis().GetNbins()):
        errorBandZeroErr.SetBinError(ibin+1,0)
    #######
    h3.Divide(errorBandZeroErr)

    for jbin in range(h3.GetXaxis().GetNbins()):
        print h3.GetBinContent(jbin+1), " +/- " ,h3.GetBinError(jbin+1)


    h1.GetXaxis().SetRangeUser(0,5000)
    h1.GetXaxis().SetTitle(Xaxis)
    h1.GetXaxis().SetLabelSize(0.08)
    h1.GetYaxis().SetLabelSize(0.08)
    h1.GetYaxis().SetTitle("Obs./Exp.")
    h1.GetXaxis().SetNdivisions(505)
    h1.GetYaxis().SetNdivisions(5)
    h1.GetXaxis().SetTitleSize(0.15)
    h1.GetYaxis().SetTitleSize(0.15)
    h1.GetYaxis().SetTitleOffset(0.5)
    h1.GetYaxis().SetLabelOffset(0.02)
    h1.GetXaxis().SetTitleOffset(0.9)
    h1.GetXaxis().SetLabelSize(0.11)
    h1.GetYaxis().SetLabelSize(0.11)
    h1.GetXaxis().SetTitleFont(42)
    h1.GetYaxis().SetTitleFont(42)
    h1.GetXaxis().SetRangeUser(0,MaxRange)
#    h1.GetYaxis().SetRangeUser(0,1.99)

#    h1.SetMaximum(1.99)
#    for i in range(h3.GetNbinsX()):
#        if i > 5 : h3.SetBinContent(i+1,0)


    h1.Draw("e2")
    h3.Draw("Ex0psame")


#    c.cd()
#    pad1.Draw()

#    ROOT.gPad.RedrawAxis()

#    c.Modified()
    h1.GetYaxis().SetRangeUser(.01,2.99)
#    c.Modified()
    c.SaveAs("_Finalplot"+categoriy+Status+"_CMB.pdf")
#    c.SaveAs("_Finalplot_"+categoriy+".pdf")
    #       c.SaveAs("mvis"+categoriy+".png")


    print "Data.Integral()", file.Get(categoriy).Get("data_obs").Integral()


#channelDirectory = ["et"]
#channelDirectory = ["EleTau"]
#Category=["lq_et_1_13TeV_prefit","lq_et_1_13TeV_postfit"]
#Category = ["_JetBJet"]
#Category = ["_inclusive"]



#FileNamesInfo=[
#               ["postfit_shapes.root","Codex__mj_cmb_1_13TeV_prefit","m_{#muj} [GeV]","#mu j ",2000,"Codex_","LQ 1200GeV (DM 500 GeV)",10],
#               ["postfit_shapes.root","Codex__mj_cmb_1_13TeV_postfit","m_{#muj} [GeV]","#mu j ",2000,"Codex_","LQ 1200GeV (DM 500 GeV)",10],
#               ]

FileNamesInfo=[
#               ["postfit_shapes_CMB_DM1000.root","Codex__mj_cmb_1_13TeV_prefit","m_{#muj} [GeV]","#mu j ",2000,"Codex_","LQ 1000GeV (DM 400 GeV)",10],
#               ["postfit_shapes_CMB_DM1000.root","Codex__mj_cmb_1_13TeV_postfit","m_{#muj} [GeV]","#mu j ",2000,"Codex_","LQ 1000GeV (DM 400 GeV)",10],
               ["postfit_shapes.root","Codex__mj_cmb_1_13TeV_postfit","m_{#muj} [GeV]","#mu j ",2000,"Codex_","LQ 1 TeV (DM 400 GeV, #it{B}=0.5)","LQ 1 TeV (DM 400 GeV, #it{B}=0.1)",10],
               ]










#for ch in channelDirectory:
#    for cat in Category:
for i in range(0,len(FileNamesInfo)):

#    FileName="ztt_"+ch+"_shapes.root"
    MakePlot(FileNamesInfo[i][0],FileNamesInfo[i][1],FileNamesInfo[i][3],FileNamesInfo[i][2],FileNamesInfo[i][4],FileNamesInfo[i][5],FileNamesInfo[i][6],FileNamesInfo[i][7],FileNamesInfo[i][8],"LOG")
#    MakePlot(FileNamesInfo[i][0],FileNamesInfo[i][1],FileNamesInfo[i][3],FileNamesInfo[i][2],FileNamesInfo[i][4],FileNamesInfo[i][5],FileNamesInfo[i][6],FileNamesInfo[i][7],"Normal")
#    MakePlot(FileNamesInfo[i][0],FileNamesInfo[i][1],FileNamesInfo[i][3],FileNamesInfo[i][2],FileNamesInfo[i][4],FileNamesInfo[i][5],FileNamesInfo[i][6],FileNamesInfo[i][7],"Normal")



#import os
#os.system("cp _FinalplotCodex__mj_2017_1_13TeV_postfitLOG.pdf  /Users/abdollah1/Documents/SVNNew/myDir/papers/EXO-17-015/trunk/Figure_002-b.pdf")




#Table for HEP DATA

