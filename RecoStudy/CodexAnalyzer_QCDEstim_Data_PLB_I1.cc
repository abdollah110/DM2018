////////////////////////////////////////////////////////////
// This code is run over specific skimmed samples with muon pt > 60 GeV, jet pt > 50 GeV and MET > 40 GeV and mu RelIso < 1.0. The out files are storeed in
// Outfile_QCD
////////////////////////////////////////////////////////////

#include "../interface/Functions.h"
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
    float BJetPtCut=20;
    float SimpleJetPtCut=30;
    float ElectronPtCut_=15;
    //    float CSVCut=   0.9535   ;                  //  https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
    float CSVCut=   0.8838   ;                  //  https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
    float LeptonIsoCut=0.15;
    
    //########################################################################################################################################################
    //########################################################################################################################################################
    //########################################################################################################################################################
    //                                                  Loop over inout ROOT files
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
        
        
        
        //#####################################################################
        //#####################################################################
        //                           Loop over Events in each ROOT files
        //#####################################################################
        //#####################################################################
        Int_t nentries_wtn = (Int_t) Run_Tree->GetEntries();
        cout<<"nentries_wtn===="<<nentries_wtn<<"\n";
        for (Int_t i = 0; i < nentries_wtn; i++) {
            //                    for (Int_t i = 0; i < 10000; i++) {
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
            
            WBosonPt=genInfo[1];
            WBosonMass=genInfo[3];
            
            size_t isWJetsToLNu_Inc = InputROOT.find("WJetsToLNu_Inc");
            //            size_t isWJets = InputROOT.find("WJets");
            size_t isWJets = InputROOT.find("JetsToLNu");
            size_t isWToMuNu = (InputROOT.find("WToMuNu") );
            size_t isWToTauNu = (InputROOT.find("WToTauNu") );
            
            if (WBosonMass > 100 && (isWToMuNu!= string::npos || isWToTauNu!=string::npos)) WBosonKFactor=HistMassDepKFactor->GetBinContent(int(WBosonMass)/10 +1); //Mass binned K-factor
            if (WBosonMass <= 100 && isWJets!= string::npos  )WBosonKFactor= FuncBosonKFactor("W1Cen") + FuncBosonKFactor("W2Cen") * WBosonPt; //HT binned & inclusive K-factor
            //            if (WBosonMass <= 100 && isWJets!= string::npos  )WBosonKFactor= 1.21; //JetBinned binned & inclusive K-
            
            //................................................................................................................
            //................................................................................................................
            if (isWJets!= string::npos && WBosonMass > 100) continue;
            if (isWJetsToLNu_Inc!= string::npos && (genHT > 100.0 && genHT < 2500.0)) continue; //FIXME until I have 2 missing 70 and Inf samples
            //            if (isWJetsToLNu_Inc!= string::npos && genHT > 70.0) continue;
            //................................................................................................................
            //................................................................................................................
            
            //            //######################## Z K-factor
            float ZBosonPt=0;
            float ZBosonKFactor=1;
            size_t isDYJets = InputROOT.find("DYJets");
            ZBosonPt=genInfo[2];
            if (isDYJets!= string::npos) ZBosonKFactor= FuncBosonKFactor("Z1Cen") + FuncBosonKFactor("Z2Cen") * ZBosonPt;
            
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
                //                cout<<"puTrue->at(0)= "<<puTrue->at(0)<< "       puNUmmc= "<<puNUmmc << "   puNUmdata= "<<puNUmdata<<" PUWeight===="<<PUWeight<<  " PUData_"<<   PUData_<<  " PUMC_ "<< PUMC_  <<"\n";
                
            }
            
            
            //############################################################################################
            //   Final Total Weight
            //############################################################################################
            //  FIXME   No PU reweighting
            //            PUWeight=1;
            //############################################################################################
            
//            float TotalWeight = LumiWeight * GetGenWeight * PUWeight * TopPtReweighting * WBosonKFactor * ZBosonKFactor ; //For QCD Estim remove Top Pt reweighting
            float TotalWeight = LumiWeight * GetGenWeight * PUWeight * WBosonKFactor * ZBosonKFactor ;
            
            
            
            //            cout <<"  LumiWeight * GetGenWeight * PUWeight * TopPtReweighting * WBosonKFactor * ZBosonKFactor  "  <<  LumiWeight <<"   "<< GetGenWeight <<"   "<< PUWeight <<"   "<< TopPtReweighting <<"   "<< WBosonKFactor <<"   "<<  ZBosonKFactor<<"\n";
            //###########       numTau   ###########################################################
            int numTau= getNumTau();
            
            //###########       Ele Veto   ###########################################################
            //            https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2#Recommended_MVA_recipes_for_2016
            int numElectron=0;
            float ElectronCor=1;
            TLorentzVector Ele4Momentum;
            float ElectronEffVeto=1;
            Ele4Momentum.SetPtEtaPhiM(0,0,0,0);
            for  (int jele=0 ; jele < nEle; jele++){  //FIXME
                
                if ( elePt->at(jele) < 15 || fabs(eleEta->at(jele)) > 2.5) continue;
                
                bool eleMVAIdExtra= false;
                if (fabs (eleSCEta->at(jele)) <= 0.8 && eleIDMVAIso->at(jele) >   -0.83  ) eleMVAIdExtra= true;
                else if (fabs (eleSCEta->at(jele)) >  0.8 &&fabs (eleSCEta->at(jele)) <=  1.5 && eleIDMVAIso->at(jele) >   -0.77  ) eleMVAIdExtra= true;
                else if ( fabs (eleSCEta->at(jele)) >=  1.5 && eleIDMVAIso->at(jele) >  -0.69  ) eleMVAIdExtra= true;
                else eleMVAIdExtra= false;
                
                
                
                if (!(eleMVAIdExtra )) {
                    ElectronEffVeto= ElectronEffVeto * getEffVetoMVA90WPElectron94X(isData,  elePt->at(jele),eleSCEta->at(jele),    HistoEleMVAIdIso90 , HistoEleMVAIdIso90_EffMC,HistoEleMVAIdIso90_EffData);
                    continue;
                }
                
                ElectronCor=getCorrFactorMVA90WPElectron94X(isData,  elePt->at(jele),eleSCEta->at(jele),    HistoEleMVAIdIso90 );
                ElectronCor=1;
                Ele4Momentum.SetPtEtaPhiM(elePt->at(jele),eleEta->at(jele),elePhi->at(jele),eleMass);
                numElectron++;
                
                break;
            }
            //###########       BTag SF   ###########################################################
            float FinalBTagSF=FuncFinalBTagSF(isData,Btagg_TT,BJetPtCut,CSVCut);
            //            float FinalBTagSF=1;
            
            
            //###########       numBJet   ###########################################################
            int numBJet=numBJets(BJetPtCut,CSVCut);
            
            //###########       numJet   ###########################################################
            int numJet=numJets(SimpleJetPtCut);
            
            //###########       numZboson   ###########################################################
            int numZboson = getNumZBoson();
            
            //###############################################################################################
            //  Some Histogram Filling
            //###############################################################################################
            plotFill("_WeightLumi",LumiWeight,10000,0,1000);
            plotFill("_WeightGen",GetGenWeight,10000,0,1000);
            plotFill("_WeightPU",PUWeight,10000,0,1000);
            plotFill("_WeightTopPtReweighting",TopPtReweighting,100,0,2);
            plotFill("_WeightWBosonKFactor",WBosonKFactor,500,0,5);
            plotFill("_ZeightWBosonKFactor",ZBosonKFactor,500,0,5);
            
            
            
            plotFill("_WBosonPt",WBosonPt,150,0,1500,PUWeight);
            plotFill("_FinalBTagSF", FinalBTagSF,200,0,2);
            
            for (int qq=0; qq < 60;qq++){
                if ((HLTEleMuX >> qq & 1) == 1)
                    plotFill("_HLT",qq,60,0,60);
            }
            
            
            //############################################################################################
            //###########       Loop over MuJet events   #################################################
            //############################################################################################
            TLorentzVector Mu4Momentum, Jet4Momentum,KJet4Momentum,LQ4Momentum,Mu24Momentum;
            
            for  (int imu=0 ; imu < nMu; imu++){
                
                float IsoMu=muPFChIso->at(imu)/muPt->at(imu);
                if ( (muPFNeuIso->at(imu) + muPFPhoIso->at(imu) - 0.5* muPFPUIso->at(imu) )  > 0.0)
                    IsoMu= ( muPFChIso->at(imu) + muPFNeuIso->at(imu) + muPFPhoIso->at(imu) - 0.5* muPFPUIso->at(imu))/muPt->at(imu);
                //                    IsoMu= ( muPFChIso->at(imu)/muPt->at(imu) + muPFNeuIso->at(imu) + muPFPhoIso->at(imu) - 0.5* muPFPUIso->at(imu))/muPt->at(imu); BUG at APril2018
                
                bool MuPtCut = muPt->at(imu) > LeptonPtCut_ && fabs(muEta->at(imu)) < 2.4 ;
                bool MuIdIso=( (muIDbit->at(imu) >> 2 & 1)  && fabs(muD0->at(imu)) < 0.045 && fabs(muDz->at(imu)) < 0.2); //Tight Muon Id
                
                
                if (! MuPtCut || !MuIdIso || IsoMu > 1.0) continue;
                
                
                float MuonCor=getCorrFactorMuon94X(isData,  muPt->at(imu), muEta->at(imu) , HistoMuId,HistoMuIso,HistoMuTrg,HistoMuTrack);
                
                Mu4Momentum.SetPtEtaPhiM(muPt->at(imu),muEta->at(imu),muPhi->at(imu),MuMass);
                
                
                
                //###########      Finding the closest jet near mu   ###########################################################
                
                float CLoseJetMuPt=muPt->at(imu);
                float CLoseJetMuEta=muEta->at(imu);
                
                if (MuPtCut && MuIdIso ){
                    
                    double Refer_R_jetmu = 5;
                    
                    for (int kjet= 0 ; kjet < nJet ; kjet++){
                        KJet4Momentum.SetPtEtaPhiE(jetPt->at(kjet),jetEta->at(kjet),jetPhi->at(kjet),jetEn->at(kjet));
                        
                        
                        if (KJet4Momentum.DeltaR(Mu4Momentum) < Refer_R_jetmu) {
                            Refer_R_jetmu = KJet4Momentum.DeltaR(Mu4Momentum);
                            if (Refer_R_jetmu < 0.5 && jetPt->at(kjet)  >= muPt->at(imu)) {
                                CLoseJetMuPt = jetPt->at(kjet);
                                CLoseJetMuEta = jetEta->at(kjet);
                                
                            }
                        }
                    }
                }
                
                
                
                
                
                //###########    loop over  Jet    ###########################################################
                for (int ijet= 0 ; ijet < nJet ; ijet++){
                    
                    
                    
                    
                    
                    Jet4Momentum.SetPtEtaPhiE(jetPt->at(ijet),jetEta->at(ijet),jetPhi->at(ijet),jetEn->at(ijet));
                    
                    
                    bool goodJet = (jetPFLooseId->at(ijet) > 0.5 && jetPt->at(ijet) > JetPtCut && fabs(jetEta->at(ijet)) < 2.4 && Jet4Momentum.DeltaR(Mu4Momentum) > 0.5);
                    if (! goodJet) continue;
                    
                    LQ4Momentum=Jet4Momentum + Mu4Momentum;
                    
                    bool isThisJetElectron= Jet4Momentum.DeltaR(Ele4Momentum) < 0.5;

                    
                    
                    
                    //###############################################################################################
                    //  Isolation Categorization
                    //###############################################################################################
                    //###############################################################################################
                    bool LepPassIsolation= IsoMu < LeptonIsoCut;
                    
                    const int size_isoCat = 3;
                    bool Isolation = LepPassIsolation;
                    bool AntiIsolation =  !LepPassIsolation;
                    bool Total = 1;
                    
                    bool Iso_category[size_isoCat] = {Isolation, AntiIsolation,Total};
                    std::string iso_Cat[size_isoCat] = {"_Iso", "_AntiIso","_Total"};
                    //###############################################################################################
                    //  MT Categorization
                    //###############################################################################################
                    float tmass_MuMet= TMass_F(muPt->at(imu), muPt->at(imu)*cos(muPhi->at(imu)),muPt->at(imu)*sin(muPhi->at(imu)) , pfMET, pfMETPhi);
                    
                    const int size_mTCat = 3;
                    bool NoMT = 1;
                    bool LoWMT = (tmass_MuMet < 40);
                    bool HighMT = (tmass_MuMet > 100);
                    
                    bool MT_category[size_mTCat] = {NoMT,LoWMT,HighMT};
                    std::string MT_Cat[size_mTCat] = {"_NoMT", "_LowMT","_HighMT"};
                    
                    float tmass_JetMet= TMass_F(jetPt->at(ijet), jetPt->at(ijet)*cos(jetPhi->at(ijet)),jetPt->at(ijet)*sin(jetPhi->at(ijet)) , pfMET, pfMETPhi);
                    float tmass_LQMet= TMass_F(LQ4Momentum.Pt(), LQ4Momentum.Px(),LQ4Momentum.Py(), pfMET, pfMETPhi);
                    
                    //###############################################################################################
                    //  dPhi Jet_MET Categorization
                    //###############################################################################################
                    const int size_jetMetPhi = 2;
//                    bool lowDPhi = (deltaPhi(Jet4Momentum.Phi(),pfMETPhi) < 0.5 || deltaPhi(Mu4Momentum.Phi(),pfMETPhi) < 0.5 );
//                    bool HighDPhi = (deltaPhi(Jet4Momentum.Phi(),pfMETPhi) >= 0.5 && deltaPhi(Mu4Momentum.Phi(),pfMETPhi) >= 0.5  );
                    bool lowDPhi = deltaPhi(Jet4Momentum.Phi(),pfMETPhi) < 0.5;
                    bool HighDPhi = deltaPhi(Jet4Momentum.Phi(),pfMETPhi) > 0.5;
                    
                    bool jetMetPhi_category[size_jetMetPhi] = {lowDPhi,HighDPhi};
                    std::string jetMetPhi_Cat[size_jetMetPhi] = {"_LowDPhi", "_HighDPhi"};
                    
                    //###############################################################################################
                    //  LQ eta Categorization
                    //###############################################################################################
                    const int size_lqEta = 1;
                    bool TotLQ = 1;
                    bool lqEta_category[size_lqEta] = {TotLQ};
                    std::string lqEta_Cat[size_lqEta] = {"_TotEta"};
                    
                    //###############################################################################################
                    //  TTbar control region Categorization
                    //###############################################################################################
                    const int size_CR = 1;
                    bool signalRegion = numTau+numZboson + numElectron + numBJet < 1 ;
                    bool region_category[size_CR] = {signalRegion};
                    std::string region_Cat[size_CR] = {""};
                    
                    //###############################################################################################
                    
                    std::string CHL="MuJet";
                    
                    plotFill("Weight_Mu", MuonCor,200,0,2);
                    plotFill("TotalWeight_Mu",TotalWeight*MuonCor,1000,0,10);
                    plotFill("TotalNonLumiWeight_Mu",TotalWeight*MuonCor/LumiWeight,1000,0,10);
                    
                    
                    for (int iso = 0; iso < size_isoCat; iso++) {
                        if (Iso_category[iso]) {
                            for (int imt = 0; imt < size_mTCat; imt++) {
                                if (MT_category[imt]) {
                                    for (int jpt = 0; jpt < size_jetMetPhi; jpt++) {
                                        if (jetMetPhi_category[jpt]) {
                                            for (int ieta = 0; ieta < size_lqEta; ieta++) {
                                                if (lqEta_category[ieta]) {
                                                    for (int iCR = 0; iCR < size_CR; iCR++) {
                                                        if (region_category[iCR]) {
                                                            
                                                            
                                                            
                                                            
                                                            float FullWeight = TotalWeight * MuonCor * FinalBTagSF;
                                                            std::string FullStringName = MT_Cat[imt] + jetMetPhi_Cat[jpt] + lqEta_Cat[ieta] + region_Cat[iCR] + iso_Cat[iso]  ;
                                                            
                                                            
                                                            
                                                            //##################
                                                            //This check is used to make sure that each event is just filled once for any of the categories ==> No doube-counting of events  (this is specially important for ttbar events where we have many jets and leptons)
                                                            if (!( std::find(HistNamesFilled.begin(), HistNamesFilled.end(), FullStringName) != HistNamesFilled.end())){
                                                                HistNamesFilled.push_back(FullStringName);
                                                                
                                                                plotFill(CHL+"_tmass_MuMet"+FullStringName,tmass_MuMet,200,0,2000,FullWeight);
//                                                                plotFill(CHL+"_tmass_JetMet"+FullStringName,tmass_JetMet,200,0,2000,FullWeight);
//                                                                plotFill(CHL+"_tmass_LQMet"+FullStringName,tmass_LQMet,200,0,2000,FullWeight);
                                                                
                                                                plotFill(CHL+"_JetPt"+FullStringName,jetPt->at(ijet) ,2000,0,2000,FullWeight);
//                                                                plotFill(CHL+"_JetEta"+FullStringName,jetEta->at(ijet),100,-2.5,2.5,FullWeight);
                                                                plotFill(CHL+"_LepPt"+FullStringName,muPt->at(imu),2000,0,2000,FullWeight);
                                                                plotFill(CHL+"_LepEta"+FullStringName,muEta->at(imu),100,-2.5,2.5,FullWeight);
                                                                plotFill(CHL+"_CloseJetLepPt"+FullStringName,CLoseJetMuPt,1000,0,1000,FullWeight);
                                                                plotFill(CHL+"_CloseJetLepEta"+FullStringName,CLoseJetMuEta,100,-2.5,2.5,FullWeight);
                                                                
//                                                                if (fabs(muEta->at(imu)) < 1.5) plotFill(CHL+"_CloseJetLepPtBarrel"+FullStringName,CLoseJetMuPt,1000,0,1000,FullWeight);
//                                                                if (fabs(muEta->at(imu)) >= 1.5) plotFill(CHL+"_CloseJetLepPtEndcap"+FullStringName,CLoseJetMuPt,1000,0,1000,FullWeight);
//
//                                                                plotFill(CHL+"_nVtx"+FullStringName,nVtx,50,0,50,FullWeight);
//                                                                plotFill(CHL+"_nVtx_NoPU"+FullStringName,nVtx,50,0,50,TotalWeight * MuonCor / PUWeight);
                                                                
                                                                plotFill(CHL+"_MET"+FullStringName,pfMET,200,0,2000,FullWeight);
                                                                plotFill(CHL+"_NumBJet"+FullStringName,numBJet,5,0,5,FullWeight);
                                                                plotFill(CHL+"_FinalBTagSF"+FullStringName,FinalBTagSF,500,0,5,FullWeight);
                                                                
//                                                                plotFill(CHL+"_LQMass"+FullStringName,LQ4Momentum.M(),200,0,2000,FullWeight);
//                                                                plotFill(CHL+"_LQEta"+FullStringName,LQ4Momentum.Eta(),300,-3,3,FullWeight);
//                                                                plotFill(CHL+"_LQPt"+FullStringName,LQ4Momentum.Pt(),200,0,2000,FullWeight);
//                                                                plotFill(CHL+"_genHT"+FullStringName,genHT,200,0,2000,FullWeight);
                                                                
                                                                //                                                            plotFill(CHL+"_MuPtOverJetPt"+FullStringName,muPt->at(imu)/jetPt->at(ijet),1000,0,10,FullWeight);
                                                                //                                                            plotFill(CHL+"_LQPtOverMET"+FullStringName,LQ4Momentum.Pt()/pfMET,1000,0,10,FullWeight);
                                                                
                                                                plotFill(CHL+"_dPhi_Jet_Met"+FullStringName,deltaPhi(Jet4Momentum.Phi(),pfMETPhi),200,0,4,FullWeight);
//                                                                plotFill(CHL+"_dPhi_Mu_Met"+FullStringName,deltaPhi(Mu4Momentum.Phi(),pfMETPhi),200,0,4,FullWeight);
                                                                
//                                                                plotFill(CHL+"_BosonKFactor"+FullStringName,ZBosonKFactor*WBosonKFactor,200,0,2,FullWeight);

                                                                
                                                                
                                                                
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
                    
                    //###############################################################################################
                    //  Doing EleTau Analysis
                    //###############################################################################################
                    
                    
                } //End of Tree
            }//End of file
            //##############  end of dielectron
            
        }
        
    }
    
    fout->cd();
    
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
