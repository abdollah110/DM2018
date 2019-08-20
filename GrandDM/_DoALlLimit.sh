#!/bin/bash

printf "TXT To WS ...\n\n\n\n"
combineTool.py -M T2W -i LIMITS/* -o workspace.root --parallel 8

printf "Compute Asymptotic  ...\n\n\n\n"
combineTool.py -M AsymptoticLimits  -d */*/workspace.root --there -n .limit --parallel 8

printf "Collect Limit  ...\n\n\n\n"
combineTool.py -M CollectLimits */*/*.limit.* --use-dirs -o limits.json


printf "cd 14 ...\n\n\n\n"
cd LIMITS/14/

printf "Collect Limit  ...\n\n\n\n"
combine -M FitDiagnostics workspace.root --robustFit=1 --rMin -5 --rMax 5

printf "Make PostFit  ...\n\n\n\n"
PostFitShapes -o postfit_shapes.root -m 14 -f fitDiagnostics.root:fit_s --postfit --sampling --print -d combined.txt.cmb

printf "Significance  ...\n\n\n\n"
combine -M Significance --significance workspace.root

printf "Impact  ...\n\n\n\n"
combineTool.py -M Impacts -d workspace.root -m 14 --doInitialFit --robustFit 1 --rMin -5 --rMax 5 --parallel 8
combineTool.py -M Impacts -d workspace.root -m 14 --robustFit 1 --doFits --rMin -5 --rMax 5 --expectSignal=1 --parallel 8 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP
combineTool.py -M Impacts -d workspace.root -m 14 -o impacts.json
plotImpacts.py -i impacts.json -o impacts


# Do Anderson Darling first
ALGO=AD
combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 14 --there -d workspace.root -n ".$ALGO.toys" --fixedSignalStrength=1 -t 50 -s 0:19:1 --parallel 12
combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 14 --there -d workspace.root -n ".$ALGO" --fixedSignalStrength=1

combineTool.py -M CollectGoodnessOfFit --input higgsCombine.${ALGO}.GoodnessOfFit.mH14.root higgsCombine.${ALGO}.toys.GoodnessOfFit.mH14.*.root -o collectGoodness_${ALGO}.json

python ../../../../scripts/plotGof.py --statistic ${ALGO} --mass 14.0 collectGoodness_${ALGO}.json --title-right="77.4 fb^{-1} (13 TeV)" --output='-AD'





# Do KS test
ALGO=KS
combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 14 --there -d workspace.root -n ".$ALGO.toys" --fixedSignalStrength=1 -t 50 -s 0:19:1 --parallel 12
combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 14 --there -d workspace.root -n ".$ALGO" --fixedSignalStrength=1

combineTool.py -M CollectGoodnessOfFit --input higgsCombine.${ALGO}.GoodnessOfFit.mH14.root higgsCombine.${ALGO}.toys.GoodnessOfFit.mH14.*.root -o collectGoodness_${ALGO}.json

python ../../../../scripts/plotGof.py --statistic ${ALGO} --mass 14.0 collectGoodness_${ALGO}.json --title-right="77.4 fb^{-1} (13 TeV)" --output='-KS'




# Do KS test
ALGO=saturated
combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 14 --there -d workspace.root -n ".$ALGO.toys" --fixedSignalStrength=1 -t 50 -s 0:19:1 --parallel 12
combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 14 --there -d workspace.root -n ".$ALGO" --fixedSignalStrength=1

combineTool.py -M CollectGoodnessOfFit --input higgsCombine.${ALGO}.GoodnessOfFit.mH14.root higgsCombine.${ALGO}.toys.GoodnessOfFit.mH14.*.root -o collectGoodness_${ALGO}.json

python ../../../../scripts/plotGof.py --statistic ${ALGO} --mass 14.0 collectGoodness_${ALGO}.json --title-right="77.4 fb^{-1} (13 TeV)" --output='Codex__mj_1_13TeV-KS'




