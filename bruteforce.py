#!/usr/bin/env python3

import sys
import pandas as pd
from time import time
from math import ceil
from multiprocessing import Process, Manager, cpu_count

MAX_EXPENSE = 500

NAME, PRICE, PROFIT_PERCENT, PROFIT_EURO = 0, 1, 2, 3


class Bruteforce(Process):
    """
    Create a new process for bruteforce on a combination interval.
    """

    def __init__(self, stocks, range_combinations, stocks_quantity):
        Process.__init__(self)
        self.stocks = stocks
        self.stock_quantity = stocks_quantity
        self.range_combinations = range_combinations
        self.start()

    def run(self):
        """
        Run bruteforce
        """
        self.max_profit = 0

        # Convert the combination number into a matrix
        for combination in self.range_combinations:
            matrix = self.to_matrix(combination)
            expense, profit = 0, 0

            # If the value is '1', then the stock is to be added
            for i in range(self.stock_quantity):
                if matrix[i] == '1':
                    expense += self.stocks[i][PRICE]

                    # Calculates the profit
                    if expense <= MAX_EXPENSE:
                        profit += self.stocks[i][PROFIT_EURO]

            # Get the best
            if profit > self.max_profit:
                self.max_profit = profit
                self.total_cost = expense
                self.best_invest = combination

        # Add best result of this process to list
        results.append([self.max_profit, self.total_cost, self.best_invest])

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


def to_stocks_list(number):
    """
    Get a list of stocks from combination number.

        Args:
            number (int): The number of combination

        Returns:
            stocks (list): List of stocks
    """
    stocks_list = []

    matrix = bin(number)[2:]
    matrix = '0' * (stocks_quantity - len(matrix)) + matrix
    for i in range(stocks_quantity):
        if matrix[i] == '1':
            stocks_list.append(stocks[i])

    return stocks_list


def get_allocation_ranges():
    """
    Gives an allocation list for each process.

        Returns:
            ranges (list)
    """
    range_per_core = ceil(max_combinations / cpu_count())
    ranges, i = [], 0

    for core in range(cpu_count()):
        ranges.append((i, i + range_per_core))
        i += range_per_core

    return ranges


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

        # Start bruteforce on multiple process
        manager = Manager()
        results = manager.list()
        process = []
        range_allocations = get_allocation_ranges()

        for i in range_allocations:
            p = Bruteforce(
                stocks,
                range(i[0], i[1]),
                stocks_quantity
            )
            process.append(p)

        for p in process:
            p.join()

        # # Get best result
        results.sort(reverse=True)
        best_invest = to_stocks_list(results[0][2])

        # # Show the result
        print("Bruteforce successfully completed !\n")
        print("-------------------------\n")
        print(f"Maximum profit is {round(results[0][0], 2)}€ "
              f"for a total cost of {round(results[0][1], 2)}€\n")
        print("List of stocks to buy:")
        for stock in best_invest:
            print(f"{stock[NAME]}: {stock[PRICE]}€")
        execution_time = round(time() - start_time, 3)
        print(f"\nExecution time: {execution_time}s")
