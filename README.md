# Requirements
## Input
- symbol
- start date
- end date
- interval

## output
print k-line data in csv format (Doc: https://github.com/binance/binance-public-data/)

| Open time | Open | High | Low | Close | Volume | Close time | Quote asset volume | Number of trades | Taker buy base asset volume | Taker buy quote asset volume | Ignore |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1601510340000 | 4.15070000 | 4.15870000 | 4.15060000 | 4.15540000 | 539.23000000 | 1601510399999 | 2240.39860900 | 13 | 401.82000000 | 1669.98121300 | 0 |

# Usage
| Argument        | Explanation | Default | Mandatory |      
| :---------------: | ---------------- | :----------------: | :----------------: |
| -t              | Market type: **spot**, **um** (USD-M Futures), **cm** (COIN-M Futures) | spot | Yes |
| -s              | Single **symbol** or multiple **symbols** separated by space | All symbols | No |
| -i              | single kline **interval** or multiple **intervals** separated by space      | All intervals | No |
| -y              | Single **year** or multiple **years** separated by space| All available years from 2020 to current year | No |
| -m              | Single **month** or multiple **months** separated by space | All available months | No |
| -d              | single **date** or multiple **dates** separated by space    | All available dates from 2020-01-01 | No |
| -startDate      | **Starting date** to download in [YYYY-MM-DD] format    | 2020-01-01 | No |
| -endDate        | **Ending date** to download in [YYYY-MM-DD] format     | Current date | No |
| -skip-monthly   | 1 to skip downloading of monthly data | 0 | No |
| -skip-daily     | 1 to skip downloading of daily data | 0 | No |
| -folder         | **Directory** to store the downloaded data    | Current directory | No |
| -c              | 1 to download **checksum file** | 0 | No |
| -h              | show help messages| - | No |

And the results will be put into a directory `save/`
## Example
- `python3 main.py -t spot -s BNBBUSD -startDate 2020-01-01 -endDate 2022-02-01 -i 1w`

- download ETHUSDT BTCUSDT BNBBUSD spot kline of 1 week interval from year 2020, month of Feb and Dec with CHECKSUM file:
`python3 main.py -t spot -s ETHUSDT BTCUSDT BNBBUSD -i 1w -y 2020 -m 02 -d 12 -c 1`

- download all symbols' daily USD-M futures kline of 1 minute interval from 2021-01-01 to 2021-02-02: `python3 main.py -t um -i 1m -skip-monthly 1 -startDate 2021-01-01 -endDate 2021-02-02`

## Build from Docker
I provide a dockerfile so you can build via docker.

```shellscript
$ docker build -t test .
$ docker run -it test python main.py -t spot -s BNBBUSD -startDate 2020-01-01 -endDate 2022-02-01 -i 1w
```