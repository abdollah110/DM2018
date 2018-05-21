import os
import ROOT
from ROOT import *
import math

#OutF=TFile('Out1200.root','RECREATE')
#outHistSys=TH1F('MeanSys','',20,0,2)
#
#File=TFile('test1200.root','R')
#sum=0
#for isys in range(0,100):
#    HistSys=File.Get('___Sys_%s'%str(isys))
#    mean=HistSys.GetMean()
#    print mean
#    OutF.cd()
#    sum +=(mean*mean)
#    outHistSys.Fill(mean)
#
#outHistSys.Write()
#OutF.Write()
#OutF.Close()
#print "sum=",sum
#


def add_CMS():
    lowX=0.51
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
    lowX=0.51
    lowY=0.63
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(52)
    lumi.SetTextSize(0.06)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("Simulation")
    return lumi




def _Get_PDF_Unc(InputRootFile,Name,MTCut):

    ROOT.gStyle.SetFrameLineWidth(3)
    ROOT.gStyle.SetLineWidth(3)
    ROOT.gStyle.SetOptStat(0)

    OutF=TFile('out.root','RECREATE')
    PlusPDF=TH1F('pdfUp','',20,0,2000)
    MinusPDF=TH1F('pdfDown','',20,0,2000)
    PlusScale=TH1F('qcdScaleUp','',20,0,2000)
    MinusScale=TH1F('qcdScaleDown','',20,0,2000)


    File=TFile(InputRootFile,'R')


    c=ROOT.TCanvas("canvas","",0,0,600,600)
    c.cd()




    pad1 = ROOT.TPad("pad1","pad1",0,0.35,1,1)
    #pad1.SetLogy()
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


    HistCentral=File.Get('MuJet_LQMass_Scale0_MT%s_MET100_Iso'%MTCut)

    HistCentral.Draw('pe')
    
    
    
    l2=add_CMS()
    l2.Draw("same")
    l3=add_Preliminary()
    l3.Draw("same")

    #HistCentral.GetXaxis().SetTitle("M_{#muj}")
    HistCentral.GetXaxis().SetTitleSize(0)
    HistCentral.GetXaxis().SetLabelSize(0)
    HistCentral.GetXaxis().SetNdivisions(505)
    HistCentral.GetYaxis().SetLabelFont(42)
    HistCentral.GetYaxis().SetLabelOffset(0.01)
    HistCentral.GetYaxis().SetLabelSize(0.06)
    HistCentral.GetYaxis().SetTitleSize(0.075)
    HistCentral.GetYaxis().SetTitleOffset(1.04)
    HistCentral.SetTitle("")
    #    HistCentral.Setlabel("")
    HistCentral.GetYaxis().SetTitle("Events")
    HistCentral.SetLineColor(38)
    HistCentral.SetLineWidth(2)
    HistCentral.SetMarkerColor(38)
    HistCentral.SetMarkerStyle(20)


    pad1.RedrawAxis()



    categ  = ROOT.TPaveText(0.2, 0.3+0.013, 0.39, 0.4+0.1, "NDC")
    categ.SetBorderSize(   0 )
    categ.SetFillStyle(    0 )
    categ.SetTextAlign(   12 )
    categ.SetTextSize ( 0.05 )
    categ.SetTextColor(    1 )
    categ.AddText(Name.replace('.root',''))
    categ.Draw()


    c.cd()
    pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.35);
    pad2.SetTopMargin(0.05);
    pad2.SetBottomMargin(0.3);
    pad2.SetLeftMargin(0.18);
    pad2.SetRightMargin(0.05);
    #pad2.SetTickx(1)
    #pad2.SetTicky(1)
    pad2.SetFrameLineWidth(3)
    pad2.SetGridx()
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()


    for ibin in range(0,20):


###########################################################################################
## PDF Uncertainty
###########################################################################################
#        sumP=0
#        numP=0
#
#        sumN=0
#        numN=0
#        for isys in range(0,100):
#            HistCentral=File.Get('MuJet_LQMass_MT500_MET100_Iso')
#            HistSys=File.Get('MuJet_LQMass_PDF%s_MT500_MET100_Iso'%str(isys))
#            
#    #        HistCentral.Rebin(10)
#    #        HistSys.Rebin(10)
#
#
#            
#    #        meanCental=HistCentral.Integral()
#    #        meanSys=HistSys.Integral()
#            meanCental=HistCentral.GetBinContent(ibin+1)
#            meanSys=HistSys.GetBinContent(ibin+1)
#            
#            if meanCental==0: continue
#            
#
#            if meanSys > meanCental:
#                sumP +=pow( (meanSys-meanCental)  ,2)
#                numP +=1
#
#            if meanSys < meanCental:
#                sumN +=pow( (meanCental-meanSys)  ,2)
#                numN +=1
#
#
#
#
#        print ibin+1, 'numP ', numP,   'sumP= ', sumP,  ' Final Number plus is=', math.sqrt( 1./(numP -1) * sumP  ),  '  unc= ', math.sqrt( 1./(numP -1) * sumP  )/ meanCental
#        
#        BinValuPlus=math.sqrt( 1./(numP -1) * sumP  )/ meanCental
#        PlusPDF.SetBinContent(ibin+1,1+BinValuPlus )
#
#        print  ibin+1,  'numN ', numN,   'sumN= ', sumN,  ' Final Number minus is=', math.sqrt( 1./(numN -1) * sumN  ),  '  unc= ', math.sqrt( 1./(numN -1) * sumN  )/ meanCental
#
#        BinValuMinus=math.sqrt( 1./(numN -1) * sumN  )/ meanCental
#        MinusPDF.SetBinContent(ibin+1,1 - BinValuMinus )




##########################################################################################
# Scale Uncertainty
##########################################################################################
        Minimum=0
        Maximum=100
        
        for isys in range(1,9):
            
            if isys==5 or isys==7: continue  # these 2 are non-physical related to the (2,0.5) or (0.5,2)
            
            HistCentral=File.Get('MuJet_LQMass_Scale0_MT%s_MET100_Iso'%MTCut)
            HistSys=File.Get('MuJet_LQMass_Scale%s_MT%s_MET100_Iso'%(str(isys),MTCut))
            
#            HistCentral.Rebin(10)
#            HistSys.Rebin(10)

            
            
            #        meanCental=HistCentral.Integral()
            #        meanSys=HistSys.Integral()
            meanCental=HistCentral.GetBinContent(ibin+1)
            meanSys=HistSys.GetBinContent(ibin+1)
            
            if meanCental==0:
                largestDeviationUp=largestDeviationDown=1
            else:
            
            
                if meanSys/meanCental > Minimum:
                    largestDeviationUp=meanSys/meanCental
                    Minimum=largestDeviationUp
                
                
                if meanSys/meanCental < Maximum:
                    largestDeviationDown=meanSys/meanCental
                    Maximum=largestDeviationDown



        print ibin, largestDeviationUp, largestDeviationDown

        PlusScale.SetBinContent(ibin+1,largestDeviationUp )
        MinusScale.SetBinContent(ibin+1,largestDeviationDown )


##########################################################################################





    PlusScale.GetXaxis().SetTitle("")
    PlusScale.GetXaxis().SetLabelSize(0.06)
    PlusScale.GetYaxis().SetLabelSize(0.05)
    PlusScale.GetYaxis().SetTitle("QCD Scale Unc")
    PlusScale.GetXaxis().SetNdivisions(505)
    PlusScale.GetYaxis().SetNdivisions(10)
    PlusScale.GetXaxis().SetTitleSize(0.1)
    PlusScale.GetYaxis().SetTitleSize(0.1)
    PlusScale.GetYaxis().SetTitleOffset(0.5)
    PlusScale.GetXaxis().SetTitleOffset(1.04)
    PlusScale.GetXaxis().SetLabelSize(0.08)
    PlusScale.GetYaxis().SetLabelSize(0.08)
    PlusScale.GetXaxis().SetTitleFont(42)
    PlusScale.GetYaxis().SetTitleFont(42)
    PlusScale.GetXaxis().SetTitle('M_{#muj} (GeV)')
    PlusScale.SetMinimum(0.5)
    PlusScale.SetMaximum(1.5)


#    PlusPDF.Draw('PL')
#    PlusPDF.SetMinimum(0.5)
#    PlusPDF.SetMaximum(1.5)
#    PlusPDF.SetMarkerStyle(20)
#    PlusPDF.SetMarkerColor(38)
#    PlusPDF.SetLineColor(38)
#    PlusPDF.SetLineWidth(2)
#    PlusPDF.SetMarkerColor(38)
#    PlusPDF.SetMarkerStyle(20)
#    
#    
#    MinusPDF.Draw('PLsame')
#    MinusPDF.SetLineColor(38)
#    MinusPDF.SetLineWidth(2)
#    MinusPDF.SetMarkerColor(38)
#    MinusPDF.SetMarkerStyle(20)

    PlusScale.Draw('PL')
    PlusScale.SetLineColor(8)
    PlusScale.SetLineWidth(2)
    PlusScale.SetMarkerColor(8)
    PlusScale.SetMarkerStyle(21)

    MinusScale.Draw('PLsame')
    MinusScale.SetLineColor(8)
    MinusScale.SetLineWidth(2)
    MinusScale.SetMarkerColor(8)
    MinusScale.SetMarkerStyle(21)



    c.cd()
    pad1.Draw()

    ROOT.gPad.RedrawAxis()

    c.Modified()

    c.SaveAs('FINALSYS__%s.pdf'%(Name.replace('.root','')))

    fileOut=TFile('QCDScale_%s.root'%Name,'RECREATE')
    fileOut.cd()
    PlusScale.Write()
    MinusScale.Write()
    fileOut.Close()




_Get_PDF_Unc('testQCDScalettbar.root','TTbar','500')
#_Get_PDF_Unc('OutFiles_FullSelection/WJetsToLNu.root','W','500')






