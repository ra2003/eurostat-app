from eurostat.data import Data, ourcache

class TestData:
    def test_01_peeis(self):
        d = Data()
        out = d.peeis()
        assert len(out) == 22

    def test_02_peeis_download(self):
        d = Data()
        d.peeis_download()
    
    def test_03_extract(self):
        d = Data()
        # gdp
        tabular = d.extract(ourcache.cache_path('teina011.tsv'))
        assert tabular.header[1] == 'Austria', tabular.header
        # one with a different heading structure
        tabular = d.extract(ourcache.cache_path('teibs010.tsv'))
        assert tabular.header[-1] == 'UK', tabular.header

