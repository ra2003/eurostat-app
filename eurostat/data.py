import gzip
from swiss import cache
from swiss.misc import floatify
import swiss
base = 'http://epp.eurostat.ec.europa.eu/NavTree_prod/everybody/BulkDownloadListing?file=data/'
filenames = ['teina011.tsv.gz', 'teina021.tsv.gz', 'teicp000.tsv.gz']
# teicp000.tsv.gz

ourcache = cache.Cache('static/cache')

for fn in filenames:
    url = base + fn
    fp = ourcache.cache_path(fn)
    ourcache.download(url, fp)
    newfp = fp[:-3]
    print newfp
    contents = gzip.GzipFile(fp).read()
    open(newfp, 'w').write(contents)
    reader = swiss.tabular.CsvReader()
    tab = reader.read(open(newfp), dialect='excel-tab')
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
    writer = swiss.tabular.JsonWriter()
    jsonfp = fp.split('.')[0] + '.json'
    writer.write(tab, open(jsonfp, 'w'))

