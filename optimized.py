#!/usr/bin/env python3

import sys
import pandas as pd

MAX_EXPENSE = 500


def greedy_algorithm(stocks):
    NAME, PRICE, PROFIT_PERCENT, PROFIT_EURO = 0, 1, 2, 3
    expense, total_profit, selected_stocks = 0, 0, []

    # Calculate the profit in euro
    for stock in stocks:
        profit_euro = stock[PRICE] * stock[PROFIT_PERCENT]
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

    stocks = selected_stocks

    print(f"Maximum profit is {total_profit}€ "
          f"for a total investissement of {expense}€\n")
    print("List of stocks to buy:")
    for stock in stocks:
        print(f"{stock[NAME]}: {stock[PRICE]}€")


def main():
    if len(sys.argv) < 2:
        print("You must specify a dataframe file  as argument.")
        return
    elif len(sys.argv) != 2:
        print("There are too many arguments specified.")
        return
    else:
        try:
            print("Loading the dataframe...\n")
            df = pd.read_csv(sys.argv[1], header=0)
            stocks = df.values.tolist()
            print(f"{df}\n")
            greedy_algorithm(stocks)
        except FileNotFoundError:
            print(f"No such file or directory: '{sys.argv[1]}'\n")
            return


if __name__ == "__main__":
    main()
