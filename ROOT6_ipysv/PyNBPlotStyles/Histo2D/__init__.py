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
    col_z: str,
    hname: str,
    htitle: str,
    nbinsx: int,
    xmin: float,
    xmax: float,
    nbinsy: int,
    ymin: float,
    ymax: float,
    col_zerr: int = None,
    categories_x: list[str] = None,
    categories_y: list[str] = None
) -> TH2D:
    CheckParameters(inpdf, col_x, col_y, col_z, hname, htitle, nbinsx, xmin, xmax, nbinsy, ymin, ymax, col_zerr, categories_x, categories_y)
    res = init_histogram(hname, htitle, nbinsx, xmin, xmax, nbinsy, ymin, ymax, categories_x, categories_y)
    res = fill_histogram(res, inpdf, col_x, col_y, col_z)
    res = ResetBinError(res, col_zerr)
    return res


# helpers

def CheckParameters(
    inpdf: pandas.DataFrame, 
    col_x: str, 
    col_y: str, 
    col_z: str, 
    hname: str, 
    htitle: str, 
    nbinsx: int, 
    xmin: float, 
    xmax: float, 
    nbinsy: int, 
    ymin: float, 
    ymax: float, 
    col_zerr: int = None, 
    categories_x: list[str] = None, 
    categories_y: list[str] = None
):
    assert_df(inpdf)
    assert_axis(nbinsx, xmin, xmax)
    assert_axis(nbinsy, ymin, ymax)
    assert_valcols([col_x, col_y, col_z], inpdf)
    
    if col_zerr is None:
        print('set bin_error as sqrt(z)')
    else:
        print('set bin_error from '+col_zerr)
        assert col_zerr in columns

    if categories_x is not None:
        assert_cats(nbinsx, xmax, categories_x)

    if categories_y is not None:
        assert_cats(nbinsy, ymax, categories_y)

def ResetBinError(
    res: TH2D,
    inpdf: pandas.DataFrame,
    col_zerr: str = None
) -> TH2D:
    dict_err2 = dict()
    binx_width = res.GetXaxis().GetBinWidth(1) # for constant binning
    biny_width = res.GetYaxis().GetBinWidth(1) # for constant binning
    if col_zerr is not None:
        for irow in inpdf.iterrows():
            xval = irow[1][col_x] + 0.5 * binx_width
            yval = irow[1][col_y] + 0.5 * biny_width
            yerr = irow[1][col_zerr]
            ibinx = res.FindBin(xval)
            ibiny = res.FindBin(yval)
            if (ibinx,ibiny) in dict_err2:
                dict_err2[(ibinx,ibiny)] += zerr2
            else:
                dict_err2[(ibinx,ibiny)] = 0.
    for ikey in dict_err2.keys():
        zerr2 = dict_err2[ikey]
        if zerr2 > 0:
            res.SetBinError(ikey[0], ikey[1], TMath.Sqrt(zerr2))
    return res

def CleanBinError(inph: TH2D) -> TH2D:
    print('clean bin errors')
    for ibinx in range(inph.GetNbinsX()+2):
        for ibiny in range(inph.GetNbinsY()+2):
            inph.SetBinError(ibinx, ibiny, 0)
    return inph

def MakeTemplate(
    list_histos: list[TH2D],
    htitle: str,
    categories_x: list[str] = None,
    categories_y: list[str] = None
) -> TH2D:
    h_tmp = list_histos[0].Clone("h_tmp")
    h_tmp.Reset()
    if categories_x is not None:
        for icat in categories_x:
            h_tmp.Fill(icat, 0)
    if categories_y is not None:
        for icat in categories_y:
            h_tmp.Fill(icat, 0)
    zmax = max(map(lambda x: x.GetMaximum(), list_histos))
    zmin = min(map(lambda x: x.GetMinimum(), list_histos))
    h_tmp.SetMinimum(zmin)
    h_tmp.SetMaximum(zmax)
    h_tmp.SetTitle(htitle)
    h_tmp.GetZaxis().SetRangeUser(0.3333*h_tmp.GetMinimum(), 3*h_tmp.GetMaximum())
    return h_tmp


## workers

def init_histogram(
    hname: str,
    htitle: str,
    nbinsx: int,
    xmin: float,
    xmax: float,
    nbinsy: int,
    ymin: float,
    ymax: float,
    categories_x: list[str] = None,
    categories_y: list[str] = None
):
    obj_chk = gROOT.FindObject(hname)
    if obj_chk != None:
        print('Deleteing previous hname='+hname)
        obj_chk.Delete()
    res = TH2D(hname, htitle, nbinsx, xmin, xmax, nbinsy, ymin, ymax)
    if categories_x is not None:
        for icat in categories_x:
            res.Fill(icat, 0)
    if categories_y is not None:
        for icat in categories_y:
            res.Fill(icat, 0)
    return res

def fill_histogram(
    res: TH2D,
    inpdf: pandas.DataFrame,
    col_x: str,
    col_y: str,
    col_z: str
) -> TH2D:
    binx_width = res.GetXaxis().GetBinWidth(1) # for constant binning
    biny_width = res.GetYaxis().GetBinWidth(1) # for constant binning
    for irow in inpdf.iterrows():
        xval = irow[1][col_x] + 0.5 * binx_width
        yval = irow[1][col_y] + 0.5 * biny_width
        res.Fill(xval, yval)
    return res


