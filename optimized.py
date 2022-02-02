#!/usr/bin/env python3

import sys
import pandas as pd

MAX_EXPENSE = 500
NAME, PRICE, PROFIT_PERCENT, PROFIT_EURO = 0, 1, 2, 3


def remove_incorrect_data(stocks):
    new_stocks = []
    for stock in stocks:
        if stock[PRICE] > 0 and stock[PROFIT_PERCENT] > 0:
            new_stocks.append(stock)
    return new_stocks


def greedy_algorithm(stocks):
    expense, total_profit, selected_stocks = 0, 0, []
    # Calculate the profit in euro
    for stock in stocks:
        profit_euro = stock[PRICE] * (stock[PROFIT_PERCENT] / 100)
        stock.append(round(profit_euro, 2))
    # Sort stocks by profit (%)
    stocks.sort(key=lambda x: x[PROFIT_PERCENT], reverse=True)
    for stock in stocks:
        if expense + stock[PRICE] <= MAX_EXPENSE:
            expense += stock[PRICE]
            expense = round(expense, 2)
            total_profit += stock[PROFIT_EURO]
            total_profit = round(total_profit, 2)
            selected_stocks.append(stock)
    print(f"Maximum profit is {total_profit}€ "
          f"for a total investissement of {expense}€\n")
    print("List of stocks to buy:")
    for stock in selected_stocks:
        print(f"{stock[NAME]}: {stock[PRICE]}€")


def dynamic_programming():
    pass


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
            stocks = remove_incorrect_data(stocks)
            print(f"{df}\n")
            print("--------------------\n")
            print("Greedy algorithm\n")
            print("--------------------\n")
            greedy_algorithm(stocks)
        except FileNotFoundError:
            print(f"No such file or directory: '{sys.argv[1]}'\n")


if __name__ == "__main__":
    main()
