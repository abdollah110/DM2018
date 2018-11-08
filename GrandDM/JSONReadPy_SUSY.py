import os
import json
from pprint import pprint


MassXS=[
[40,800,300,330],
[41,800,350,385],
[42,900,300,330],
[43,900,350,385],
[44,900,400,440],
[1,1000,300,330],
[2,1000,350,385],
[3,1000,400,440],
[4,1000,450,495],
[5,1100,300,330],
[6,1100,350,385],
[7,1100,400,440],
[8,1100,450,495],
[9,1100,500,550],
[10,1200,300,330],
[11,1200,350,385],
[12,1200,400,440],
[13,1200,450,495],
[14,1200,500,550],
[15,1200,550,595],
[16,1300,300,330],
[17,1300,350,385],
[18,1300,400,440],
[19,1300,450,495],
[20,1300,500,550],
[21,1300,550,605],
[22,1300,600,660],
[23,1400,300,330],
[24,1400,350,385],
[25,1400,400,440],
[26,1400,450,495],
[27,1400,500,550],
[28,1400,550,605],
[29,1400,600,660],
[30,1400,650,715],
[31,1500,300,330],
[32,1500,350,385],
[33,1500,400,440],
[34,1500,450,495],
[35,1500,500,550],
[36,1500,550,605],
[37,1500,600,660],
[38,1500,650,715],
[39,1500,700,770],

]




def LQXS(LQ):
        if LQ==800: return 2.73E-02
        elif LQ==900: return 1.23E-02
        elif LQ==1000: return 5.86E-03
        elif LQ==1100: return 2.91E-03
        elif LQ==1200: return 1.50E-03
        elif LQ==1300: return 7.95E-04
        elif LQ==1400: return 4.33E-04
        elif LQ==1500: return 2.40E-04
        else: return 0


#BR=0.5*0.5*2  # 50% Branching ratio for visible and invisible
#BR=1  # 50% Branching ratio for visible and invisible


LimitJson=            [
#                      'limits_LIMITS_2016.json',
#                      'limits_LIMITS_2017.json',
                      'limits_LIMITS_cmb.json'
                      ]


lqmass=[800,900,1000,1100,1200,1300,1400,1500]
dmmass=[300,350,400,450,500,550,600,650,700]
B0=0.5
delta=0.1

def GetLQBin(LQ):
    lqbin=0
    for i in range(0,8):
        if LQ==lqmass[i]:  lqbin=i+1
    return lqbin

def GetDMBin(DM):
    dmbin=0
    for i in range(0,9):
        if DM==dmmass[i]:  dmbin=i+1
    return dmbin



for FinalSampleDirectory in LimitJson:
    with open(FinalSampleDirectory) as data_file:
        data = json.load(data_file)

        NameTxtFile=FinalSampleDirectory.replace('limits_LIMITS','limit_scan').replace('json','txt')
        outTxt=open(NameTxtFile,'w')


        for bin, M in enumerate(MassXS,1):
            tau=pow((M[2]*1.0/M[1]),2)
            K=pow((1-delta*delta*tau),0.5)*pow((1-(2+delta)*(2+delta)*tau),1.5)
            BR_visible=B0/(B0+(1-B0)*K)
            BR_Invisible=1-BR_visible
            BR=2*BR_visible*BR_Invisible
            XbinLQ=GetLQBin(M[1])
            YbinDM=GetDMBin(M[2])
            
            XS_BR=(LQXS(M[1])* 1000 * BR)
            
            print '%d  %d  %2.3f  %2.3f  %2.3f  %2.3f  %2.3f  %2.3f  %2.3f '%(M[1], M[2], XS_BR,  data[str(M[0])]["obs"]/XS_BR, data[str(M[0])]["obs"]/XS_BR, data[str(M[0])]["obs"]/XS_BR,data[str(M[0])]["exp0"]/XS_BR, data[str(M[0])]["exp+2"]/XS_BR, data[str(M[0])]["exp-2"]/XS_BR),1.00,1.00

            outTxt.write('%d  %d  %2.3f  %2.3f  %2.3f  %2.3f  %2.3f  %2.3f  %2.3f %2.3f  %2.3f \n'%(M[1], M[2], XS_BR,  data[str(M[0])]["obs"]/XS_BR, data[str(M[0])]["obs"]/XS_BR, data[str(M[0])]["obs"]/XS_BR,data[str(M[0])]["exp0"]/XS_BR, data[str(M[0])]["exp+2"]/XS_BR, data[str(M[0])]["exp-2"]/XS_BR,1.00,1.00))

    outTxt.close()


