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
        self.combinations = range_combinations
        self.start()

    def run(self):
        """
        Run bruteforce
        """
        self.max_profit = 0

        # Convert the combination number into a matrix
        for combination in range(self.combinations[0], self.combinations[1]):
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


def create_list(dataframe):
    """
    Convert dataframe to a list and remove unnecessary or incorrect lines.

            Args:
                dataframe (object)

            Returns:
                new_stocks (list)
                total_incorrects (int)
    """
    stocks, total_incorrects = [], 0

    for stock in dataframe.values.tolist():
        if stock[PRICE] > 0 and stock[PROFIT_PERCENT] > 0:
            stock.append(stock[PRICE] * (stock[PROFIT_PERCENT] / 100))
            stocks.append(stock)
        else:
            total_incorrects += 1

    return stocks, total_incorrects


def allocate_ressources():
    """
    Launches several bruteforce processes in parallel calculation.

        Returns:
            process (list)
    """
    range_per_core = ceil(max_combinations / cpu_count())
    process, i = [], 0

    for core in range(cpu_count()):
        process.append(
            Bruteforce(
                stocks,
                (i, i + range_per_core),
                stocks_quantity
            )
        )
        i += range_per_core

    return process


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


# ----------
# RUN
# ----------
if __name__ == "__main__":

    start_time = time()
    stdout = sys.stdout

    if len(sys.argv) < 2:
        print("You must specify a dataframe file  as argument.")
    elif len(sys.argv) != 2:
        print("There are too many arguments specified.")
    else:
        try:
            print("Loading the dataframe...\n")
            df = pd.read_csv(sys.argv[1], header=0)
            print(f"{df[['name', 'price', 'profit']]}\n")
            stocks, incorrects = create_list(df)
            print(f"Deletion of {incorrects} incorrect rows\n")
        except FileNotFoundError:
            print(f"No such file or directory: '{sys.argv[1]}'\n")

        print("-------------------------\n")
        print("Starting the bruteforce...\n")

        # Determine the maximum number of combinations
        stocks_quantity = len(stocks)
        max_combinations = 2 ** stocks_quantity
        print(f"Maximum combinations: {max_combinations}\n")

        # Start bruteforce on multiple process
        manager = Manager()
        results = manager.list()
        process = allocate_ressources()
        for p in process:
            p.join()

        # # Get best result
        results.sort(reverse=True)
        df = pd.DataFrame(
                to_stocks_list(results[0][2]),
                columns=['name', 'price', 'profit', 'profit_euro']
        )

        # # Show result
        print("Bruteforce successfully completed !\n")
        print("-------------------------\n")
        print(f"Maximum profit is {round(results[0][0], 2)}€ "
              f"for a total cost of {round(results[0][1], 2)}€\n")
        print("List of stocks to buy:\n")
        print(f"{df[['name', 'price', 'profit']]}")

        execution_time = round(time() - start_time, 3)
        print(f"\nExecution time: {execution_time}s")
