import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


def main():
    # The file name here has been updated based on my BU ID. 09-10 will be used.
    # Header names: Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country
    file_name = 'BreadBasket_DMS_output.csv'
    df = pd.read_csv(file_name, encoding='ISO-8859-1')
    # Question 1
    transactions_group_by_hours_count = df[['Hour', 'Transaction']].groupby(['Hour']).agg(['count'])
    transactions_group_by_day_count = df[['Weekday', 'Transaction']].groupby(['Weekday']).agg(['count'])
    transactions_group_by_period_count = df[['Period', 'Transaction']].groupby(['Period']).agg(['count'])
    # Question 2
    transactions_group_by_hours_sum = df[['Hour', 'Item_Price']].groupby(['Hour']).agg(['sum'])
    transactions_group_by_day_sum = df[['Weekday', 'Item_Price']].groupby(['Weekday']).agg(['sum'])
    transactions_group_by_period_sum = df[['Period', 'Item_Price']].groupby(['Period']).agg(['sum'])
    # Question 3
    item_popularity = df[['Transaction', 'Item']].groupby('Item').count()
    # There may be multiple items with the same number of transactions
    maximum_item_number = item_popularity.max().values[0]
    minimum_item_number = item_popularity.min().values[0]
    maximum_item_list = item_popularity[item_popularity['Transaction'] == maximum_item_number].index
    minimum_item_list = item_popularity[item_popularity['Transaction'] == minimum_item_number].index
    # Question 4
    # Maximums of transactions per weekday for every day
    transactions_group_by_date = df[['Year', 'Month', 'Day', 'Weekday', 'Transaction']].groupby(['Year', 'Month', 'Day', 'Weekday']).agg(['count'])
    # Drop the dates that we used to group, reset the index so we can group by it again
    transactions_group_by_date.index = transactions_group_by_date.index.droplevel([0, 1, 2])
    transactions_group_by_date.reset_index(inplace=True)
    transactions_group_by_date.columns = ['Weekday', 'Transaction_Count']
    transactions_max_by_date = transactions_group_by_date.groupby(['Weekday']).agg(['max'])

    print('Question 1')
    print('(a) What is the busiest hour in terms of most transactions per hour?')
    print('Here is the sorted number of transactions to hours list:')
    print(transactions_group_by_hours_count.T)
    print('The maximum transactions for a given hour are: ')
    print(transactions_group_by_hours_count.idxmax().values[0])
    print('(b) What is the busiest day of the week in terms of most transactions per day?')
    print(transactions_group_by_day_count.T)
    print('The maximum transactions for a given day of the week are: ')
    print(transactions_group_by_day_count.idxmax().values[0])
    print('(c) What is the busiest period of the week in terms of most transactions per period?')
    print(transactions_group_by_period_count.T)
    print('The maximum transactions for a given day of the week are: ')
    print(transactions_group_by_period_count.idxmax().values[0])

    print('\nQuestion 2')
    print('(a) What is the most profitable hour for revenue?')
    print('Here is the sorted number of revenues to sum list:')
    print(transactions_group_by_hours_sum.T)
    print('The maximum revenue for the highest hour is: ')
    print(transactions_group_by_hours_sum.idxmax().values[0])
    print('(b) What is the most profitable day of the week for revenue?')
    print('Here is the sorted number of revenues to sum list:')
    print(transactions_group_by_day_sum.T)
    print('The maximum revenue for the highest day of the week is: ')
    print(transactions_group_by_day_sum.idxmax().values[0])
    print('(c) What is the most profitable period for revenue?')
    print('Here is the sorted number of period to sum list:')
    print(transactions_group_by_period_sum.T)
    print('The maximum revenue for the highest period of the week is: ')
    print(transactions_group_by_period_sum.idxmax().values[0])

    print('\nQuestion 3')
    print('List of all items: ')
    print(item_popularity.T)
    print('The most popular items are: {} with {} transactions'.format(str(maximum_item_list.values), str(maximum_item_number)))
    print('The least popular items are: {} with {} transactions'.format(str(minimum_item_list.values), str(minimum_item_number)))

    print('\nQuestion 4')
    print('Finding the maximum number of transactions for each day of the week should allow us to allocate the correct number of baristas')
    print('Find the amount of transactions occured for each day of the week for every day in the dataset')
    print(transactions_group_by_date.T)
    print('Find and list all the maximum transactions given a certain day')
    print(transactions_max_by_date.T)



if __name__ == "__main__":
    main()