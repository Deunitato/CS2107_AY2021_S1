#!/usr/bin/env python
from __future__ import print_function
import datetime, random, sys, time

def readline():
    return sys.stdin.readline().strip()

def get_epoch_seconds(timestamp):
    return int((timestamp - datetime.datetime.utcfromtimestamp(0)).total_seconds())

def main():
    flag = "You need to interact with the server to get the prize."

    current_timestamp = datetime.datetime.utcnow()
    date_str2 = "2020-09-13 15:41:28"
    date_dt2 = datetime.datetime.strptime(date_str2, '%Y-%m-%d %H:%M:%S')
    print(get_epoch_seconds(date_dt2))
     # Seed PRNG with current time
    random.seed(get_epoch_seconds(date_dt2))

    # Five attempts to guess my random number
    fakeAnswer = int(random.random() * 133333333333337)
    print("Fake answer: " + str(fakeAnswer))

    print("Can you guess my random numbers?")
    print("Predict any of my 5 random numbers correctly and you'll get an amazing reward!")
    print("The current time is: {timestamp}".format(timestamp=current_timestamp.strftime("%Y-%m-%d %H:%M:%S")))
    print()

    # Seed PRNG with current time
    random.seed(get_epoch_seconds(current_timestamp))

    # Five attempts to guess my random number
    answer = int(random.random() * 133333333333337)
    print("actual answer:" + str(answer))


if __name__ == "__main__":
    main()
