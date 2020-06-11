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
    trading_hist_df = pd.DataFrame(np.array(trading_history), columns=['Year', 'Trading Week', 'Balance'])
    trading_hist_df['Balance'] = np.round(trading_hist_df[['Balance']].astype(float), 2)

    return trading_hist_df

def plot_trading_growth(trading_strategy_payout_df, name='Q_2_Trading_Growth'):
    '''
    trading_strategy_payout_df: dataframe of relevant trading returns
    name: file output name
    returns: None
    '''
    ax = trading_strategy_payout_df.plot(y='Balance', kind='line', title='Trading Strategy WMT')
    ax.set_xlabel('Week Number')
    ax.set_ylabel('Balance ($)')
    plt.savefig(fname=name)
    plt.close()

def calculate_weeks_decrease_increase(trading_strategy_payout_df):
    '''
    trading_strategy_payout_df: dataframe of relevant trading returns
    returns: tuple of ints with max increase and max decrease
    '''
    # Max increase and decrease algorithm
    max_increase = 0
    max_decrease = 0
    index = 0
    while(index < len(trading_strategy_payout_df.index) - 1):
        increase = 0
        decrease = 0

        # Find the next consecutive green set of weeks and trade on them
        while(index < len(trading_strategy_payout_df.index) - 1 and
             np.round(float(trading_strategy_payout_df.iloc[index+1][['Balance']].values[0]), 2) > np.round(float(trading_strategy_payout_df.iloc[index][['Balance']].values[0]), 2)):
            index += 1
            increase += 1
        if max_increase < increase:
            max_increase = increase
        # Find the next consecutive set of red weeks
        while(index < len(trading_strategy_payout_df.index) - 1 and
            np.round(float(trading_strategy_payout_df.iloc[index+1][['Balance']].values[0]), 2) < np.round(float(trading_strategy_payout_df.iloc[index][['Balance']].values[0]), 2)):
            index += 1
            decrease += 1
        if max_decrease < decrease:
            max_decrease = decrease
        # If we have a flat week we reset continue to the next week
        if(index < len(trading_strategy_payout_df.index) - 1 and
            np.round(float(trading_strategy_payout_df.iloc[index+1][['Balance']].values[0]), 2) == np.round(float(trading_strategy_payout_df.iloc[index][['Balance']].values[0]), 2)):
            index += 1
    return max_increase, max_decrease

def main():
    file_name = 'WMT_Labeled_Weeks_Self.csv'
    df = pd.read_csv(file_name, encoding='ISO-8859-1')
    df_trading_weeks = transform_trading_days_to_trading_weeks(df)
    # Split data into 2018 and 2019
    trading_weeks_2018 = df_trading_weeks[df_trading_weeks['Year'] == '2018']
    trading_weeks_2018.reset_index(inplace=True)
    trading_weeks_2019 = df_trading_weeks[df_trading_weeks['Year'] == '2019']
    trading_weeks_2019.reset_index(inplace=True)

    trading_strategy_payout_df_2018 = trading_strategy(trading_weeks_2018)
    trading_strategy_payout_df_2019 = trading_strategy(trading_weeks_2019)
    print('Trading Strategy Results:')
    print('For 2018')
    print(trading_strategy_payout_df_2018)
    print('For 2019')
    print(trading_strategy_payout_df_2019)

    print('\n2018 Results:')
    print('\nQuestion 1:')
    print('The mean is ${}'.format(np.round(trading_strategy_payout_df_2018[['Balance']].mean().values[0], 2)))
    print('The sigma is ${}'.format(np.round(trading_strategy_payout_df_2018[['Balance']].std().values[0], 2)))
    print('\nQuestion 2:')
    plot_trading_growth(trading_strategy_payout_df_2018, name='Q_2_Trading_Growth_2018')
    print('Plot Generated Name: Q_2_Trading_Growth_2018')
    print('\nQuestion 3:')
    print('The min is ${}'.format(np.round(trading_strategy_payout_df_2018[['Balance']].min().values[0], 2)))
    print('The max is ${}'.format(np.round(trading_strategy_payout_df_2018[['Balance']].max().values[0], 2)))
    print('\nQuestion 4:')
    print('The final value of the account is ${}'.format(np.round(trading_strategy_payout_df_2018[['Balance']].iloc[-1].values[0], 2)))
    print('\nQuestion 5:')
    print('We are ignoring weeks where we don\'t trade and are flat')
    increasing_weeks_2018, decreasing_weeks_2018 = calculate_weeks_decrease_increase(trading_strategy_payout_df_2018)
    print('Max number of monotonically increasing weeks: {}'.format(increasing_weeks_2018))
    print('Max number of monotonically decreasing, or flat weeks: {}'.format(decreasing_weeks_2018))

    print('\n2019 Results:')
    print('\nQuestion 1:')
    print('The mean is ${}'.format(np.round(trading_strategy_payout_df_2019[['Balance']].mean().values[0], 2)))
    print('The sigma is ${}'.format(np.round(trading_strategy_payout_df_2019[['Balance']].std().values[0], 2)))
    print('\nQuestion 2:')
    plot_trading_growth(trading_strategy_payout_df_2019, name='Q_2_Trading_Growth_2019')
    print('Plot Generated Name: Q_2_Trading_Growth_2019')
    print('\nQuestion 3:')
    print('The min is ${}'.format(np.round(trading_strategy_payout_df_2019[['Balance']].min().values[0], 2)))
    print('The max is ${}'.format(np.round(trading_strategy_payout_df_2019[['Balance']].max().values[0], 2)))
    print('\nQuestion 4:')
    print('The final value of the account is ${}'.format(np.round(trading_strategy_payout_df_2019[['Balance']].iloc[-1].values[0], 2)))
    print('\nQuestion 5:')
    print('We are ignoring weeks where we don\'t trade and are flat')
    increasing_weeks_2019, decreasing_weeks_2019 = calculate_weeks_decrease_increase(trading_strategy_payout_df_2019)
    print('Max number of monotonically increasing weeks: {}'.format(increasing_weeks_2019))
    print('Max number of monotonically decreasing, or flat weeks: {}'.format(decreasing_weeks_2019))



if __name__ == "__main__":
    main()