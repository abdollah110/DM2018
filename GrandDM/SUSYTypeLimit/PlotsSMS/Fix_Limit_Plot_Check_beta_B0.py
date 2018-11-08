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


template=[
['limit_scan_cmb_beta_0.100000_B0_0.100000.root', 120 ],
['limit_scan_cmb_beta_0.100000_B0_0.500000.root', 110 ],
['limit_scan_cmb_beta_0.500000_B0_0.100000.root', 120 ],
['limit_scan_cmb_beta_0.500000_B0_0.500000.root', 110 ],
['limit_scan_cmb_beta_1.000000_B0_0.100000.root', 120 ],
['limit_scan_cmb_beta_1.000000_B0_0.500000.root', 110 ],
          ]


for temp in template:

    inputF=[
    #['config/SUS16037/MonoLQ_2016.root ','SMOOTH/limit_scan_smooth10_2016.root'],
    #['config/SUS16037/MonoLQ_2017.root ','SMOOTH/limit_scan_smooth10_2017.root'],
    ['config/SUS16037/MonoLQ_cmb.root ', 'SMOOTH/'+temp[0]]
    #['config/SUS16037/MonoLQ_cmb.root ', 'SMOOTH/limit_scan_smooth10_cmb_PreCWR.root']
            
    ]

    for Inp in inputF:


        OutFile=TFile(Inp[0],'RECREATE')


        for tgr in TGR:
            inputFile=TFile(Inp[1])
            Gr_exp=inputFile.Get(tgr[0])
    #        print Gr_exp.Eval(1400)
            x=Gr_exp.GetX()
            y=Gr_exp.GetY()
            ex=Gr_exp.GetEX()


            NewX, NewY=array( 'd' ), array( 'd' )
        #    NewX.clear()
        #    NewY.clear()
            print Gr_exp.GetN()
            for i in range(0,110):
    #        for i in range(0,300):

                print "i=", i, tgr,  x[i],y[i]
    #            if tgr[0]=='T1ttttExpectedLimitDown':
    #                if   x[i] < 1200 and  x[i+1] > x[i]:
    #            
    #                    break
    #            else:
    #                if x[i+1] > x[i]:
    #                    break

                NewX.append(x[i])
                NewY.append(y[i])



            NewX.append(800)
            NewY.append(340)

            n=len(NewX)

            inputFile.Close()
            OutFile.cd()
            NewGraph=TGraph(n,NewX,NewY)



            NewGraph.Write(tgr[1])

        inputFile=TFile(Inp[1])
        Xsec=inputFile.Get('T1ttttObservedExcludedXsec')
        #Xsec=inputFile.Get('hXsec_exp_corr')

        OutFile.cd()
        Xsec.Write('hXsec_exp_corr')

        OutFile.Close()




    #os.system("python python/makeSMSplots.py config/SUS16037/MonoLQ_2016.cfg MonoLQ2016_B0_0p5_")
    #os.system("python python/makeSMSplots.py config/SUS16037/MonoLQ_2017.cfg MonoLQ2017_B0_0p5_")
    os.system("python python/makeSMSplots.py config/SUS16037/MonoLQ_cmb.cfg MonoLQcmb_%s"%temp[0].replace('00000',''))