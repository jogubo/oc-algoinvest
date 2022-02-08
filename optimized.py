#!/usr/bin/env python3

import sys
import pandas as pd
from time import time

MAX_EXPENSE = 500
NAME, PRICE, PROFIT_PERCENT, PROFIT_EURO = 0, 1, 2, 3


class Converter():
    """
    Contains method to convert data.
    """

    def __init__(self, stocks):
        self.stocks = stocks
        self.budget = MAX_EXPENSE

    def to_integer(self):
        """
        Convert to integer by multiplying by 100.
        """
        self.budget = round(self.budget * 100)
        for stock in self.stocks:
            stock[PRICE] = round(stock[PRICE] * 100)
            stock[PROFIT_PERCENT] = round(stock[PROFIT_PERCENT] * 100)
            stock[PROFIT_EURO] = round(stock[PROFIT_EURO] * 100)
        if self. profit is not None:
            self.profit = round(self.profit * 100)

    def to_float(self):
        """
        Convert to float by dividing by 100.
        """
        self.budget = round((self.budget / 100), 2)
        for stock in self.stocks:
            stock[PRICE] = round((stock[PRICE] / 100), 2)
            stock[PROFIT_PERCENT] = round((stock[PROFIT_PERCENT] / 100), 2)
            stock[PROFIT_EURO] = round((stock[PROFIT_EURO] / 100), 2)
        if self. profit is not None:
            self.profit = round((self.profit / 100), 2)

    @property
    def stocks(self):
        return stocks

    @stocks.setter
    def stocks(self, stocks):
        self._stocks = stocks

    @property
    def budget(self):
        return self._budget

    @budget.setter
    def budget(self, budget):
        self._budget = budget

    @property
    def df(self):
        df = pd.DataFrame(
            self.selected_stocks,
            columns=['name', 'price', 'profit', 'profit_euro']
        )
        return df

    @staticmethod
    def create_list(dataframe):
        """
        Convert a dataframe into a list and calculates the profit  in euro.
        Deletes incorrect data.

            Args:
                dataframe (object)

            Returns:
                stocks (list): list of stocks
                total_incorrects (int): the number of incorrect elements
        """
        stocks, total_incorrects = [], 0

        for stock in dataframe.values.tolist():
            if stock[PRICE] > 0 and stock[PROFIT_PERCENT] > 0:
                stocks.append(
                    [
                        stock[NAME],
                        stock[PRICE],
                        stock[PROFIT_PERCENT],
                        stock[PRICE] * stock[PROFIT_PERCENT] / 100
                    ]
                )
            else:
                total_incorrects += 1

        return stocks, total_incorrects


class Dynamic(Converter):
    """
    Dynamic programming algorithm.
    """

    def __init__(self, stocks):
        self.matrix = None
        self.profit = None
        self.selected_stocks = None
        self.stocks.sort(key=lambda x: x[PRICE], reverse=True)
        Converter.__init__(self, stocks)

    def __repr__(self):
        return "Dynamic Programming"

    def run(self):
        self.to_integer()

        stocks = self._stocks
        matrix = self.create_matrix()

        for i in range(1, len(stocks) + 1):

            for w in range(self.budget + 1):
                if stocks[i - 1][PRICE] <= w:
                    matrix[i][w] = max(
                        stocks[i - 1][PROFIT_EURO]
                        + matrix[i - 1][w - stocks[i - 1][PRICE]],
                        matrix[i - 1][w]
                    )
                else:
                    matrix[i][w] = matrix[i - 1][w]

        w = self.budget
        n = len(stocks)
        selected = []

        while w >= 0 and n >= 0:
            stock = stocks[n - 1]

            if matrix[n][w] == \
               matrix[n - 1][w - stock[PRICE]] + stock[PROFIT_EURO]:

                selected.append(stock)
                w -= stock[PRICE]

            n -= 1

        self.profit = matrix[-1][-1]
        self.selected_stocks = selected

        self.to_float()

    def create_matrix(self):
        self.matrix = []

        for x in range(len(self._stocks) + 1):
            self.matrix.append([0 for x in range(self.budget + 1)])

        return self._matrix

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, matrix):
        self._matrix = matrix

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


class Greedy(Converter):
    """
    Greedy algorithm.
    """

    def __init__(self, stocks):
        self.profit = None
        self.selected_stocks = None
        Converter.__init__(self, stocks)

    def __repr__(self):
        return "Greedy Algorithm"

    def run(self):
        expense, profit, selected = 0, 0, []

        # Sort stocks by profit in euro
        self.stocks.sort(key=lambda x: x[PROFIT_PERCENT], reverse=True)

        # Add the most profitable stocks as long as their price does not
        # exceed the budget
        for stock in self._stocks:
            if expense + stock[PRICE] <= self.budget:
                expense += stock[PRICE]
                profit += stock[PROFIT_EURO]
                selected.append(stock)

        self.profit = round(profit, 2)
        self.expense = round(expense, 2)
        self.selected_stocks = selected

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
            stocks, incorrects = Converter.create_list(df)
            print(f"Deletion of {incorrects} incorrect rows\n")
        except FileNotFoundError:
            print(f"No such file or directory: '{sys.argv[1]}'\n")

        # Algorithm selection
        print("--------------------\n")
        choice = None
        while not choice:
            choice = input("Choose an algorithm:\n\n"
                           "[1] Greedy (fast)\n"
                           "[2] Dynamic (better)\n\n"
                           ">> "
                           )
            print()
            if choice == '1':
                algorithm = Greedy(stocks)
            elif choice == '2':
                algorithm = Dynamic(stocks)

        start_time = time()

        # Start algorithm
        print("--------------------\n")
        print(f"{algorithm}\n")
        print("--------------------\n")
        algorithm.run()

        # # Get result
        print(f"Maximum profit is {algorithm.profit}€ "
              f"for a total cost of {algorithm.expense}€\n")
        print("List of stocks to buy:\n")
        print(f"{algorithm.df[['name', 'price', 'profit']]}")

        execution_time = round(time() - start_time, 3)
        print(f"\nExecution time: {execution_time}s")
