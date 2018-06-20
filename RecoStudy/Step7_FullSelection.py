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
from ctypes import *
import ROOT as r
import re
from array import array


##### Get Jet to Tau FR
from Step1_JetToMuFR_Data import Make_Mu_FakeRate
from Step1_JetToMuFR_Data import *
from Step5_TT_W_ScaleFactor import *
##### Get Jet to Tau FR

gROOT.Reset()
import os


ROOT.gROOT.SetBatch(True)

#SubRootDir = 'NewOutFiles_FinalSelection_First/'
#SubRootDir = 'NewOutFiles_FinalSelection_FixBSF/'
#SubRootDir = 'NewOutFiles_FinalSelection_noBtagVeto/'
#SubRootDir = 'NewOutFiles_FinalSelection_Approval_v1/'
SubRootDir = 'NewOutFiles_FinalSelection_Approval_v3_relaxQCD/'


verbos_ = True
JetScale = ["JetESDown", "", "JetESUp"]
JetResol = ["JetERDown", "", "JetERUp"]
#JetResol = [""]
METScale = ["METUESDown", "", "METUESUp","METJESDown","METJESUp"]
SystematicTopPtReWeight = ["TopPtRWUp","TopPtRWDown"]
FinalName = ["_mj"]

SystematicsystWk_factor= ["_ewkKfactor_WDown","_ewkKfactor_WUp"]
SystematicsystZk_factor= ["_ewkKfactor_ZDown","_ewkKfactor_ZUp"]


Systematicsyst_PDF_Alpha_W=["_W_PDF_AlphaS_Down","_W_PDF_AlphaS_Up"]


############################################################################################################
def _FileReturn(Name, channel,cat,HistoName,PostFixJet,PostFixJetRes,PostFixMET):

    if not os.path.exists(SubRootDir):
        os.makedirs(SubRootDir)
    myfile = TFile(SubRootDir + Name + '.root')
    if verbos_: print "##### --->>>>>>> File name is ", SubRootDir + Name + '.root'  "   and histo is -->  ", channel+HistoName + cat+PostFixJet+PostFixJetRes+PostFixMET
    Histo =  myfile.Get(channel+HistoName + cat+PostFixJet+PostFixJetRes+PostFixMET)
    if not os.path.exists("Extra"):
        os.makedirs("Extra")
    NewFile=TFile("Extra/XXX.root","RECREATE")
    NewFile.WriteObject(Histo,"XXX")
    myfile.Close()
    return NewFile


####################################################
##   Start Making the Datacard Histograms
####################################################
def MakeTheHistogram(channel,NormMC,NormQCD,ShapeQCD,NormMCTT,chl,Binning):
    
    
    signal = ['Codex_']
    signalName = ['Codex_']
#    mass = [
#    '800',
#    '900',
#    '1000',
#    '1100',
#    '1200',
#    '1300',
#    '1400',
#    '1500'
#    ]


#    TOTMASS = ['800','900','1000','1100','1200','1300','1400','1500']
    category = [""]

    SystematicsystWk_factor= ["_ewkKfactor_WDown","_ewkKfactor_WUp"]
    SystematicsystZk_factor= ["_ewkKfactor_ZDown","_ewkKfactor_ZUp"]

    JetScaleOut = ["_CMS_scale_jes"+"Down", "", "_CMS_scale_jes"+"Up"]
    JetResolOut = ["_CMS_scale_jer"+"Down", "", "_CMS_scale_jer"+"Up"]
#    JetResolOut = [""]
    METScaleOut = ["_CMS_scale_met_UES"+"Down", "", "_CMS_scale_met_UES"+"Up","_CMS_scale_met_JES"+"Down", "_CMS_scale_met_JES"+"Up"]
    Signal_Unc_TopPTRW = ["_CMS_top_pt_Reweighting"+"Up","_CMS_top_pt_Reweighting"+"Down"]

    myOut = TFile(FinalName[chl]+NormMC+".root" , 'RECREATE') # Name Of the output file


    for NameCat in category:
        print "starting NameCat=%s and channel=%s and HistoName=%s "%(NameCat, channel, NormMC)

        tDirectory= myOut.mkdir(channel + str(NameCat))
        tDirectory.cd()
        for jscale in range(len(JetScale)):
            for jres in range(len(JetResol)):
                for mscale in range(len(METScale)):
                
                    if jscale != 1 and mscale!=1 : continue
                    if jscale != 1 and jres!=1 : continue
                    if jres != 1 and mscale!=1 : continue
                    ################################################
                    #   Filling Signal
                    ################################################
                    for sig in range(len(signal)):
                        for m in range(1,45):
                            print "===>", str(m)

                            print "--------------------------------------------------->     Processing  Signal ", signal[sig]+str(m)
                            tDirectory.cd()

                            Name= str(signal[sig])+str(m)
                            NameOut= str(signalName[sig]) +str(m)+str(JetScaleOut[jscale])+str(JetResolOut[jres])+str(METScaleOut[mscale])

                                    
                            NormFile= _FileReturn(Name, channel,NameCat, NormMC, JetScale[jscale] , JetResol[jres] , METScale[mscale])
                            NormHisto=NormFile.Get("XXX")
                    
                            NormHisto.Scale(0.00115)
                            RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
                            tDirectory.WriteObject(RebinedHist,NameOut)


                    ################################################
                    #  Filling SingleTop
                    ################################################
                    print "--------------------------------------------------->     Processing SingleTop"
                    tDirectory.cd()
                
                    Name= "SingleTop"
                    NameOut= "SingleTop"+str(JetScaleOut[jscale])+str(JetResolOut[jres])+str(METScaleOut[mscale])
                    
                    NormFile= _FileReturn(Name, channel,NameCat, NormMC, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                    NormHisto=NormFile.Get("XXX")
                    
                    RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
                    tDirectory.WriteObject(RebinedHist,NameOut)
                    

                    ################################################
                    #  Filling VV
                    ################################################
                    print "--------------------------------------------------->     Processing VV"
                    tDirectory.cd()
                
                    Name= "VV"
                    NameOut= "VV"+str(JetScaleOut[jscale])+str(JetResolOut[jres])+str(METScaleOut[mscale])
                    
                    NormFile= _FileReturn(Name, channel,NameCat, NormMC, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                    NormHisto=NormFile.Get("XXX")
                    
                    RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
                    tDirectory.WriteObject(RebinedHist,NameOut)
                    



                    ################################################
                    #  Filling TOP
                    ################################################
                    print "--------------------------------------------------->     Processing TOP"
                    tDirectory.cd()

                    Name= "TTJets"
                    NameOut= "TT"+str(JetScaleOut[jscale])+str(JetResolOut[jres])+str(METScaleOut[mscale])

                    
                    print NormMCTT
                    NormFile= _FileReturn(Name, channel,NameCat, NormMCTT, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                    NormHisto=NormFile.Get("XXX")
                    
                    NormFileShape= _FileReturn(Name, channel,NameCat, NormMC, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                    NormHistoShape=NormFileShape.Get("XXX")
                    
                    
                    
                    
                    NormHistoShape.Scale(NormHisto.Integral()*1.0/NormHistoShape.Integral())
                    NormHistoShape.Scale(SF_TT_SingleLep())
                    RebinedHist= NormHistoShape.Rebin(len(Binning)-1,"",Binning)
                    
                    ##  To cure negative bins
                    for jbin in range(0,RebinedHist.GetNbinsX()):
                        if RebinedHist.GetBinContent(jbin) < 0: RebinedHist.SetBinContent(jbin,0.001)


                    tDirectory.WriteObject(RebinedHist,NameOut)
                    FinalTTbarNormalization=RebinedHist.Integral() # needed for top pt reweighting
                    
                    ###############  Systematics on Shape and Norm for  qcd Scale #### FIX ME need to add scale back
                    if jscale==1 and mscale==1 and jres==1:
                        qcdScaleTT=TFile('../interface/QCDScale_TTbar.root','R')
                        ttScaleUp=qcdScaleTT.Get('qcdScaleUp')
                        ttScaleDown=qcdScaleTT.Get('qcdScaleDown')
                
                        ScaleUpTT=RebinedHist.Clone()
                        ScaleDownTT=RebinedHist.Clone()
                        for ibin in range(RebinedHist.GetNbinsX()):
                            ScaleUpTT.SetBinContent(ibin+1,RebinedHist.GetBinContent(ibin+1)*ttScaleUp.GetBinContent(ibin+1))
                            ScaleDownTT.SetBinContent(ibin+1,RebinedHist.GetBinContent(ibin+1)*ttScaleDown.GetBinContent(ibin+1))
                    
                        tDirectory.WriteObject(ScaleUpTT,'TT_qcdScale_TTUp')
                        tDirectory.WriteObject(ScaleDownTT,'TT_qcdScale_TTDown')

    
                    ###############  Systematics on Shape and Norm for  To PT Reweighting ####
                    if jscale==1 and mscale==1 and jres==1:
                        for systTopRW in range(len(SystematicTopPtReWeight)):
                            tDirectory.cd()

                            HistogramNorm = NormMCTT
                            HistogramShape = NormMC.replace("_LQMass","_LQMass"+SystematicTopPtReWeight[systTopRW])
                            
                            NameOut= "TT"+str(Signal_Unc_TopPTRW[systTopRW])

                            NormFile= _FileReturn(Name, channel,NameCat, HistogramNorm, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                            NormHisto=NormFile.Get("XXX")
                            
                            NormFileShape= _FileReturn(Name, channel,NameCat, HistogramShape, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                            NormHistoShape=NormFileShape.Get("XXX")

                            NormHistoShape.Scale(NormHisto.Integral()*1.0/NormHistoShape.Integral())
                            NormHistoShape.Scale(SF_TT_SingleLep())
                            RebinedHist= NormHistoShape.Rebin(len(Binning)-1,"",Binning)
                            
                            ##  To cure negative bins
                            for jbin in range(0,RebinedHist.GetNbinsX()):
                                if RebinedHist.GetBinContent(jbin) < 0: RebinedHist.SetBinContent(jbin,0.001)
                            
                            RebinedHist.Scale(FinalTTbarNormalization/RebinedHist.Integral())
                            tDirectory.WriteObject(RebinedHist,NameOut)
                                
        
                    ################################################
                    #  Filling ZTT
                    ################################################
                    print "--------------------------------------------------->     Processing ZTT"
                    tDirectory.cd()

                    Name= "DYJetsToLL"
                    NameOut= "ZTT"+str(JetScaleOut[jscale])+str(JetResolOut[jres])+str(METScaleOut[mscale])
                    
                    NormFile= _FileReturn(Name, channel,NameCat, NormMC, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                    NormHisto=NormFile.Get("XXX")
                    
                    RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
                    tDirectory.WriteObject(RebinedHist,NameOut)
                    
                    
                    
                    ###############  Systematics on DY k-factor for ewk correction ####
                    if jscale==1 and mscale==1 and jres==1:
                        for zkfactor in range(len(SystematicsystZk_factor)):
                            tDirectory.cd()
                            
                            HistogramNorm = NormMC+SystematicsystZk_factor[zkfactor]
                            
                            NameOut= "ZTT"+str(SystematicsystZk_factor[zkfactor])
                            
                            NormFile= _FileReturn(Name, channel,NameCat, HistogramNorm, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                            NormHisto=NormFile.Get("XXX")
                            
                            NormFileShape= _FileReturn(Name, channel,NameCat, HistogramNorm, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                            NormHistoShape=NormFileShape.Get("XXX")
                            
                            NormHistoShape.Scale(NormHisto.Integral()*1.0/NormHistoShape.Integral())
                            RebinedHist= NormHistoShape.Rebin(len(Binning)-1,"",Binning)
                            tDirectory.WriteObject(RebinedHist,NameOut)
                                
                    

                    ################################################
                    #  Filling W
                    ################################################
                    print "--------------------------------------------------->     Processing W"
                    tDirectory.cd()
        
                    Name="WJetsToLNu"
                    NameOut= "W"+str(JetScaleOut[jscale])+str(JetResolOut[jres])+str(METScaleOut[mscale])
                
                    NormFileWNoCor= _FileReturn(Name, channel,NameCat, NormMC.replace("","") +"", JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                    NormHistoWNoCor=NormFileWNoCor.Get("XXX")
                    WNoCorNormaliztaion=NormHistoWNoCor.Integral()
                    
                    
                    NormFile= _FileReturn(Name, channel,NameCat, NormMC, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                    NormHisto=NormFile.Get("XXX")
                    
                    NormHisto.Scale(WNoCorNormaliztaion/NormHisto.Integral())
                    NormHisto.Scale(SF_W_SingleLep())
                    print "--------------->    NormHisto with NO correction", NormHisto.Integral()
                    RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
                    tDirectory.WriteObject(RebinedHist,NameOut)
                    
                    
                    #                    ###############  Systematics on Shape and Norm for  qcd Scale ####  NOT USED ANYMORE
                    #                    if jscale==1 and mscale==1 and jres==1:
                    #                        qcdScaleW=TFile('../interface/QCDScale_W.root','R')
                    #                        wScaleUp=qcdScaleW.Get('qcdScaleUp')
                    #                        wScaleDown=qcdScaleW.Get('qcdScaleDown')
                    #
                    #                        ScaleUpW=RebinedHist.Clone()
                    #                        ScaleDownW=RebinedHist.Clone()
                    #                        for ibin in range(RebinedHist.GetNbinsX()):
                    #                            ScaleUpW.SetBinContent(ibin+1,RebinedHist.GetBinContent(ibin+1)*wScaleUp.GetBinContent(ibin+1))
                    #                            ScaleDownW.SetBinContent(ibin+1,RebinedHist.GetBinContent(ibin+1)*wScaleDown.GetBinContent(ibin+1))
                    #
                    #                        tDirectory.WriteObject(ScaleUpW,'W_qcdScale_WUp')
                    #                        tDirectory.WriteObject(ScaleDownW,'W_qcdScale_WDown')
                    
                    
                    
                    ###############  Systematics on W k-factor for ewk correction ####
                    if jscale==1 and mscale==1 and jres==1:
                        for wpdf in range(len(Systematicsyst_PDF_Alpha_W)):
                            tDirectory.cd()
                            
                            HistogramNorm = NormMC+Systematicsyst_PDF_Alpha_W[wpdf]
                            #                            HistogramNorm = NormMC.replace("_LQMass","_LQMass"+Systematicsyst_PDF_Alpha_W[wpdf])
                            
                            NameOut= "W"+str(Systematicsyst_PDF_Alpha_W[wpdf])
                            
                            NormFile= _FileReturn(Name, channel,NameCat, HistogramNorm, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                            NormHisto=NormFile.Get("XXX")
                            print "--------------->    NormHisto Systematicsyst_PDF_Alpha_W XXXXXX correction", NormHisto.Integral()
                            
                            NormFileShape= _FileReturn(Name, channel,NameCat, HistogramNorm, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                            NormHistoShape=NormFileShape.Get("XXX")
                            
                            NormHistoShape.Scale(NormHisto.Integral()*1.0/NormHistoShape.Integral())
                            NormHistoShape.Scale(SF_W_SingleLep())
                            print "--------------->    NormHisto Systematicsyst_PDF_Alpha_W with correction", NormHistoShape.Integral()
                            RebinedHist= NormHistoShape.Rebin(len(Binning)-1,"",Binning)
                            tDirectory.WriteObject(RebinedHist,NameOut)
                
                
                
                
                    ###############  Systematics on W k-factor for ewk correction ####
                    if jscale==1 and mscale==1 and jres==1:
                        for wkfactor in range(len(SystematicsystWk_factor)):
                            tDirectory.cd()
                            
                            HistogramNorm = NormMC+SystematicsystWk_factor[wkfactor]
                            #                            HistogramNorm = NormMC.replace("_LQMass","_LQMass"+SystematicsystWk_factor[wkfactor])
                            
                            NameOut= "W"+str(SystematicsystWk_factor[wkfactor])
                            
                            NormFile= _FileReturn(Name, channel,NameCat, HistogramNorm, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                            NormHisto=NormFile.Get("XXX")
                            print "--------------->    NormHisto SystematicsystWk_factor XXXXXX correction", NormHisto.Integral()
                            
                            NormFileShape= _FileReturn(Name, channel,NameCat, HistogramNorm, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                            NormHistoShape=NormFileShape.Get("XXX")
                            
                            NormHistoShape.Scale(NormHisto.Integral()*1.0/NormHistoShape.Integral())
                            NormHistoShape.Scale(SF_W_SingleLep())
                            print "--------------->    NormHisto  SystematicsystWk_factor with correction", NormHistoShape.Integral()
                            RebinedHist= NormHistoShape.Rebin(len(Binning)-1,"",Binning)
                            tDirectory.WriteObject(RebinedHist,NameOut)
                                
                                

                    ################################################
                    #  Filling QCD
                    ################################################
                    if jscale==1 and mscale==1 and jres==1:
                        print "--------------------------------------------------->     Processing QCD"
                        tDirectory.cd()
                        
                        Name= "SingleTop"
                        SingleTSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                        SingleTSampleQCDShape= _FileReturn(Name, channel,NameCat, ShapeQCD, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                        
                        Name= "VV"
                        VVSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                        VVSampleQCDShape= _FileReturn(Name, channel,NameCat, ShapeQCD, JetScale[jscale] , JetResol[jres] , METScale[mscale] )

                        Name= "TTJets"
                        TTSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                        TTSampleQCDShape= _FileReturn(Name, channel,NameCat, ShapeQCD, JetScale[jscale] , JetResol[jres] , METScale[mscale] )

                        Name= "DYJetsToLL"
                        ZTTSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                        ZTTSampleQCDShape= _FileReturn(Name, channel,NameCat, ShapeQCD, JetScale[jscale] , JetResol[jres] , METScale[mscale] )

                        Name= "WJetsToLNu"
                        WSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                        WSampleQCDShape= _FileReturn(Name, channel,NameCat, ShapeQCD, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                                    
                        Name="Data"
                        DataSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                        DataSampleQCDShape= _FileReturn(Name, channel,NameCat, ShapeQCD, JetScale[jscale] , JetResol[jres] , METScale[mscale] )



                        SingleTSampleQCDShapeHist=SingleTSampleQCDShape.Get("XXX")
                        VVSampleQCDShapeHist=VVSampleQCDShape.Get("XXX")
                        TTSampleQCDShapeHist=TTSampleQCDShape.Get("XXX")
                        ZTTSampleQCDShapeHist=ZTTSampleQCDShape.Get("XXX")
                        WSampleQCDShapeHist=WSampleQCDShape.Get("XXX")
                        DataSampleQCDShapeHist=DataSampleQCDShape.Get("XXX")

                        print "\n---->   ##########\nlooseQCDShape before=",    DataSampleQCDShapeHist.Integral()
                        
                        if (SingleTSampleQCDShapeHist) : DataSampleQCDShapeHist.Add(SingleTSampleQCDShapeHist, -1)
                        if (VVSampleQCDShapeHist): DataSampleQCDShapeHist.Add(VVSampleQCDShapeHist, -1)
                        DataSampleQCDShapeHist.Add(TTSampleQCDShapeHist, -1)
                        DataSampleQCDShapeHist.Add(ZTTSampleQCDShapeHist, -1)
                        DataSampleQCDShapeHist.Add(WSampleQCDShapeHist, -1)
                        print "\n---->   ##########\nlooseQCDShaoe after=",    DataSampleQCDShapeHist.Integral()


                        SingleTSampleQCDNormHist=SingleTSampleQCDNorm.Get("XXX")
                        VVSampleQCDNormHist=VVSampleQCDNorm.Get("XXX")
                        TTSampleQCDNormHist=TTSampleQCDNorm.Get("XXX")
                        TTSampleQCDNormHist.Scale(1.12)
                        ZTTSampleQCDNormHist=ZTTSampleQCDNorm.Get("XXX")
                        WSampleQCDNormHist=WSampleQCDNorm.Get("XXX")
                        WSampleQCDNormHist.Scale(1.11)
                        DataSampleQCDNormHist=DataSampleQCDNorm.Get("XXX")
                        

                        if (SingleTSampleQCDNormHist) : DataSampleQCDNormHist.Add(SingleTSampleQCDNormHist, -1)
                        if (VVSampleQCDNormHist): DataSampleQCDNormHist.Add(VVSampleQCDNormHist, -1)
                        DataSampleQCDNormHist.Add(TTSampleQCDNormHist, -1)
                        DataSampleQCDNormHist.Add(ZTTSampleQCDNormHist, -1)
                        DataSampleQCDNormHist.Add(WSampleQCDNormHist, -1)
                        
                        
                        
                        
                        print "\n##########\nlooseQCDNORM after=",    DataSampleQCDNormHist.Integral()                        
                        FR_FitMaram=Make_Mu_FakeRate(channel,'Lepton')
                        QCDEstimation=0
                        for bin in xrange(50,1000):
                            value=DataSampleQCDNormHist.GetBinContent(bin)
#                            if value < 0 : value=0
                            FR= ApplyTheFakeRate(bin+1.5,FR_FitMaram,'Lepton')
                            if FR> 0.9: FR=0.9
                            QCDEstimation += value * FR/(1-FR)
                        if verbos_: print "\n##########\n QCDEstimation",    QCDEstimation


#                        print "\n##########\nlooseQCDNORM after=",    DataSampleQCDNormHist.Integral()
#                        FR_FitMaram=Make_Mu_FakeRate(channel)
#                        QCDEstimation=0
#                        for bin in xrange(50,1000):
#                            value=DataSampleQCDNormHist.GetBinContent(bin)
#                            if value < 0 : value=0
#                            FR= _FIT_Jet_Function(bin+1.5,FR_FitMaram)
#                            if FR> 0.9: FR=0.9
#                            QCDEstimation += value * FR/(1-FR)
#                        print "\n##########\n QCDEstimation",    QCDEstimation

                        NameOut= "QCD"+str(JetScaleOut[jscale])+str(JetResolOut[jres])+str(METScaleOut[mscale])
                        DataSampleQCDShapeHist.Scale(QCDEstimation/DataSampleQCDShapeHist.Integral())  # The shape is from btag-Loose Need get back norm
                        RebinedHist= DataSampleQCDShapeHist.Rebin(len(Binning)-1,"",Binning)
                        
                        ##  To cure negative bins
                        for jbin in range(0,RebinedHist.GetNbinsX()):
                            if RebinedHist.GetBinContent(jbin) < 0: RebinedHist.SetBinContent(jbin,0.001)
                        
                        tDirectory.WriteObject(RebinedHist,NameOut)

                    ################################################
                    #  Filling Data
                    ################################################
                    if jscale==1 and mscale==1 and jres==1:
                        print "--------------------------------------------------->     Processing Data"
                        tDirectory.cd()

                        Name='Data'
                        NameOut='data_obs'

                        NormFile= _FileReturn(Name, channel,NameCat, NormMC, JetScale[jscale] , JetResol[jres] , METScale[mscale] )
                        NormHisto=NormFile.Get("XXX")
                    
                        RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
                        tDirectory.WriteObject(RebinedHist,NameOut)




    myOut.Close()

if __name__ == "__main__":
#    RecoStudy $ for((i=0;i<=2000;i+=50)); do printf "\t $i,"; done
    Binning = array("d",[0,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000])
#    Binning = array("d",[0,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000,1050,1100,1150,1200,1250,1300,1350,1400,1450,1500,1550,1600,1650,1700,1750,1800,1850,1900,1950,2000])


#    Met_Cat= ["_MET100", "_MET150","_MET200", "_MET250","_MET300", "_MET350","_MET400", "_MET450","_MET500"]
#    MT_Cat = ["_MT100", "_MT150","_MT200", "_MT250","_MT300", "_MT350","_MT400", "_MT450","_MT500"]

    Met_Cat= [ "_MET100"]
    MT_Cat = ["_MT500"]
#    MT_Cat = ["_MT100"]

    for met in Met_Cat:
        for mt in MT_Cat:


            NormMC="_LQMass"+mt+met+"_Iso"
            NormQCD="_LepPt"+mt+met+"_AntiIso"
#            NormQCD="_CloseJetLepPt"+mt+met+"_AntiIso"
            ShapeQCD="_LQMass"+"_MT400"+met+"_AntiIso_NoDPhi"
            NormMCTT="_LQMass_NoTopRW"+mt+met+"_Iso"
            
            MakeTheHistogram("MuJet",NormMC,NormQCD,ShapeQCD,NormMCTT,0,Binning)

