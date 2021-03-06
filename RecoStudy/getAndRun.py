import os
import argparse

import ROOT
from ROOT import *
parser = argparse.ArgumentParser(description='Process some integers.')


parser.add_argument('-i','--in',dest='list', default='[]',
                    help="Provide a code name")


args = parser.parse_args()
filename= args.list

j=0
with open(filename) as fl:
    for line in fl:
        print "\n\n"
        TF=TFile(line.replace('\n',''),"r")

#        Hist=TF.Get('MuJet_LQMass_MT500_HighDPhi_Iso')
#        Hist=TF.Get('MuJet_tmass_MuMet_NoMT_HighDPhi_TotEta_Total')
#        Hist=TF.Get('MuJet_tmass_MuMet_HighMT_LowDPhi_TotEta_Iso')
#        Hist=TF.Get('MuJet_tmass_MuMet_HighMT_LowDPhi_TotEta_Total')
#        if Hist: print line.replace('\n',''), 'HighMT  Entry',Hist.GetEntries(), ' Integral', Hist.Integral()

        Hist2=TF.Get('MuJet_dPhi_Mu_Jet_NoMT_HighDPhi_Iso')
        print line.replace('\n',''), 'NoMT  Entry',Hist2.GetEntries(), ' Integral', Hist2.Integral()


        Hist2=TF.Get('MuJet_dPhi_Mu_Jet_HighMT_HighDPhi_Iso')
        print line.replace('\n',''), 'HighMT  Entry',Hist2.GetEntries(), ' Integral', Hist2.Integral()

        Hist2=TF.Get('MuJet_dPhi_Mu_Jet_MT300_HighDPhi_Iso')
        print line.replace('\n',''), 'MT300  Entry',Hist2.GetEntries(), ' Integral', Hist2.Integral()

        Hist2=TF.Get('MuJet_dPhi_Mu_Jet_MT500_HighDPhi_Iso')
        print line.replace('\n',''), 'MT500  Entry',Hist2.GetEntries(), ' Integral', Hist2.Integral()





        Hist2=TF.Get('MuJet_dPhi_Mu_Jet_NoMT_HighDPhi_ttbarCRDiLep_Iso')
        print line.replace('\n',''), '_ttbarCRDiLep NoMT  Entry',Hist2.GetEntries(), ' Integral', Hist2.Integral()
        
        
        Hist2=TF.Get('MuJet_dPhi_Mu_Jet_HighMT_HighDPhi_ttbarCRDiLep_Iso')
        print line.replace('\n',''), '_ttbarCRDiLep HighMT  Entry',Hist2.GetEntries(), ' Integral', Hist2.Integral()
        
        Hist2=TF.Get('MuJet_dPhi_Mu_Jet_MT300_HighDPhi_ttbarCRDiLep_Iso')
        print line.replace('\n',''), '_ttbarCRDiLep MT300  Entry',Hist2.GetEntries(), ' Integral', Hist2.Integral()


        Hist2=TF.Get('MuJet_dPhi_Mu_Jet_MT500_HighDPhi_ttbarCRDiLep_Iso')
        print line.replace('\n',''), '_ttbarCRDiLep MT500  Entry',Hist2.GetEntries(), ' Integral', Hist2.Integral()





        Hist2=TF.Get('MuJet_dPhi_Mu_Jet_NoMT_HighDPhi_ttbarCRSingleLep_Iso')
        print line.replace('\n',''), '_ttbarCRSingleLep NoMT  Entry',Hist2.GetEntries(), ' Integral', Hist2.Integral()
        
        
        Hist2=TF.Get('MuJet_dPhi_Mu_Jet_HighMT_HighDPhi_ttbarCRSingleLep_Iso')
        print line.replace('\n',''), '_ttbarCRSingleLep HighMT  Entry',Hist2.GetEntries(), ' Integral', Hist2.Integral()
        

        Hist2=TF.Get('MuJet_dPhi_Mu_Jet_MT300_HighDPhi_ttbarCRSingleLep_Iso')
        print line.replace('\n',''), '_ttbarCRSingleLep MT300  Entry',Hist2.GetEntries(), ' Integral', Hist2.Integral()



        Hist2=TF.Get('MuJet_dPhi_Mu_Jet_MT500_HighDPhi_ttbarCRSingleLep_Iso')
        print line.replace('\n',''), '_ttbarCRSingleLep MT500  Entry',Hist2.GetEntries(), ' Integral', Hist2.Integral()
