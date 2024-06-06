import pandas
import ROOT
from ROOT import TCanvas, TFormula, TF1, TH1D, TH2D, TH1I, TLegend, TDatime, TEfficiency, TGraphAsymmErrors, TMath
from ROOT import gROOT, gSystem, gPad
from ROOT import gStyle

from PyNBPlotStyles.assert_funcs import assert_df, assert_axis, assert_valcols, assert_cats


# Main

def MakeHistogram(
    inpdf: pandas.DataFrame,
    col_x: str,
    col_y: str,
    hname: str,
    htitle: str,
    nbinsx: int,
    xmin: float,
    xmax: float,
    col_yerr: str = None,
    categories_x: list[str] = None,
    b_reseterr: bool = True
) -> TH1D:
    CheckParameters(inpdf, col_x, col_y, hname, htitle, nbinsx, xmin, xmax, col_yerr, categories_x, b_reseterr)
    res = init_histogram(hname, htitle, nbinsx, xmin, xmax, categories_x)
    res = fill_histogram(res, inpdf, col_x, col_y)
    if b_reseterr:
        res = ResetBinError(res, col_yerr)
    return res


# helpers

def CheckParameters(
    inpdf: pandas.DataFrame,
    col_x: str,
    col_y: str,
    hname: str,
    htitle: str,
    nbinsx: int,
    xmin: float,
    xmax: float,
    col_yerr: str = None,
    categories_x: list[str] = None,
    b_reseterr: bool = True
):
    assert_df(inpdf)
    assert_axis(nbinsx, xmin, xmax)
    assert_valcols([col_x, col_y], inpdf)

    if col_yerr is None:
        if b_reseterr:
            print('set bin_error as sqrt(y)')
        else:
            print('set bin_error by default')
    else:
        print('set bin_error from '+col_yerr)
        assert col_yerr in inpdf.columns
      
    if categories_x is not None:
        assert_cats(nbinsx, xmax, categories_x)

def ResetBinError(
    res: TH1D,
    inpdf: pandas.DataFrame,
    col_yerr: str = None
) -> TH1D:
    dict_err2 = dict()
    if col_yerr is not None:
        for irow in inpdf.iterrows():
            xval = irow[1][col_x] + 0.5 * bin_width
            yerr = irow[1][col_yerr]
            ibin = res.FindBin(xval)
            dict_err2[ibin] += yerr2
    for ibin in range(res.GetNbinsX()+1):
        yerr2 = res.GetBinContent(ibin) if (col_yerr is None) else dict_err2[ibin]
        if yerr2 >= 0:
            res.SetBinError(ibin, TMath.Sqrt(yerr2))
    return res

def CleanBinError(inph: TH1D) -> TH1D:
    print('clean bin errors')
    for ibin in range(inph.GetNbinsX()+2):
        inph.SetBinError(ibin, 0)
    return inph

def MakeTemplate(
    list_histos: list[TH1D],
    htitle: str,
    categories_x: list[str] = None
) -> TH1D:
    h_tmp = list_histos[0].Clone("h_tmp")
    h_tmp.Reset()
    if categories_x is not None:
        for icat in categories_x:
            h_tmp.Fill(icat, 0)
    ymax = max(map(lambda x: x.GetMaximum(), list_histos))
    ymin = min(map(lambda x: x.GetMinimum(), list_histos))
    h_tmp.SetMinimum(ymin)
    h_tmp.SetMaximum(ymax)
    h_tmp.SetTitle(htitle)
    h_tmp.GetYaxis().SetRangeUser(0.3333*h_tmp.GetMinimum(), 3*h_tmp.GetMaximum())
    return h_tmp


## workers

def init_histogram(
    hname: str,
    htitle: str,
    nbinsx: int,
    xmin: float,
    xmax: float,
    categories_x: list[str] = None
) -> TH1D:
    obj_chk = gROOT.FindObject(hname)
    if obj_chk != None:
        print('Deleteing previous hname='+hname)
        obj_chk.Delete()
    res = TH1D(hname, htitle, nbinsx, xmin, xmax)
    if categories_x is not None:
        for icat in categories_x:
            res.Fill(icat, 0)
    return res

def fill_histogram(
    res: TH1D,
    inpdf: pandas.DataFrame,
    col_x: str,
    col_y: str
) -> TH1D:
    bin_width = res.GetBinWidth(1) # for constant binning
    for irow in inpdf.iterrows():
        xval = irow[1][col_x] + 0.5 * bin_width
        yval = irow[1][col_y]
        res.Fill(xval, yval)
    return res


