#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.
#http://root.cern.ch/viewvc/trunk/tutorials/pyroot/hsimple.py?revision=20881&view=markup
__author__ = "abdollahmohammadi"
__date__ = "$Feb 23, 2013 10:39:33 PM$"

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




ROOT.gROOT.SetBatch(True)
#SubRootDir = 'OutFiles_QCD/'
#SubRootDir = 'OutFiles_QCD_NoTrgMC/'
#SubRootDir = 'OutFiles_QCD_40GeVMeT/'
#SubRootDir = 'NewOutFiles_QCDEstim_Data_lowerJetPt/'
#SubRootDir = 'NewOutFiles_QCDEstim_Data_QCD/'
#SubRootDir = 'NewOutFiles_QCDEstim_Data_noMETCut/'
#SubRootDir = 'NewOutFiles_QCDEstim_Data_MediumBTag/'
SubRootDir = 'NewOutFiles_QCDEstim_Data_RemoveTopPtRW/'

verbos_ = False



def add_lumi():
    lowX=0.69
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.03)
    lumi.SetTextFont (   42 )
    lumi.AddText("41.5 fb^{-1} (13 TeV)")
    return lumi

def add_CMS():
    lowX=0.11
    lowY=0.75
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(61)
    lumi.SetTextSize(0.05)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("CMS")
    return lumi

lowX=0.11
lowY=0.68
def add_Preliminary():
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(52)
    lumi.SetTextSize(0.05)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("Preliminary")
    return lumi

def make_legend():
    output = ROOT.TLegend(0.44,lowY+0.06, 0.88, lowY+0.21, "", "brNDC")
    output.SetLineWidth(0)
    output.SetLineStyle(0)
    output.SetFillStyle(0)
    output.SetBorderSize(0)
    output.SetTextFont(62)
    output.SetTextSize(.045)
    return output

############################################################################################################
def _FileReturn(Name, channel,HistoName):
    if not os.path.exists(SubRootDir):
        os.makedirs(SubRootDir)
    myfile = TFile(SubRootDir + Name + '.root')
    Histo =  myfile.Get(channel+HistoName)
#    if Name != "Data":
#        Histo.Scale(1)
    if verbos_: print "0--------->>>>>>  ",SubRootDir,Name, channel+HistoName
    if not os.path.exists("Extra"):
        os.makedirs("Extra")
    NewFile=TFile("Extra/HISTO.root","RECREATE")
    NewFile.WriteObject(Histo,"HISTO")
    myfile.Close()
    return NewFile


####################################################
##   Start Making the Datacard Histograms
####################################################
def MakeTheHistogram(channel,NormQCD,ShapeQCD,Binning,doBinning,HistoType):
    
    
    
    
            Name= "SingleTop"
            SingleTSampleQCDNorm= _FileReturn(Name, channel, NormQCD)
            SingleTSampleQCDShape= _FileReturn(Name, channel, ShapeQCD)
            
            Name= "VV"
            VVSampleQCDNorm= _FileReturn(Name, channel, NormQCD)
            VVSampleQCDShape= _FileReturn(Name, channel, ShapeQCD)
            
            Name= "TTJets"
            TTSampleQCDNorm= _FileReturn(Name, channel, NormQCD)
            TTSampleQCDShape= _FileReturn(Name, channel, ShapeQCD)
            
            Name= "DYJetsToLL"
            ZTTSampleQCDNorm= _FileReturn(Name, channel, NormQCD)
            ZTTSampleQCDShape= _FileReturn(Name, channel, ShapeQCD)
            
            Name= "WJetsToLNu"
            WSampleQCDNorm= _FileReturn(Name, channel, NormQCD)
            WSampleQCDShape= _FileReturn(Name, channel, ShapeQCD)
            
            Name="Data"
            DataSampleQCDNorm= _FileReturn(Name, channel, NormQCD)
            DataSampleQCDShape= _FileReturn(Name, channel, ShapeQCD)
            
            
            
            SingleTSampleQCDShapeHist=SingleTSampleQCDShape.Get("HISTO")
            VVSampleQCDShapeHist=VVSampleQCDShape.Get("HISTO")
            TTSampleQCDShapeHist=TTSampleQCDShape.Get("HISTO")
            ZTTSampleQCDShapeHist=ZTTSampleQCDShape.Get("HISTO")
            WSampleQCDShapeHist=WSampleQCDShape.Get("HISTO")
            DataSampleQCDShapeHist=DataSampleQCDShape.Get("HISTO")
            
            DataSampleQCDShapeHist.Add(SingleTSampleQCDShapeHist, -1)
            DataSampleQCDShapeHist.Add(VVSampleQCDShapeHist, -1)
            DataSampleQCDShapeHist.Add(TTSampleQCDShapeHist, -1)
            DataSampleQCDShapeHist.Add(ZTTSampleQCDShapeHist, -1)
            DataSampleQCDShapeHist.Add(WSampleQCDShapeHist, -1)
            
            
            SingleTSampleQCDNormHist=SingleTSampleQCDNorm.Get("HISTO")
            VVSampleQCDNormHist=VVSampleQCDNorm.Get("HISTO")
            TTSampleQCDNormHist=TTSampleQCDNorm.Get("HISTO")
            ZTTSampleQCDNormHist=ZTTSampleQCDNorm.Get("HISTO")
            WSampleQCDNormHist=WSampleQCDNorm.Get("HISTO")
            DataSampleQCDNormHist=DataSampleQCDNorm.Get("HISTO")
            

            SingleT_qcd=SingleTSampleQCDNormHist.Integral()
            VV_qcd=VVSampleQCDNormHist.Integral()
            TT_qcd=TTSampleQCDNormHist.Integral()
            ZTT_qcd=ZTTSampleQCDNormHist.Integral()
            W_qcd=WSampleQCDNormHist.Integral()
            
            
            
            print "\n ----> Data before subtraction is = ", DataSampleQCDNormHist.Integral()
            QCDEstimation= (DataSampleQCDNormHist.Integral()- (TT_qcd+ZTT_qcd+W_qcd+SingleT_qcd+VV_qcd))
            print "\n ---->  Data aftre ____ subtraction is = ", QCDEstimation , "  which should be =", DataSampleQCDShapeHist.Integral()
            
            
            #            NameOut= "QCD"+str(TauScaleOut[tscale])
            DataSampleQCDShapeHist.Scale(QCDEstimation/DataSampleQCDShapeHist.Integral())  # The shape is from btag-Loose Need get back norm
            if doBinning:    RebinedHist= DataSampleQCDShapeHist.Rebin(len(Binning)-1,"",Binning)
            else : RebinedHist= DataSampleQCDShapeHist
            #            tDirectory.WriteObject(RebinedHist,NameOut)
            
            
            
            #####   This part is for making the QCD purity plot    Draw_QCDPurity.py
            HistoTypeFile=TFile("Extra/%s.root"%HistoType,"RECREATE")
            HistoTypeFile.WriteObject(RebinedHist,"HISTO")
            HistoTypeFile.WriteObject(DataSampleQCDNormHist,"data")
            HistoTypeFile.WriteObject(WSampleQCDNormHist,"W")
            HistoTypeFile.WriteObject(ZTTSampleQCDNormHist,"ZTT")
            HistoTypeFile.WriteObject(TTSampleQCDNormHist,"TT")
            HistoTypeFile.WriteObject(VVSampleQCDNormHist,"VV")
            HistoTypeFile.WriteObject(SingleTSampleQCDNormHist,"SingleT")
            ################################################################################
            
            
            NewShapeForQCD=TFile("Extra/HISTO.root","RECREATE")
            NewShapeForQCD.WriteObject(RebinedHist,"HISTO")
            NewShapeForQCD.WriteObject(DataSampleQCDNormHist,"data")
            NewShapeForQCD.WriteObject(WSampleQCDNormHist,"W")
            NewShapeForQCD.WriteObject(ZTTSampleQCDNormHist,"ZTT")
            NewShapeForQCD.WriteObject(TTSampleQCDNormHist,"TT")
            NewShapeForQCD.WriteObject(VVSampleQCDNormHist,"VV")
            NewShapeForQCD.WriteObject(SingleTSampleQCDNormHist,"SingleT")
            
            
            
            return NewShapeForQCD


#############################################################################################################
##   Fit Functions
#############################################################################################################
def _FIT_Jet(x, p):
    Land = p[2] * TMath.Landau(x[0], p[3], p[4])
    Pol0 = p[0]+p[1]*x[0]
    return Land + Pol0


#def _FIT_Lepton( x,  p) :
#    Land = p[2] * TMath.Landau(x[0], p[3], p[4])
#    Pol0 = p[0]
#    return Land + Pol0


def _FIT_Lepton( x,  p) :
    Land=p[0]+p[1]*x[0]+p[2]*x[0]*x[0]+p[3]*x[0]*x[0]*x[0]+p[4]*x[0]*x[0]*x[0]*x[0]
    #    Land = p[2] * TMath.Landau(x[0], p[3], p[4])
    #    Pol0 = p[0]
    #    return Land + Pol0
    return Land



#############################################################################################################
##   Aplly the Fit Functions (to measure the fake rate )
#############################################################################################################
def ApplyTheFakeRate(x, p,parametrization):

    if parametrization=='Jet':
        Land = p[2] * TMath.Landau(x, p[3], p[4])
        Pol0 = p[0]+p[1]*x
        return Land + Pol0
    elif parametrization=='Lepton':
        if x > 225: x=225
        Land=p[0]+p[1]*pow(x,1)+p[2]*pow(x,2)+p[3]*pow(x,3)+p[4]*pow(x,4)
#        if x > 250: x=250
#        Land = p[2] * TMath.Landau(x, p[3], p[4])
#        Pol0 = p[0]
#        return Land + Pol0
        return Land
    else:
        raise Exception("Not a valid parametrization")


#############################################################################################################
##   Calculating the Fake Rate ---> "Linear Fit, 2 parameters"
#############################################################################################################
def Make_Mu_FakeRate(channelName,Parametrization):
    
    
    
    if Parametrization=='Lepton':
        ObjectPT="_LepPt"
        FR_vs_LeptonPT=1
        BinningFake = array.array("d",[0,60,70,80,90,100,110,120,130,150,200,250])
    elif Parametrization=='Jet':
        ObjectPT="_CloseJetLepPt"
        FR_vs_LeptonPT=0
        BinningFake = array.array("d",[0,60,80,100,120,150,200,250,300,400,500,600,800])
    #    BinningFake = array.array("d",[0,60,80,110,150,200,300,400,500])
    else:
        raise Exception("Not a valid parametrization")



    
    
    HistoFakeNum=ObjectPT+"_HighMT_LowDPhi_TotEta_Iso"
    HistoFakeDeNum=ObjectPT+"_HighMT_LowDPhi_TotEta_Total"

#    HistoFakeNum=ObjectPT+"_LowMT_LowDPhi_TotEta_Iso"
#    HistoFakeDeNum=ObjectPT+"_LowMT_LowDPhi_TotEta_Total"



    
    
    ShapeDeNum=MakeTheHistogram(channelName,HistoFakeDeNum,HistoFakeDeNum,BinningFake,1,"qcdPurity_DeNum%s"%ObjectPT)
    HistoDeNum=ShapeDeNum.Get("HISTO")
    ShapeNum=MakeTheHistogram(channelName,HistoFakeNum,HistoFakeNum,BinningFake,1,"qcdPurity_Num%s"%ObjectPT)
    HistoNum=ShapeNum.Get("HISTO")
    
    
    print "\n---------------------------------------------------------------------------\n"
    print "overal FR = ",  HistoNum.Integral(), "/",  HistoDeNum.Integral(), "  =  ", HistoNum.Integral()/ HistoDeNum.Integral(), "\n"
    print "---------------------------------------------------------------------------\n\n"
    HistoNum.Divide(HistoDeNum)
    
    
    
    canv = TCanvas("canv", "histograms", 600, 600)
    #    HistoNum.SetMinimum(0.5)
    #    HistoNum.GetXaxis().SetRangeUser(0,400)
    if not FR_vs_LeptonPT: canv.SetLogy()
#    canv.SetGridx()
#    canv.SetGridy()
    HistoNum.SetTitle("")
    if FR_vs_LeptonPT: HistoNum.GetXaxis().SetTitle("#mu p_{T} [GeV]")
    else: HistoNum.GetXaxis().SetTitle("Jet p_{T} [GeV]")
    HistoNum.GetYaxis().SetTitle("#mu Fake Rate  (Tight Iso + Id/ Tight Id)")
    HistoNum.GetYaxis().SetTitleOffset(1.3)
    HistoNum.GetYaxis().SetRangeUser(0,.8)
    if not FR_vs_LeptonPT:  HistoNum.GetYaxis().SetRangeUser(0.011,5)
    HistoNum.SetStats(0)
    HistoNum.SetMarkerStyle(20)
    
    

    #####  Fit parameters for fake rate v.s. muon Pt

    if FR_vs_LeptonPT:
        nPar = 5
        theFit=TF1("theFit", _FIT_Lepton, 60, 225,nPar)
        theFit.SetParameter(0, .55)
        theFit.SetParLimits(0, 0.07, 0.234)
        theFit.SetParameter(1, 5.9)
        theFit.SetParameter(2, -1.70)

    else:
        nPar = 5
        theFit=TF1("theFit",_FIT_Jet,70,800,nPar)
#        theFit.SetParLimits(0,    0,     0.5);
##        theFit.SetParameter(0, 0.03)
##        theFit.SetParameter(1, 0)
#        theFit.SetParameter(2, 0.6)
#        theFit.SetParameter(3, -0.6)
##        theFit.SetParameter(4, 196.6)
#Loose
#        theFit.SetParLimits(0,    0,     0.5);
#        theFit.SetParameter(0, 0.03)
#        theFit.SetParameter(1, 0)
#        theFit.SetParameter(2, 0.6)

        theFit.SetParLimits(1, 0.,1)
        theFit.SetParLimits(2, 0.1,3)
#        theFit.SetParLimits(3, 0,1000)
#        theFit.SetParLimits(4, 18, 19)


#        theFit.SetParameter(4, 96.6)

    
    theFit.Print("Quiet")
    HistoNum.Fit("theFit", "R0")
    HistoNum.Draw("E1")
    theFit.SetLineWidth(3)
    theFit.SetLineColor(3)
    FitParam=theFit.GetParameters()
    theFit.Print('Quiet')
    theFit.Draw("SAME")

#    FitParamTot=FitParam[0],FitParam[1],FitParam[2],FitParam[3],FitParam[4]
#    FR_at_400=_FIT_Jet_Function(400,FitParamTot)

#    L=r.TLine(400, FR_at_400, 800, FR_at_400)
#    L.SetLineWidth(4)
#    L.SetLineColor(3)
#    L.SetLineStyle(2)
#    L.Draw("same")

    legende=make_legend()
    legende.AddEntry(HistoNum,"Jet#rightarrow#mu fake rate","lp")
    legende.AddEntry(theFit,"Fit (Pol4)","l")
    
    legende.Draw()
    
    l1=add_lumi()
    l1.Draw("same")
    l2=add_CMS()
    l2.Draw("same")
    l3=add_Preliminary()
    l3.Draw("same")


    categ  = ROOT.TPaveText(0.51, 0.45+0.013, 0.93, 0.60+0.155, "NDC")
    categ.SetBorderSize(   0 )
    categ.SetFillStyle(    0 )
    categ.SetTextAlign(   12 )
    categ.SetTextSize ( 0.04 )
    categ.SetTextColor(    1 )
    categ.SetTextFont (   41 )
    categ.AddText(channelName+" channel")
#    categ.Draw()


    canv.SaveAs("muFakeRate"+ObjectPT+".pdf")
    canv.SaveAs("muFakeRate"+ObjectPT+".root")
    
    
#    if FR_vs_LeptonPT:
#        return FitParam[0],FitParam[1],FitParam[2]
#    else:
    return FitParam[0],FitParam[1],FitParam[2],FitParam[3],FitParam[4]


##########################################    ##########################################    ##########################################
##########################################    ##########################################    ##########################################
##########################################    ##########################################    ##########################################

if __name__ == "__main__":
    FR_FitMaram=Make_Mu_FakeRate("MuJet","Lepton")
    FR_FitMaram=Make_Mu_FakeRate("MuJet","Jet")



