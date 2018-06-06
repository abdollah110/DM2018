import os
import ROOT
from ROOT import *

def MakeCompare(r1,hist1,r2,hist2,name,RB_,XTit,name2):

    ROOT.gStyle.SetFrameLineWidth(3)
    ROOT.gStyle.SetLineWidth(3)
    ROOT.gStyle.SetOptStat(0)
    
    
    file1=TFile(r1,"open")
    file2=TFile(r2,"open")
    
    print "----->file =1 %s   file2=%s    histo=%s"%(r1,r2,hist1)

#    Histo1=file1.Get(cat1+'/'+hist1)
    Histo1=file1.Get(hist1)
    Histo1.SetLineColor(2)
    Histo1.SetLineWidth(2)
    Histo1.SetMarkerColor(3)
    Histo1.SetMarkerStyle(24)
    Histo1.Rebin(RB_)
    Histo1.SetMaximum(Histo1.GetMaximum()*2)
    print Histo1.GetName(), Histo1.Integral()
#    Histo1.Scale(1/Histo1.Integral())

#    Histo2=file2.Get(cat2+'/'+hist2)
    Histo2=file2.Get(hist2)
    print 'fileis',r1, '  histo is', hist2
    Histo2.SetLineColor(3)
    Histo2.SetMarkerColor(3)
    Histo2.SetMarkerStyle(20)
    Histo2.SetLineWidth(2)
    Histo2.Rebin(RB_)
    print Histo2.GetName(), Histo2.Integral()
#    Histo2.Scale(1/Histo2.Integral())

    
#    Histo3=file.Get(Cat+'/'+hist3)
#    Histo3.SetLineColor(4)
#    Histo3.SetLineWidth(2)
#
    Can=TCanvas("canvas","",0,0,600,600)
#    Can.SetLogy()



    Xname1= r1.replace('NewOutFiles_Preselection_Approval_V1/TotalRootForLimit_PreSelection_MuJet','').replace('.root','').replace('_HighDPhi_Iso','')
    Xname2= hist1.replace('MuJet/','')
    
    Histo1.SetTitle('')
    Histo1.GetXaxis().SetTitle(Xname1)
    Histo1.GetXaxis().SetLabelSize(0.034)
    Histo1.GetXaxis().SetNdivisions(505)
    Histo1.GetXaxis().SetTitleSize(0.045)
    Histo1.GetXaxis().SetTitleOffset(0.7)
    Histo1.GetXaxis().SetLabelSize(0.04)
    Histo1.GetXaxis().SetTitleFont(42)
    Histo1.GetYaxis().SetTitle("Events")
#
#
#
#    
#


    
    
    Histo1.Draw('F')
    Histo2.Draw('Fsame')
#    Histo3.Draw('same')
#
    leg=TLegend(.45,.7,.9,.9, "", "brNDC")
    leg.SetLineWidth(1)
    leg.SetLineStyle(0)
    leg.SetFillStyle(0)
#    leg.SetBorderSize(0)
    leg.SetTextFont(62)
#    leg.AddEntry(Histo1,'Mu channel','l')
#    leg.AddEntry(Histo2,'electron channel','l')
#    leg.AddEntry(Histo1,'HT-based kFactor (ala Mono-Jet)','l')
#    leg.AddEntry(Histo2,'Mass-based kFactor (ala Wprime)','l')
    leg.AddEntry(Histo1,'with PU reweighting','lp')
    leg.AddEntry(Histo2,'no PU reweighting','lp')
#    leg.AddEntry(Histo3,hist3.replace("_CMS_scale",""),'l')
    leg.Draw()

#    Xname1= r1.replace('OutFiles_Preselection_Approval_V1/TotalRootForLimit_PreSelection_MuJet','').replace('.root','')
#    Xname2= hist1.replace('MuJet/','')

    categ  = ROOT.TPaveText(0.15, 0.65+0.013, 0.43, 0.80+0.155, "NDC")
    categ.SetBorderSize(   0 )
    categ.SetFillStyle(    0 )
    categ.SetTextAlign(   12 )
    categ.SetTextSize ( 0.05 )
    categ.SetTextColor(    9 )
    categ.AddText(Xname2)
    categ.Draw()
    
    
    
    Can.SaveAs('OUT_%s_%s.pdf'%(Xname1,Xname2))


#F1='OutFiles_PreSelection/Data.root'
#F2='OutFiles_PreSelection_SampleLQ1/Data.root'


#F1='OutFiles_Excess_LQMore1100/Data.root'
#F2='Data_LQ1100.root'



#process=[
#         ['Jet_LepEta_MT500_HighDPhi_Iso',10,'Lepton #eta'],
#         ['Jet_JetEta_MT500_HighDPhi_Iso',10,'Jet #eta'],
#         ['Jet_LQMass_MT500_HighDPhi_Iso',10,'M_{LQ} GeV'],
#         ['Jet_MET_MT500_HighDPhi_Iso',10,'MET GeV'],
#         ['Jet_JetPt_MT500_HighDPhi_Iso',50,'Jet pT GeV'],
#         ['Jet_LepPt_MT500_HighDPhi_Iso',50,'lepton pT GeV'],
#         ['Jet_dEta_Mu_Jet_MT500_HighDPhi_Iso',50,'#Delta#eta lep,jet']
#         ]
#
#
#for i in range(0,len(process)):
##    MakeCompare(F1,'Mu'+process[i][0],F2,'Ele'+process[i][0].replace('_HighMT','_MT500'),process[i][0],process[i][1],process[i][2])
#    MakeCompare(F1,'Mu'+process[i][0],F2,'Ele'+process[i][0],process[i][0],process[i][1],process[i][2],'_MTHigh')
#    MakeCompare(F1,'Mu'+process[i][0].replace('_MT500','_HighMT'),F2,'Ele'+process[i][0].replace('_MT500','_HighMT'),process[i][0],process[i][1],process[i][2],'_MT500')
#



#MakeCompare('test_W_oldkfactor_ChangeMutoL.root','MuJet_LQMass_HighMT_HighDPhi_Iso','test_W_NewmassDep_Kfactor.root','MuJet_LQMass_HighMT_HighDPhi_Iso','HighMTMLQ',10,'M_{LQ} GeV','M_{T} > 100 GeV')
#MakeCompare('test_W_oldkfactor_ChangeMutoL.root','MuJet_LQMass_MT500_HighDPhi_Iso','test_W_NewmassDep_Kfactor.root','MuJet_LQMass_MT500_HighDPhi_Iso','MT500MLQ',10,'M_{LQ} GeV','M_{T} > 500 GeV')

#MakeCompare('ScaleCorretion/Codex.root','MuJet_LQMassCorrMuScale_MT500_HighDPhi_Iso','ScaleCorretion/Codex.root','MuJet_LQMass_MT500_HighDPhi_Iso','HighMTMLQ',10,'M_{LQ} GeV','M_{T} > 500 GeV')
#MakeCompare('ScaleCorretion/WJet.root','MuJet_LQMassCorrMuScale_MT500_HighDPhi_Iso','ScaleCorretion/WJet.root','MuJet_LQMass_MT500_HighDPhi_Iso','HighMTMLQ',10,'M_{LQ} GeV','M_{T} > 500 GeV')
#MakeCompare('ScaleCorretion/Data.root','MuJet_LQMassCorrMuScale_MT500_HighDPhi_Iso','ScaleCorretion/Data.root','MuJet_LQMass_MT500_HighDPhi_Iso','HighMTMLQ',10,'M_{LQ} GeV','M_{T} > 500 GeV')


AllHist=['TotalRootForLimit_PreSelection_MuJet_JetEta_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_JetEta_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_JetEta_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_JetEta_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_JetEta_NoMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_JetPt_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_JetPt_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_JetPt_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_JetPt_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_JetPt_NoMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LQMass_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LQMass_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LQMass_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LQMass_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LQMass_NoMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LepEta_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LepEta_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LepEta_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LepEta_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LepEta_NoMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LepPhi_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LepPhi_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LepPhi_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LepPhi_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LepPhi_NoMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LepPt_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LepPt_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LepPt_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LepPt_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_LepPt_NoMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_METPhi_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_METPhi_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_METPhi_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_METPhi_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_METPhi_NoMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_MET_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_MET_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_MET_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_MET_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_MET_NoMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_NumBJet_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_NumBJet_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_NumBJet_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_NumBJet_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_NumBJet_NoMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_NumJet_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_NumJet_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_NumJet_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_NumJet_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_NumJet_NoMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_ST_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_ST_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_ST_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_ST_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_ST_NoMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dPhi_Jet_Met_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dPhi_Jet_Met_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dPhi_Jet_Met_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dPhi_Jet_Met_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dPhi_Jet_Met_NoMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dPhi_Mu_Jet_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dPhi_Mu_Jet_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dPhi_Mu_Jet_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dPhi_Mu_Jet_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dPhi_Mu_Jet_NoMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dPhi_Mu_Met_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dPhi_Mu_Met_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dPhi_Mu_Met_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dPhi_Mu_Met_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dPhi_Mu_Met_NoMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dR_Mu_Jet_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dR_Mu_Jet_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dR_Mu_Jet_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dR_Mu_Jet_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_dR_Mu_Jet_NoMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_nVtx_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_nVtx_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_nVtx_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_nVtx_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_nVtx_NoMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_nVtx_NoPU_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_nVtx_NoPU_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_nVtx_NoPU_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_nVtx_NoPU_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_nVtx_NoPU_NoMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_recoHT_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_recoHT_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_recoHT_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_recoHT_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_recoHT_NoMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_tmass_LQMet_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_tmass_LQMet_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_tmass_LQMet_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_tmass_LQMet_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_tmass_LQMet_NoMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_tmass_MuMet_HighMT_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_tmass_MuMet_MT300_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_tmass_MuMet_MT500_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_tmass_MuMet_MT50To150_HighDPhi_Iso.root',
 'TotalRootForLimit_PreSelection_MuJet_tmass_MuMet_NoMT_HighDPhi_Iso.root']




Samples=['W','VV','ZTT','SingleTop','TT']

 
for histo in AllHist:
    for sam in Samples:

        MakeCompare('NewOutFiles_Preselection_Approval_V1/'+histo,'MuJet/'+sam, 'NewOutFiles_Preselection_Approval_V2_NoPUWeighting/'+histo,'MuJet/'+sam ,'allEta',10,'M_{LQ}_{cor} - M_{LQ}_{uncor} / M_{LQ}_{uncor}','M_{T} > 500 GeV')

#MakeCompare('ScaleCorretion/Codex_EtaCheckMuCor.root','MuJet_LQMassDifference_Barrel_MT500_HighDPhi_Iso','ScaleCorretion/Codex_EtaCheckMuCor.root','MuJet_LQMassDifference_Barrel_MT500_HighDPhi_Iso','Barrel',10,'M_{LQ}_{cor} - M_{LQ}_{uncor} / M_{LQ}_{uncor}','M_{T} > 500 GeV, |#eta| < 1.5')
#
#MakeCompare('ScaleCorretion/Codex_EtaCheckMuCor.root','MuJet_LQMassDifference_EndCap_MT500_HighDPhi_Iso','ScaleCorretion/Codex_EtaCheckMuCor.root','MuJet_LQMassDifference_EndCap_MT500_HighDPhi_Iso','Endcap',10,'M_{LQ}_{cor} - M_{LQ}_{uncor} / M_{LQ}_{uncor}','M_{T} > 500 GeV, |#eta > 1.5|')





#MakeCompare('test_W_oldkfactor_ChangeMutoL.root','MuJet_LQMass_MT500_HighDPhi_Iso','test_W_NewmassDep_Kfactor.root','MuJet_LQMass_MT500_HighDPhi_Iso','MT500MLQ',10,'M_{LQ} GeV','M_{T} > 500 GeV')



