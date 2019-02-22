//Change of muon eta from 2.4 to 2.0
//#include "../interface/CodexAnalyzer.h"
//#include "../interface/WeightCalculator.h"
//#include "../interface/Corrector.h"
#include "../interface/Functions.h"
//#include "../interface/makeHisto.h"
#include <string>
#include <ostream>
#include <vector>


int main(int argc, char** argv) {
    using namespace std;
    
    std::string out = *(argv + 1);
    
    cout << "\n\n\n OUTPUT NAME IS:    " << out << endl;     //PRINTING THE OUTPUT name
    TFile *fout = TFile::Open(out.c_str(), "RECREATE");
    
    myMap1 = new std::map<std::string, TH1F*>();
    myMap2 = new map<string, TH2F*>();
    
    std::vector<string> input;
    for (int f = 2; f < argc; f++) {
        input.push_back(*(argv + f));
        cout <<"INPUT NAME IS:   " << input[f - 2] << "\n";
    }
    
    //    //########################################
    //    // Pileup files
    //    //########################################
    //    TH1F *  HistoPUData =HistPUData();
    //    TH1F * HistoPUMC=HistPUMC();
    
    //########################################
    // Muon Id, Iso, Trigger and Tracker Eff files
    //########################################
    TH2F** HistoMuId=FuncHistMuId();
    TH2F** HistoMuIso=FuncHistMuIso();
    TH1F** HistoMuTrg=FuncHistMuTrigger();
    TGraphAsymmErrors * HistoMuTrack=FuncHistMuTrack();
    
    //########################################
    // Electron MVA IdIso files
    //########################################
    TH2F * HistoEleMVAIdIso90= FuncHistEleMVAId("Tot");
    TH2F * HistoEleMVAIdIso90_EffMC= FuncHistEleMVAId("MC");
    TH2F * HistoEleMVAIdIso90_EffData= FuncHistEleMVAId("Data");
    
    //########################################
    // W and DY K-factor files  (Bin-based K-factor)
    //########################################
    std::string ROOTLocHT= "/Users/abdollah1/GIT_abdollah110/DM2018/ROOT94X/2017/";
    vector<float> W_HTBinROOTFiles = W_HTBin(ROOTLocHT);
    vector<float> WMuNu_MassBinROOTFiles = WMuNu_MassBin(ROOTLocHT);
    vector<float> WTauNu_MassBinROOTFiles = WTauNu_MassBin(ROOTLocHT);
    
    TFile * MassDepKFactor=TFile::Open("../interface/k_fakNNLO_use.root");
    TH1F* HistMassDepKFactor= (TH1F*) MassDepKFactor->Get("k_fak_mean");
    TH1F* HistMassDepKFactor_ewkUp= (TH1F*) MassDepKFactor->Get("k_fakp");
    TH1F* HistMassDepKFactor_ewkDown= (TH1F*) MassDepKFactor->Get("k_fakm");
    
    //########################################
    // Btagging scale factor and uncertainties
    //########################################
    TH2F ** Btagg_TT=FuncHistBTagSF();
    
    //###############################################################################################
    //  Fix Parameters
    //###############################################################################################
    float MuMass= 0.10565837;
    float eleMass= 0.000511;
    float LeptonPtCut_=60;
    float TauPtCut_=20;
    float JetPtCut=100;
    float BJetPtCut=30;
    float SimpleJetPtCut=30;
    float ElectronPtCut_=15;
    float CSVCut=   0.9693   ;                  //  https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
    float LeptonIsoCut=0.15;
    Int_t nBin=500;
    Int_t binMin=0;
    Int_t binMax= 5000;
    //########################################################################################################################################################
    //########################################################################################################################################################
    //########################################################################################################################################################
    //########################################################################################################################################################
    //########################################################################################################################################################
    //                                                  Loop over inout ROOT files
    //########################################################################################################################################################
    //########################################################################################################################################################
    //########################################################################################################################################################
    //########################################################################################################################################################
    //########################################################################################################################################################
    for (int k = 0; k < input.size(); k++) {
        
        TFile *f_Double = TFile::Open(input[k].c_str());
        cout << "\n  Now is running on ------->   " << std::string(f_Double->GetName()) << "\n";
        
        std::string InputROOT= std::string(f_Double->GetName());
        TFile * myFile = TFile::Open(f_Double->GetName());
        TH1F * HistoTot = (TH1F*) myFile->Get("hcount");
        
        TTree *  Run_Tree;
        Run_Tree= Xttree(f_Double);
        
        
        
        
        //########################################
        // Pileup files
        //########################################
        
        TH1F *  HistoPUData =HistPUData();
        // Need a fix for PU distribution
        
        //    TH1F * HistoPUMC=HistPUMC();
        //        TH1F *  HistoPUMC =HistPUData();
        size_t isDataXXX = InputROOT.find("Data");
        bool check_data=0;
        if (isDataXXX!= string::npos)  check_data=1;
        TH1F * HistoPUMC=HistPUMC(check_data,f_Double);
        
        
        
        //########################################################################################################################################################
        //########################################################################################################################################################
        //########################################################################################################################################################
        //                                                  Loop over Events in each ROOT files
        //########################################################################################################################################################
        //########################################################################################################################################################
        //########################################################################################################################################################
        
        
        
        float jetES[3]={-1,0,1};
        std::string ResolJet_Cat[3] = {"JetERDown", "", "JetERUp"};
        std::string ScaleJet_Cat[3] = {"JetESDown", "", "JetESUp"};
        std::string ScaleMETUE_Cat[5] = {"METUESDown", "", "METUESUp","METJESDown","METJESUp"};
        
        
        Int_t nentries_wtn = (Int_t) Run_Tree->GetEntries();
        cout<<"nentries_wtn===="<<nentries_wtn<<"\n";
        for (Int_t i = 0; i < nentries_wtn; i++) {
            Run_Tree->GetEntry(i);
            if (i % 10000 == 0) fprintf(stdout, "\r  Processed events: %8d of %8d ", i, nentries_wtn);
            fflush(stdout);
            
            
            
            
            //###############################################################################################
            //  MET Filters (only on Data)
            //###############################################################################################
            if (isData && (metFilters!=0)) continue;   //FIXME
            
            //###########       Trigger Requirement ###########################################################
            bool PassTrigger = ((HLTEleMuX >> 21 & 1)==1); //   else if (name.find("HLT_Mu50_v") != string::npos) bitEleMuX = 21;
            if (! PassTrigger) continue;
            
            //###############################################################################################
            //  This part is to avoid of the duplicate of mu-j pair from one events
            //###############################################################################################
            std::vector<string> HistNamesFilled;
            HistNamesFilled.clear();
            
            
            
            
            
            //###############################################################################################
            //  GenInfo
            //###############################################################################################
            vector<float>  genInfo=GeneratorInfo();
            
            //            //######################## Top Pt Reweighting
            float TopPtReweighting = 1;
            size_t isTTJets = InputROOT.find("TTJets");
            if (isTTJets!= string::npos) TopPtReweighting = genInfo[0];
            
            //            //######################## W K-factor
            float WBosonPt=0;
            float WBosonMass=0;
            float WBosonKFactor=1;
            float WBosonKFactor_ewkUp=1;
            float WBosonKFactor_ewkDown=1;
            
            
            WBosonPt=genInfo[1];
            WBosonMass=genInfo[3];
            
            size_t isWJetsToLNu_Inc = InputROOT.find("WJetsToLNu_Inc");
            size_t isWJets = InputROOT.find("WJets");
            size_t isWToMuNu = (InputROOT.find("WToMuNu") );
            size_t isWToTauNu = (InputROOT.find("WToTauNu") );
            
            if (WBosonMass > 100 && (isWToMuNu!= string::npos || isWToTauNu!=string::npos)) {
                
                WBosonKFactor=HistMassDepKFactor->GetBinContent(int(WBosonMass)/10 +1); //Mass binned K-factor
                WBosonKFactor_ewkUp=HistMassDepKFactor_ewkUp->GetBinContent(int(WBosonMass)/10 +1); //Mass binned K-factor
                WBosonKFactor_ewkDown=HistMassDepKFactor_ewkDown->GetBinContent(int(WBosonMass)/10 +1); //Mass binned K-factor
            }
            if (WBosonMass <= 100 && isWJets!= string::npos  ){
                
                WBosonKFactor= FuncBosonKFactor("W1Cen") + FuncBosonKFactor("W2Cen") * WBosonPt; //HT binned & inclusive K-factor
                WBosonKFactor_ewkUp= FuncBosonKFactor("W1Up") + FuncBosonKFactor("W2Up") * WBosonPt; //HT binned & inclusive K-factor
                WBosonKFactor_ewkDown= FuncBosonKFactor("W1Down") + FuncBosonKFactor("W2Down") * WBosonPt; //HT binned & inclusive K-factor
                
            }
            
            //................................................................................................................
            //................................................................................................................
            if (isWJets!= string::npos && WBosonMass > 100) continue;
            if (isWJetsToLNu_Inc!= string::npos && (genHT > 100.0)) continue;
            //................................................................................................................
            //................................................................................................................
            
            //            //######################## Z K-factor
            float ZBosonPt=0;
            float ZBosonKFactor=1;
            
            float ZBosonKFactor_ewkUp=1;
            float ZBosonKFactor_ewkDown=1;
            size_t isDYJets = InputROOT.find("DYJets");
            ZBosonPt=genInfo[2];
            if (isDYJets!= string::npos) {
                
                ZBosonKFactor= FuncBosonKFactor("Z1Cen") + FuncBosonKFactor("Z2Cen") * ZBosonPt;
                ZBosonKFactor_ewkUp= FuncBosonKFactor("Z1Up") + FuncBosonKFactor("Z2Up") * ZBosonPt;
                ZBosonKFactor_ewkDown= FuncBosonKFactor("Z1Down") + FuncBosonKFactor("Z2Down") * ZBosonPt;
                
            }
            
            
            
            //###############################################################################################
            //  Lumi, GEN & PileUp Weight
            //###############################################################################################
            
            float LumiWeight = 1;
            float GetGenWeight=1;
            float PUWeight = 1;
            
            if (!isData){
                
                //######################## Lumi Weight
                if (HistoTot) LumiWeight = weightCalc(HistoTot, InputROOT,genHT, W_HTBinROOTFiles, WBosonMass, WMuNu_MassBinROOTFiles,WTauNu_MassBinROOTFiles);
                //######################## Gen Weight
                GetGenWeight=genWeight;
                
                //######################## PileUp Weight
                //                int puNUmmc=int(puTrue->at(0)*10);
                int puNUmmc=int(puTrue->at(0)*5);
                int puNUmdata=int(puTrue->at(0)*5);
                float PUMC_=HistoPUMC->GetBinContent(puNUmmc+1);
                float PUData_=HistoPUData->GetBinContent(puNUmdata+1);
                if (PUMC_ ==0)
                    cout<<"PUMC_ is zero!!! & num pileup= "<< puTrue->at(0)<<"\n";
                else
                    PUWeight= PUData_/PUMC_;
                if  (puNUmmc==1 || puNUmmc==0) continue;
            }
            
            
            //############################################################################################
            //   Final Total Weight
            //############################################################################################
            float TotalWeight_withTopPtRW = LumiWeight * GetGenWeight * PUWeight * TopPtReweighting * WBosonKFactor * ZBosonKFactor ;
            float TotalWeight_NoTopPtRW = LumiWeight * GetGenWeight * PUWeight * WBosonKFactor * ZBosonKFactor ;
            
            
            
            
            //###########       numTau   ###########################################################
            int numTau= getNumTau();
            
            //###########       Ele Veto   ###########################################################
            int numElectron= getNumElectron();
            
            //###########       BTag SF   ###########################################################
            //                float FinalBTagSF=FuncFinalBTagSF(isData,Btagg_TT);
            
            //###########       numBJet   ###########################################################
            //                int numBJet=numBJets();
            
            
            
            
            //###########       bJet Veto   ###########################################################
            int numBJet=0;
            int numlightJet=0;
            float EffJet =1;
            
            float SF=1;
            float SFUp=1;
            float SFDown=1;
            
            float P_Data_P_mc=1;
            float P_Data_P_mcUp=1;
            float P_Data_P_mcDown=1;
            
            float FinalBTagSF=1;
            float FinalBTagSFUp=1;
            float FinalBTagSFDown=1;
            
            
            for (int ijet= 0 ; ijet < nJet ; ijet++){
                
                float HadronFlavor= isData ? 1 : jetHadFlvr->at(ijet);
                
                if (jetPFLooseId->at(ijet) > 0.5 && jetPt->at(ijet) > BJetPtCut && fabs(jetEta->at(ijet)) < 2.4 ){
                    
                    
                    if ( jetCSV2BJetTags->at(ijet) >  CSVCut ){
                        numBJet++;
                        EffJet= getBtagEfficiency( isData, 1,  jetPt->at(ijet), fabs(jetEta->at(ijet)), Btagg_TT);
                        SF= GetBJetSF(isData, jetPt->at(ijet), jetPt->at(ijet), HadronFlavor);
                        P_Data_P_mc=SF*EffJet/EffJet;
                        
                        
                    }
                    else{
                        EffJet= getBtagEfficiency( isData, 0,  jetPt->at(ijet), fabs(jetEta->at(ijet)), Btagg_TT);
                        numlightJet++;
                        
                        SF=GetBJetSF(isData,jetPt->at(ijet), jetPt->at(ijet), HadronFlavor);
                        SFUp=GetBJetSFUp(isData,jetPt->at(ijet), jetPt->at(ijet), HadronFlavor);
                        SFDown=GetBJetSFDown(isData,jetPt->at(ijet), jetPt->at(ijet), HadronFlavor);
                        
                        P_Data_P_mc=(1-SF*EffJet)/(1-EffJet);
                        P_Data_P_mcUp=(1-SFUp*EffJet)/(1-EffJet);
                        P_Data_P_mcDown=(1-SFDown*EffJet)/(1-EffJet);
                        
                    }
                    
                }
                
                FinalBTagSF *=P_Data_P_mc;
                FinalBTagSFUp *=P_Data_P_mcUp;
                FinalBTagSFDown *=P_Data_P_mcDown;
            }
            if (isData) FinalBTagSF=1;
            
            
            
            
            //###########       numJet   ###########################################################
            int numJet=numJets(SimpleJetPtCut);
            
            //###########       numZboson   ###########################################################
            int numZboson = getNumZBoson();
            
            //#######################################################################################
            //  Some Histogram Filling
            //#######################################################################################
            plotFill("_WeightLumi",LumiWeight,1000,0,10);
            plotFill("_TopPtReweighting",TopPtReweighting,100,0,2);
            plotFill("_WeightPU",PUWeight,100,0,5);
            plotFill("_TotalWeight_withTopPtRW",TotalWeight_withTopPtRW,50,0,2);
            plotFill("_TotalWeight_NoTopPtRW",TotalWeight_NoTopPtRW,50,0,2);
            plotFill("_nVtx_NoPUCorr",nVtx,60,0,60);
            plotFill("_nVtx_PUCorr",nVtx,60,0,60,PUWeight);
            plotFill("_WBosonPt",WBosonPt,150,0,1500,PUWeight);
            plotFill("_FinalBTagSF", FinalBTagSF,200,0,2);
            
            for (int qq=0; qq < 60;qq++){
                if ((HLTEleMuX >> qq & 1) == 1)
                    plotFill("_HLT",qq,60,0,60);
            }
            
            
            
            
            //############################################################################################
            //###########       Loop over MuJet events   #################################################
            //############################################################################################
            
            for  (int imu=0 ; imu < nMu; imu++){
                
                float IsoMu=muPFChIso->at(imu)/muPt->at(imu);
                if ( (muPFNeuIso->at(imu) + muPFPhoIso->at(imu) - 0.5* muPFPUIso->at(imu) )  > 0.0)
                    IsoMu= ( muPFChIso->at(imu) + muPFNeuIso->at(imu) + muPFPhoIso->at(imu) - 0.5* muPFPUIso->at(imu))/muPt->at(imu);
                //                IsoMu= ( muPFChIso->at(imu)/muPt->at(imu) + muPFNeuIso->at(imu) + muPFPhoIso->at(imu) - 0.5* muPFPUIso->at(imu))/muPt->at(imu);
                
                bool MuPtCut = muPt->at(imu) > LeptonPtCut_ && fabs(muEta->at(imu)) < 2.4 ;
                bool MuIdIso=( (muIDbit->at(imu) >> 2 & 1)  && fabs(muD0->at(imu)) < 0.045 && fabs(muDz->at(imu)) < 0.2); //Tight Muon Id
                
                if (! MuPtCut || !MuIdIso ) continue;
                
                
                float LepCor=getCorrFactorMuon94X(isData,  muPt->at(imu), muEta->at(imu) , HistoMuId,HistoMuIso,HistoMuTrg,HistoMuTrack);
                
                
                
                TLorentzVector Mu4Momentum,Jet4MomentumNonSmear, Jet4Momentum,KJet4Momentum,NewJet4Collection,LQ;
                Mu4Momentum.SetPtEtaPhiM(muPt->at(imu),muEta->at(imu),muPhi->at(imu),MuMass);
                
                
                
                
                //###########    loop over  Jet    ###########################################################
                
                for (int ijet= 0 ; ijet < nJet ; ijet++){
                    
                    
                    float JetSmearResolution[3]={1,1,1};
                    if (!isData){
                        // NOT available for all samples need to apply for signal though
//                        JetSmearResolution[0]=jetP4SmearDo->at(ijet);
//                        JetSmearResolution[1]=jetP4Smear->at(ijet);
//                        JetSmearResolution[2]=jetP4SmearUp->at(ijet);
                                                //
                                                JetSmearResolution[0]=1.0;
                                                JetSmearResolution[1]=1.0;
                                                JetSmearResolution[2]=1.0;
                        
                    }
                    
                    float UESMET[5]={pfMET_T1UESDo,pfMET,pfMET_T1UESUp,pfMET_T1JESDo,pfMET_T1JESUp};
                    float UESMETPhi[5]={pfMETPhi_T1UESDo,pfMETPhi,pfMETPhi_T1UESUp,pfMETPhi_T1JESDo,pfMETPhi_T1JESUp};
                    
                    
                        for (int jetRes=0;jetRes<3;jetRes++){
                            for (int metUE=0; metUE < 5; metUE++){
                                for (int jetScl=0;jetScl<3;jetScl++){
                                    
                                    
                                    // This is to check that we only make the plots only either JES or MET is applied (not both of them simultaneously)!
                                    if (jetRes!=1 && metUE != 1  ) continue;
                                    if (jetRes!=1 && jetScl != 1 ) continue;
                                    if (metUE != 1 && jetScl != 1 ) continue;
                                    
                                    
                                    Jet4MomentumNonSmear.SetPtEtaPhiE(jetPt->at(ijet),jetEta->at(ijet),jetPhi->at(ijet),jetEn->at(ijet));
                                    Jet4Momentum=Jet4MomentumNonSmear*JetSmearResolution[jetRes];
                                    
                                    
                                    NewJet4Collection.SetPtEtaPhiE(Jet4Momentum.Pt()*(1+ jetES[jetScl]*jetJECUnc->at(ijet)) ,jetEta->at(ijet),jetPhi->at(ijet),Jet4Momentum.E()*(1+ jetES[jetScl]*jetJECUnc->at(ijet)));
                                    
                                    
                                    
                                    bool goodJet = (jetPFLooseId->at(ijet) > 0.5 && NewJet4Collection.Pt() > JetPtCut && fabs(NewJet4Collection.Eta() ) < 2.4 && NewJet4Collection.DeltaR(Mu4Momentum) > 0.5);
                                    if (! goodJet) continue;
                                    
                                    
                                    
                                    float jetMET=UESMET[metUE];
                                    float jetMETPhi=UESMETPhi[metUE];
                                    
                                    float jetMET_x = UESMET[metUE] * TMath::Cos(UESMETPhi[metUE]) - (Jet4Momentum.Px()- NewJet4Collection.Px()) ;
                                    float jetMET_y = UESMET[metUE] * TMath::Sin(UESMETPhi[metUE]) - (Jet4Momentum.Py()- NewJet4Collection.Py()) ;
                                    jetMET = sqrt (pow(jetMET_x,2)+ pow(jetMET_y,2));
                                    jetMETPhi = atan(jetMET_y / jetMET_x);
                                    if (UESMETPhi[metUE] > (TMath::Pi() / 2)) jetMETPhi += TMath::Pi();
                                    if (UESMETPhi[metUE] < (-TMath::Pi() / 2)) jetMETPhi -= TMath::Pi();
                                    
                                    
                                    
                                    LQ=NewJet4Collection + Mu4Momentum;
                                    
                                    //###############################################################################################
                                    // Apply all veto cuts
                                    //###############################################################################################
//                                    if ((numTau+numElectron +numZboson + numBJet) > 0) continue;
                                    //###############################################################################################
                                    //  dPhi Jet_MET Categorization (To get a relaxed cut for QCD template)
                                    //###############################################################################################
                                    const int size_jetMetPhi = 2;
                                    
                                    bool HighDPhi = deltaPhi(NewJet4Collection.Phi(),jetMETPhi) > 0.5 && deltaPhi(Mu4Momentum.Phi(),jetMETPhi) > 0.5;
                                    bool noDPhi = 1;
                                    
                                    
                                    bool jetMetPhi_category[size_jetMetPhi] = {HighDPhi,noDPhi};
                                    std::string jetMetPhi_Cat[size_jetMetPhi] = {"", "_NoDPhi"};
                                    
                                    
                                    //###############################################################################################
                                    //  Isolation Categorization
                                    //###############################################################################################
                                    //###############################################################################################
                                    
                                    
                                    bool LepPassIsolation= IsoMu < LeptonIsoCut;
                                    
                                    const int size_isoCat = 2;
                                    bool Isolation = LepPassIsolation;
                                    bool AntiIsolation =  !LepPassIsolation;
                                    
                                    
                                    bool Iso_category[size_isoCat] = {Isolation, AntiIsolation};
                                    std::string iso_Cat[size_isoCat] = {"_Iso", "_AntiIso"};
                                    //###############################################################################################
                                    //  MT Categorization
                                    //###############################################################################################
                                    float tmass_LQMet= TMass_F(LQ.Pt(), LQ.Px(),LQ.Py(), pfMET, pfMETPhi);
                                    float tmass_MuMet= TMass_F(muPt->at(imu), muPt->at(imu)*cos(muPhi->at(imu)),muPt->at(imu)*sin(muPhi->at(imu)) , jetMET, jetMETPhi);
                                    const int size_mTCat = 3;
                                    bool MT100 = tmass_MuMet > 100;
                                    bool MT50To150=(tmass_MuMet > 50 && tmass_MuMet <= 150);
                                    bool MT400 = tmass_MuMet > 400;
                                    bool MT_category[size_mTCat] = {MT100,MT50To150,MT400};
                                    std::string MT_Cat[size_mTCat] = {"_MT100","_MT50To150","_MT400"};
                                    
                                    
                                    //###############################################################################################
                                    //  MET Categorization
                                    //###############################################################################################
                                    
                                    
                                    
                                    
                                    
                                    const int size_METcut = 2;
                                    
                                    bool signalRegion = numTau+numZboson + numElectron  + numBJet < 1;
                                    
                                    
                                    bool TTcontrolRegion_SingleLep = (numTau+numZboson + numElectron  < 1  && numBJet >= 1);
                                    
                                    bool MetCut_category[size_METcut] = {signalRegion,TTcontrolRegion_SingleLep};
                                    std::string MetCut_Cat[size_METcut] = {"", "_ttbarCRSingleLep"};
                                    
                                    
                                    //###############################################################################################
                                    //  Top Pt Reweighting Cat: The SF is meant to correct only the shape of the pt(top) distribution- not the amount of generated events ( you have to consider that the average weight is not 1 ! ) So we define two category for ttbar events
                                    
                                    //###############################################################################################
                                    int size_topPtRW =2;
                                    
                                    float TotalWeight[2] = {TotalWeight_withTopPtRW,TotalWeight_NoTopPtRW};
                                    std::string topPtRW[2] = {"", "_NoTopRW"};
                                    
                                    if (isTTJets == string::npos) size_topPtRW = 1; // If the sample in not ttbar, don't care about new category
                                    
                                    //###############################################################################################
                                    
                                    
                                    
                                    std::string CHL="MuJet";
                                    
                                    plotFill("Weight_Mu", LepCor,200,0,2);
                                    plotFill("TotalWeight_Mu",TotalWeight_NoTopPtRW*LepCor,1000,0,10);
                                    plotFill("TotalNonLumiWeight_Mu",TotalWeight_NoTopPtRW*LepCor/LumiWeight,1000,0,10);
                                    
                                    
                                    for (int iso = 0; iso < size_isoCat; iso++) {
                                        if (Iso_category[iso]) {
                                            for (int imt = 0; imt < size_mTCat; imt++) {
                                                if (MT_category[imt]) {
                                                    for (int jpt = 0; jpt < size_METcut; jpt++) {
                                                        if (MetCut_category[jpt]) {
                                                            
                                                            for (int jmet = 0; jmet < size_jetMetPhi; jmet++) {
                                                                if (jetMetPhi_category[jmet]) {
                                                                    
                                                                    
                                                                    for (int itopRW = 0; itopRW < size_topPtRW; itopRW++) {
                                                                        
                                                                        
                                                                        
                                                                        float FullWeight = TotalWeight[itopRW] * LepCor *FinalBTagSF ;
                                                                        std::string FullStringName = topPtRW[itopRW] + MT_Cat[imt] + MetCut_Cat[jpt]+  iso_Cat[iso] + jetMetPhi_Cat[jmet]+  ScaleJet_Cat[jetScl]+ResolJet_Cat[jetRes]+ ScaleMETUE_Cat[metUE];
                                                                        
                                                                        //This check is used to make sure that each event is just filled once for any of the categories ==> No doube-counting of events  (this is specially important for ttbar events where we have many jets and leptons)
                                                                        if (!( std::find(HistNamesFilled.begin(), HistNamesFilled.end(), FullStringName) != HistNamesFilled.end())){
                                                                            HistNamesFilled.push_back(FullStringName);
                                                                            
                                                                            
                                                                            //###########################################################################################
                                                                            
                                                                            
                                                                            plotFill(CHL+"_LepPt"+FullStringName,Mu4Momentum.Pt(),2000,0,2000,FullWeight);
                                                                            plotFill(CHL+"_LQMass"+FullStringName,LQ.M(),300,0,3000,FullWeight);
                                                                            
                                                                            
                                                                            
                                                                            //###########################################################################################
                                                                            ////////   Systematic on BTag SF
                                                                            //###########################################################################################
                                                                            
                                                                            //                                                                    plotFill(CHL+"_LQMass_BtagUp"+FullStringName,LQ.M(),300,0,3000,FullWeight*FinalBTagSFUp/FinalBTagSF);
                                                                            //                                                                    plotFill(CHL+"_LQMass_BtagDown"+FullStringName,LQ.M(),300,0,3000,FullWeight*FinalBTagSFDown/FinalBTagSF);
                                                                            
                                                                            //###########################################################################################
                                                                            ////////   Systematic on Top Pt Reweighting
                                                                            //###########################################################################################
                                                                            if (isTTJets!= string::npos) {
                                                                                
                                                                                plotFill(CHL+"_LQMassTopPtRWUp"+FullStringName,LQ.M(),nBin,binMin,binMax,FullWeight * TopPtReweighting);
                                                                                plotFill(CHL+"_LQMassTopPtRWDown"+FullStringName,LQ.M(),nBin,binMin,binMax,FullWeight / TopPtReweighting);
                                                                            }
                                                                            
                                                                            
                                                                            //###########################################################################################
                                                                            ////////   Systematic on W k-factor   PDF + alpha_S
                                                                            //###########################################################################################
                                                                            if (isWJets!= string::npos || isWToMuNu!= string::npos || isWToTauNu!= string::npos) {
                                                                                
                                                                                
                                                                                plotFill(CHL+"_LQMass"+FullStringName+"_ewkKfactor_WUp",LQ.M(),300,0,3000,FullWeight*WBosonKFactor_ewkUp/WBosonKFactor);
                                                                                plotFill(CHL+"_LQMass"+FullStringName+"_ewkKfactor_WDown",LQ.M(),300,0,3000,FullWeight*WBosonKFactor_ewkDown/WBosonKFactor);
                                                                                plotFill(CHL+"_LQMass"+FullStringName+"_W_PDF_AlphaS_Up",LQ.M(),nBin,binMin,binMax,FullWeight*W_PDFAlphaS(WBosonMass,1));
                                                                                plotFill(CHL+"_LQMass"+FullStringName+"_W_PDF_AlphaS_Down",LQ.M(),nBin,binMin,binMax,FullWeight*W_PDFAlphaS(WBosonMass,-1));
                                                                            }
                                                                            
                                                                            
                                                                            
                                                                            
                                                                            //###########################################################################################
                                                                            ////////   Systematic on DY k-factor
                                                                            //###########################################################################################
                                                                            
                                                                            
                                                                            if (isDYJets!= string::npos) {
                                                                                
                                                                                
                                                                                plotFill(CHL+"_LQMass"+FullStringName+"_ewkKfactor_ZUp",LQ.M(),300,0,3000,FullWeight*ZBosonKFactor_ewkUp/ZBosonKFactor);
                                                                                plotFill(CHL+"_LQMass"+FullStringName+"_ewkKfactor_ZDown",LQ.M(),300,0,3000,FullWeight*ZBosonKFactor_ewkDown/ZBosonKFactor);
                                                                                
                                                                            }
                                                                            
                                                                            //##############################################################################
                                                                            //  QCD Scale Uncertainty (alpha_s) for TTbar and W+Jets
                                                                            //##############################################################################
                                                                            //                                                                    //                                                                    if (isTTJets== string::npos &&  isWJets== string::npos &&  isDYJets== string::npos)
                                                                            //                                                                    if (isTTJets== string::npos &&  isWJets== string::npos && isWToMuNu== string::npos)
                                                                            //                                                                        continue; //scale factor only for W and TT
                                                                            //
                                                                            //                                                                    int counterscale=0;
                                                                            //                                                                    int counterpdf=0;
                                                                            //                                                                    int StartNumber=0;  // qcd scale uncertainty for W Madgraph starts from 1000
                                                                            //                                                                        if (isTTJets!= string::npos) StartNumber=1000; // qcd scale uncertainty for ttbar powheg starts from 1000
                                                                            //                                                                        for (int isys=0; isys < pdfSystWeight->size(); isys++){
                                                                            //
                                                                            //                                                                            if (atoi(pdfSystWeightId->at(isys).c_str()) > StartNumber && atoi(pdfSystWeightId->at(isys).c_str()) < StartNumber+10){
                                                                            //
                                                                            //
                                                                            //                                                                                plotFill(CHL+"_LQMass_Scale"+std::to_string(counterscale)+FullStringName,LQ.M(),20,0,2000,FullWeight*pdfSystWeight->at(isys)/pdfWeight);
                                                                            //                                                                                counterscale++;
                                                                            //
                                                                            //                                                                            }
                                                                            //                                                                        }
                                                                            //##############################################################################
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                    
                    //qcd control region   MET > 100 && MT > 150  && Jet < 100 && jet > 50;
                    //qcd
                    
                    //###############################################################################################
                    //  Doing EleTau Analysis
                    //###############################################################################################
                    
                    
                } //End of Tree
            }//End of file
            //##############  end of dielectron
            
        }
        
    }
    
    fout->cd();
    //    BG_Tree->Write();
    
    map<string, TH1F*>::const_iterator iMap1 = myMap1->begin();
    map<string, TH1F*>::const_iterator jMap1 = myMap1->end();
    
    for (; iMap1 != jMap1; ++iMap1)
        nplot1(iMap1->first)->Write();
    
    map<string, TH2F*>::const_iterator iMap2 = myMap2->begin();
    map<string, TH2F*>::const_iterator jMap2 = myMap2->end();
    
    for (; iMap2 != jMap2; ++iMap2)
        nplot2(iMap2->first)->Write();
    
    fout->Close();
    
    
}
