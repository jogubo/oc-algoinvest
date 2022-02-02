#!/usr/bin/env python3

import sys
import pandas as pd

MAX_EXPENSE = 500


def bruteforce(stocks):
    NAME, PRICE, PROFIT_PERCENT, PROFIT_EURO = 0, 1, 2, 3

    # Calculate the profit in euro
    for stock in stocks:
        profit_euro = stock[PRICE] * stock[PROFIT_PERCENT]
        stock.append(round(profit_euro, 2))

    number_of_action = len(stocks)
    max_combinations = 2 ** number_of_action
    valid_combinations = []
    matrice = [i for i in range(max_combinations)]
    matrice = [bin(i)[2:] for i in matrice]
    matrice = ['0' * (number_of_action - len(i)) + i for i in matrice]
    for combination in matrice:
        expense = 0
        valids = []
        for i in range(number_of_action):
            if combination[i] == '1':
                expense += stocks[i][PRICE]
                valids.append(stocks[i])
        if expense <= MAX_EXPENSE:
            valid_combinations.append(valids)

    max_profit, i = 0, 0
    for stocks in valid_combinations:
        total_profit = 0
        for stock in stocks:
            total_profit += stock[PROFIT_EURO]
        if total_profit > max_profit:
            max_profit = round(total_profit, 2)
            best_invest = valid_combinations[i]
        i += 1
    print(f"Maximum profit is {max_profit}€\n")
    print("List of stocks to buy:")
    for stock in best_invest:
        print(f"{stock[NAME]}")


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
            bruteforce(stocks)
        except FileNotFoundError:
            print(f"No such file or directory: '{sys.argv[1]}'\n")
            return


if __name__ == "__main__":
    main()
