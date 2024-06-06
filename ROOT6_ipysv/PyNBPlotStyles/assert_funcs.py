import pandas


def assert_df(inpdf: pandas.DataFrame):
    assert type(inpdf) is pandas.DataFrame

def assert_axis(nbins: int, axis_min: float, axis_max: float):
    assert type(nbins) is int
    assert nbins > 0    
    assert axis_max > axis_min

def assert_valcols(list_cols: list, inpdf: pandas.DataFrame):
    columns = inpdf.columns
    for icol in list_cols:
        assert icol in columns

def assert_cats(nbins: int, axis_max: float, categories: list):
    assert nbins == len(categories)
    assert int(axis_max) == nbins

def assert_confidentlevels(level, level_sigma):
    if level is not None:
        print('set level from {}'.format(level))
        assert (level >= 0) and (level<=1)
    else:
        print('set level as {}-sigma gaussian'.format(level_sigma))
        assert level_sigma >= 0

def assert_lowedges(lowedges, xmin):
    if len(lowedges)>0:
        assert xmin == lowedges[0]
        assert sorted(lowedges) == lowedges

