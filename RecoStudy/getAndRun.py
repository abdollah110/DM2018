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

        Hist=TF.Get('MuJet_LQMass_MT500_HighDPhi_Iso')
        if Hist: print line.replace('\n',''), 'HighMT  Entry',Hist.GetEntries(), ' Integral', Hist.Integral()

#        Hist2=TF.Get('MuJet_LQMass_MT500_HighDPhi_Iso')
#        print line.replace('\n',''), 'MT500  Entry',Hist2.GetEntries(), ' Integral', Hist2.Integral()