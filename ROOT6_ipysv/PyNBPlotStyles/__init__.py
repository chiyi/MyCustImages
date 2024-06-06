import pandas
import ROOT
from ROOT import TCanvas, TFormula, TF1, TH1D, TH2D, TH1I, TLegend, TDatime, TEfficiency, TGraphAsymmErrors, TMath
from ROOT import gROOT, gSystem, gPad
from ROOT import gStyle

import PyNBPlotStyles.Histo1D
import PyNBPlotStyles.Histo2D
import PyNBPlotStyles.Eff1D
import PyNBPlotStyles.Eff2D


def MakeHistogram1D(
    inpdf: pandas.DataFrame,
    col_x: str,
    col_y: str,
    hname: str,
    htitle: str,
    nbinsx: int,
    xmin: float,
    xmax: float,
    col_yerr: str = None,
    categories_x: list = None,
    b_reseterr: bool = True
) -> TH1D:
    res = Histo1D.MakeHistogram(inpdf, col_x, col_y, hname, htitle, nbinsx, xmin, xmax, col_yerr, categories_x, b_reseterr)
    return res


def MakeTemplateHisto1D(
    list_histos: list[TH1D],
    htitle: str,
    categories_x: list[str] = None
) -> TH1D:
    res = Histo1D.MakeTemplate(list_histos, htitle, categories_x)
    return res


def MakeHistogram2D(
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
    res = Histo2D.MakeHistogram(inpdf, col_x, col_y, col_z, hname, htitle, nbinsx, xmin, xmax, nbinsy, ymin, ymax, col_zerr, categories_x, categories_y)
    return res


def MakeTemplateHisto2D(
    list_histos: list[TH2D],
    htitle: str,
    categories_x: list[str] = None,
    categories_y: list[str] = None
) -> TH2D:
    res = Histo2D.MakeTemplate(list_histos, htitle, categories_x, categories_y)
    return res


def MakeEfficiency1D(
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
    res = Eff1D.MakeEfficiency(inpdf, col_x, col_y_pass, col_y_total, effname, efftitle, nbinsx, xmin, xmax, level, level_sigma, categories_x, bin_lowedges)
    return res


def MakeTemplateEff1D(
    list_effs: list[TEfficiency],
    efftitle: str,
    categories_x: list[str] = None
) -> TH1D:
    res = Eff1D.MakeTemplate(list_effs, efftitle, categories_x)
    return res


def MakeEfficiency2D(
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
    res = Eff2D.MakeEfficiency(inpdf, col_x, col_y, col_z_pass, col_z_total, effname, efftitle, nbinsx, xmin, xmax, nbinsy, ymin, ymax, level, level_sigma, categories_x, categories_y)
    return res


def MakeTemplateEff2D(
    list_effs: list[TEfficiency],
    efftitle: str,
    categories_x: list[str] = None,
    categories_y: list[str] = None
) -> TH2D:
    res = Eff2D.MakeTemplate(list_effs, efftitle, categories_x, categories_y)
    return res


def MakeAsymError(
    inpeff: TEfficiency,
    asymname: str,
    option: str = "EL"
) -> TEfficiency:
    inpeff.Draw(option)
    gPad.Update()
    res = inpeff.GetPaintedGraph().Clone(asymname)
    return res


def InitCanvas(width=1200, height=800) -> TCanvas:
    cname = 'canvas_default'
    obj_chk = gROOT.FindObject('canvas_default')
    if obj_chk:
        obj_chk.Close()

    res = TCanvas(cname, cname, width, height)
    res.cd()
    res.SetGridx(1)
    res.SetGridy(1)
    res.SetRightMargin(0.10)
    res.SetRightMargin(0.20)
    res.SetBottomMargin(0.20)
    gStyle.SetOptStat(0)
    return res


def MakeLegend(list_objs, legend=None):
    legend = TLegend(0.85, 0.0, 1.0, 1.0) if legend is None else legend
    for iobj in list_objs:
        legend.AddEntry(iobj, iobj.GetTitle(), "LEP")
    return legend    

