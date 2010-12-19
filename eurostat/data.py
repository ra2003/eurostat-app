'''Code for obtaining and cleaning data from Eurostat.
'''
import os
import re
import gzip
import json

from swiss import cache, tabular
from swiss.misc import floatify
base = 'http://epp.eurostat.ec.europa.eu/NavTree_prod/everybody/BulkDownloadListing?file=data/'

ourcache = cache.Cache('static/cache')

def download(dataset_id):
    '''Download a eurostat dataset based on its `dataset_id`
    '''
    fn = dataset_id + '.tsv.gz'
    url = base + fn
    # do not use retrieve as we get random ugly name
    fp = ourcache.cache_path(fn)
    ourcache.download(url, fp)
    newfp = fp[:-3]
    contents = gzip.GzipFile(fp).read()
    open(newfp, 'w').write(contents)
    return newfp

def extract(newfp):
    '''Extract data from tsv file at `filepath`, clean it and save it as json
    to file with same basename and extension json'''
    reader = tabular.CsvReader()
    tab = reader.read(open(newfp), dialect='excel-tab')
    # some data has blank top row!
    if not tab.header:
        tab.header = tab.data[0]
        del tab.data[0]
    alldata = [tab.header] + tab.data
    transposed = zip(*alldata)
    tab.header = transposed[0]
    def parsedate(cell):
        if 'Q' in cell:
            items = cell.split('Q')
            return float(items[0]) + 0.25 * (int(items[1]) - 1)
        elif 'M' in cell:
            items = cell.split('M')
            return float(items[0]) + 1/12.0 * (int(items[1]) - 1)
    def cleanrow(row):
        newrow = [ x.strip() for x in row ]
        newrow = [parsedate(newrow[0])] + [ floatify(x) for x in newrow[1:] ]
        return newrow
    tab.data = map(cleanrow, transposed[1:])
    writer = tabular.JsonWriter()
    jsonfp = newfp.split('.')[0] + '.json'
    writer.write(tab, open(jsonfp, 'w'))

PEEI_LIST = 'peeis.json'
def peeis():
    '''Scrape the Eurostat Prinicipal Economic Indicators (PEEI) list'''
    # turns out they iframe the data!
    # url = 'http://epp.eurostat.ec.europa.eu/portal/page/portal/euroindicators/peeis/'
    url = 'http://epp.eurostat.ec.europa.eu/cache/PEEIs/PEEIs_EN.html'
    fp = ourcache.retrieve(url)
    html = open(fp).read()
    dataset_ids = re.findall(r'pcode=([^&]+)&', html)
    reader = tabular.HtmlReader()
    tab = reader.read(fp, 1)
    peeis = []
    for row in tab.data[3:]:
        series_name = row[1].strip()
        if series_name[0] not in '%0123456789':
            peeis.append(series_name)
        if series_name == 'Euro-dollar exchange rate':
            break
    peeis = zip(dataset_ids, peeis)
    dumppath = ourcache.cache_path(PEEI_LIST)
    json.dump(peeis, open(dumppath, 'w'), indent=2)
    print 'PEEIs extracted to %s' % dumppath

def peeis_download():
    '''Download (and extract to json) all PEEI datasets.'''
    peei_list_fp = ourcache.cache_path(PEEI_LIST)
    peeis = json.load(open(peei_list_fp))
    for eurostatid, title in peeis:
        print 'Processing: %s - %s' % (eurostatid, title)
        fp = download(eurostatid)
        extract(fp)
    
from swiss.clitools import _main
if __name__ == '__main__':
    _main(locals())

