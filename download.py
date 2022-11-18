#!/usr/bin/env python
import sys
from datetime import *
import pandas as pd
import csv
from utility import download_file, get_all_symbols, get_parser, get_start_end_date_objects, convert_to_date_object, get_path, START_DATE, END_DATE, DAILY_INTERVALS, PERIOD_START_DATE
from logger import logger
import os
import zipfile
import shutil


def download_monthly_klines(trading_type, symbols, num_symbols, intervals, years, months, start_date, end_date, folder, checksum):
    current = 0
    date_range = None

    if start_date and end_date:
        date_range = start_date + " " + end_date

    if not start_date:
        start_date = START_DATE
    else:
        start_date = convert_to_date_object(start_date)

    if not end_date:
        end_date = END_DATE
    else:
        end_date = convert_to_date_object(end_date)

    print("Found {} symbols".format(num_symbols))

    for symbol in symbols:
        print("[{}/{}] - start download monthly {} klines ".format(current +
              1, num_symbols, symbol))
        for interval in intervals:
            for year in years:
                for month in months:
                    current_date = convert_to_date_object(
                        '{}-{}-01'.format(year, month))
                    if current_date >= start_date and current_date <= end_date:
                        path = get_path(trading_type, "klines",
                                        "monthly", symbol, interval)
                        file_name = "{}-{}-{}-{}.zip".format(
                            symbol.upper(), interval, year, '{:02d}'.format(month))
                        download_file(path, file_name, date_range, folder)

                        if checksum == 1:
                            checksum_path = get_path(
                                trading_type, "klines", "monthly", symbol, interval)
                            checksum_file_name = "{}-{}-{}-{}.zip.CHECKSUM".format(
                                symbol.upper(), interval, year, '{:02d}'.format(month))
                            download_file(
                                checksum_path, checksum_file_name, date_range, folder)

        current += 1


def download_daily_klines(trading_type, symbols, num_symbols, intervals, dates, start_date, end_date, folder, checksum):
    current = 0
    date_range = None

    if start_date and end_date:
        date_range = start_date + " " + end_date

    if not start_date:
        start_date = START_DATE
    else:
        start_date = convert_to_date_object(start_date)

    if not end_date:
        end_date = END_DATE
    else:
        end_date = convert_to_date_object(end_date)

    # Get valid intervals for daily
    intervals = list(set(intervals) & set(DAILY_INTERVALS))
    print("Found {} symbols".format(num_symbols))

    for symbol in symbols:
        print("[{}/{}] - start download daily {} klines ".format(current +
              1, num_symbols, symbol))
        for interval in intervals:
            for date in dates:
                current_date = convert_to_date_object(date)
                if current_date >= start_date and current_date <= end_date:
                    path = get_path(trading_type, "klines",
                                    "daily", symbol, interval)
                    file_name = "{}-{}-{}.zip".format(
                        symbol.upper(), interval, date)
                    download_file(path, file_name, date_range, folder)

                    if checksum == 1:
                        checksum_path = get_path(
                            trading_type, "klines", "daily", symbol, interval)
                        checksum_file_name = "{}-{}-{}.zip.CHECKSUM".format(
                            symbol.upper(), interval, date)
                        download_file(
                            checksum_path, checksum_file_name, date_range, folder)

        current += 1


def zipfile_download():
    parser = get_parser('klines')
    args = parser.parse_args(sys.argv[1:])

    if not args.symbols:
        print("fetching all symbols from exchange")
        symbols = get_all_symbols(args.type)
        num_symbols = len(symbols)
    else:
        symbols = args.symbols
        num_symbols = len(symbols)

    if args.dates:
        dates = args.dates
    else:
        period = convert_to_date_object(datetime.today().strftime('%Y-%m-%d')) - convert_to_date_object(
            PERIOD_START_DATE)
        dates = pd.date_range(end=datetime.today(),
                              periods=period.days + 1).to_pydatetime().tolist()
        dates = [date.strftime("%Y-%m-%d") for date in dates]
        if args.skip_monthly == 0:
            download_monthly_klines(args.type, symbols, num_symbols, args.intervals, args.years,
                                    args.months, args.startDate, args.endDate, args.folder, args.checksum)
    if args.skip_daily == 0:
        download_daily_klines(args.type, symbols, num_symbols, args.intervals,
                              dates, args.startDate, args.endDate, args.folder, args.checksum)


def zipfile_parse():
    path = os.getcwd() + "/data/"
    output_path = "output/"

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".zip"):
                print(os.path.join(root, file))
                file_name = os.path.join(root, file)
                zip_ref = zipfile.ZipFile(file_name) # create zipfile object
                zip_ref.extractall(output_path)
                zip_ref.close()
    
    # write it into saved csv
    column = ["open_time","open_","high","low","close","volume","close_time","quote_asset_volume","number_of_trades","taker_by_bav","taker_by_qav","ignored"]

    save_path = "save/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for file in os.listdir(output_path):
        file_path = os.getcwd() +"/output/" + file
        df = pd.read_csv(file_path, header=None)
        symbol = file.split("-")[0]
        time_interval = file.split("-")[1]

        csv_file_name = save_path + symbol+"-"+time_interval+".csv"

        if os.path.exists(csv_file_name):
            # append data frame to CSV file
            df.to_csv(csv_file_name, mode='a', index=False, header=False)
        else:
            with open(csv_file_name, 'w', newline='') as outcsv:
                writer = csv.writer(outcsv)
                writer.writerow(column)
            df.to_csv(csv_file_name, mode='a', index=False, header=False)
    logger.log("All zip file parse finished")


def remove_dir(dir_name):
    try:
        shutil.rmtree(dir_name)
    except OSError as e:
        logger.log("Error: %s : %s" % (dir_name, e.strerror))
        print("Error: %s : %s" % (dir_name, e.strerror))


if __name__ == '__main__':
    zipfile_download()
    zipfile_parse()
    # remove redundant files
    remove_dir("data/")
    remove_dir("output/")
    
    