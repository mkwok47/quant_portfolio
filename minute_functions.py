#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 02:47:27 2022

@author: michaelkwok
"""

import datetime
import pandas as pd
import alpaca_table2

market_open_time = datetime.time(6,30)
market_close_time = datetime.time(13)

# =============================================================================
# Functions
# =============================================================================

def view_utc_offsets(df_input):
  
    '''
    PURPOSE: deal with daylight time savings, ensure data is as expected
    '''
    
    df = df_input.copy(deep=True)
    unique_time_diffs = df['timestamp_pacific_str'].str[-5:].unique()
    print(unique_time_diffs)
    for unique_time_diff in unique_time_diffs:
        print(unique_time_diff, len(df[df['timestamp_pacific_str'].str[-5:] == unique_time_diff]))
    if len(unique_time_diffs) != 2:
        raise ValueError('check utc offset')
    
def obtain_data(tickers, timeframes, action=None, start_date='2000-01-01', end_date=str(datetime.datetime.today().date() - datetime.timedelta(days=1))):
    
    '''
    PURPOSE: obtain dictionary of dataframes
    note: unique_dates will be in pacific time
    '''
    
    dicts = {ticker:{timeframe:{} for timeframe in timeframes} for ticker in tickers}
    
    for timeframe in timeframes:
        
        for ticker in tickers:
            
            df = alpaca_table2.obtain_table(ticker, timeframe, action=action, start_date=start_date)
            dicts[ticker][timeframe]['df'] = df.copy(deep=True)
            
            dicts[ticker][timeframe]['df']['timestamp_pacific'] = dicts[ticker][timeframe]['df'].index.tz_convert('US/Pacific')
            dicts[ticker][timeframe]['df']['timestamp_pacific_str'] = dicts[ticker][timeframe]['df']['timestamp_pacific'].astype(str)
            
            dicts[ticker][timeframe]['df'] = dicts[ticker][timeframe]['df'][dicts[ticker][timeframe]['df']['timestamp_pacific'] < end_date]
            
            dicts[ticker][timeframe]['df'].loc[(dicts[ticker][timeframe]['df']['timestamp_pacific'].dt.time >= market_open_time) & (dicts[ticker][timeframe]['df']['timestamp_pacific'].dt.time <= market_close_time), 'market_hours'] = 'regular'
            dicts[ticker][timeframe]['df'].loc[(dicts[ticker][timeframe]['df']['timestamp_pacific'].dt.time < market_open_time), 'market_hours'] = 'premarket'
            dicts[ticker][timeframe]['df'].loc[(dicts[ticker][timeframe]['df']['timestamp_pacific'].dt.time > market_close_time), 'market_hours'] = 'aftermarket'
            print(len(dicts[ticker][timeframe]['df']), timeframe)
            view_utc_offsets(dicts[ticker][timeframe]['df'])
            dicts[ticker]['unique_dates'] = dicts[ticker][timeframe]['df']['timestamp_pacific'].dt.date.unique()
            # dicts[ticker]['unique_dates']  = [x for x in dicts[ticker]['unique_dates'] if (x.weekday() <= 4 and len(dicts[ticker][timeframe]['df'][dicts[ticker][timeframe]['df']['timestamp_pacific'].dt.date==x])>=100)] # 2nd part takes too long, do in-research
            dicts[ticker]['unique_dates']  = [x for x in dicts[ticker]['unique_dates'] if x.weekday() <= 4]
            print(ticker, len(dicts[ticker]['unique_dates']), 'days')
            display(dicts[ticker][timeframe]['df'])
            
    return dicts

def obtain_conjunction(ticker_descript_dict, dicts, timeframe, tail_n=1000000):
    
    '''
    PURPOSE: join bull/bear ETF datasets together
    ticker_descript_dict = {'LABU':'bull', 'LABD':'bear'}
    '''
        
    df = dicts[list(ticker_descript_dict.keys())[0]][timeframe]['df'].tail(tail_n).copy(deep=True)
    df = df[(df['timestamp_pacific'].dt.time >= market_open_time) & (df['timestamp_pacific'].dt.time < market_close_time)]
    conjunction_df = pd.DataFrame(index=df.index)

    for ticker in ticker_descript_dict.keys():
        df = dicts[ticker][timeframe]['df'].tail(tail_n).copy(deep=True)
        df = df[(df['timestamp_pacific'].dt.time >= market_open_time) & (df['timestamp_pacific'].dt.time < market_close_time)]
        df['green'] = df['open'] < df['close']
        descript = ticker_descript_dict[ticker]
        df.rename(columns={col:f'{descript}_{col}' for col in df}, inplace=True)
        conjunction_df = conjunction_df.merge(df, left_index=True, right_index=True, how='outer')
        
    dicts[ticker][timeframe]['df']['timestamp_pacific'] = dicts[ticker][timeframe]['df'].index.tz_convert('US/Pacific')
    dicts[ticker][timeframe]['df']['timestamp_pacific_str'] = dicts[ticker][timeframe]['df']['timestamp_pacific'].astype(str)

    descripts = list(ticker_descript_dict.values())    
    for descript in descripts:
        conjunction_df.drop(columns=[f'{descript}_timestamp_pacific', f'{descript}_timestamp_pacific_str'], inplace=True)

    conjunction_df['timestamp_pacific'] = conjunction_df.index.tz_convert('US/Pacific')
    conjunction_df['timestamp_pacific_str'] = conjunction_df['timestamp_pacific'].astype(str)
    view_utc_offsets(conjunction_df)
    
    return conjunction_df

def obtain_daily_attributes(dicts, timeframe, min_length):
    
    '''
    PURPOSE: join day-level price data with minute-level price data
    uses minutely data to infer daily data (to maintain consistency of data source)
    '''
    
    for ticker in dicts.keys():
        unique_dates = dicts[ticker]['unique_dates'].copy()
        df = dicts[ticker][timeframe]['df'].copy(deep=True)
        daily_df = pd.DataFrame()
        
        for unique_date in unique_dates:
            temp_df = df[(df['timestamp_pacific'].dt.date == unique_date) & (df['market_hours']=='regular')].copy(deep=True)
            if len(temp_df) < min_length:
                continue
            daily_df.at[unique_date, 'day_open'] = temp_df['open'].iloc[0]
            daily_df.at[unique_date, 'day_high'] = max(temp_df['high'])
            daily_df.at[unique_date, 'day_low'] = min(temp_df['low'])
            daily_df.at[unique_date, 'day_close'] = temp_df['close'].iloc[-1]
            
        dicts[ticker]['day'] = {}
        dicts[ticker]['day']['df'] = daily_df
        
        for unique_date in unique_dates:
            for col in ['day_open', 'day_high', 'day_low', 'day_close']:
                dicts[ticker][timeframe]['df'].loc[dicts[ticker][timeframe]['df']['timestamp_pacific'].dt.date==unique_date, col] = daily_df[daily_df.index==unique_date][col][0]

    return dicts
