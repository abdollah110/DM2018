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
#    Xname1= r1.replace('NewOutFiles_Preselection_Approval_V1/___','').replace('TopPtRW/TotalRootForLimit_PreSelection_MuJet_JetPt_HighMT_HighDPhi_ttbarCRSingleLep_Iso.root','')
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

    categ  = ROOT.TPaveText(0.5, 0.45+0.013, 0.83, 0.60+0.155, "NDC")
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
    h1.SetMarkerColor(1)
    h1.SetLineColor(1)
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




    
    
    c.SaveAs('OUT_TopPtRW_%s_%s.pdf'%(Xname1,Xname2))



MakeCompare('NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_LQMass_HighMT_HighDPhi_Iso','NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_LQMass_TopRW_HighMT_HighDPhi_Iso','HighMTMLQ',10,'M_{LQ} GeV','M_{T} > 100 GeV, Signal Region')

MakeCompare('NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_LQMass_MT500_HighDPhi_Iso','NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_LQMass_TopRW_MT500_HighDPhi_Iso','HighMTMLQ',10,'M_{LQ} GeV','M_{T} > 500 GeV, Signal Region')


MakeCompare('NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_JetPt_HighMT_HighDPhi_Iso','NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_JetPt_TopRW_HighMT_HighDPhi_Iso','HighMTMLQ',50,'jet p_{T} GeV','M_{T} > 100 GeV, Signal Region')

MakeCompare('NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_JetPt_MT500_HighDPhi_Iso','NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_JetPt_TopRW_MT500_HighDPhi_Iso','HighMTMLQ',50,'jet p_{T} GeV','M_{T} > 500 GeV, Signal Region')


MakeCompare('NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_JetPt_HighMT_HighDPhi_ttbarCRSingleLep_Iso','NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_JetPt_TopRW_HighMT_HighDPhi_ttbarCRSingleLep_Iso','HighMTMLQ',50,'jet p_{T} GeV','M_{T} > 100 GeV, TT CR')

MakeCompare('NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_JetPt_MT500_HighDPhi_ttbarCRSingleLep_Iso','NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_JetPt_TopRW_MT500_HighDPhi_ttbarCRSingleLep_Iso','HighMTMLQ',50,'jet p_{T} GeV','M_{T} > 500 GeV, TT CR')

MakeCompare('NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_LQMass_HighMT_HighDPhi_ttbarCRSingleLep_Iso','NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_LQMass_TopRW_HighMT_HighDPhi_ttbarCRSingleLep_Iso','HighMTMLQ',10,'M_{LQ} GeV','M_{T} > 100 GeV, TT CR')

MakeCompare('NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_LQMass_MT500_HighDPhi_ttbarCRSingleLep_Iso','NewOutFiles_Preselection_Approval_V1/TTJets.root','MuJet_LQMass_TopRW_MT500_HighDPhi_ttbarCRSingleLep_Iso','HighMTMLQ',10,'M_{LQ} GeV','M_{T} > 500 GeV, TT CR')



#MakeCompare('NewOutFiles_Preselection_Approval_V1/___NoTopPtRW/TotalRootForLimit_PreSelection_MuJet_JetPt_HighMT_HighDPhi_ttbarCRSingleLep_Iso.root','MuJet/TT','NewOutFiles_Preselection_Approval_V1/___WithTopPtRW/TotalRootForLimit_PreSelection_MuJet_JetPt_HighMT_HighDPhi_ttbarCRSingleLep_Iso.root','MuJet/TT','HighMTMLQ',50,'jet p_{T} GeV','M_{T} > 100 GeV, TT CR')








