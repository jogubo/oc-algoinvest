#!/usr/bin/env python3

import sys
import threading
from math import ceil
import pandas as pd

MAX_EXPENSE = 500
NAME, PRICE, PROFIT_PERCENT, PROFIT_EURO = 0, 1, 2, 3


def remove_incorrect_data(stocks):
    new_stocks, incorrect = [], 0
    for stock in stocks:
        if stock[PRICE] > 0 and stock[PROFIT_PERCENT] > 0:
            new_stocks.append(stock)
        else:
            incorrect += 1
    print(f"Deletion of {incorrect} incorrect rows\n")
    return new_stocks


class ValidCombinations(threading.Thread):
    def __init__(self, range_max_combinations):
        threading.Thread.__init__(self)
        self.max_combinations = range_max_combinations

    @classmethod
    def data(cls, stocks, number_of_action):
        cls.stocks = stocks
        cls.number_of_action = number_of_action

    def run(self):
        self.valid_combinations = []
        for combination in self.max_combinations:
            expense, valids = 0, []
            matrix = bin(combination)[2:]
            matrix = '0' * (self.number_of_action - len(matrix)) + matrix
            for i in range(self.number_of_action):
                if matrix[i] == '1':
                    expense += self.stocks[i][PRICE]
                    valids.append(self.stocks[i])
            if expense <= MAX_EXPENSE:
                self.valid_combinations.append(valids)


def bruteforce(stocks):
    # Calculate the profit in euro
    for stock in stocks:
        profit_euro = stock[PRICE] * (stock[PROFIT_PERCENT] / 100)
        stock.append(profit_euro)
    # Determine the maximum number of combinations
    number_of_action = len(stocks)
    max_combinations = 2 ** number_of_action
    median_combinations = ceil(max_combinations / 2)
    print(f"Maximum combinations: {max_combinations}\n")
    # Retrieve only the list of valid combinations (<=MAX_EXPENSE)
    ValidCombinations.data(stocks, number_of_action)
    th1 = ValidCombinations(range(0, median_combinations))
    th2 = ValidCombinations(range(median_combinations, max_combinations))
    th1.run()
    th2.run()
    valid_combinations = th1.valid_combinations + th2.valid_combinations
    # th1.join()
    # th2.join()
    # Calculates the profit of each combination and keeps the best
    max_profit, amount_of_expense, i = 0, 0, 0
    print(f"Possible combinations: {len(valid_combinations)}\n")
    for stocks in valid_combinations:
        total_profit = 0
        total_expense = 0
        for stock in stocks:
            total_profit += stock[PROFIT_EURO]
            total_expense += stock[PRICE]
        if total_profit > max_profit:
            max_profit = round(total_profit, 2)
            amount_of_expense = round(total_expense, 2)
            best_invest = valid_combinations[i]
        i += 1
    # Show the result of the bruteforce
    print("Bruteforce successfully completed !\n")
    print("-------------------------\n")
    print(f"Maximum profit is {max_profit}€ "
          f"for a total cost of {amount_of_expense}€\n")
    print("List of stocks to buy:")
    for stock in best_invest:
        print(f"{stock[NAME]}: {stock[PRICE]}€")


def main():
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
            stocks = remove_incorrect_data(stocks)
            print("-------------------------\n")
            print("Starting the bruteborce...\n")
            bruteforce(stocks)
        except FileNotFoundError:
            print(f"No such file or directory: '{sys.argv[1]}'\n")


if __name__ == "__main__":
    main()
