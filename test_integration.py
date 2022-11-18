# to ensure download data integrity
import unittest
import os


class TestBasic(unittest.TestCase):
    def setUp(self):
        # Load test data
        self.check_cmd = "sha256sum -c" # add checksum file
        self.symbol_list = ["BNBBUSD", "1INCHBTC", "1INCHBUSD", "1INCHDOWNUSDT", "1INCHUPUSDT", "1INCHUSDT"]
        for symbol in self.symbol_list:
            download_cmd = "python3 test_data_download.py -t spot -s {} -startDate 2021-01-01 -i 1w -c 1".format(symbol)
            os.system(download_cmd)

    def test_data_integrity_check(self):
        path = os.getcwd() + "/data/"
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".CHECKSUM"):
                    os.chdir(root)
                    if os.system("sha256sum -c {}".format(file)) != 0:
                        print("======================== "+file+" Error =====================")
                        raise ValueError


if __name__ == '__main__':
    unittest.main()