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
        TF=TFile(line.replace('\n',''),"r")

#        Hist=TF.Get('MuJet_LQMass_MT500_HighDPhi_Iso')
#        Hist=TF.Get('MuJet_tmass_MuMet_HighMT_LowDPhi_TotEta_Iso')
        Hist=TF.Get('MuJet_tmass_MuMet_HighMT_LowDPhi_TotEta_Total')
        if Hist: print line.replace('\n',''), 'HighMT  Entry',Hist.GetEntries(), ' Integral', Hist.Integral()

#        Hist2=TF.Get('MuJet_LQMass_MT500_HighDPhi_Iso')
#        print line.replace('\n',''), 'MT500  Entry',Hist2.GetEntries(), ' Integral', Hist2.Integral()




config.General.requestName = "WToTauNu_M-1000_"
config.Data.inputDataset = "/WToTauNu_M-1000_TuneCP5_13TeV-pythia8-tauola/RunIIFall17MiniAOD-PU2017_94X_mc2017_realistic_v11-v1/MINIAODSIM"
submit(config)

config.General.requestName = "WToTauNu_M-100_"
config.Data.inputDataset = "/WToTauNu_M-100_TuneCP5_13TeV-pythia8-tauola/RunIIFall17MiniAOD-PU2017_94X_mc2017_realistic_v11-v1/MINIAODSIM"
submit(config)

config.General.requestName = "WToTauNu_M-2000_"
config.Data.inputDataset = "/WToTauNu_M-2000_TuneCP5_13TeV-pythia8-tauola/RunIIFall17MiniAOD-PU2017_94X_mc2017_realistic_v11-v1/MINIAODSIM"
submit(config)

config.General.requestName = "WToTauNu_M-200_"
config.Data.inputDataset = "/WToTauNu_M-200_TuneCP5_13TeV-pythia8-tauola/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM"
submit(config)

config.General.requestName = "WToTauNu_M-4000_"
config.Data.inputDataset = "/WToTauNu_M-4000_TuneCP5_13TeV-pythia8-tauola/RunIIFall17MiniAOD-PU2017_94X_mc2017_realistic_v11-v1/MINIAODSIM"
submit(config)