#!/usr/bin/env python3

import sys
import pandas as pd

MAX_EXPENSE = 500
NAME, PRICE, PROFIT_PERCENT, PROFIT_EURO = 0, 1, 2, 3


def bruteforce(stocks):
    print("-------------------------\n")
    print("Starting the bruteborce...\n")
    # Calculate the profit in euro
    for stock in stocks:
        profit_euro = stock[PRICE] * (stock[PROFIT_PERCENT] / 100)
        stock.append(round(profit_euro, 2))
    # Determine the maximum number of combinations
    number_of_action = len(stocks)
    max_combinations = 2 ** number_of_action
    print(f"Maximum combinations: {max_combinations}\n")
    # Retrieve only the list of valid combinations (<=MAX_EXPENSE)
    valid_combinations = []
    for combination in range(max_combinations):
        expense, valids = 0, []
        matrix = bin(combination)[2:]
        matrix = '0' * (number_of_action - len(matrix)) + matrix
        for i in range(number_of_action):
            if matrix[i] == '1':
                expense += stocks[i][PRICE]
                valids.append(stocks[i])
        if expense <= MAX_EXPENSE:
            valid_combinations.append(valids)
    # Calculates the profit of each combination and keeps the best
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
    # Show the result of the bruteforce
    print("Bruteforce successfully completed !\n")
    print("-------------------------\n")
    print(f"Maximum profit is {max_profit}€ "
          f"for a total cost of {amount_of_expense}€\n")
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
