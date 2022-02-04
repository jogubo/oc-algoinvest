#!/usr/bin/env python3

import sys
import pandas as pd
from time import time
from math import ceil
from threading import Thread

MAX_EXPENSE = 500

NAME, PRICE, PROFIT_PERCENT, PROFIT_EURO = 0, 1, 2, 3


class Bruteforce(Thread):
    """
    Create a thread for bruteforce on a combination interval.
    """

    def __init__(
        self,
        stocks,
        range_combinations,
        stocks_quantity
    ):
        Thread.__init__(self)
        self.stocks = stocks
        self.stock_quantity = stocks_quantity
        self.range_combinations = range_combinations
        self.price = PRICE
        self.max_expense = MAX_EXPENSE
        self.profit_euro = PROFIT_EURO
        self.start()

    def run(self):
        self.max_profit = 0
        # Convert the combination number into a matrix
        for combination in self.range_combinations:
            matrix = self.to_matrix(combination)
            expense, profit = 0, 0

            # If the value is '1', then the stock is to be added
            for i in range(self.stock_quantity):
                if matrix[i] == '1':
                    expense += self.stocks[i][self.price]

                    # Calculates the profit
                    if expense <= self.max_expense:
                        profit += self.stocks[i][self.profit_euro]

            # Get the best
            if profit > self.max_profit:
                self.max_profit = profit
                self.total_cost = expense
                self.best_invest = combination

    def to_matrix(self, number):
        """
        Convert the combination number into a matrix.

            Args:
                number (int): The number of combination

            Returns:
                matrix (str): The matrix of combination
        """
        matrix = bin(number)[2:]
        matrix = '0' * (self.stock_quantity - len(matrix)) + matrix

        return matrix


def remove_incorrect_data(stocks):
    """
    Remove unnecessary or incorrect lines.

            Args:
                stocks (list): List of stocks

            Returns:
                new_stocks (list)
                total_incorrects (int)
    """
    new_stocks, total_incorrects = [], 0

    for stock in stocks:
        if stock[PRICE] > 0 and stock[PROFIT_PERCENT] > 0:
            new_stocks.append(stock)
        else:
            total_incorrects += 1

    return new_stocks, total_incorrects


def to_combination(number):
    """
    Get a list of stocks from combination number.

        Args:
            number (int): The number of combination

        Returns:
            combination (list): List of stocks
    """
    combination = []

    matrix = bin(number)[2:]
    matrix = '0' * (stocks_quantity - len(matrix)) + matrix
    for i in range(stocks_quantity):
        if matrix[i] == '1':
            combination.append(stocks[i])

    return combination


# ----------
# RUN
# ----------
start_time = time()

if __name__ == "__main__":
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
        print("Starting the bruteforce...\n")

        # Calculate the profit in euro
        for stock in stocks:
            profit_euro = stock[PRICE] * (stock[PROFIT_PERCENT] / 100)
            stock.append(profit_euro)

        # Determine the maximum number of combinations
        stocks_quantity = len(stocks)
        max_combinations = 2 ** stocks_quantity
        median_combinations = ceil(max_combinations / 2)
        print(f"Maximum combinations: {max_combinations}\n")

        # Start bruteforce on multiple threads
        thread_1 = Bruteforce(
            stocks,
            range(0, median_combinations),
            stocks_quantity,
        )
        thread_2 = Bruteforce(
            stocks,
            range(median_combinations, max_combinations),
            stocks_quantity
        )
        thread_1.join()
        thread_2.join()

        # Get best result
        if thread_1.max_profit >= thread_2.max_profit:
            best_invest = to_combination(thread_1.best_invest)
            total_cost = thread_1. total_cost
            profit = round(thread_1.max_profit, 2)
        else:
            best_invest = to_combination(thread_2.best_invest)
            total_cost = thread_2. total_cost
            profit = round(thread_2.max_profit, 2)

        # Show the result
        print("Bruteforce successfully completed !\n")
        print("-------------------------\n")
        print(f"Maximum profit is {profit}€ "
              f"for a total cost of {total_cost}€\n")
        print("List of stocks to buy:")
        for stock in best_invest:
            print(f"{stock[NAME]}: {stock[PRICE]}€")
        execution_time = round(time() - start_time, 3)
        print(f"\nExecution time: {execution_time}s")
