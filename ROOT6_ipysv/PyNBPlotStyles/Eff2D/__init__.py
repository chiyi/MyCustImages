import numpy
import pandas
import functools
import ROOT
from ROOT import TCanvas, TFormula, TF1, TH1D, TH2D, TH1I, TLegend, TDatime, TEfficiency, TGraphAsymmErrors, TMath
from ROOT import gROOT, gSystem, gPad
from ROOT import gStyle

from PyNBPlotStyles.assert_funcs import assert_df, assert_axis, assert_valcols, assert_cats, assert_confidentlevels, assert_lowedges


# Main

def MakeEfficiency(
    inpdf: pandas.DataFrame,
    col_x: str,
    col_y: str,
    col_z_pass: str,
    col_z_total: str,
    effname: str,
    efftitle: str,
    nbinsx: int,
    xmin: float,
    xmax: float,
    nbinsy: int,
    ymin: float,
    ymax: float,
    level: float = None,
    level_sigma: float = 1,
    categories_x: list[str] = None,
    categories_y: list[str] = None
) -> TEfficiency:
    CheckParameters(inpdf, col_x, col_y, col_z_pass, col_z_total, effname, efftitle, nbinsx, xmin, xmax, nbinsy, ymin, ymax, level, level_sigma, categories_x, categories_y)
    res = init_efficiency(effname, efftitle, nbinsx, xmin, xmax, nbinsy, ymin, ymax, level, level_sigma)
    res = fill_efficiency(res, inpdf, col_x, col_y, col_z_pass, col_z_total)
    return res


# helpers

def CheckParameters(
    inpdf: pandas.DataFrame, 
    col_x: str, 
    col_y: str, 
    col_z_pass: str, 
    col_z_total: str, 
    effname: str, 
    efftitle: str, 
    nbinsx: int, 
    xmin: float, 
    xmax: float, 
    nbinsy: int, 
    ymin: float, 
    ymax: float, 
    level: float = None, 
    level_sigma: float = 1, 
    categories_x: list[str] = None, 
    categories_y: list[str] = None
):
    assert_df(inpdf)
    assert_axis(nbinsx, xmin, xmax)
    assert_axis(nbinsy, ymin, ymax)
    assert_valcols([col_x, col_y, col_z_pass, col_z_total], inpdf)
    assert_confidentlevels(level, level_sigma)

    if categories_x is not None:
        assert_cats(nbinsx, xmax, categories_x)
    if categories_y is not None:
        assert_cats(nbinsy, ymax, categories_y)


def MakeTemplate(
    list_effs: list[TEfficiency],
    efftitle: str,
    categories_x: list[str] = None,
    categories_y: list[str] = None
) -> TH2D:
    h_tmp = list_effs[0].GetPassedHistogram().Clone("h_tmp")
    h_tmp.Reset()
    if categories_x is not None and categories_y is not None:
        for icatx in categories_x:
            for icaty in categories_y:
                h_tmp.Fill(icatx, icaty, 0)

    binsx = range(h_tmp.GetNbinsX()+2)
    binsy = range(h_tmp.GetNbinsY()+2)
    pairs2d = list(map(lambda x: list(map(lambda y: (x,y), binsy)) , binsx))
    pairs1d = functools.reduce(lambda x,y: x+y, pairs2d, [])
    zvals = list()
    for eff in list_effs:
        list_bin2d = list(map(lambda ipair: eff.FindFixBin(ipair[0], ipair[1]), pairs1d))
        zvals += list(map(lambda ibin: eff.GetEfficiency(ibin), list_bin2d))
    zmax = max(zvals)
    zmin = min(zvals)
    h_tmp.SetMinimum(zmin)
    h_tmp.SetMaximum(zmax)
    h_tmp.SetTitle(efftitle)
    h_tmp.GetZaxis().SetRangeUser(0.3333*h_tmp.GetMinimum(), 3*h_tmp.GetMaximum())
    return h_tmp


## workers

def init_efficiency(
    effname: str,
    efftitle: str,
    nbinsx: int,
    xmin: float,
    xmax: float,
    nbinsy: int,
    ymin: float,
    ymax: float,
    level: float = None,
    level_sigma: float = 1
) -> TEfficiency:
    obj_chk = gROOT.FindObject(effname)
    if obj_chk != None: #special null pointer
        print('Deleteing previous effname='+effname)
        obj_chk.Delete()
    res = TEfficiency(effname, efftitle, nbinsx, xmin, xmax, nbinsy, ymin, ymax)
    if level is not None:
        res.SetConfidenceLevel(level)
    elif level_sigma!=1:
        level = ROOT.Math.normal_cdf(level_sigma) - ROOT.Math.normal_cdf(-level_sigma)
        res.SetConfidenceLevel(level)
    else:
        print('default Confidence Level')       
    return res


def fill_efficiency(
    res: TEfficiency,
    inpdf: pandas.DataFrame,
    col_x: str,
    col_y: str,
    col_z_pass: str,
    col_z_total: str
) -> TEfficiency:
    bin_widthx = res.GetTotalHistogram().GetXaxis().GetBinWidth(1) # for constant binning
    bin_widthy = res.GetTotalHistogram().GetYaxis().GetBinWidth(1) # for constant binning
    for irow in inpdf.iterrows():
        xval = irow[1][col_x] + 0.5 * bin_widthx
        yval = irow[1][col_y] + 0.5 * bin_widthy
        z_total = irow[1][col_z_total]
        z_pass = irow[1][col_z_pass]
        ibin2d = res.FindFixBin(xval, yval)
        res.SetTotalEvents(ibin2d, int(z_total))
        res.SetPassedEvents(ibin2d, int(z_pass))
    return res

