#include "../interface/CodexAnalyzer.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TTree.h"
#include "TFile.h"
#include "TSystem.h"
#include <string>
#include <ostream>
#include <vector>


int main(int argc, char** argv) {
    using namespace std;
    
    std::string out = *(argv + 1);
    
    cout << "\n\n\n OUTPUT NAME IS:    " << out << endl;     //PRINTING THE OUTPUT name
    TFile *fout = TFile::Open(out.c_str(), "RECREATE");
    
    std::vector<string> input;
    for (int f = 2; f < argc; f++) {
        input.push_back(*(argv + f));
        cout << "\n INPUT NAME IS:   " << input[f - 2] << "\n";
    }
    
    
    Float_t Ptbins[] = {0,50,70,100,140,200,300,600,1000};
    Float_t Etabins[] = {0,0.8,1.5,2.5};
    Int_t  Ptbin_ = sizeof(Ptbins)/sizeof(Float_t) - 1; // or just = 9
    Int_t  Etabin_ = sizeof(Etabins)/sizeof(Float_t) - 1; // or just = 9
    TH2F* BSF_FLV0_Total = new TH2F("BSF_FLV0_Total","BSF_FLV0_Total", Ptbin_, Ptbins, Etabin_, Etabins);
    TH2F* BSF_FLV0_Btagged = new TH2F("BSF_FLV0_Btagged","BSF_FLV0_Btagged", Ptbin_, Ptbins, Etabin_, Etabins);
    TH2F* BSF_FLV5_Total = new TH2F("BSF_FLV5_Total","BSF_FLV5_Total", Ptbin_, Ptbins, Etabin_, Etabins);
    TH2F* BSF_FLV5_Btagged = new TH2F("BSF_FLV5_Btagged","BSF_FLV5_Btagged", Ptbin_, Ptbins, Etabin_, Etabins);
    
    
    for (int k = 0; k < input.size(); k++) {
        
        //std::string input = *(argv + 2);
        TFile *f_Double = TFile::Open(input[k].c_str());
        cout << "\n  Now is running on ------->   " << std::string(f_Double->GetName()) << "\n";
        
        std::string InputROOT= std::string(f_Double->GetName());
        TFile * myFile = TFile::Open(f_Double->GetName());
        TH1F * HistoTot = (TH1F*) myFile->Get("hcount");
        
        TTree *Run_Tree = (TTree*) f_Double->Get("EventTree");
        
        cout.setf(ios::fixed, ios::floatfield);
        cout.precision(6);
        
        //########################################   Jet Info
        Run_Tree->SetBranchAddress("nJet",&nJet);
        Run_Tree->SetBranchAddress("jetPt",&jetPt);
        Run_Tree->SetBranchAddress("jetEta",&jetEta);
        Run_Tree->SetBranchAddress("jetPhi",&jetPhi);
        Run_Tree->SetBranchAddress("jetEn",&jetEn);
        Run_Tree->SetBranchAddress("jetCSV2BJetTags",&jetCSV2BJetTags);
        Run_Tree->SetBranchAddress("jetPFLooseId",&jetPFLooseId);
        Run_Tree->SetBranchAddress("jetPUID",&jetPUID);
        Run_Tree->SetBranchAddress("jetRawPt",&jetRawPt);
        Run_Tree->SetBranchAddress("jetJECUnc",&jetJECUnc);
        Run_Tree->SetBranchAddress("jetRawEn",&jetRawEn);
        Run_Tree->SetBranchAddress("jetHadFlvr",&jetHadFlvr);
        
        //###############################################################################################
        //  parameters
        //###############################################################################################
        float BJetPtCut=30;
        float CSVCut=   0.9693   ;                  //  https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
        
        
        Int_t nentries_wtn = (Int_t) Run_Tree->GetEntries();
        cout<<"nentries_wtn===="<<nentries_wtn<<"\n";
        for (Int_t i = 0; i < nentries_wtn; i++) {
            Run_Tree->GetEntry(i);
            if (i % 10000 == 0) fprintf(stdout, "\r  Processed events: %8d of %8d ", i, nentries_wtn);
            fflush(stdout);
            
            if (isData && (metFilters!=1536)) continue;
            std::vector<string> HistNamesFilled;
            HistNamesFilled.clear();
            //###############################################################################################
            //  Loop Over jets
            //###############################################################################################
            for (int ijet= 0 ; ijet < nJet ; ijet++){
                
                if (jetPFLooseId->at(ijet) > 0.5 && jetPt->at(ijet) > BJetPtCut && fabs(jetEta->at(ijet)) < 2.4 ){
                                        
                    if (jetHadFlvr->at(ijet)==0)  BSF_FLV0_Total->Fill(jetPt->at(ijet),fabs(jetEta->at(ijet)));
                    if (jetHadFlvr->at(ijet)==4)  BSF_FLV5_Total->Fill(jetPt->at(ijet),fabs(jetEta->at(ijet)));
                    if (jetHadFlvr->at(ijet)==5)  BSF_FLV5_Total->Fill(jetPt->at(ijet),fabs(jetEta->at(ijet)));
                    
                    if (jetHadFlvr->at(ijet)==0 && jetCSV2BJetTags->at(ijet)>CSVCut)  BSF_FLV0_Btagged->Fill(jetPt->at(ijet),fabs(jetEta->at(ijet)));
                    if (jetHadFlvr->at(ijet)==4 && jetCSV2BJetTags->at(ijet)>CSVCut)  BSF_FLV5_Btagged->Fill(jetPt->at(ijet),fabs(jetEta->at(ijet)));
                    if (jetHadFlvr->at(ijet)==5 && jetCSV2BJetTags->at(ijet)>CSVCut)  BSF_FLV5_Btagged->Fill(jetPt->at(ijet),fabs(jetEta->at(ijet)));
                    
                }
            }
        }
    }
    
    fout->cd();
    BSF_FLV0_Total->Write();
    BSF_FLV0_Btagged->Write();
    BSF_FLV5_Total->Write();
    BSF_FLV5_Btagged->Write();
    fout->Close();
}
