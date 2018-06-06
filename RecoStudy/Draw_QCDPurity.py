#!/usr/bin/env python

import math
import ROOT
from ROOT import Double
from ROOT import TCanvas
from ROOT import TFile
from ROOT import TH1F
from ROOT import TH2F
from ROOT import TNtuple
from ROOT import TProfile
from ROOT import gBenchmark
from ROOT import gROOT
from ROOT import gRandom
from ROOT import gSystem
from ROOT import TF1
from ROOT import TPaveText
from ROOT import TMath
from ctypes import *
import ROOT as r
import array

gROOT.Reset()
import os



RB_=10
def add_lumi():
    lowX=0.6
    lowY=0.85
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.20, lowY+0.1, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.04)
    lumi.SetTextFont (   42 )
    lumi.AddText("41.5 fb^{-1} (13 TeV)")
    return lumi

def add_CMS():
    lowX=0.21
    lowY=0.70
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(61)
    lumi.SetTextSize(0.06)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("CMS")
    return lumi

def add_Preliminary():
    lowX=0.21
    lowY=0.63
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.1, lowY+0.1, "NDC")
    lumi.SetTextFont(52)
    lumi.SetTextSize(0.04)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("Preliminary")
    return lumi

def make_legend():
        output = ROOT.TLegend(0.65, 0.4, 0.82, 0.72, "", "brNDC")
        output.SetLineWidth(0)
        output.SetLineStyle(0)
        output.SetFillStyle(0)
        output.SetBorderSize(0)
        output.SetTextFont(62)
        return output


def MakePlot(FileName,categoriy,HistName,Xaxis,Info,RB_,channel,yMin,isLOG,ttbarCR,Sample,Binning):
    ROOT.gStyle.SetFrameLineWidth(3)
    ROOT.gStyle.SetLineWidth(3)
    ROOT.gStyle.SetOptStat(0)

    c=ROOT.TCanvas("canvas","",0,0,600,600)
#    c.cd()

    file=ROOT.TFile(FileName,"r")

#    adapt=ROOT.gROOT.GetColor(12)
#    new_idx=ROOT.gROOT.GetListOfColors().GetSize() + 1


    Data_=file.Get("data")
    Data= Data_.Rebin(len(Binning)-1,"",Binning)
    
#    QCD=file.Get("QCD")
#    QCD.Rebin(RB_)


    W_=file.Get("W")
#    W.Rebin(RB_)
    W= W_.Rebin(len(Binning)-1,"",Binning)
#    if ttbarCR=="" :  W.Scale(SF_W_SingleLep())
#    if ttbarCR=="_ttbarCRSingleLep" :  W.Scale(SF_W_SingleLep())
#    if ttbarCR=="_ttbarCRDiLep" :  W.Scale(SF_W_DiLep())
#    W.Scale(1)


    TT_=file.Get("TT")
    TT= TT_.Rebin(len(Binning)-1,"",Binning)
#    TT.Rebin(RB_)
#    TT.Scale(1)
#    if ttbarCR=="" :  TT.Scale(SF_TT_SingleLep())
#    if ttbarCR=="_ttbarCRSingleLep" :  TT.Scale(SF_TT_SingleLep())
#    if ttbarCR=="_ttbarCRDiLep" :  TT.Scale(SF_TT_DiLep())

    SingleT_=file.Get("SingleT")
    SingleT= SingleT_.Rebin(len(Binning)-1,"",Binning)

    VV_=file.Get("VV")
#    VV.Rebin(RB_)
    VV= VV_.Rebin(len(Binning)-1,"",Binning)


    DYS_=file.Get("ZTT")
#    DYS.Rebin(RB_)
    DYS= DYS_.Rebin(len(Binning)-1,"",Binning)

    Data.GetXaxis().SetTitle("")
#    Data.GetXaxis().SetTitleSize(0)
#    Data.GetXaxis().SetNdivisions(505)
#    Data.GetYaxis().SetLabelFont(42)
#    Data.GetYaxis().SetLabelOffset(0.01)
#    Data.GetYaxis().SetLabelSize(0.06)
#    Data.GetYaxis().SetTitleSize(0.075)
#    Data.GetYaxis().SetTitleOffset(1.04)
    Data.SetTitle("")
    Data.GetYaxis().SetTitle("Events")
    Data.GetXaxis().SetTitle(Xaxis)


#    Signal=file.Get("Codex_1200")
#    Signal.Scale(1.50E-03*.5)
#    Signal.Rebin(RB_)
#    Signal.SetLineStyle(11)
#    Signal.SetLineWidth(3)
#    Signal.SetLineColor(4)
#    Signal.SetMarkerColor(4)


#    QCD.SetFillColor(ROOT.TColor.GetColor(408, 106, 154))
    W.SetFillColor(ROOT.TColor.GetColor(200, 2, 285))
    TT.SetFillColor(ROOT.TColor.GetColor(208, 376, 124))
    SingleT.SetFillColor(ROOT.TColor.GetColor(150, 132, 232))
    VV.SetFillColor(ROOT.TColor.GetColor(200, 282, 232))
    DYS.SetFillColor(ROOT.TColor.GetColor(108, 226, 354))
    
   




    Data.SetMarkerStyle(20)
    Data.SetMarkerSize(1)
#    QCD.SetLineColor(ROOT.kBlack)
    W.SetLineColor(ROOT.kBlack)
    TT.SetLineColor(ROOT.kBlack)
    DYS.SetLineColor(ROOT.kBlack)
    VV.SetLineColor(ROOT.kBlack)
    SingleT.SetLineColor(ROOT.kBlack)
    Data.SetLineColor(ROOT.kBlack)
    Data.SetLineWidth(2)
    



    stack=ROOT.THStack("stack","stack")
#    stack.Add(QCD)
    stack.Add(VV)
    stack.Add(DYS)
    stack.Add(SingleT)
    stack.Add(TT)
    stack.Add(W)

    errorBand = W.Clone()
#    errorBand.Add(QCD)
    errorBand.Add(TT)
    errorBand.Add(VV)
    errorBand.Add(SingleT)
    errorBand.Add(DYS)
    errorBand.SetMarkerSize(0)
    errorBand.SetFillColor(16)
    errorBand.SetFillStyle(3001)
    errorBand.SetLineWidth(1)

#    pad1 = ROOT.TPad("pad1","pad1",0,0.1,1,1)
#    if isLOG: pad1.SetLogy()
#    pad1.Draw()
#    pad1.cd()
#    pad1.SetFillColor(0)
#    pad1.SetBorderMode(0)
#    pad1.SetBorderSize(10)
#    pad1.SetTickx(1)
#    pad1.SetTicky(1)
#    pad1.SetLeftMargin(0.18)
#    pad1.SetRightMargin(0.05)
#    pad1.SetTopMargin(0.122)
#    pad1.SetBottomMargin(0.026)
#    pad1.SetFrameFillStyle(0)
#    pad1.SetFrameLineStyle(0)
#    pad1.SetFrameLineWidth(3)
#    pad1.SetFrameBorderMode(0)
#    pad1.SetFrameBorderSize(10)

#    Data.GetXaxis().SetLabelSize(0)
    if isLOG: Data.SetMaximum(Data.GetMaximum()*10000)
    else:  Data.SetMaximum(Data.GetMaximum()*3)
    Data.SetMinimum(yMin)
    Data.Draw("e")
    stack.Draw("histsame")
    errorBand.Draw("e2same")
    Data.Draw("esame")
#    Signal.Draw("histsame")

#    Data.GetXaxis().SetTitle(Xaxis)
#    Data.GetXaxis().SetLabelSize(0.04)




    legende=make_legend()
    legende.AddEntry(Data,"Observed","elp")
#    legende.AddEntry(Signal,"Codex_1200","l")
    legende.AddEntry(TT,"t#bar{t}+jets","f")
    legende.AddEntry(SingleT,"SingleTop","f")
    legende.AddEntry(DYS,"DY #rightarrowll ","f")
    legende.AddEntry(VV,"Diboson","f")
    legende.AddEntry(W,"W","f")
#    legende.AddEntry(QCD,"QCD multijet","f")
    legende.AddEntry(errorBand,"Uncertainty","f")

    legende.Draw()

    l1=add_lumi()
    l1.Draw("same")
    l2=add_CMS()
    l2.Draw("same")
    l3=add_Preliminary()
    l3.Draw("same")



#    Data.GetYaxis().SetLabelSize(0.01)
##    Data.GetXaxis().SetNdivisions(505)
##    Data.GetYaxis().SetNdivisions(5)
#    Data.GetXaxis().SetTitleSize(0.04)
#    Data.GetYaxis().SetTitleSize(0.04)
#    Data.GetYaxis().SetTitleOffset(1)
#    
#    Data.GetXaxis().SetTitleOffset(1.1)
#    Data.GetXaxis().SetLabelSize(0.04)
#    Data.GetYaxis().SetLabelSize(0.04)
#    Data.GetXaxis().SetTitleFont(42)
#    Data.GetYaxis().SetTitleFont(42)


#    pad1.RedrawAxis()

    categ  = ROOT.TPaveText(0.18, 0.5+0.013, 0.33, 0.60+0.155, "NDC")
    categ.SetBorderSize(   0 )
    categ.SetFillStyle(    0 )
    categ.SetTextAlign(   12 )
    categ.SetTextSize ( 0.04 )
    categ.SetTextColor(    1 )
    categ.SetTextFont (   41 )
    #       if i==1 or i==3: 
#    categ.AddText(ttbarCR)
#    categ.AddText(MTLegend)
    #       else :
    categ.AddText(HistName)
    categ.Draw()

#    c.cd()
##    pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.35);
##    pad2.SetTopMargin(0.05);
##    pad2.SetBottomMargin(0.35);
##    pad2.SetLeftMargin(0.18);
##    pad2.SetRightMargin(0.05);
##    pad2.SetTickx(1)
##    pad2.SetTicky(1)
##    pad2.SetFrameLineWidth(3)
##    pad2.SetGridx()
##    pad2.SetGridy()
##    pad2.Draw()
##    pad2.cd()
#
#    h1=errorBand.Clone()
#    h1.SetMaximum(1.5)
#    h1.SetMinimum(0.5)
#    h1.SetMarkerStyle(20)
#
#    h3=Data.Clone()
#    
#    h3.Sumw2()
#    h1.Sumw2()
#    
#    
#    h1.SetStats(0)
#    h3.SetStats(0)
#    h1.SetTitle("")
#    
#    h1.Divide(errorBand)
#    #######  set the bin errors to zero befive divinig data to that
#    errorBandZeroErr=errorBand.Clone()
#    for ibin in range(errorBandZeroErr.GetXaxis().GetNbins()):
#        errorBandZeroErr.SetBinError(ibin+1,0)
#    #######
#    h3.Divide(errorBandZeroErr)
#
#
#    h1.GetXaxis().SetTitle(Xaxis)
#    h1.GetXaxis().SetLabelSize(0.08)
#    h1.GetYaxis().SetLabelSize(0.08)
#    h1.GetYaxis().SetTitle("Obs./Exp.")
#    h1.GetXaxis().SetNdivisions(505)
#    h1.GetYaxis().SetNdivisions(5)
#    h1.GetXaxis().SetTitleSize(0.15)
#    h1.GetYaxis().SetTitleSize(0.15)
#    h1.GetYaxis().SetTitleOffset(0.56)
#    h1.GetXaxis().SetTitleOffset(1.04)
#    h1.GetXaxis().SetLabelSize(0.11)
#    h1.GetYaxis().SetLabelSize(0.11)
#    h1.GetXaxis().SetTitleFont(42)
#    h1.GetYaxis().SetTitleFont(42)
#    
#    h1.Draw("e2")
#    h3.Draw("E0psame")
#
#    c.cd()
#    pad1.Draw()
#
    ROOT.gPad.RedrawAxis()

#    c.Modified()
    c.SaveAs("_plot"+Sample+str(isLOG)+".pdf")


#
#-rw-r--r--  1 abdollah  48669 Aug  4 12:10 qcdPurity_Num_CloseJetLepPt.root
#-rw-r--r--  1 abdollah  54495 Aug  4 12:10 qcdPurity_DeNum_CloseJetLepPt.root
#-rw-r--r--  1 abdollah  51235 Aug  4 12:11 qcdPurity_Num_LepPt.root
#-rw-r--r--  1 abdollah  52063 Aug  4 12:11 qcdPurity_DeNum_LepPt.root
#
#

Binning = array.array("d",[0,60,80,100,120,150,200,250,300,400,500,600,800])
MakePlot("Extra/qcdPurity_DeNum_CloseJetLepPt.root","","Denumerator","Jet p_{T} (GeV)","",10,"",1,0,"","DenumCloseJet",Binning)
MakePlot("Extra/qcdPurity_Num_CloseJetLepPt.root","","Numerator","Jet p_{T} (GeV)","",10,"",1,0,"","NumCloseJet",Binning)



Binning = array.array("d",[0,60,70,80,90,100,110,120,130,150,175,200,230,260,300])
MakePlot("Extra/qcdPurity_DeNum_LepPt.root","","Denumerator"," #mu p_{T} (GeV)","",10,"",1,0,"","DenumLep",Binning)
MakePlot("Extra/qcdPurity_Num_LepPt.root","","Numerator","#mu p_{T} (GeV)","",10,"",1,0,"","NumLep",Binning)



