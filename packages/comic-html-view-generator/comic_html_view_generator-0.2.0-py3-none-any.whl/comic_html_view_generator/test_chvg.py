import unittest
from os import path

from .chvg import mirror_unzip_cbz


class TestMirrorUnzipCBZ(unittest.TestCase):
    def setUp(self):
        pass

    def testExtractOdd(self):
        basepath = path.dirname(path.abspath(__file__))
        testfile = 'simulated_comic_volume_001.cbz'
        testfpath = path.join(basepath, testfile)

        testout = path.join(basepath, 'test_output_volume')
        print('input folder:', basepath)
        print('output dir  :', testout)
        mirror_unzip_cbz(basepath, testout, verbose=True)


if __name__ == '__main__':
    unittest.main()
