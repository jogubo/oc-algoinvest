#!/usr/bin/env python3

import sys
import pandas as pd
from time import time

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

    price, profit = PRICE, PROFIT_EURO
    max_expense = MAX_EXPENSE * 100
    s = []
    for stock in stocks:
        s.append(
            [
                stock[NAME],
                round(stock[PRICE] * 100),
                round(stock[PROFIT_PERCENT] * 100),
                round(stock[PROFIT_EURO] * 100)
            ]
        )

    s.sort(key=lambda x: x[PRICE], reverse=True)

    matrix = [[0 for x in range(max_expense + 1)] for x in range(len(s) + 1)]

    for i in range(1, len(s) + 1):

        for w in range(max_expense + 1):
            if s[i - 1][price] <= w:
                matrix[i][w] = max(
                    s[i - 1][profit] + matrix[i - 1][w - s[i - 1][price]],
                    matrix[i - 1][w]
                )
            else:
                matrix[i][w] = matrix[i - 1][w]

    n = len(s)
    selected_stocks = []
    w = max_expense

    while w >= 0 and n >= 0:
        stock = s[n - 1]

        if matrix[n][w] == matrix[n - 1][w - stock[price]] + stock[profit]:
            selected_stocks.append(stock)

            w -= stock[price]

        n -= 1

    total_profit = matrix[-1][-1] / 100
    total_cost = 0
    for stock in selected_stocks:
        stock[PRICE] = stock[PRICE] / 100
        stock[PROFIT_PERCENT] = stock[PROFIT_PERCENT] / 100,
        stock[PROFIT_EURO] = stock[PROFIT_EURO] / 100
        total_cost += stock[PRICE]
    # Show the suggestion of the algorithm

    print(f"The estimated maximum profit is {total_profit}€ "
          f"for a total cost of {total_cost}€\n")
    print("List of stocks to buy:")
    for stock in selected_stocks:
        print(f"{stock[NAME]}: {stock[PRICE]}€")


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
            print("Dynamic Programming Algorithm\n")
            print("--------------------\n")
            # greedy_algorithm(stocks)
        except FileNotFoundError:
            print(f"No such file or directory: '{sys.argv[1]}'\n")

        print()
        dynamic_programming(stocks)
        execution_time = round(time() - start_time, 3)
        print(f"\nExecution time: {execution_time}s")
