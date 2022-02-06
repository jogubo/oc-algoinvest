#!/usr/bin/env python3

import sys
import pandas as pd
from time import time

MAX_EXPENSE = 50000  # amount in cents, an integer is required
NAME, PRICE, PROFIT_PERCENT, PROFIT_EURO = 0, 1, 2, 3


class Dynamic():

    def __init__(self, stocks):
        self.stocks = stocks
        self.matrix = None
        self.profit = None
        self.selected_stocks = None
        self.stocks.sort(key=lambda x: x[PRICE], reverse=True)

    def __repr__(self):
        return "Dynamic Programming"

    def run(self):
        stocks = self._stocks
        matrix = self.create_matrix()

        for i in range(1, len(stocks) + 1):

            for w in range(MAX_EXPENSE + 1):
                if stocks[i - 1][PRICE] <= w:
                    matrix[i][w] = max(
                        stocks[i - 1][PROFIT_EURO]
                        + matrix[i - 1][w - stocks[i - 1][PRICE]],
                        matrix[i - 1][w]
                    )
                else:
                    matrix[i][w] = matrix[i - 1][w]

        w = MAX_EXPENSE
        n = len(stocks)
        selected = []

        while w >= 0 and n >= 0:
            stock = stocks[n - 1]

            if matrix[n][w] == \
               matrix[n - 1][w - stock[PRICE]] + stock[PROFIT_EURO]:

                selected.append(stock)
                w -= stock[PRICE]

            n -= 1

        self._profit = matrix[-1][-1]
        self._selected_stocks = selected

    def create_matrix(self):
        self._matrix = []

        for x in range(len(self._stocks) + 1):
            self._matrix.append([0 for x in range(MAX_EXPENSE + 1)])

        return self._matrix

    @property
    def stocks(self):
        return stocks

    @stocks.setter
    def stocks(self, stocks):
        self._stocks = stocks

    @property
    def profit(self):
        return self._profit

    @profit.setter
    def profit(self, profit):
        self._profit = profit

    @property
    def expense(self):
        expense = 0
        for stock in self.selected_stocks:
            expense += stock[PRICE]
            print(stock)
        return expense

    @expense.setter
    def expense(self, expense):
        self._expense = expense

    @property
    def selected_stocks(self):
        return self._selected_stocks

    @selected_stocks.setter
    def selected_stocks(self, selected_stocks):
        self._selected_stocks = selected_stocks


class Greedy():

    def __init__(self, stocks):
        self.stocks = stocks
        self.profit = None
        self.selected_stocks = None
        self.stocks.sort(key=lambda x: x[PROFIT_PERCENT], reverse=True)

    def __repr__(self):
        return "Greedy Algorithm"

    def run(self):
        expense, profit, selected = 0, 0, []
        for stock in self._stocks:
            if expense + stock[PRICE] <= MAX_EXPENSE:
                expense += stock[PRICE]
                profit += stock[PROFIT_EURO]
                selected.append(stock)

        self.profit = profit
        self.expense = expense
        self.selected_stocks = selected

    @property
    def stocks(self):
        return self._stocks

    @stocks.setter
    def stocks(self, stocks):
        self._stocks = stocks

    @property
    def profit(self):
        return self._profit

    @profit.setter
    def profit(self, profit):
        self._profit = profit

    @property
    def expense(self):
        return self._expense

    @expense.setter
    def expense(self, expense):
        self._expense = expense


def create_list(dataframe):
    stocks, total_incorrects = [], 0

    for stock in dataframe.values.tolist():
        if stock[PRICE] > 0 and stock[PROFIT_PERCENT] > 0:
            stocks.append(
                [
                    stock[NAME],
                    round(stock[PRICE] * 100),
                    round(stock[PROFIT_PERCENT] * 100),
                    round(stock[PRICE] * stock[PROFIT_PERCENT])
                ]
            )
        else:
            total_incorrects += 1

    return stocks, total_incorrects


# ----------
# RUN
# ----------
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("You must specify a dataframe file  as argument.")
    elif len(sys.argv) != 2:
        print("There are too many arguments specified.")
    else:
        try:
            print("Loading the dataframe...\n")
            df = pd.read_csv(sys.argv[1], header=0)
            print(f"{df}\n")
            stocks, incorrects = create_list(df)
            print(f"Deletion of {incorrects} incorrect rows\n")
        except FileNotFoundError:
            print(f"No such file or directory: '{sys.argv[1]}'\n")

        print("--------------------\n")
        choice = None
        while not choice:
            choice = input("Choose an algorithm:\n\n"
                           "[1] Greedy (fast)\n"
                           "[2] Dynamic (better)\n\n"
                           ">> "
                           )
            if choice == '1':
                algorithm = Greedy(stocks)
            elif choice == '2':
                algorithm = Dynamic(stocks)
        start_time = time()
        print("--------------------\n")
        print(f"{algorithm}\n")
        print("--------------------\n")
        algorithm.run()
        for stock in algorithm.selected_stocks:
            print(stock)

        execution_time = round(time() - start_time, 3)
        print(f"\nExecution time: {execution_time}s")
