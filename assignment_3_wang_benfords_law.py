
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

def pre_process_data(df):
    '''
    df: dataframe of relevant data
    returns: dataframe with processed data, only keeping country, 
    '''
    # Select only necessary columns
    # Based on a look at various stock codes, there are items with the same stock code but different prices.
    # We won't remove "duplicate" entries
    # Prices are unit prices, so no preprocessing for that is necessary
    # Stockcode will be more unique than desc
    relevant_columns_df = df[['StockCode', 'Price', 'Country']]
    # Remove all values that don't have 0 as a leading digit. Also ignoring negative numbers as well since Benford doesn't handle this
    remove_leading_digit = relevant_columns_df[(relevant_columns_df['Price'] >= 1)].copy()
    remove_leading_digit['LeadingDigit'] = relevant_columns_df['Price'].astype(str)
    remove_leading_digit['LeadingDigit'] = remove_leading_digit['LeadingDigit'].apply(lambda x: x[0]).astype(int)
    return remove_leading_digit[['StockCode', 'LeadingDigit', 'Country']]

def model_1_equal_weight_distribution(size):
    '''
    size: input size for creating uniform weight distribution
    returns: a dataframe with a list of digits that are uniformly distributed
    '''
    df = pd.DataFrame(np.array([i%9+1 for i in range(0,size)]), columns=['Equal Weight Distribution'])
    return df

def model_2_benford_weight_distribution(size):
    '''
    size: input size for creating benford weight distribution
    returns: a dataframe with a list of digits that are benford distributed
    '''
    # This distribution is calculated using a sample size and a probability vector.
    # Small data sets will 
    probability_vector = [math.log10(1+1/d) for d in range(1,10)]
    value_vector = [i for i in range(1,10)]
    return pd.DataFrame(np.random.choice(value_vector, size, p=probability_vector), columns=['Benford Distribution'])

def plot_and_save_histogram_digits(df, title=None, name=None):
    '''
    df: dataframe of relevant data
    title: name of the title. If none, will throw error
    name: name of the plot. If none, will throw error
    returns: None
    '''
    try:
        ax = df.plot(kind='hist', bins=9, title=title, alpha=0.5, grid=True, rwidth=0.9)
        ax.set_xlabel('Digits')
        ax.set_ylabel('Frequencies')
        plt.savefig(fname=name)
        plt.close()
    except ValueError:
        print('Please pass name and/or as a param')

def plot_and_save_bar_chart_digits(df, title=None, name=None, ylabel=None):
    '''
    df: dataframe of relevant data
    title: name of the title. If none, will throw error
    name: name of the plot. If none, will throw error
    ylabel: x label is always digits for this project, but y label may vary
    returns: None
    '''
    try:
        ax = df.plot(kind='bar', title=title, alpha=0.5, grid=True)
        ax.set_xlabel('Digits')
        ax.set_ylabel(ylabel)
        plt.savefig(fname=name)
        plt.close()
    except ValueError:
        print('Please pass name and/or as a param')

def create_dist_order(dist_vector):
    '''
    dist_vector: vector for real data
    return: df with distribution counts
    '''
    sorted_vector = dist_vector.iloc[:,0].value_counts().sort_index()
    indices = sorted_vector.index
    not_present_indices = []
    for i in range(1, 10):
        if i not in indices:
            not_present_indices.append(i)
    if len(not_present_indices) > 0:
        sorted_vector_dict = sorted_vector.to_dict()
        for index in not_present_indices:
            sorted_vector_dict[index] = 0
        return pd.Series(sorted_vector_dict, name=sorted_vector.name).sort_index()
    return sorted_vector


def relative_error(actual_vector, approximate_vector, name='Relative Error'):
    '''
    actual_vector: vector for real data
    approximate_vector: vector for approximate data
    returns: Relative vector as a vector of floats
    '''
    # Get value counts of series
    actual_counts = create_dist_order(actual_vector)
    approximate_counts = create_dist_order(approximate_vector)
    estimation_approx = np.subtract(actual_counts, approximate_counts)
    absolute_estimation = np.abs(estimation_approx)
    return pd.DataFrame(np.array(np.divide(absolute_estimation, actual_counts)), columns=[name]).sort_index()

def rmse(actual_vector, approximate_vector):
    '''
    actual_vector: vector for real data
    approximate_vector: vector for approximate data
    returns: RMSE value
    '''
    # Get value counts of series
    actual_counts = create_dist_order(actual_vector)
    approximate_counts = create_dist_order(approximate_vector)

    estimation_approx = np.subtract(actual_counts, approximate_counts)

    abs_vector_diff_squared = np.square(estimation_approx)
    total_sum = np.sum(abs_vector_diff_squared)
    size = len(actual_vector)
    mean_calculation = np.divide(total_sum, size)
    rmse = np.round(np.sqrt(mean_calculation), 5)

    return rmse

def main():
    # The file name here has been updated based on my BU ID. 09-10 will be used.
    # Header names: Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country
    file_name = 'Retail_09_10.csv'
    df = pd.read_csv(file_name, encoding='ISO-8859-1')
    post_process_df = pre_process_data(df)
    df_rows_length = len(post_process_df.index)
    df_model_1 = model_1_equal_weight_distribution(df_rows_length)
    df_model_2 = model_2_benford_weight_distribution(df_rows_length)
    df_actual = pd.DataFrame(np.array(post_process_df['LeadingDigit']), columns=['Actual Distribution'])
    plot_and_save_histogram_digits(df_model_1, title='Model 1-Uniform Distribution', name='Q_1_Model_1')
    plot_and_save_histogram_digits(df_model_2, title='Model 2-Benford Distribution', name='Q_1_Model_2')
    plot_and_save_histogram_digits(df_actual, title='Actual Distribution', name='Q_1_Actual_Distribution')
    print('Question 1:')
    print('See the following files: Q1_Model_1.png for uniform distribution, Q1_Model_2.png for Benford\'s law, Q1_Actual_Distribution.png for ')
    print('the real distribution of 09-10 data.')
    print('\nQuestion 2:')
    print('Actual graph vs Model 1: Q_2_Model_1_Actual_Relative_Error')
    print('Usually relative error assumes an "actual" dataset, but when comparing Model 1 to Model 2, we can do the converse since we have no "actual" model.')
    plot_and_save_bar_chart_digits(relative_error(df_actual, df_model_1, name='Relative Error Model 1 vs Actual'),
        title='Model 1 vs Actual Graph Relative Error', name='Q_2_Model_1_Actual_Relative_Error', ylabel='Relative Error')
    print('Actual graph vs Model 2: Q_2_Model_2_Actual_Relative_Error')
    plot_and_save_bar_chart_digits(relative_error(df_actual, df_model_2, name='Relative Error Model 2 vs Actual'),
        title='Model 2 vs Actual Graph Relative Error', name='Q_2_Model_2_Actual_Relative_Error', ylabel='Relative Error')
    print('Model 1 vs Model 2: Q_2_Model_1_Model_2')
    plot_and_save_bar_chart_digits(relative_error(df_model_1, df_model_2, name='Relative Error Model 1 vs Model 2'),
        title='Model 1 vs Model 2', name='Q_2_Model_1_Model_2', ylabel='Relative Error')
    print('Model 2 vs Model 1: Q_2_Model_2_Model_1')
    plot_and_save_bar_chart_digits(relative_error(df_model_2, df_model_1, name='Relative Error Model 2 vs Model 1'),
        title='Model 2 vs Model 1', name='Q_2_Model_2_Model_1', ylabel='Relative Error')
    print('\nQuestion 3:')
    print('RMSE is calculated between the two vectors of distribution. Each vector contains the counts for each digit.')   
    print('Model 1 vs Actual')
    print(rmse(df_actual, df_model_1))
    print('Model 2 vs Actual')
    print(rmse(df_actual, df_model_2))
    print('Benford\'s model is closer to the real distribution.')
    print('\nQuestion 4:')
    print('Picking Japan from Asia, United Kingdom in Europe, and United Arab Emirates in the Middle East')
    print('(a) computing F, P, and pi')
    print('Frequencies')
    # Pull country specific data, along with the length of each vector to create the P and pi
    # Create dataframe for distribution and then the counts for the country
    # Japan
    japan_data = post_process_df[['LeadingDigit']][(post_process_df['Country'] == 'Japan')].copy()
    df_rows_japan = len(japan_data.index)
    df_actual_japan = pd.DataFrame(np.array(japan_data['LeadingDigit']), columns=['Japan Actual Distribution'])
    japan_counts = create_dist_order(df_actual_japan)
    df_model_1_japan = model_1_equal_weight_distribution(df_rows_japan)
    df_model_2_japan = model_2_benford_weight_distribution(df_rows_japan)
    japan_model_1_counts = create_dist_order(df_model_1_japan)
    japan_model_2_counts = create_dist_order(df_model_2_japan)
    # United Kingdom
    uk_data = post_process_df[['LeadingDigit']][(post_process_df['Country'] == 'United Kingdom')].copy()
    df_rows_uk = len(uk_data.index)
    df_actual_uk = pd.DataFrame(np.array(uk_data['LeadingDigit']), columns=['United Kingdom Actual Distribution'])
    uk_counts = create_dist_order(df_actual_uk)
    df_model_1_uk = model_1_equal_weight_distribution(df_rows_uk)
    df_model_2_uk = model_2_benford_weight_distribution(df_rows_uk)
    uk_model_1_counts = create_dist_order(df_model_1_uk)
    uk_model_2_counts = create_dist_order(df_model_2_uk)
    # United Arab Emirates
    uae_data = post_process_df[['LeadingDigit']][(post_process_df['Country'] == 'United Arab Emirates')].copy()
    df_rows_uae = len(uae_data.index)
    df_actual_uae = pd.DataFrame(np.array(uae_data['LeadingDigit']), columns=['United Arab Emirates Actual Distribution'])
    uae_counts = create_dist_order(df_actual_uae)
    df_model_1_uae = model_1_equal_weight_distribution(df_rows_uae)
    df_model_2_uae = model_2_benford_weight_distribution(df_rows_uae)
    uae_model_1_counts = create_dist_order(df_model_1_uae)
    uae_model_2_counts = create_dist_order(df_model_2_uae)


    print('Japan Frequency: ')
    print(japan_counts.to_frame().T)
    print('Japan P: ')
    print(japan_model_1_counts.to_frame().T)
    print('Japan Pi: ')
    print(japan_model_2_counts.to_frame().T)
    print('United Kingdom Frequency: ')
    print(uk_counts.to_frame().T)
    print('United Kingdom P: ')
    print(uk_model_1_counts.to_frame().T)
    print('United Kingdom Pi: ')
    print(uk_model_2_counts.to_frame().T)
    print('United Arab Emirates: ')
    print(uae_counts.to_frame().T)
    print('United Arab Emirates P: ')
    print(uae_model_1_counts.to_frame().T)
    print('United Arab Emirates Pi: ')
    print(uae_model_2_counts.to_frame().T)
    print('(b) Calculate each county\'s RMSE ')
    print('Japan RMSE Actual to P')
    print(rmse(df_actual_japan, df_model_1_japan))
    print('United Kingdom RMSE Actual to P')
    print(rmse(df_actual_uk, df_model_1_uk))
    print('United Arab Emirates RMSE Actual to P')
    print(rmse(df_actual_uae, df_model_1_uae))
    print('Japan has the lowest RMSE of data to uniform distribution')
    print('\nQuestion 5')
    print('It seems that based on the models, the distribution of sales from 2009 to 2010 fits Benford\'s law moreso than a uniform distribution ')
    print('in terms of the shape of the distribution. The relative error calculations were calculated between the two models and the data. The ')
    print('relative error between Model 1 and Model 2 with Model 1 as the actual data has the greatest error for the first few digits, the lowest for 3 and 4, and an increase in ')
    print('relative error for digits afterwards, which is consistent with Benford\'s distribution having greater frequencies for earlier digits and ')
    print('lower frequencies for later digits. Calculation of the relative error between Model 2 and Model 1 with Model 2 as the actual model show the converse, ')
    print('with a greater relative error at digit 9 (since Model 2 assumes the fewest frequency at that digit). The relative error calculations between these two models are consistent with expectations. ')
    print('The relative error for Actual Distribution vs Model 1 has the highest discrepancy between digits 6 to 9. This is due to the relative error model\'s ')
    print('denominator being fewer for the higher digits, which results in a greater relative error. Model 1\'s frequency does not change, but relative error will increase ')
    print('with a decreased denominator. The relative error for Actual Distribution vs Model 2 show similar results, but the relative error is overall ')
    print('less. The maximum relative error is ~1.75 between Model 2 and Actual Distribution, but ~6 between Model 1 and Actual Distribution. The smaller denominator ')
    print('for higher digits most likely has the same effect between Model 2 and Actual, but this relative error calculation still shows that Benford\'s distribution has less relative error ')
    print('against the Actual data than the uniform distribution. The RMSE calculations for Model 1 and Actual vs Model 2 and Actual indicate this as well, with Model 2 having the lower RMSE.')
    print('Benford\'s distribution was calculated empirically with a distribution, so some smaller datasets do not follow exactly said distribution. Regardless, I believe ')
    print('it is an acceptable model for comparing the three countries in problem 4. The three countries had significantly different frequencies, with Japan having the ')
    print('least transactions and the United Kingdom having the most transactions. Japan however, lacked transactions with digits 8 and 9. The United Arab Emirates lacked transactions ')
    print('with the digit 9. The United Kingdom had all digits in its transactions. While Japan\'s data with lack of two digit frequency indicates that it is closer to a Benford distribution, the ')
    print('UAE seems to have a larger percentage of smaller digit frequencies, and therefore has a slightly higher RMSE. In addition, the UK differed the most in RMSE from a uniform distribution. It seems ')
    print('that the larger the data set, the closer the digit distribution becomes a Benford distribution.')

if __name__ == "__main__":
    main()