import numpy
import pandas
import ROOT
from ROOT import TCanvas, TFormula, TF1, TH1D, TH2D, TH1I, TLegend, TDatime, TEfficiency, TGraphAsymmErrors, TMath
from ROOT import gROOT, gSystem, gPad
from ROOT import gStyle

from PyNBPlotStyles.assert_funcs import assert_df, assert_axis, assert_valcols, assert_cats, assert_confidentlevels, assert_lowedges


# Main

def MakeEfficiency(
    inpdf: pandas.DataFrame,
    col_x: str,
    col_y_pass: str,
    col_y_total: str,
    effname: str,
    efftitle: str,
    nbinsx: int,
    xmin: float,
    xmax: float,
    level: float = None,
    level_sigma: float = 1,
    categories_x: list[str] = None, 
    bin_lowedges: list[float] = []
) -> TEfficiency:
    CheckParameters(inpdf, col_x, col_y_pass, col_y_total, effname, efftitle, nbinsx, xmin, xmax, level, level_sigma, categories_x, bin_lowedges)
    res = init_efficiency(effname, efftitle, nbinsx, xmin, xmax, level, level_sigma, bin_lowedges)
    if len(bin_lowedges)<=0:
        res = fill_efficiency(res, inpdf, col_x, col_y_pass, col_y_total)
    else:
        res = fill_efficiency_dynbins(res, inpdf, col_x, col_y_pass, col_y_total, bin_lowedges)
    return res


# helpers

def CheckParameters(
    inpdf: pandas.DataFrame, 
    col_x: str, 
    col_y_pass: str, 
    col_y_total: str, 
    effname: str, 
    efftitle: str, 
    nbinsx: int, 
    xmin: float, 
    xmax: float, 
    level: float = None, 
    level_sigma: float = 1, 
    categories_x: list[str] = None, 
    bin_lowedges: list[float] = []
):
    assert_df(inpdf)
    assert_axis(nbinsx, xmin, xmax)
    assert_valcols([col_x, col_y_pass, col_y_total], inpdf)
    assert_confidentlevels(level, level_sigma)
    
    if categories_x is not None:
        assert_cats(nbinsx, xmax, categories_x)

    assert_lowedges(bin_lowedges, xmin)


def MakeTemplate(
    list_effs: list[TEfficiency],
    efftitle: str,
    categories_x: list[str] = None
) -> TH1D:
    h_tmp = list_effs[0].GetPassedHistogram().Clone("h_tmp")
    h_tmp.Reset()
    if categories_x is not None:
        for icat in categories_x:
            h_tmp.Fill(icat, 0)
    binsx = range(1, 1+h_tmp.GetNbinsX())
    yvals = list()
    for eff in list_effs:
        yvals += list(map(lambda ibin: eff.GetEfficiency(ibin), binsx))
    ymax = max(yvals)
    ymin = min(yvals)
    h_tmp.SetMinimum(ymin)
    h_tmp.SetMaximum(ymax)
    h_tmp.SetTitle(efftitle)
    h_tmp.GetYaxis().SetRangeUser(0.3333*h_tmp.GetMinimum(), 3*h_tmp.GetMaximum())
    return h_tmp


## workers

def init_efficiency(
    effname: str,
    efftitle: str,
    nbinsx: int,
    xmin: float,
    xmax: float,
    level: float = None,
    level_sigma: float = 1,
    bin_lowedges: list[float] = []
) -> TEfficiency:
    obj_chk = gROOT.FindObject(effname)
    if obj_chk != None: #special null pointer
        print('Deleteing previous effname='+effname)
        obj_chk.Delete()
    if len(bin_lowedges)<=0:
        res = TEfficiency(effname, efftitle, nbinsx, xmin, xmax)
    else:
        res = TEfficiency(effname, efftitle, nbinsx, numpy.array(bin_lowedges+[xmax]))
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
    col_y_pass: str,
    col_y_total: str
) -> TEfficiency:
    bin_width = res.GetTotalHistogram().GetBinWidth(1) # for constant binning
    for irow in inpdf.iterrows():
        xval = irow[1][col_x] + 0.5 * bin_width
        y_total = irow[1][col_y_total]
        y_pass = irow[1][col_y_pass]
        ibin = res.FindFixBin(xval)
        res.SetTotalEvents(ibin, int(y_total))
        res.SetPassedEvents(ibin, int(y_pass))
    return res


def fill_efficiency_dynbins(
    res: TEfficiency,
    inpdf: pandas.DataFrame,
    col_x: str,
    col_y_pass: str,
    col_y_total: str,
    bin_lowedges: list[float]
) -> TEfficiency:
    xmax = res.GetTotalHistogram().GetBinLowEdge(len(bin_lowedges)+1)
    bin_edges = numpy.array(bin_lowedges+[xmax])
    for irow in inpdf.iterrows():
        xval = irow[1][col_x]
        ibin = int(numpy.where(bin_edges==xval)[0][0] + 1)
        bin_width = res.GetTotalHistogram().GetBinWidth(ibin)
        xval += 0.5 * bin_width
        y_total = irow[1][col_y_total]
        y_pass = irow[1][col_y_pass]
        res.SetTotalEvents(ibin, int(y_total))
        res.SetPassedEvents(ibin, int(y_pass))
    return res

