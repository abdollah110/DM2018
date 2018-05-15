#!/usr/bin/env python
import ROOT
import re
from array import array

#from Step5_TT_W_ScaleFactor import *
#from Step5_TT_W_ScaleFactor_ForJet50 import *
#................................................................................................................................
#................................................................................................................................



#InputFilesLocation = 'NewOutFiles_Preselection_/'
#InputFilesLocation = 'NewOutFiles_Preselection_addPhi/'
#InputFilesLocation = 'NewOutFiles_Preselection_Check3/'
#InputFilesLocation = 'NewOutFiles_Preselection__Check4_vertex/'
InputFilesLocation2016 = '/Users/abdollah1/GIT_abdollah110/DM2017/RecoStudy/2016_2017/'
InputFilesLocation2017 = '2016_2017/'

#................................................................................................................................
#................................................................................................................................

RB_=20
def add_lumi(Type):
    lowX=0.59
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.06)
    lumi.SetTextFont (   42 )
    lumi.AddText("13 TeV '%s'"%Type)
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
        output = ROOT.TLegend(0.65, 0.6, 0.92, 0.82, "", "brNDC")
        output.SetLineWidth(0)
        output.SetLineStyle(0)
        output.SetFillStyle(0)
        output.SetBorderSize(0)
        output.SetTextFont(62)
        return output


def MakePlot(FileName,categoriy,HistName,Xaxis,Info,RB_,channel,yMin,isLOG,ttbarCR,MTLegend,SSS,isData):
#    yMin*=0.1
    ROOT.gStyle.SetFrameLineWidth(3)
    ROOT.gStyle.SetLineWidth(3)
    ROOT.gStyle.SetOptStat(0)

    c=ROOT.TCanvas("canvas","",0,0,600,600)
    c.cd()

    file2016=ROOT.TFile(InputFilesLocation2016+FileName,"r")

    file2017=ROOT.TFile(InputFilesLocation2017+FileName,"r")

#    adapt=ROOT.gROOT.GetColor(12)
#    new_idx=ROOT.gROOT.GetListOfColors().GetSize() + 1





    W2016=file2016.Get(categoriy).Get("W")
    if isData: W2016=file2016.Get(categoriy).Get("data_obs")
    W2016.Rebin(RB_)
#    W2016.Scale(1./W2016.Integral())


    W2017=file2017.Get(categoriy).Get("W")
    if isData: W2017=file2017.Get(categoriy).Get("data_obs")
    W2017.Rebin(RB_)
    W2017.Scale(35.9/41.1)





    W2016.GetXaxis().SetTitle("")
    W2016.GetXaxis().SetTitleSize(0)
    W2016.GetXaxis().SetNdivisions(505)
    W2016.GetYaxis().SetLabelFont(42)
    W2016.GetYaxis().SetLabelOffset(0.01)
    W2016.GetYaxis().SetLabelSize(0.06)
    W2016.GetYaxis().SetTitleSize(0.075)
    W2016.GetYaxis().SetTitleOffset(1.04)
    W2016.SetTitle("")
    W2016.GetYaxis().SetTitle("Events")




#    W2016.SetFillColor(ROOT.TColor.GetColor(200, 2, 285))
#    W2017.SetFillColor(ROOT.TColor.GetColor(408, 106, 154))

 

    W2017.SetMarkerStyle(20)
    W2017.SetMarkerSize(1)
    W2017.SetMarkerColor(2)
    W2017.SetLineColor(ROOT.kRed)
    if isData: W2017.SetMarkerColor(3)
    if isData: W2017.SetLineColor(ROOT.kGreen)
    W2017.SetLineWidth(2)
    
    
    W2016.SetMarkerStyle(24)
    W2016.SetMarkerSize(1)
    W2016.SetMarkerColor(4)
    W2016.SetLineColor(ROOT.kBlue)
    if isData: W2016.SetMarkerColor(9)
    if isData: W2016.SetLineColor(9)
    W2016.SetLineWidth(2)
    
    
    
#    W2016.Scale(1./W2016.Integral())
#    W2017.Scale(1./W2017.Integral())

#    W2017.SetLineColor(ROOT.kBlack)

    


    #Making the plot blind
    if isData and FileName.find("LQMass") > 0 :
        print "##################################\n", FileName
        for i in range(W2016.GetNbinsX()):
#            if i > 15 : W2016.SetBinContent(i+1,0)
            if i > 19 : W2016.SetBinContent(i+1,0)
            if i > 19 : W2017.SetBinContent(i+1,0)
#
#    if FileName.find("MET") > 0 :
#        print "##################################\n", FileName
#        for i in range(W2016.GetNbinsX()):
#            if i > 9 : W2016.SetBinContent(i+1,0)
#
#    if FileName.find("tmass_MuMet") > 0 :
#        print "##################################\n", FileName
#        for i in range(W2016.GetNbinsX()):
#                if i > 9 : W2016.SetBinContent(i+1,0)






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

    W2016.GetXaxis().SetLabelSize(0)
#    W2016.SetMaximum(50)
#    W2017.SetMaximum(100)
    if isLOG: W2016.SetMaximum(W2016.GetMaximum()*1000)
    else:  W2016.SetMaximum(W2016.GetMaximum()*3)
#    W2016.SetMinimum(yMin)
    W2016.Draw("e")
    W2017.Draw("esame")

    legende=make_legend()
    legende.AddEntry(W2016,"2016 (35.9/fb)","pl")
    legende.AddEntry(W2017,"2017 (scaled to 35.9/fb)","pl")


    legende.Draw()

    l1=add_lumi('W')
    if isData: l1=add_lumi('Data')
    l1.Draw("same")
    l2=add_CMS()
    l2.Draw("same")
    l3=add_Preliminary()
    l3.Draw("same")

    pad1.RedrawAxis()

    categ  = ROOT.TPaveText(0.20, 0.45+0.013, 0.43, 0.60+0.155, "NDC")
    categ.SetBorderSize(   0 )
    categ.SetFillStyle(    0 )
    categ.SetTextAlign(   12 )
    categ.SetTextSize ( 0.04 )
    categ.SetTextColor(    1 )
#    categ.SetTextFont (   41 )
    #       if i==1 or i==3:
    if MTLegend=='_NoMT': categ.AddText("M_{T}(#mu,MET) > 0 GeV")
    elif MTLegend=='_HighMT': categ.AddText("M_{T}(#mu,MET) > 100 GeV")
    elif MTLegend=='_MT300': categ.AddText("M_{T}(#mu,MET) > 300 GeV")
    elif MTLegend=='_MT500': categ.AddText("M_{T}(#mu,MET) > 500 GeV")
#    categ.AddText("lumiWeight+PUWeight+MuCorr")

    if isData: categ.AddText("        Norm Ratio=%.2f"%(W2017.Integral()/W2016.Integral()))
    else: categ.AddText("%s        Norm Ratio=%.2f"%(SSS.replace('WJets_',''),W2017.Integral()/W2016.Integral()))
    
    categ.AddText("\t\t%s"%ttbarCR)
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
    
    h1=W2017.Clone()
    h1.SetMaximum(2)
    h1.SetMinimum(0)
    h1.SetMarkerStyle(20)

    h3=W2016.Clone()
    
    h3.Sumw2()
    h1.Sumw2()
    
    
    h1.SetStats(0)
    h3.SetStats(0)
    h1.SetTitle("")
    
    h1.Divide(W2016)
#    #######  set the bin errors to zero befive divinig W2016 to that
#    errorBandZeroErr=errorBand.Clone()
#    for ibin in range(errorBandZeroErr.GetXaxis().GetNbins()):
#        errorBandZeroErr.SetBinError(ibin+1,0)
#    #######
#    h3.Divide(errorBandZeroErr)


    h1.GetXaxis().SetTitle(Xaxis)
    h1.GetXaxis().SetLabelSize(0.08)
    h1.GetYaxis().SetLabelSize(0.08)
    h1.GetYaxis().SetTitle("2017/2016")
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
    h1.SetMarkerColor(1)
    h1.SetLineColor(1)
    h1.SetMarkerStyle(3)
    h1.Draw("E0p")
    
#    h3.Draw("E0psame")

    c.cd()
    pad1.Draw()

    ROOT.gPad.RedrawAxis()

    c.Modified()
    outName=((FileName.replace('TotalRootForLimit_%s_MuJet'%SSS,'').replace('.root','')).replace('_HighDPhi_Iso','')).replace('_HighMT','_MT100')
    
    if isData: c.SaveAs(InputFilesLocation2017+'_MuJet_Data'+outName+SSS+".pdf")
    else: c.SaveAs(InputFilesLocation2017+'_MuJet_W'+outName+SSS+".pdf")


FileNamesInfo=[
#               ["_tmass_JetMet","M_{T}(jet,MET) (GeV)","",5,1],
               ["_tmass_LQMet","M_{T}(LQ,MET)  (GeV)","",10,1],
               ["_LepPt","lepton p_{T} (GeV)","",50,1],
               ["_LepEta","lepton #eta ","",5,10],
               ["_JetPt","jet p_{T} (GeV)","",50,1],
               ["_JetEta","jet #eta ","",5,10],
#               ["_nVtx","# of vertex","",2,10],
#               ["_nVtx_NoPU","# of vertex before PU reweighting","",2,10],
               ["_MET","MET  (GeV)","",5,1],
               ["_LQMass","M_{LQ}   (GeV)","",5,1],
               ["_tmass_MuMet","M_{T}(#mu,MET) (GeV)","",5,1],
               ["_dPhi_Jet_Met","#Delta#phi (jet,MET)","",5,1],
               ["_dPhi_Mu_Jet","#Delta#phi (#mu,jet)","",5,1],
               ["_dPhi_Mu_Met","#Delta#phi (#mu,MET)","",5,1],
               ["_METPhi","MET #phi","",10,10],
               ["_LepPhi","#mu #phi","",10,10],
               ["_Cos_dPhi_Mu_Met","1- cos(#Delta#phi_{#mu,MET})","",10,10],
               
               ["_NumJet","Jet multiplicity","",1,1],
               ["_NumBJet","BJet multiplicity","",1,1],
               
#               ["_tmass_MuMet_LowPU","M_{T}(jet,MET) (GeV) numVtx < 20","",5,.000001],
#               ["_tmass_MuMet_MedPU","M_{T}(jet,MET) (GeV) 20<numVtx < 35","",5,.000001],
#               ["_tmass_MuMet_HighPU","M_{T}(jet,MET) (GeV) numVtx > 35","",5,.000001],
#               
#               ["_dPhi_Mu_Met_LowPU","#Delta#phi (#mu,MET)numVtx < 20","",5,.001],
#               ["_dPhi_Mu_Met_MedPU","#Delta#phi (#mu,MET)20<numVtx < 35","",5,.001],
#               ["_dPhi_Mu_Met_HighPU","#Delta#phi (#mu,MET) numVtx > 35","",5,.001],
               
                              
               
               
               ]


#PlotName=["_LepPhi","_Cos_dPhi_Mu_Met"]






isData=1


#    Isolation=["_Iso", "_AntiIso","_Total"]

Isolation=["_Iso"]
#MT=["_HighMT"]
#MT=["_HighMT","_MT500"]
#MT= ["_NoMT","_HighMT","_MT300","_MT500"]
#MT= ["_NoMT"]
MT= ["_NoMT","_HighMT","_MT300"]
#MT= ["_MT100","_MT150"]
#MT_legend= [" 50 < M_{T} < 100","100 < M_{T} < 150"]
#MT= ["_NoMT","_HighMT"]
#    JPT=["_LowDPhi", "_HighDPhi"];
JPT=[ "_HighDPhi"]

#lqEta= ["_Barrel", "_Endcap","_TotEta"]
lqEta= [""]
#region = ["_LowPU", "_MedPU","_HighPU"];
region= [""]
#region= ["_ttbarCRDiLep","_ttbarCRSingleLep"]

#logStat=[0]
logStat=[1]




#samples=["WJets_Weight_1","WJets_Weight_PUWeight","WJets_Weight_PUWeightMuCorr","WJets_Weight_Tot"]
#samples=["WJets_Weight_PUWeight","WJets_Weight_PUWeightMuCorr","WJets_Weight_Tot"]
samples=["WJets_Weight_Tot"]



for SSS in samples:
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
                        
                                FileName="TotalRootForLimit_"+SSS+"_MuJet"+NormMC+reg+mt+jpt+etalq+iso+".root"
                                Info=NormMC+reg+mt+jpt+etalq+iso
                                print "---->", FileName
                                MakePlot(FileName,"MuJet","",axisName,Info,Bin,"",yMin,isLOG,reg,mt,SSS,isData)



#MakeTheHistogram("MuJet",NormMC+mt+jpt+dr+iso,NormMC+mt+jpt+dr+iso,"",1)
#
#
#
#
#
#for ch in channelDirectory:
#    for cat in Category:
#        for i in range(0,len(FileNamesInfo)):
#
##            FileName="TotalRootForLimit_PreSelection_"+ch+FileNamesInfo[i][0]+"_OS.root"
#            FileName="TotalRootForLimit_PreSelection_"+ch+FileNamesInfo[i][0]+".root"
#            MakePlot(FileName,ch+cat,FileNamesInfo[i][0],FileNamesInfo[i][1],FileNamesInfo[i][2],FileNamesInfo[i][3],ch+cat)
#
