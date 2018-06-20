import os
import ROOT
from ROOT import *
from array import array


#TFile*		T1tttt_limit_scan_smooth4.root
#    KEY: TH2D	T1ttttObservedExcludedXsec;1


TGR=[
['T1ttttObservedLimit','graph_smoothed_Obs'],
['T1ttttObservedLimitUp','graph_smoothed_ObsP'],
['T1ttttObservedLimitDown','graph_smoothed_ObsM'],
['T1ttttExpectedLimit','graph_smoothed_Exp'],
['T1ttttExpectedLimitUp','graph_smoothed_ExpP'],
['T1ttttExpectedLimitDown','graph_smoothed_ExpM']
]


#TGR=[
#     ['graph_smoothed_Obs','graph_smoothed_Obs'],
#     ['graph_smoothed_ObsP','graph_smoothed_ObsP'],
#     ['graph_smoothed_ObsM','graph_smoothed_ObsM'],
#     ['graph_smoothed_Exp','graph_smoothed_Exp'],
#     ['graph_smoothed_ExpP','graph_smoothed_ExpP'],
#     ['graph_smoothed_ExpM','graph_smoothed_ExpM']
#     ]





OutFile=TFile('_pruned_2016.root','RECREATE')


for tgr in TGR:
    inputFile=TFile("XXX_YYY_limit_scan_smooth1.root")
    Gr_exp=inputFile.Get(tgr[0])
    print Gr_exp.Eval(1400)
    x=Gr_exp.GetX()
    y=Gr_exp.GetY()
    ex=Gr_exp.GetEX()


    NewX, NewY=array( 'd' ), array( 'd' )
#    NewX.clear()
#    NewY.clear()
    print Gr_exp.GetN()
    for i in range(0,332):
        
        print tgr,  x[i],y[i]
        if tgr[0]=='T1ttttExpectedLimitDown':
            if   x[i] < 1200 and  x[i+1] > x[i]:
                break
        else:
            if x[i+1] > x[i]:
                break
        
        NewX.append(x[i])
        NewY.append(y[i])



    NewX.append(800)
    NewY.append(340)

    n=len(NewX)

    inputFile.Close()
    OutFile.cd()
    NewGraph=TGraph(n,NewX,NewY)



    NewGraph.Write(tgr[1])

inputFile=TFile("XXX_YYY_limit_scan_smooth1.root")
#Xsec=inputFile.Get('T1ttttObservedExcludedXsec')
Xsec=inputFile.Get('hXsec_exp_corr')

OutFile.cd()
Xsec.Write('hXsec_exp_corr')

OutFile.Close()
