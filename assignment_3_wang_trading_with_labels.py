import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

def transform_trading_days_to_trading_weeks(df):
    '''
    df: dataframe of relevant data
    returns: dataframe with processed data, only keeping weeks, their open and close for said week
    '''
    trading_list = deque()
    # Iterate through each trading week
    for trading_week, df_trading_week in df.groupby(['Year','Week_Number']):
        classification =  df_trading_week.iloc[0][['Classification']].values[0]
        opening_day_of_week = df_trading_week.iloc[0][['Open']].values[0]
        closing_day_of_week = df_trading_week.iloc[-1][['Close']].values[0]
        trading_list.append([trading_week[0], trading_week[1], opening_day_of_week, closing_day_of_week, classification])
    trading_list_df = pd.DataFrame(np.array(trading_list), columns=['Year', 'Trading Week', 'Week Open', 'Week Close', 'Classification'])
    return trading_list_df

def make_trade(cash, open, close):
    '''
    cash: float of cash on hand
    open: float of open price
    close: float of close price
    returns: The cash made from a long position from open to close
    '''
    shares = np.divide(cash, open)
    return np.multiply(shares, close)

def trading_strategy(trading_df, weekly_balance=100):
    '''
    trading_df: dataframe of relevant weekly data
    returns: A df of trades made based on classifications
    '''
    # The weekly balance we will be using
    weekly_balance_acc = weekly_balance
    trading_history = deque()
    index = 0
    while(index < len(trading_df.index) - 1):
        trading_week_index = index
        if weekly_balance_acc != 0:
            # Find the next consecutive green set of weeks and trade on them
            while(trading_week_index < len(trading_df.index) - 1 and trading_df.iloc[trading_week_index][['Classification']].values[0] == 'GREEN'):
                trading_week_index += 1
            green_weeks = trading_df.iloc[index:trading_week_index][['Week Open', 'Week Close']]
            # Check if there are green weeks, and if there are not, we add a row for trading history
            if len(green_weeks.index) > 0:
                # Buy shares at open and sell shares at close of week
                green_weeks_open = float(green_weeks.iloc[0][['Week Open']].values[0])
                green_weeks_close = float(green_weeks.iloc[-1][['Week Close']].values[0])
                # We append the money after we make the trade
                weekly_balance_acc = make_trade(weekly_balance_acc, green_weeks_open, green_weeks_close)
            # Regardless of whether we made a trade or not, we append the weekly cash and week over
            trading_history.append([trading_df.iloc[trading_week_index][['Year']].values[0],
                trading_df.iloc[trading_week_index][['Trading Week']].values[0],
                weekly_balance_acc])
        else:
            # If we have no money we will not be able to trade
            trading_history.append([trading_df.iloc[trading_week_index][['Year']].values[0],
                    trading_df.iloc[trading_week_index][['Trading Week']].values[0],
                    weekly_balance_acc])
        index = trading_week_index+1
    trading_hist_df = pd.DataFrame(trading_history, columns=['Year', 'Trading Week', 'Balance'])
    trading_hist_df['Balance'] = np.round(trading_hist_df[['Balance']], 2)

    return trading_hist_df

def main():
    # The file name here has been updated based on my BU ID. 09-10 will be used.
    # Header names: Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country
    file_name = 'WMT_Labeled_Weeks_Self.csv'
    df = pd.read_csv(file_name, encoding='ISO-8859-1')
    df_trading_weeks = transform_trading_days_to_trading_weeks(df)
    trading_strategy_payout_df = trading_strategy(df_trading_weeks)
    print('Trading Strategy Results:')
    print(trading_strategy_payout_df)
    print('\nQuestion 1:')
    print('The mean is ${}'.format(np.round(trading_strategy_payout_df[['Balance']].mean().values[0], 2)))
    print('The sigma is ${}'.format(np.round(trading_strategy_payout_df[['Balance']].std().values[0], 2)))




if __name__ == "__main__":
    main()