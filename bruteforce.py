#!/usr/bin/env python3

import sys
import threading
from math import ceil
import pandas as pd


class Bruteforce(threading.Thread):
    def __init__(self, range_combinations):
        threading.Thread.__init__(self)
        self.range_combinations = range_combinations

    @classmethod
    def stocks(cls, stocks):
        cls.stocks = stocks

    def run(self):
        self.max_profit = 0
        for combination in self.range_combinations:
            max_profit, i = 0, 0
            matrix = to_matrix(combination, STOCKS_QUANTITY)
            expense, profit = 0, 0
            for i in range(STOCKS_QUANTITY):
                if matrix[i] == '1':
                    expense += self.stocks[i][PRICE]
            if expense <= MAX_EXPENSE:
                profit += self.stocks[i][PROFIT_EURO]
            if profit > max_profit:
                self.max_profit = profit
                self.best_invest = combination


def remove_incorrect_data(stocks):
    new_stocks, total_incorrects = [], 0
    for stock in stocks:
        if stock[PRICE] > 0 and stock[PROFIT_PERCENT] > 0:
            new_stocks.append(stock)
        else:
            total_incorrects += 1
    return new_stocks, total_incorrects


def to_matrix(number, stocks_quantity):
    matrix = bin(number)[2:]
    matrix = '0' * (stocks_quantity - len(matrix)) + matrix
    return matrix


def to_combination(stocks, number):
    combination = []
    print(number)
    matrix = to_matrix(number, len(stocks))
    for i in range(matrix):
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
            Bruteforce.stocks(stocks)
            th1 = Bruteforce(range(0, MEDIAN_COMBINATION))
            th2 = Bruteforce(range(MAX_CONBINATION, MAX_CONBINATION))
            th1.run()
            th2.run()

            if th1.max_profit >= th2.max_profit:
                print(f"Best: {th1.best_invest}")
                # best_invest = to_combination(stocks, th1.best_invest)
            else:
                print(f"Best: {th2.best_invest}")
                # best_invest = to_combination(stocks, th2.best_invest)

            # Show the result of the bruteforce
            print("Bruteforce successfully completed !\n")
            print("-------------------------\n")
            # print(f"Maximum profit is {max_profit}€ "
            #       f"for a total cost of {amount_of_expense}€\n")
            # print("List of stocks to buy:")
            # for stock in best_invest:
            #     print(f"{stock[NAME]}: {stock[PRICE]}€")

        except FileNotFoundError:
            print(f"No such file or directory: '{sys.argv[1]}'\n")
