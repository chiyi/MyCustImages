#include "TH1D.h"
#include "TF1.h"

TH1D *h_GLOBAL;

Double_t cust_func1(Double_t *x, Double_t *par)
{
 Double_t xx =x[0];
 Double_t f = par[0]* h_GLOBAL->GetBinContent(h_GLOBAL->FindBin(xx));
 return f;
}

TF1* GenTF1_fromTH1D(TH1D* h_inp, char outname[], int xmin, int xmax, int npar)
{
 h_GLOBAL = h_inp;
 TF1 *fout = new TF1(outname, cust_func1, xmin, xmax, npar);
 fout->SetParNames("bias");
 return fout;
}