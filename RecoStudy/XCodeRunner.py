import os

import argparse
import logging
import os
import shutil
import subprocess
import sys
import re
import subprocess

parser = argparse.ArgumentParser(description='Process some integers.')

#parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                    help='an integer for the accumulator')
#parser.add_argument('--sum', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')

parser.add_argument('SingleMuon', action='store_true',default='SingleMuon',
                    help="Which dataset")
parser.add_argument('-i','--in',dest='codex', default='CodexAnalyzer_Preselection',
                    help="Provide a code name")
parser.add_argument('-x','--x',dest='extra', default='',
                    help="Provide extra name to be added in the Directory")
parser.add_argument('-s','--s',dest='sample', default='SingleMu',
                    help="Provide which dataset your are running")
parser.add_argument('-f','--f',dest='RunFullSample', default=False,
                    help="Run Full Sample")

                                                        

args = parser.parse_args()
print args.codex

preName='NewOutFiles_'
dirName=('%s%s_%s'%(preName,args.codex,args.extra)).replace('CodexAnalyzer_','')

SampleLoc=''

print 'This is what we are runinng on .....',args.sample
if args.sample=='SingleMu':
    SampleLoc='/Users/abdollah1/GIT_abdollah110/DM2018/ROOT94X/2017/'

if args.sample=='SingleEle':
    SampleLoc='/Users/abdollah1/GIT_abdollah110/DM2018/ROOT94X/SampleLQ1/'

#if args.sample=='Mu50':
#    SampleLoc='/Users/abdollah1/GIT_abdollah110/DM2018/ROOT94X/lqsamples2_jetPt50_MT200/'

CodexSignal='/Users/abdollah1/GIT_abdollah110/DM2018/ROOT94X/PrivateSample/'

if not os.path.exists(dirName):
    os.makedirs(dirName)



InputBKg=[
            ['DYJetsToLL.root','DYJetsToLL_M-50_HT*.root'],
            ['WJetsToLNu.root','*JetsToLNu*.root','WTo*root'],
            ['TTJets.root','TTJets*.root'],
            ['VV.root','ZZ*.root','WZ*.root','WW*.root'],
            ['SingleTop.root','ST_*.root'],
            ['Data.root','Data.root'],
]


InputSignal=[
             ['Codex_1200.root','Codex_1200_DM_500_X_550.root']
]

FullSignal=[
            ['Codex_1.root' , 'Codex_1000_DM_300_X_330.root'],
            ['Codex_2.root' , 'Codex_1000_DM_350_X_385.root'],
            ['Codex_3.root' , 'Codex_1000_DM_400_X_440.root'],
            ['Codex_4.root' , 'Codex_1000_DM_450_X_495.root'],
            ['Codex_5.root' , 'Codex_1100_DM_300_X_330.root'],
            ['Codex_6.root' , 'Codex_1100_DM_350_X_385.root'],
            ['Codex_7.root' , 'Codex_1100_DM_400_X_440.root'],
            ['Codex_8.root' , 'Codex_1100_DM_450_X_495.root'],
            ['Codex_9.root' , 'Codex_1100_DM_500_X_550.root'],
            ['Codex_10.root' , 'Codex_1200_DM_300_X_330.root'],
            ['Codex_11.root' , 'Codex_1200_DM_350_X_385.root'],
            ['Codex_12.root' , 'Codex_1200_DM_400_X_440.root'],
            ['Codex_13.root' , 'Codex_1200_DM_450_X_495.root'],
            ['Codex_14.root' , 'Codex_1200_DM_500_X_550.root'],
            ['Codex_15.root' , 'Codex_1200_DM_550_X_595.root'],
            ['Codex_16.root' , 'Codex_1300_DM_300_X_330.root'],
            ['Codex_17.root' , 'Codex_1300_DM_350_X_385.root'],
            ['Codex_18.root' , 'Codex_1300_DM_400_X_440.root'],
            ['Codex_19.root' , 'Codex_1300_DM_450_X_495.root'],
            ['Codex_20.root' , 'Codex_1300_DM_500_X_550.root'],
            ['Codex_21.root' , 'Codex_1300_DM_550_X_605.root'],
            ['Codex_22.root' , 'Codex_1300_DM_600_X_660.root'],
            ['Codex_23.root' , 'Codex_1400_DM_300_X_330.root'],
            ['Codex_24.root' , 'Codex_1400_DM_350_X_385.root'],
            ['Codex_25.root' , 'Codex_1400_DM_400_X_440.root'],
            ['Codex_26.root' , 'Codex_1400_DM_450_X_495.root'],
            ['Codex_27.root' , 'Codex_1400_DM_500_X_550.root'],
            ['Codex_28.root' , 'Codex_1400_DM_550_X_605.root'],
            ['Codex_29.root' , 'Codex_1400_DM_600_X_660.root'],
            ['Codex_30.root' , 'Codex_1400_DM_650_X_715.root'],
            ['Codex_31.root' , 'Codex_1500_DM_300_X_330.root'],
            ['Codex_32.root' , 'Codex_1500_DM_350_X_385.root'],
            ['Codex_33.root' , 'Codex_1500_DM_400_X_440.root'],
            ['Codex_34.root' , 'Codex_1500_DM_450_X_495.root'],
            ['Codex_35.root' , 'Codex_1500_DM_500_X_550.root'],
            ['Codex_36.root' , 'Codex_1500_DM_550_X_605.root'],
            ['Codex_37.root' , 'Codex_1500_DM_600_X_660.root'],
            ['Codex_38.root' , 'Codex_1500_DM_650_X_715.root'],
            ['Codex_39.root' , 'Codex_1500_DM_700_X_770.root'],
            ['Codex_40.root' , 'Codex_800_DM_300_X_330.root'],
            ['Codex_41.root' , 'Codex_800_DM_350_X_385.root'],
            ['Codex_42.root' , 'Codex_900_DM_300_X_330.root'],
            ['Codex_43.root' , 'Codex_900_DM_350_X_385.root'],
            ['Codex_44.root' , 'Codex_900_DM_400_X_440.root'],
]



outF=open('out%s.txt'%dirName,'w')

outF.write("\n ./Make.sh %s.cc"%args.codex)
outF.write("\n cp %s.* %s/."%(args.codex,dirName))
outF.write("\n cp out%s.txt %s/."%(dirName,dirName))


for sam in range(0,len(InputBKg)):

    if len(InputBKg[sam])==2: outF.write("\n./%s.exe   %s/%s      %s%s "%(args.codex,dirName,InputBKg[sam][0],SampleLoc, InputBKg[sam][1] ))
    if len(InputBKg[sam])==3: outF.write("\n./%s.exe   %s/%s    %s%s %s%s"%(args.codex,dirName,InputBKg[sam][0],SampleLoc, InputBKg[sam][1], SampleLoc,InputBKg[sam][2] ))
    if len(InputBKg[sam])==4: outF.write("\n./%s.exe   %s/%s  %s%s %s%s %s%s"%(args.codex,dirName,InputBKg[sam][0],SampleLoc, InputBKg[sam][1], SampleLoc,InputBKg[sam][2], SampleLoc,InputBKg[sam][3] ))


if not args.RunFullSample:
    for sig in range(0,len(InputSignal)):
        outF.write("\n./%s.exe   %s/%s      %s%s "%(args.codex,dirName,InputSignal[sig][0],CodexSignal, InputSignal[sig][1] ))

if args.RunFullSample:
    for sig in range(0,len(FullSignal)):
          outF.write("\n./%s.exe   %s/%s      %s%s "%(args.codex,dirName,FullSignal[sig][0],CodexSignal, FullSignal[sig][1] ))
                                                        

outF.close()

print "Run the following line"
print "source out%s.txt"%dirName
                
