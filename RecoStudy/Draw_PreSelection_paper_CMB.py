#!/usr/bin/env python
import ROOT
import re
from array import array
import os

from Step5_TT_W_ScaleFactor import *
#from Step5_TT_W_ScaleFactor_ForJet50 import *
#................................................................................................................................
#................................................................................................................................




#InputFilesLocation = 'NewOutFiles_Preselection_Approval_V1/___WithTopPtRW/'
#InputFilesLocation = 'NewOutFiles_Preselection_Approval_V1/___NoTopPtRW/'
InputFilesLocation = '_CMB/'

#................................................................................................................................
#................................................................................................................................
ForAN=0
RB_=20
def add_lumi():
    lowX=0.59
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.06)
    lumi.SetTextFont (   42 )
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
        output = ROOT.TLegend(0.65, 0.4, 0.92, 0.82, "", "brNDC")
        output.SetLineWidth(0)
        output.SetLineStyle(0)
        output.SetFillStyle(0)
        output.SetBorderSize(0)
        output.SetTextFont(62)
        return output


def MakePlot(FileName,categoriy,HistName,Xaxis,Info,RB_,channel,yMin,isLOG,ttbarCR,MTLegend):
#    yMin*=0.1
    ROOT.gStyle.SetFrameLineWidth(3)
    ROOT.gStyle.SetLineWidth(3)
    ROOT.gStyle.SetOptStat(0)

    c=ROOT.TCanvas("canvas","",0,0,600,600)
    c.cd()

    file=ROOT.TFile(InputFilesLocation+FileName,"r")

    adapt=ROOT.gROOT.GetColor(12)
    new_idx=ROOT.gROOT.GetListOfColors().GetSize() + 1


    Data=file.Get(categoriy).Get("data_obs")
    Data.Rebin(RB_)
    
    
    QCD=file.Get(categoriy).Get("QCD")
#    if not QCD:
#        QCD=file.Get(categoriy).Get("VV")
#        QCD.Scale(.0001)
#        print "\n\n\n\nn\######################### whatch out VV  instead of QCD\n\n\n\n"
    QCD.Rebin(RB_)
    





    W=file.Get(categoriy).Get("W")
    W.Rebin(RB_)
#    W.Scale(1)
#    if ttbarCR=="" :  W.Scale(SF_W_SingleLep())
#    if ttbarCR=="_ttbarCRSingleLep" :  W.Scale(SF_W_SingleLep())
#    if ttbarCR=="_ttbarCRDiLep" :  W.Scale(SF_W_DiLep())






    TT=file.Get(categoriy).Get("TT")
#    if not TT:
#        TT=file.Get(categoriy).Get("VV")
#        TT.Scale(.0001)
#        print "\n\n\n\nn\######################### whatch out VV  instead of TT\n\n\n\n"
    TT.Rebin(RB_)
#    TT.Scale(1)
#    if ttbarCR=="" :  TT.Scale(SF_TT_SingleLep())
#    if ttbarCR=="_ttbarCRSingleLep" :  TT.Scale(SF_TT_SingleLep())
#    if ttbarCR=="_ttbarCRDiLep" :  TT.Scale(SF_TT_DiLep())





    SingleT=file.Get(categoriy).Get("SingleTop")
#    if not SingleT:
#        SingleT=file.Get(categoriy).Get("VV")
#        SingleT.Scale(.0001)
#        print "\n\n\n\nn\######################### whatch out VV  instead of SingleT\n\n\n\n"
    SingleT.Rebin(RB_)





    VV=file.Get(categoriy).Get("VV")
    VV.Rebin(RB_)






    DYS=file.Get(categoriy).Get("ZTT")
#    if not DYS:
#        DYS=file.Get(categoriy).Get("VV")
#        DYS.Scale(.0001)
#        print "\n\n\n\nn\######################### whatch out VV  instead of DYS\n\n\n\n"
    DYS.Rebin(RB_)

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


#    Signal=file.Get(categoriy).Get("Codex_1200")
    Signal=file.Get(categoriy).Get("VV")
    Signal.Scale(1.50E-03*.5)
    Signal.Rebin(RB_)
    Signal.SetLineStyle(11)
    Signal.SetLineWidth(3)
    Signal.SetLineColor(4)
    Signal.SetMarkerColor(4)



    ##### chnage binning content
    ALLSample=[Data,QCD,W,TT,SingleT,VV,DYS]
    for sample in ALLSample:
        for ibin in range(sample.GetXaxis().GetNbins()):
            #            print ibin+1, sample.GetBinWidth(ibin+1)
            
            sample.SetBinContent(ibin+1,1.0*sample.GetBinContent(ibin+1)/sample.GetBinWidth(ibin+1))
            sample.SetBinError(ibin+1,1.0*sample.GetBinError(ibin+1)/sample.GetBinWidth(ibin+1))
            
            if sample==Data and sample.GetBinContent(ibin+1)==0: #https://twiki.cern.ch/twiki/bin/view/CMS/PoissonErrorBars
                sample.SetBinError(ibin+1,1.0*1.8/sample.GetBinWidth(ibin+1))


    QCD.SetFillColor(ROOT.TColor.GetColor(408, 106, 154))
    W.SetFillColor(ROOT.TColor.GetColor(200, 2, 285))
    TT.SetFillColor(ROOT.TColor.GetColor(208, 376, 124))
    SingleT.SetFillColor(ROOT.TColor.GetColor(150, 132, 232))
    VV.SetFillColor(ROOT.TColor.GetColor(200, 282, 232))
    DYS.SetFillColor(ROOT.TColor.GetColor(108, 226, 354))
    
    
    
    ######  Add OverFlow Bin
#    if not FileName.find("_tmass_MuMet") > 0:
#    QCD.SetBinContent(QCD.GetNbinsX(),QCD.GetBinContent(QCD.GetNbinsX()+1)+QCD.GetBinContent(QCD.GetNbinsX()))
#    W.SetBinContent(W.GetNbinsX(),W.GetBinContent(W.GetNbinsX()+1)+W.GetBinContent(W.GetNbinsX()))
#    TT.SetBinContent(TT.GetNbinsX(),TT.GetBinContent(TT.GetNbinsX()+1)+TT.GetBinContent(TT.GetNbinsX()))
#    SingleT.SetBinContent(SingleT.GetNbinsX(),SingleT.GetBinContent(SingleT.GetNbinsX()+1)+SingleT.GetBinContent(SingleT.GetNbinsX()))
#    VV.SetBinContent(VV.GetNbinsX(),VV.GetBinContent(VV.GetNbinsX()+1)+VV.GetBinContent(VV.GetNbinsX()))
#    DYS.SetBinContent(DYS.GetNbinsX(),DYS.GetBinContent(DYS.GetNbinsX()+1)+DYS.GetBinContent(DYS.GetNbinsX()))
#    Data.SetBinContent(Data.GetNbinsX(),Data.GetBinContent(Data.GetNbinsX()+1)+Data.GetBinContent(Data.GetNbinsX()))







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


#    #Making the plot blind
#    if FileName.find("LQMass") > 0 :
#        print "##################################\n", FileName
#        for i in range(Data.GetNbinsX()):
##            if i > 15 : Data.SetBinContent(i+1,0)
#            if i > 9 :
#                Data.SetBinContent(i+1,0)
#                Data.SetBinError(i+1,0)
#
#    if FileName.find("MET") > 0 :
#        print "##################################\n", FileName
#        for i in range(Data.GetNbinsX()):
#            if i > 9 : Data.SetBinContent(i+1,0)
#
#    if FileName.find("tmass_MuMet") > 0 :
#        print "##################################\n", FileName
#        for i in range(Data.GetNbinsX()):
#                if i > 9 : Data.SetBinContent(i+1,0)




    stack=ROOT.THStack("stack","stack")
    
    stack.Add(VV)
    stack.Add(DYS)
    stack.Add(QCD)
    stack.Add(SingleT)

    if ttbarCR=="":
        stack.Add(TT)
        stack.Add(W)
    else:
        stack.Add(W)
        stack.Add(TT)

    errorBand = W.Clone()
    errorBand.Add(QCD)
    errorBand.Add(TT)
    errorBand.Add(VV)
    errorBand.Add(SingleT)
    errorBand.Add(DYS)
    errorBand.SetMarkerSize(0)
    errorBand.SetFillColor(16)
    errorBand.SetFillStyle(3001)
    errorBand.SetLineWidth(1)

    pad1 = ROOT.TPad("pad1","pad1",0,0.35,1,1)
    if isLOG: pad1.SetLogy()
    pad1.Draw()
    pad1.cd()
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
    if isLOG: Data.SetMaximum(Data.GetMaximum()*1000)
    else:  Data.SetMaximum(Data.GetMaximum()*3)
    Data.SetMinimum(yMin)
    Data.Draw("e")
    stack.Draw("histsame")
    errorBand.Draw("e2same")
    Data.Draw("esame")
#    Signal.Draw("histsame")

    legende=make_legend()
    legende.AddEntry(Data,"Data","elp")
    if ttbarCR=="":
        legende.AddEntry(W,"W+jets","f")
        legende.AddEntry(TT,"t#bar{t}+jets","f")

    else:
        legende.AddEntry(TT,"t#bar{t}+jets","f")
        legende.AddEntry(W,"W+jets","f")

    legende.AddEntry(SingleT,"Single Top","f")
    legende.AddEntry(QCD,"QCD multijet","f")
    legende.AddEntry(DYS,"DY#rightarrowll+jets ","f")
    legende.AddEntry(VV,"Diboson","f")
    legende.AddEntry(errorBand,"Stat. Uncertainty","f")

    legende.Draw()

    l1=add_lumi()
    l1.Draw("same")
    l2=add_CMS()
    l2.Draw("same")
#    l3=add_Preliminary()
#    l3.Draw("same")

    pad1.RedrawAxis()

    categ  = ROOT.TPaveText(0.20, 0.45+0.013, 0.43, 0.60+0.155, "NDC")
    categ.SetBorderSize(   0 )
    categ.SetFillStyle(    0 )
    categ.SetTextAlign(   12 )
    categ.SetTextSize ( 0.04 )
    categ.SetTextColor(    1 )
#    categ.SetTextFont (   41 )
    #       if i==1 or i==3:
    if ForAN:
        if MTLegend=='_NoMT': categ.AddText("M_{T}(#mu,MET) > 0 GeV")
        if MTLegend=='_HighMT': categ.AddText("M_{T}(#mu,MET) > 100 GeV")
        if MTLegend=='_MT300': categ.AddText("M_{T}(#mu,MET) > 300 GeV")
        if MTLegend=='_MT500': categ.AddText("M_{T}(#mu,MET) > 500 GeV")
        if MTLegend=='_MT50To150': categ.AddText("50 GeV <M_{T}(#mu,MET) < 150 GeV")

#    categ.AddText("1100<M_{LQ}<1400 GeV")
#    categ.AddText("Jet Pt < 200 GeV")
#    categ.AddText(ttbarCR)
#    categ.AddText('50 <Jet p_{T} < 200 GeV')
#    categ.AddText("M_{LQ} > 1100 GeV")
#    categ.AddText("#mu  p_{T} < 300 GeV")
#    categ.AddText('q_{#mu} > 0')
#    categ.AddText(MTLegend)
    #       else :
    #        categ.AddText("SS")
        categ.Draw()

    c.cd()
    pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.35);
    pad2.SetTopMargin(0.05);
    pad2.SetBottomMargin(0.35);
    pad2.SetLeftMargin(0.18);
    pad2.SetRightMargin(0.05);
    pad2.SetTickx(1)
    pad2.SetTicky(1)
    pad2.SetFrameLineWidth(3)
    pad2.SetGridx()
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()
    
    h1=errorBand.Clone()
#    h1.SetMaximum(2)
#    h1.SetMinimum(0)
    h1.SetMaximum(2.0)
    h1.SetMinimum(0.0)
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


    h1.GetXaxis().SetTitle(Xaxis)
    h1.GetXaxis().SetLabelSize(0.08)
    h1.GetYaxis().SetLabelSize(0.08)
    h1.GetYaxis().SetTitle("Obs./Exp.")
    h1.GetXaxis().SetNdivisions(505)
    h1.GetYaxis().SetNdivisions(5)
    h1.GetXaxis().SetTitleSize(0.15)
    h1.GetYaxis().SetTitleSize(0.15)
    h1.GetYaxis().SetTitleOffset(0.56)
    h1.GetXaxis().SetTitleOffset(1.04)
    h1.GetXaxis().SetLabelSize(0.11)
    h1.GetYaxis().SetLabelSize(0.11)
    h1.GetXaxis().SetTitleFont(42)
    h1.GetYaxis().SetTitleFont(42)
    
    h1.Draw("e2")
    h3.Draw("E0psame")

    c.cd()
    pad1.Draw()

    ROOT.gPad.RedrawAxis()

    c.Modified()
    outName=((FileName.replace('TotalRootForLimit_PreSelection_MuJet','').replace('.root','')).replace('_HighDPhi_Iso','')).replace('_HighMT','_MT100')
    c.SaveAs("PAPERControlPlots/"+'_MuJet'+outName+".pdf")


FileNamesInfo=[
#               ["_tmass_JetMet","M_{T}(jet,MET) (GeV)","",5,1],
#               ["_tmass_LQMet","M_{T}(LQ,MET)  (GeV)","",10,1],
#               ["_LepPt","lepton p_{T} (GeV)","",100,1],
#               ["_LepEta","lepton #eta ","",5,10],
#               ["_JetPt","jet p_{T} (GeV)","",100,1],
#               ["_JetEta","jet #eta ","",5,10],
#               ["_nVtx","# of vertex","",2,10],
#               ["_nVtx_NoPU","# of vertex before PU reweighting","",2,10],
#               ["_MET","MET  (GeV)","",10,1],
               ["_LQMass","m_{#muj}   (GeV)","",10,.001],
#               ["_tmass_MuMet","M_{T}(#mu,MET) (GeV)","",10,1],
#               ["_dPhi_Jet_Met","#Delta#phi (jet,MET)","",5,1],
#               ["_dPhi_Mu_Jet","#Delta#phi (#mu,jet)","",5,1],
#               ["_dPhi_Mu_MET","#Delta#phi (#mu,MET)","",10,1],
#               ["_METPhi","MET #phi ","",10,10],
#               ["_NumJet","Jet multiplicity","",1,1],
#               ["_NumBJet","BJet multiplicity","",1,1],
#              ["_recoHT","Jet HT  (GeV)","",10,1],
               ]

Isolation=["_Iso"]
#MT= ["_NoMT","_HighMT","_MT50To150","_MT300","_MT500"]
MT= ["_HighMT","_MT50To150"]
JPT=[ "_HighDPhi"]
lqEta= [""]
region= ["","_ttbarCRSingleLep"]

#logStat=[0]
logStat=[1]




for i in range(0,len(FileNamesInfo)):
    
    NormMC=FileNamesInfo[i][0]
    axisName=FileNamesInfo[i][1]
    nothing=FileNamesInfo[i][2]
    Bin=FileNamesInfo[i][3]
    yMin=FileNamesInfo[i][4]
    
    for iso in Isolation:
        for mt in MT:
            for jpt in JPT:
                for etalq in lqEta:
                    for reg in region:
                        for isLOG in logStat:
                            
                            if mt=="_HighMT" and reg=="": continue
                            if mt=="_MT50To150" and reg=="_ttbarCRSingleLep": continue
                    
                            FileName="TotalRootForLimit_PreSelection_"+"MuJet"+NormMC+mt+jpt+etalq+reg+iso+".root"
                            Info=NormMC+mt+jpt+etalq+reg+iso
                            print "---->", FileName
                            MakePlot(FileName,"MuJet","",axisName,Info,Bin,"",yMin,isLOG,reg,mt)






#os.system("cp PAPERControlPlots/")
#
#
#os.system("cp PAPERControlPlots/_MuJet_LQMass_MT100_HighDPhi_ttbarCRSingleLep_Iso.pdf  /Users/abdollah1/Documents/SVNNew/myDir/papers/EXO-17-015/trunk/Figure_001-b.pdf")
#os.system("cp PAPERControlPlots/_MuJet_LQMass_MT50To150.pdf  /Users/abdollah1/Documents/SVNNew/myDir/papers/EXO-17-015/trunk/Figure_001-d.pdf")


