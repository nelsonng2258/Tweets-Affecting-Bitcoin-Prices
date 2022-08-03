#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 21:58:00 2022

@author: nelsonng
"""

# Import libraries.  
import datetime as dt 
import numpy as np
import pandas as pd 

from datetime import date
from datetime import timedelta

# ----------------------------------------------------------------------------------------------

def cleaned_date_lt(df, col):  
    
    '''Create cleaned_date_lt to clean columns: 'user_created', 'date'.'''
    
    date_lt = [] 

    for i in df[col]:

        # Those without error values during conversion to datetime. 
        try:
            
            # Convert the values into year, month and day. 
            year = int(i[:4])
            month = int(i[5:7])
            day = int(i[8:10])

            # Convert them into datetime.
            actual_date = date(year, month, day)

            # Check if the actual_date is a valid datetime.date. 
            if type(actual_date) == dt.date:
                date_lt.append(actual_date)

        # Those with error values during conversion to datetime.   
        except: 

            # Append np.nan to user_date_lt. 
            date_lt.append(np.nan)

    return date_lt


def cleaned_int_lt(df, col): 
    
    '''Create cleaned_int_lt to clean columns: 'user_friends', 'user_favourites'.'''
    
    user_int_lt = [] 

    for i in df[col]:

        # Those without error values during conversion to int. 
        try:
            
            # Convert i into int and place it into number variable. 
            number = int(i)
            
            # Append name into user_int_lt. 
            user_int_lt.append(number)

        # Those with error values during conversion to int.  
        except:

            # Append nothing to user_int_lt. 
            user_int_lt.append(np.nan)

    return user_int_lt


def cleaned_boolean_lt(df, col):
    
    '''Create cleaned_boolean_lt to clean columns: 'user_verified', 'is_retweet'.'''
    
    cleaned_boolean_lt = []

    for i in df[col]:
        
        # Segregate based on booleans (True/ False)
        if i == True:
            cleaned_boolean_lt.append(True)

        elif i == False:
            cleaned_boolean_lt.append(False)

        else:
            
            # Append np.nan to cleaned_boolean_lt for non-boolean.
            cleaned_boolean_lt.append(np.nan)
            
    return cleaned_boolean_lt 


def print_unique_col(df): 
    
    '''Print number of unique values within the columns.'''
    
    # Identify the number of unique values within each column
    print('Column: Number of Unique Values')
    for i in df.columns:
        print(str(i)+': {}'.format(len(df[i].unique()))) 
        
        
def print_null_col(df):
    
    '''Print null values of columns.'''
    
    # Null values per column
    print('\033[1m' + 'Column              No. of Null Values' + '\033[0m') 
    print(df.isnull().sum())
    

def print_50_pct_null_col(df, copy_df):
    
    '''Print columns that have >50 precent of null values.'''
    
    # Create deep copy of df and df_copy.
    df = df.copy(deep=True)
    copy_df = copy_df.copy(deep=True)

    # Identify columns that have null values. 
    column_has_nan = df.columns[df.isnull().any()]

    # Search and drop columns that have at least 50% of null data.
    for column in column_has_nan:

        # Ensure that there are at least 50% of null data.
        if df[column].isnull().sum()/df.shape[0] > 0.50:
            df.drop(column, 1, inplace=True)  

    # Identify columns having >50% of null values. 
    original_columns = [i for i in copy_df.columns]
    new_columns = [i for i in df.columns]
    removed_columns = [i for i in original_columns if i not in new_columns]
    
    # Print columns having >50% of null values. 
    print('\033[1m' + 'Columns having >50% of Null Values:' + '\033[0m')
    for i in removed_columns:
        print(i)


def remove_null_row(df, col):
    
    '''Remove null row of dataframe.'''
    
    # Identify the index of the null values.
    labels=[x for x in df[df[col].isnull()].index]

    # Drop null rows of df basing on identified index.
    df.drop(labels=labels, axis=0, inplace=True)
    

def drop_duplicated_row(df, duplicated_df): 
    
    '''Drop those additional duplicated rows.'''

    duplicated_index_lt = [] 
    
    # Iterate over index of df.
    for i, j in enumerate(duplicated_df.index):
        
        # Append j for all the odd values of i into duplicated_index_lt. 
        if i%2 == 1:
            duplicated_index_lt.append(j) 
    
    # Remove duplicated rows from dataframe
    for i in duplicated_index_lt:
        df.drop(labels=i, axis=0, inplace=True) 


def duplicates_df(df, col_lt):
    
    '''Create a dataframe for duplicates.'''
    
    # Create a boolean values to identify duplicate rows.
    duplicates = df.duplicated(subset=col_lt, keep=False)
    
    # Create a boolean values to identify duplicate rows. 
    df = df[duplicates]
    
    return df


def update_col_names(df): 
    
    '''Update and capitalize the column names.'''
    
    word_lt = []
    column_lt = []
    
    # Iterate over column of dataframe. 
    for i in df.columns:
    
        char_lt = []
        
        # Iterate over column in str format. 
        for j in str(i):
            
            # Append ' ' to char_lt for '_'.
            if j == '_':
                char_lt.append(' ')

            else:
                char_lt.append(j)
        
        # Append to word_lt after joining char_lt. 
        word_lt.append(''.join(char_lt))
    
    # Iterate over word_lt. 
    for i in word_lt:

        updated_word_lt = []
        
        # Iterate over the split text of word_lt 
        for j in i.split():
            
            # Capitalize word and append it into updated_word_lt. 
            updated_word_lt.append(j.capitalize())
        
        # Append into column_lt after joining the updated_word_lt. 
        column_lt.append(' '.join(updated_word_lt))
        
    return column_lt 
        

def cleaned_float_lt(df, col): 
    
    '''Create cleaned_float_lt to clean columns: 'CBBTCUSD'.'''
    
    user_float_lt = [] 

    for i in df[col]:

        # Those without error values during conversion to float. 
        try:
            
            # Convert i into float and place it into number variable. 
            number = float(i)
            
            # Append name into user_int_lt. 
            user_float_lt.append(number)

        # Those with error values during conversion to float.  
        except:

            # Append nothing to user_float_lt. 
            user_float_lt.append(np.nan)

    return user_float_lt

# ----------------------------------------------------------------------------------------------

# Subfunction of print_drop_missing_previous_date func. 
def missing_previous_date_lt(df): 
    
    '''List of missing previous dates.'''
    
    previous_date_lt = []
    date_lt = []
    missing_date_lt = []
    missing_previous_date_lt = [] 

    # Create a list of previous day dates. 
    for i in df['Date']: 

        # Append previous day date into previous_date_lt. 
        previous_date_lt.append(i + timedelta(days=-1))

    # Create a list of available dates from dataframe.  
    for i in df['Date']:

        # Append available date into date_lt. 
        date_lt.append(i)

    # Iterate over previous_date_lt to search for dates that are not inside date_lt. 
    for i in previous_date_lt: 

        # Sort for missing date.
        if i not in date_lt:

            # Append missing date into missing_date_lt.
            missing_date_lt.append(i)

    # Create a list of dates to adjust from dataframe.
    for i in missing_date_lt:

        # Append dates with missing previous date into missing_previous_date_lt.
        missing_previous_date_lt.append(i + timedelta(days=1))

    return missing_previous_date_lt

# Subfunction of print_drop_missing_previous_date func.  
def drop_row_missing_previous_date(df, missing_prev_date_lt):
    
    '''Drop rows of dataframe of missing previous date.'''
    
    index_lt = []
    
    # Search for index of dataframe of missing previous date. 
    for i, j in enumerate(df['Date']):
        for k in missing_prev_date_lt:    
            if k == j:
                index_lt.append(i) 
    
    # Drop rows of dataframe of missing previous date.
    for i in index_lt:
        try: 
            df.drop(labels=i, axis=0, inplace=True) 
        
        # If the row has already being deleted previously. 
        except:
            pass 
        
    # Reset index of dataframe. 
    df.reset_index(inplace=True)


def print_drop_missing_previous_date(df): 
    
    '''Print out dates with missing previous dates.'''
    
    # Create list of missing previous date. 
    missing_prev_date_lt = missing_previous_date_lt(df)
    
    # Print dates of missing previous dates.
    print('\033[1m' + 'Dates that have missing previous dates and their respective rows dropped:' + '\033[0m')
    
    for i in missing_prev_date_lt:
        print(i)
        
    # Drop rows with missing previous date.
    drop_row_missing_previous_date(df, missing_prev_date_lt)

# ----------------------------------------------------------------------------------------------

def date_ctext_df(df, tweets):  
    
    '''Create a dataframe that stores date and combine text.'''
    
    # Create a deep copy of dataframe.
    df = df.copy(deep=True)
    
    # Sort dataframe based on datetime on 'Date' column.  
    df = df.sort_values('Date', ascending=True)

    # Set btc_date. 
    btc_date = df.Date.unique()[0]

    date_text_dict = {}
    text_lt = [] 

    # Iterate over the first tweets. 
    for i, j in df[:tweets].iterrows(): # maybe the remove the amount of tweets in the end? 

        # btc_date matches. 
        if btc_date == j.Date:

            # Append inside text_list. 
            text_lt.append(j.Text) 

        # btc_date does not match.
        else:

            # Store the previous text_list of the previous date into the date_text_dict. 
            date_text_dict[btc_date] = text_lt 

            # Update btc_date_lt and text_lt. 
            # Update btc_date_lt with new date.
            btc_date = j.Date

            # Update text_lt with an empty list. 
            text_lt = [] 

            # Append Text into the updated text_lt. 
            text_lt.append(j.Text) 

    # Store the previous text_list of the previous date into the date_text_dict. 
    date_text_dict[j.Date] = text_lt 

    # Create a date_text_df dataframe. 
    # Create an empty dataframe for date_text_df.
    date_ctext_df = pd.DataFrame()

    # Create a date_text_dict_df dataframe to store date and text. 
    date_lt = []
    ctext_lt = [] 
    
    # Append key and value into date_lt and ctext_lt respectively. 
    for key, value in date_text_dict.items():
        date_lt.append(key)
        ctext_lt.append(value)

    # Add date and text into date_ctext_df. 
    date_ctext_df['Date'] = date_lt
    date_ctext_df['Combined Text'] = ctext_lt
    
    # Sort dataframe based on datetime on 'Date' column.  
    date_ctext_df = date_ctext_df.sort_values('Date', ascending=True)
    
    return date_ctext_df

