from eurostat.data import Data

class TestData:
    def test_peeis(self):
        d = Data()
        out = d.peeis()
        assert len(out) == 22

    def test_peeis_download(self):
        d = Data()
        d.peeis_download()

