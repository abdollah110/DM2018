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
    Histo1.SetMarkerColor(2)
    Histo1.SetMarkerStyle(24)
    Histo1.Rebin(RB_)
#    Histo1.SetMaximum(100)
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


    
    c=ROOT.TCanvas("canvas","",0,0,600,600)
    c.cd()


    Xname1= r1.replace('NewOutFiles_Preselection_Approval_V1/','').replace('.root','').replace('_HighDPhi_Iso','')
    Xname2= hist1.replace('MuJet/','')
        
        
    Histo1.GetXaxis().SetTitle("")
    Histo1.GetXaxis().SetTitleSize(0)
    Histo1.GetXaxis().SetLabelSize(0)
    Histo1.GetXaxis().SetNdivisions(505)
    Histo1.GetYaxis().SetLabelFont(42)
    Histo1.GetYaxis().SetLabelOffset(0.01)
    Histo1.GetYaxis().SetLabelSize(0.06)
    Histo1.GetYaxis().SetTitleSize(0.075)
    Histo1.GetYaxis().SetTitleOffset(1.04)
    Histo1.SetTitle("")
    #    Histo1.Setlabel("")
    Histo1.GetYaxis().SetTitle("Events")
    #    Histo1.GetXaxis().SetRangeUser(50,1000)


#
#
#
#    
#

    pad1 = ROOT.TPad("pad1","pad1",0,0.35,1,1)
    pad1.SetLogy()
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
    
    Histo1.Scale(1./Histo1.Integral())
    Histo2.Scale(1./Histo2.Integral())
    Histo1.DrawNormalized('F')
    Histo2.DrawNormalized('Fsame')
#    Histo3.Draw('same')
#
    leg=TLegend(.45,.7,.9,.9, "", "brNDC")
    leg.SetLineWidth(0)
    leg.SetLineStyle(0)
    leg.SetFillStyle(0)
#    leg.SetBorderSize(0)
    leg.SetTextFont(62)
#    leg.AddEntry(Histo1,'Mu channel','l')
#    leg.AddEntry(Histo2,'electron channel','l')
#    leg.AddEntry(Histo1,'HT-based kFactor (ala Mono-Jet)','l')
#    leg.AddEntry(Histo2,'Mass-based kFactor (ala Wprime)','l')
    leg.AddEntry(Histo1,'No Top p_{T} reweighting','lp')
    leg.AddEntry(Histo2,'with Top p_{T} reweighting','lp')
#    leg.AddEntry(Histo3,hist3.replace("_CMS_scale",""),'l')
    leg.Draw()

#    Xname1= r1.replace('OutFiles_Preselection_Approval_V1/TotalRootForLimit_PreSelection_MuJet','').replace('.root','')
#    Xname2= hist1.replace('MuJet/','')

    categ  = ROOT.TPaveText(0.65, 0.45+0.013, 0.83, 0.60+0.155, "NDC")
    categ.SetBorderSize(   0 )
    categ.SetFillStyle(    0 )
    categ.SetTextAlign(   12 )
    categ.SetTextSize ( 0.05 )
    categ.SetTextColor(    9 )
    categ.AddText(name2)
    categ.Draw()
    
    pad1.RedrawAxis()
    
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
    



    h1=Histo1.Clone()
    h1.SetMaximum(1.5)
    h1.SetMinimum(0.5)
    h1.SetMarkerStyle(20)
    h1.SetMarkerColor(2)
    h1.GetXaxis().SetTitle('boson p_{T} (GeV)')
    
    
    
    
    h2=Histo2.Clone()
    
    
    h1.Sumw2()
    h2.Sumw2()
    
    
    #    h3.Sumw2()
    
    h1.SetStats(0)
    h2.SetStats(0)
    #    h3.SetStats(0)
    
    h1.SetTitle("")
    
    h1.Divide(h2)
    
    
    
    h1.GetXaxis().SetTitle("")
    h1.GetXaxis().SetLabelSize(0.08)
    h1.GetYaxis().SetLabelSize(0.08)
    h1.GetYaxis().SetTitle("Ratio")
    h1.GetXaxis().SetNdivisions(505)
    h1.GetYaxis().SetNdivisions(5)
    h1.GetXaxis().SetTitleSize(0.15)
    h1.GetYaxis().SetTitleSize(0.1)
    h1.GetYaxis().SetTitleOffset(0.56)
    h1.GetXaxis().SetTitleOffset(1.04)
    h1.GetXaxis().SetLabelSize(0.11)
    h1.GetYaxis().SetLabelSize(0.11)
    h1.GetXaxis().SetTitleFont(42)
    h1.GetYaxis().SetTitleFont(42)
    h1.GetXaxis().SetTitle(XTit)
    
    h1.Draw()
    
    c.cd()
    pad1.Draw()
    
    ROOT.gPad.RedrawAxis()
    
    c.Modified()




    
    
    c.SaveAs('OUT_%s_%s.pdf'%(Xname1,Xname2))


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



MakeCompare('NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_LQMass_HighMT_HighDPhi_Iso','NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_LQMass_NoTopRW_HighMT_HighDPhi_Iso','HighMTMLQ',10,'M_{LQ} GeV','M_{T} > 100 GeV')

MakeCompare('NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_LQMass_MT500_HighDPhi_Iso','NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_LQMass_NoTopRW_MT500_HighDPhi_Iso','HighMTMLQ',10,'M_{LQ} GeV','M_{T} > 500 GeV')


MakeCompare('NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_JetPt_HighMT_HighDPhi_Iso','NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_JetPt_NoTopRW_HighMT_HighDPhi_Iso','HighMTMLQ',50,'jet p_{T} GeV','M_{T} > 100 GeV')

MakeCompare('NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_JetPt_MT500_HighDPhi_Iso','NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_JetPt_NoTopRW_MT500_HighDPhi_Iso','HighMTMLQ',50,'jet p_{T} GeV','M_{T} > 500 GeV')




#MakeCompare('test_W_oldkfactor_ChangeMutoL.root','MuJet_LQMass_MT500_HighDPhi_Iso','test_W_NewmassDep_Kfactor.root','MuJet_LQMass_MT500_HighDPhi_Iso','MT500MLQ',10,'M_{LQ} GeV','M_{T} > 500 GeV')

#MakeCompare('ScaleCorretion/Codex.root','MuJet_LQMassCorrMuScale_MT500_HighDPhi_Iso','ScaleCorretion/Codex.root','MuJet_LQMass_MT500_HighDPhi_Iso','HighMTMLQ',10,'M_{LQ} GeV','M_{T} > 500 GeV')
#MakeCompare('ScaleCorretion/WJet.root','MuJet_LQMassCorrMuScale_MT500_HighDPhi_Iso','ScaleCorretion/WJet.root','MuJet_LQMass_MT500_HighDPhi_Iso','HighMTMLQ',10,'M_{LQ} GeV','M_{T} > 500 GeV')
#MakeCompare('ScaleCorretion/Data.root','MuJet_LQMassCorrMuScale_MT500_HighDPhi_Iso','ScaleCorretion/Data.root','MuJet_LQMass_MT500_HighDPhi_Iso','HighMTMLQ',10,'M_{LQ} GeV','M_{T} > 500 GeV')



#MakeCompare('ScaleCorretion/Codex_EtaCheckMuCor.root','MuJet_LQMassDifference_Barrel_MT500_HighDPhi_Iso','ScaleCorretion/Codex_EtaCheckMuCor.root','MuJet_LQMassDifference_Barrel_MT500_HighDPhi_Iso','Barrel',10,'M_{LQ}_{cor} - M_{LQ}_{uncor} / M_{LQ}_{uncor}','M_{T} > 500 GeV, |#eta| < 1.5')
#
#MakeCompare('ScaleCorretion/Codex_EtaCheckMuCor.root','MuJet_LQMassDifference_EndCap_MT500_HighDPhi_Iso','ScaleCorretion/Codex_EtaCheckMuCor.root','MuJet_LQMassDifference_EndCap_MT500_HighDPhi_Iso','Endcap',10,'M_{LQ}_{cor} - M_{LQ}_{uncor} / M_{LQ}_{uncor}','M_{T} > 500 GeV, |#eta > 1.5|')





#MakeCompare('test_W_oldkfactor_ChangeMutoL.root','MuJet_LQMass_MT500_HighDPhi_Iso','test_W_NewmassDep_Kfactor.root','MuJet_LQMass_MT500_HighDPhi_Iso','MT500MLQ',10,'M_{LQ} GeV','M_{T} > 500 GeV')



