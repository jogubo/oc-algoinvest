#!/usr/bin/env python3

import sys
import pandas as pd

MAX_EXPENSE = 500


def bruteforce(stocks):
    NAME, PRICE, PROFIT_PERCENT, PROFIT_EURO = 0, 1, 2, 3

    print("-------------------------\n")
    print("Starting the bruteborce...\n")
    # Calculate the profit in euro
    for stock in stocks:
        profit_euro = stock[PRICE] * (stock[PROFIT_PERCENT] / 100)
        stock.append(round(profit_euro, 2))

    number_of_action = len(stocks)
    max_combinations = 2 ** number_of_action
    print(f"Maximum combinations: {max_combinations}\n")
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

    max_profit, amount_of_expense, i = 0, 0, 0
    print(f"Possible combinations: {len(valid_combinations)}\n")
    for stocks in valid_combinations:
        total_profit = 0
        total_expense = 0
        for stock in stocks:
            total_profit += stock[PROFIT_EURO]
            total_expense += stock[PRICE]
        if total_profit > max_profit:
            max_profit = round(total_profit, 2)
            amount_of_expense = round(total_expense, 2)
            best_invest = valid_combinations[i]
        i += 1
    print("Bruteforce successfully completed !\n")
    print("-------------------------\n")
    print(f"Maximum profit is {max_profit}€ "
          f"for a total investissement of {amount_of_expense}€\n")
    print("List of stocks to buy:")
    for stock in best_invest:
        print(f"{stock[NAME]}: {stock[PRICE]}€")


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
            print(f"{df}\n")
            bruteforce(stocks)
        except FileNotFoundError:
            print(f"No such file or directory: '{sys.argv[1]}'\n")


if __name__ == "__main__":
    main()
