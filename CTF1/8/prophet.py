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

    print("Can you guess my random numbers?")
    print("Predict any of my 5 random numbers correctly and you'll get an amazing reward!")
    print("The current time is: {timestamp}".format(timestamp=current_timestamp.strftime("%Y-%m-%d %H:%M:%S")))
    print()

    # Seed PRNG with current time
    random.seed(get_epoch_seconds(current_timestamp))

    # Five attempts to guess my random number
    for i in range(1, 6):
        answer = int(random.random() * 133333333333337)
        print("Round #{i}:".format(i=i))
        print("Your guess => ", end="")
        sys.stdout.flush()

        try:
            guess = int(readline())
        except:
            guess = 0

        print(str(guess))

        if guess == answer:
            print("OMG!! How did you manage to guess that? :O")
            print("You must be a prophet or something!")
            print("As promised, here's your prize: {flag}".format(flag=flag))
            sys.exit(0)
        else:
            print("Nah. My number was: {answer}".format(answer=str(answer)))
            print()

    print("Not so good at guessing games, eh?")
    print("Better luck next time.")

if __name__ == "__main__":
    main()
