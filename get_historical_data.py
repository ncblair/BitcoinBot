#Copyright (c) 2018 bonsaihr
#https://github.com/bonsaihr/trading/tree/master/bitcoin_historical_data

#!/usr/bin/env python3
#############################################################################
### code used in https://blog.bonsai.hr/bitcoin-historical-data/ blog post
### to run:
###    download this file
###    install requirements: pip install -r requirements.txt
###    run the program: python3 get_historical_data.py
#############################################################################

import os
import pickle
import time
from datetime import datetime

import pandas as pd
import requests


def fetch_data(timestamp):
    request = requests.get(BASE_URL + "Trades?pair={}&since={}".format(MARKET, timestamp))
    return request.json()


def anytime(timestamp):
    return datetime.utcfromtimestamp(timestamp)


def load_checkpoint():
    if os.path.isfile(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "rb") as f:
            return pickle.load(f)
    return 0, 0


def save_checkpoint(timestamp, trade_id):
    with open(CHECKPOINT_FILE, "wb") as f_out:
        pickle.dump([timestamp, trade_id], f_out)
    print("Checkpoint saved!")


def main():

    # start where we left off (or from the beginning if there was no checkpoint)
    last_trade_id, last_timestamp = load_checkpoint()

    start_time = datetime.utcnow().timestamp()
    while True:
        try:
            # fetch the data
            print("Fetching from {}..".format(anytime(last_timestamp)))
            response = fetch_data(last_trade_id)

            # check for errors
            if len(response['error']) != 0:
                print("Response error:", response['error'])
                save_checkpoint(last_timestamp, last_trade_id)
                time.sleep(15)
                continue

            if len(response['result']) <= 1:
                continue

            # get the data into a dataframe
            df = pd.DataFrame(response['result'][MARKET])

            # get rid of unnecessary columns
            df = df[df.columns[0:3]]

            # set column names
            df.columns = ["price", "volume", "timestamp"]

            # update variables for the checkpoint
            last_trade_id = response['result']['last']
            first_timestamp = df.timestamp.min()
            last_timestamp = df.timestamp.max()

            print("Fetched from: {} -- to: {}".format(anytime(first_timestamp), anytime(last_timestamp)))

            # save data to csv
            df.to_csv("kraken.csv", mode='a', header=False, index=False)

            # data fetched, save last trade id and exit
            if last_timestamp > start_time:
                break

            # sleep to avoid breaking API call limit
            time.sleep(15)

        except KeyboardInterrupt:
            exit()

        finally:
            save_checkpoint(last_timestamp, last_trade_id)


if __name__ == '__main__':

    BASE_URL = "https://api.kraken.com/0/public/"
    MARKET = "XXBTZUSD"
    CHECKPOINT_FILE = "last_fetched.pickle"

    main()