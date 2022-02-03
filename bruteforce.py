#!/usr/bin/env python3

import sys
import threading
from math import ceil
import pandas as pd
import time


class Bruteforce(threading.Thread):

    def __init__(self, stocks, range_combinations, thread_name):
        threading.Thread.__init__(self)
        self.range_combinations = range_combinations
        self.stock = stocks
        self.thread_name = thread_name

    def run(self):
        self.max_profit = 0
        for combination in self.range_combinations:
            # time.sleep(3)
            # print(self.thread_name)
            matrix = to_matrix(combination)
            expense, profit = 0, 0
            for i in range(STOCKS_QUANTITY):
                if matrix[i] == '1':
                    expense += stocks[i][PRICE]
                    if expense <= MAX_EXPENSE:
                        profit += stocks[i][PROFIT_EURO]
            if profit > self.max_profit:
                self.max_profit = profit
                self.total_cost = expense
                self.best_invest = combination


def remove_incorrect_data(stocks):
    new_stocks, total_incorrects = [], 0
    for stock in stocks:
        if stock[PRICE] > 0 and stock[PROFIT_PERCENT] > 0:
            new_stocks.append(stock)
        else:
            total_incorrects += 1
    return new_stocks, total_incorrects


def to_matrix(number):
    matrix = bin(number)[2:]
    matrix = '0' * (STOCKS_QUANTITY - len(matrix)) + matrix
    return matrix


def to_combination(stocks, number):
    combination = []
    matrix = to_matrix(number)
    for i in range(STOCKS_QUANTITY):
        if matrix[i] == '1':
            combination.append(stocks[i])
    return combination


# ----------
# RUN
# ----------
if __name__ == "__main__":
    MAX_EXPENSE = 500
    NAME, PRICE, PROFIT_PERCENT, PROFIT_EURO = 0, 1, 2, 3
    if len(sys.argv) < 2:
        print("You must specify a dataframe file  as argument.")
    elif len(sys.argv) != 2:
        print("There are too many arguments specified.")
    else:
        try:
            print("Loading the dataframe...\n")
            df = pd.read_csv(sys.argv[1], header=0)
            stocks = df.values.tolist()
            print(f"{df}\n")
            stocks, incorrects = remove_incorrect_data(stocks)
            print(f"Deletion of {incorrects} incorrect rows\n")
        except FileNotFoundError:
            print(f"No such file or directory: '{sys.argv[1]}'\n")
        print("-------------------------\n")
        print("Starting the bruteborce...\n")
        # Calculate the profit in euro
        for stock in stocks:
            profit_euro = stock[PRICE] * (stock[PROFIT_PERCENT] / 100)
            stock.append(profit_euro)
        # Determine the maximum number of combinations
        STOCKS_QUANTITY = len(stocks)
        MAX_CONBINATION = 2 ** STOCKS_QUANTITY
        MEDIAN_COMBINATION = ceil(MAX_CONBINATION / 2)
        print(f"Maximum combinations: {MAX_CONBINATION}\n")
        # Retrieve only the list of valid combinations (<=MAX_EXPENSE)
        thread_1 = Bruteforce(
            stocks,
            range(0, MEDIAN_COMBINATION),
            "Thread_1"
        )
        thread_1.start()
        thread_2 = Bruteforce(
            stocks,
            range(MAX_CONBINATION, MAX_CONBINATION),
            "Thread_2"
        )
        thread_2.start()

        thread_1.join()
        thread_2.join()
        if thread_1.max_profit >= thread_2.max_profit:
            print(f"Best: {thread_1.best_invest}")
            best_invest = to_combination(stocks, thread_1.best_invest)
            total_cost = thread_1. total_cost
            profit = ceil(thread_1.max_profit)
        else:
            print(f"Best: {thread_2.best_invest}")
            best_invest = to_combination(stocks, thread_2.best_invest)
            total_cost = thread_2. total_cost
            profit = ceil(thread_2.max_profit)
        # Show the result of the bruteforce
        print("Bruteforce successfully completed !\n")
        print("-------------------------\n")
        print(f"Maximum profit is {profit}€ "
              f"for a total cost of {total_cost}€\n")
        print("List of stocks to buy:")
        for stock in best_invest:
            print(f"{stock[NAME]}: {stock[PRICE]}€")
