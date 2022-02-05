#!/usr/bin/env python3

import sys
import pandas as pd
from time import time
from math import ceil, floor

MAX_EXPENSE = 500
NAME, PRICE, PROFIT_PERCENT, PROFIT_EURO = 0, 1, 2, 3


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


def greedy_algorithm(stocks):
    expense, total_profit, selected_stocks = 0, 0, []

    # Sort stocks by profit (%)
    stocks.sort(key=lambda x: x[PROFIT_PERCENT], reverse=True)

    # Add stocks in descending order if total cost not exceed MAX_EXPENSE
    for stock in stocks:
        if expense + stock[PRICE] <= MAX_EXPENSE:
            expense += stock[PRICE]
            expense = round(expense, 2)
            total_profit += stock[PROFIT_EURO]
            total_profit = round(total_profit, 2)
            selected_stocks.append(stock)

    # Show the suggestion of the algorithm
    print(f"The estimated maximum profit is {total_profit}€ "
          f"for a total cost of {expense}€\n")
    print("List of stocks to buy:")
    for stock in selected_stocks:
        print(f"{stock[NAME]}: {stock[PRICE]}€")


def dynamic_programming(stocks):
    for stock in stocks:
        stock[PRICE] = ceil(stock[PRICE] * 100)
        stock[PROFIT_PERCENT] = ceil(stock[PROFIT_PERCENT] * 100)

    amount = len(stocks)
    matrix = [[0 for x in range(MAX_EXPENSE + 1)] for x in range(amount + 1)]

    for x in range(1, amount + 1):

        for y in range(1, MAX_EXPENSE + 1):
            print(stock)
            stock = stocks[x - 1]
            stock_price = stock[PRICE]
            stock_profit = stock[PROFIT_PERCENT]

            if stock_price <= y:
                matrix[x][y] = max(
                    stock_profit + matrix[x - 1][floor(y - stock_profit)],
                    matrix[x - 1][y]
                )
            else:
                matrix[x][y] = matrix[x - 1][y]

    selected, e, n = [], MAX_EXPENSE, amount
    while e >= 0 and n >= 0:
        s = stocks[amount - 1]

        if matrix[n][e] == matrix[n - 1][e - s[1]] + s[2]:
            selected.append(s)
            e -= s

        n -= 1


# ----------
# RUN
# ----------
if __name__ == "__main__":

    start_time = time()

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
            stocks, incorrects = create_list(df)
            print(f"Deletion of {incorrects} incorrect rows\n")
            print("--------------------\n")
            print("Greedy algorithm\n")
            print("--------------------\n")
            greedy_algorithm(stocks)
        except FileNotFoundError:
            print(f"No such file or directory: '{sys.argv[1]}'\n")

        execution_time = round(time() - start_time, 3)
        print(f"\nExecution time: {execution_time}s")
