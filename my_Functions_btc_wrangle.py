#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 12:15:44 2022

@author: nelsonng
"""

# Import libraries. 
import nltk 
import numpy as np
import pandas as pd 
import re
import string

from datetime import date 
from nltk.corpus import stopwords

# ----------------------------------------------------------------------------------------------

def start_end_dates_tp(df):
    
    '''Create a tuple of the start and end dates of the dataframe.'''
    
    # Find the date from the first row of 'Date' column. 
    start_date = df['Date'].head(1).values[0]
    
    # Find the date from the last row of 'Date' column. 
    end_date = df['Date'].tail(1).values[0]
    
    return start_date, end_date

# ----------------------------------------------------------------------------------------------

# Subfunction of print_date_diff func. 
def year_mth_day_tp(date_str):
    
    '''Create a tuple made of year, month and day.'''
    
    # Iterate after splitting based on '-'. 
    for i, j in enumerate(date_str.split('-')):

        # Sort for year.
        if i == 0:
            year = int(j)

        # Sort for month.
        elif i == 1:
            mth = int(j)

        # Sort for day.
        elif i == 2:
            day = int(j)
    
    return year, mth, day  

# Subfunction of print_date_diff func. 
def cnvt_dt_str_to_datetime(date_str):  
    
    '''Convert date from str to datetime format.'''
    
    # Create a tuple made of year, mth, day. 
    year, mth, day = year_mth_day_tp(date_str)
    
    # Create date into datetime format. 
    return date(year, mth, day) 


def print_date_diff(start_date, end_date):
    
    '''Print difference in days between start and end dates.'''
    
    # Convert to start and end dates to datetime format. 
    start_date_dt = cnvt_dt_str_to_datetime(start_date)
    end_date_dt = cnvt_dt_str_to_datetime(end_date)
    
    # Difference in days.
    day_diff_dt = end_date_dt - start_date_dt
    
    # Print title. 
    print('\033[1m' + "'Combined Text' column" + '\033[0m')
    
    # Print start and end dates.
    print('Start Date: ' + str(start_date))
    print('End Date: ' + str(end_date))
    
    # Print the duration of the start and end dates of the available bitcoin tweet text.
    text = 'Duration between Start Date and End Date: ' + str(day_diff_dt)
    print(text)

# ----------------------------------------------------------------------------------------------

# Subfunction of date_df func. 
def start_end_indexes(df, start_date, end_date):
    
    '''Create a tuple with indexes for start and end dates.'''
    
    start_index = None
    end_index = None
    
    # Iterate over 'Date' column of dataframe.  
    for i, j in enumerate(df['Date']):
        
        # Update start_index with index.
        if str(j)[:10] == start_date:
            start_index = i
        
        # Update end_index with index.
        if str(j)[:10] == end_date:
            end_index = i

    return start_index, end_index


def date_df(df, start_date, end_date):
    
    '''Create a dataframe based on start and end dates.'''
    
    # Find the start and end indexes from the start date and end date. 
    start_index, end_index = start_end_indexes(df, start_date, end_date)
    
    # Slice the dataframe based on the start and end indexes.
    df = df.iloc[start_index: end_index+1] # end_index + 1: This is done to include end_date or else it would be left out during slicing.
    
    return df 

# ----------------------------------------------------------------------------------------------

def df_to_txtf(df, file_path):
    
    '''Convert dataframe into an unstructured form and save it in a .txt file.'''
    
    full_txt = []
    
    # Iterate over the dataframe. 
    for index, row in df.iterrows():
        
        # Append date.
        full_txt.append(str(row[0]) + '\n')
        
        # Append bitcoin price change (%), bitcoin price (usd), and combined text.
        full_txt.append(str(row[2]) +  '..' + str(round(row[3],4)) + '..' + str(row[1]) + '\n')
    
    # Open file to write on it. 
    f = open(file_path, 'w')
    
    # Write lines inside the file.
    f.writelines(full_txt)  
    
    # Close file. 
    f.close() 

# ----------------------------------------------------------------------------------------------

# Subfunction of date_others_dict func. 
def readline_counter(file_path): 
    
    '''Find the max number of readlines of the file.'''
    
    readline_counter = 0

    # Open file to read for counting the number of readlines in the file. 
    f = open(file_path, 'r')
    
    # Use readline_counter to find the number of readlines in the file. 
    for i, j in enumerate(f):
        readline_counter += 1
        
    return readline_counter


# Subfunction of date_others_dict func. 
def date_others_tp(readline_counter, file_path): 
    
    '''Create a tuple of date_lt and other_lt (bitcoin price change (%), bitcoin price (usd), and combined text).'''
    
    date_lt = []
    others_lt = []
    
    # Open file to read to segregate the values. 
    f = open(file_path, 'r') 
    
    # Iterate over the range of the max number of readlines. 
    for i in range(readline_counter):  
        
        # Segregate to date. 
        if i == 0 or i%2 == 0:

            # Create text using f.readline.
            txt = f.readline() 

            # Append date to date_lt.
            date_lt.append(txt.strip()[:10])  

        # Segregate to bitcoin price change (%), bitcoin price (usd), and combined text.
        else:

            # Create text using f.readline.
            txt = f.readline()

            # Append bitcoin price change (%), bitcoin price (usd), and combined text to others_lt. 
            others_lt.append(txt.strip().split('..')) # '..' will split combined text as well. 
            
    return date_lt, others_lt 


# Subfunction of date_others_dict func. 
def modified_others_lt(others_lt):  
    
    '''Create a combine list of bitcoin price change (%), bitcoin price (usd)) and ctext_lt (combined text).'''
    
    modified_others_lt = []  
    
    for i in others_lt: 
    
        ctext_lt = [] 
    
        for j, k in enumerate(i): 
            
            # Segregate into bitcoin price change (%), bitcoin price (usd).
            if j == 0 or j == 1:
                
                # Append bitcoin price change (%), bitcoin price (usd) to modified_others_lt.
                modified_others_lt.append(k)
            
            # Segregate into combined text. 
            else:
                
                # Append texts of combined text into ctext_lt. 
                ctext_lt.append(k)
        
        # Append ctext_lt into modified_others_lt. 
        modified_others_lt.append(ctext_lt)
        
    return modified_others_lt 


# Subfunction of date_others_dict func.  
def final_lt(modified_others_lt): 
    
    '''Create a list of bitcoin price change (%), bitcoin price (usd), and consolidated combined text based on date.'''
    
    holding_lt = [] 
    final_lt = []
    counter = 0 
    
    # Create list within list within final_lt by reorganizing modified_others_lt. 
    for i, j in enumerate(modified_others_lt):
        
        # Segregate bitcoin price change (%), bitcoin price (usd), consolidated combined text based on date. 
        if counter <=2:
    
            # Append into holding_lt.  
            holding_lt.append(j) 
    
            counter += 1
        
        # Reset done to prepare for the next index. 
        if counter == 3:
    
            # Append holding_lt to final_lt. 
            final_lt.append(holding_lt)
            
            # Reset the holding_lt. 
            holding_lt = []
    
            # Reset the counter. 
            counter = 0
    
    return final_lt 


def date_others_dict(file_path): 
    
    '''Create a dictionary containing key: date, items: bitcoin price change (%), bitcoin price (usd), and consolidated combined text.'''

    # Find the max number of readlines of the file. 
    f_readline_counter = readline_counter(file_path) 
    
    # Segregate into date_lt and others_lt (bitcoin price change (%), bitcoin price (usd), and combined text.
    date_lt, others_lt = date_others_tp(f_readline_counter, file_path) 
    
    # Create a list of bitcoin price change (%), bitcoin price (usd)) and consolidated combined text.
    f_modified_others_lt = modified_others_lt(others_lt) 
    
    # Create a list of bitcoin price change (%), bitcoin price (usd), and consolidated combined text based on date.
    f_final_lt = final_lt(f_modified_others_lt)  
    
    # Create a dictionaryof key: date, items: bitcoin price change (%), bitcoin price (usd), and consolidated combined text.
    date_others_dict = dict(zip(date_lt, f_final_lt)) 
    
    return date_others_dict 

# ---------------------------------------------------------------------------------------------- 

def upp_low_pctl_tp(df, upper, lower):
    
    '''Create a tuple of upper and lower percentiles.'''
    
    # Record the chosen upper and lower percentiles from col of dataframe.
    upp_pctl, low_pctl = np.percentile(df['Bitcoin Price Percentage Change (%)'], [upper, lower])

    return upp_pctl, low_pctl


# ---------------------------------------------------------------------------------------------- 

# Subfunction of tkword_freq_pctchg_price_dict func. 
def convt_dict_to_text(date_others_dict, arb_date):
    
    '''Convert date_others_dict into text.'''
    
    # Join text_lt to create text based on the chosen date. 
    text_lt = date_others_dict[arb_date][2] 
    text = ''.join(text_lt) 
    
    return text 


# Subfunction of tkword_freq_pctchg_price_dict func. 
def clean_text(text):
    
    '''Remove hyperlinks, punctuations, numeric and special characters, and perform conversion to lowercasing on text.'''
    
    # Remove hyperlinks. 
    text = re.sub(r'https?:\/\/\S+', '', text)
    
    # Remove punctuations from text. 
    text = ''.join([char for char in text if char not in string.punctuation])
    
    # Remove numeric and special characters from text. 
    text = re.sub('[0-9]+','', text)
    
    # Convert text to lowercase.
    text = text.lower() 
    
    # Remove large spaces in between text.
    text = ' '.join(text.split())
             
    return text


# Subfunction of tkword_freq_pctchg_price_dict func.  
def remove_comm_dup_words(text, comm_words, dup_words_1, dup_words_2):
    
    '''Remove common and duplicate words from text and red.'''
    
    # Tokenized cleaned text. 
    word_tokens = nltk.word_tokenize(text) 
    
    # Convert tokenized words into text. 
    word_tokens = nltk.Text(word_tokens)  
    
    # Create set of stop_words to be removed from the word_tokens. 
    stop_words = set(stopwords.words('english') + list(comm_words) + list(dup_words_1) + list(dup_words_2)) 

    # Convert word_tokens into lower case if they are not part of stop_words. 
    words = [text.lower() for text in word_tokens if not text.lower() in stop_words] 
    
    return words 


# Subfunction of tkword_freq_pctchg_price_dict func.  
def convt_str_to_float(tkword_freq_pctchg_price_dict): 
    
    '''Convert str type to float type within the items of the dictionary.'''

    new_tkword_freq_pctchg_price_dict = {} 

    # Iterate over tkword_freq_pctchg_price_dict.  
    for key, items in tkword_freq_pctchg_price_dict.items():

        items_lt = []

        # Iterate over items to convert those str type to float type. 
        for i in items:

            # Convert str type to float type.
            if type(i) == str:
                items_lt.append(float(i))

            # Append all the other types. 
            else:
                items_lt.append(i)

        # Add items_lt into new_tkword_freq_pctchg_price_dict. 
        new_tkword_freq_pctchg_price_dict[key] = items_lt
        
    return new_tkword_freq_pctchg_price_dict


# Subfunction of tkword_freq_pctchg_price_dict func.  
def ordered_kword_freq_dict(words, char_len, word_freq):
    
    '''Key words ordered in descending frequency.'''
    
    # Find the frequency for the words. 
    freq = nltk.FreqDist(words) 
    vocabl = freq.keys() 
    
    # Create a dictionary to record word and its frequency.
    word_freq_dict = {i: freq[i] for i in list(freq)}
    
    # Sort text based on character length and frequency occurred. 
    kword_lt = [w for w in vocabl if len(w) >= char_len and freq[w] > word_freq]
    
    # Create a dictionary to record the chosen word and its frequency.
    kword_freq_dict = {i: word_freq_dict[i] for i in kword_lt}
    
    key_lt = []
    value_lt = []
    
    # Sort based on frequency in descending order.
    for key, value in word_freq_dict.items():
        
        # Append those keys found within kword_freq_dict into key_lt and value_lt. 
        try: 
            if kword_freq_dict[key]:
                key_lt.append(key)
                value_lt.append(value)
        
        # Pass those keys not found within kword_freq_dict. 
        except:
            pass
    
    # Returned a dictionary with ordered frequency. 
    return dict(zip(key_lt, value_lt))


def tkword_freq_pctchg_price_dict(date_others_dict, arb_date, char_len, word_freq, top_kw, comm_words, dup_words_1, dup_words_2): 
    
    '''Create dictionary for top keywords based on frequency in descending order for that particular day.'''
    
    tkword_freq_pctchg_price_dict = {} 
    
    # Join text_lt to create text.  
    text = convt_dict_to_text(date_others_dict, arb_date)
    
    # Remove hyperlinks, punctuations, numeric and special characters, and conversion to lowercasing. 
    ctext = clean_text(text)
    
    # Remove common and duplicate words using stopwords and selected words. 
    words = remove_comm_dup_words(ctext, comm_words, dup_words_1, dup_words_2) 
    
    # Dictionary created based on keyword's frequency ordered in descending order. 
    kword_freq_dict = ordered_kword_freq_dict(words, char_len, word_freq) 
    
    # Create a dictionary based on the top key words based on keyword's frequency ordered in descending order. 
    tkword_freq_dict = {i: kword_freq_dict[i] for i in list(kword_freq_dict)[:top_kw]} 
    
    # For loop to create a tkword_freq_pctchg_price_dict with key: keyword, items: frequency, bitcoin price change (%), bitcoin price (usd). 
    for tkword, freq in tkword_freq_dict.items():    
        tkword_freq_pctchg_price_dict[tkword] = [freq, date_others_dict[arb_date][0],  date_others_dict[arb_date][1]] 
    
    # Convert items in str type to float type for items in tkword_freq_pctchg_price_dict. 
    new_tkword_freq_pctchg_price_dict = convt_str_to_float(tkword_freq_pctchg_price_dict)
    
    return new_tkword_freq_pctchg_price_dict

# ----------------------------------------------------------------------------------------------

def upp_low_mid_pctl_tp(date_others_dict, char_len, word_freq, top_kw, low_pctl, upp_pctl, comm_words, dup_words_1, dup_words_2): 
    
    '''Create a tuple segregating into lists of dictionaries of key: top keyword, items: frequency, bitcoin price change (%), bitcoin price (usd) based on the customized upper, lower and middle percentile.'''
    
    upp_pctl_lt = [] 
    low_pctl_lt = [] 
    mid_pctl_lt = []
    
    # Iterate over date_others_dic.
    for i, j in date_others_dict.items():

        # Set arb_date using i.
        arb_date = i 

        # Sort for the customerized upper percentile. Note: Customized upper percentile might not equate to 75 percentile. 
        if float(j[0]) >= upp_pctl:
            upp_pctl_lt.append(tkword_freq_pctchg_price_dict(date_others_dict, arb_date, char_len, word_freq, top_kw, comm_words, dup_words_1, dup_words_2))

        # Sort for the customerized lower percentile. Note: Customized lower percentile might not equate to 25 percentile. 
        elif float(j[0]) <= low_pctl:
            low_pctl_lt.append(tkword_freq_pctchg_price_dict(date_others_dict, arb_date, char_len, word_freq, top_kw, comm_words, dup_words_1, dup_words_2))

        # Sort for the customized middle percentile.  
        else:
            mid_pctl_lt.append(tkword_freq_pctchg_price_dict(date_others_dict, arb_date, char_len, word_freq, top_kw, comm_words, dup_words_1, dup_words_2))
            
    return upp_pctl_lt, low_pctl_lt, mid_pctl_lt

# ---------------------------------------------------------------------------------------------- 

# Subfunction of key_sum_mean_median_freq_pctchg_price_tp func. 
def tkword_lt(pctl_lt):
    
    '''Create a list of top keywords of the selected percentile. Top keywords are based on the selected dates.'''

    tkword_lt = []
 
    # Iterate over the percentile list that is filled with dictionaries of key: top keyword, items: frequency, bitcoin price change (%), bitcoin price (usd).
    for i in pctl_lt:

        # Iterate over the keywords.
        for j in i.keys(): 

            # Pass if the keyword is already inside tkword_lt. 
            if j in tkword_lt:
                pass

            # Append keyword into kword_lt if it not inside tkword_lt. 
            else:
                tkword_lt.append(j)
                
    return tkword_lt


# Subfunction of key_sum_mean_median_freq_pctchg_price_tp func. 
def grp_tkword_freq_pctchg_price_dict(pctl_lt, tkword_lt): 
    
    '''Create a dictionary with key: top keywords of the day, items: occurred frequency, bitcoin price change (%), bitcoin price (usd) within the percentile.'''

    grp_tkword_freq_pctchg_price_dict = {}
    
    # Iterate over top keyword list. 
    for i in tkword_lt:

        combine_lt = []

        # Iterate over the percentile list that is filled with dictionaries of key: top keyword, items: frequency, bitcoin price change (%), bitcoin price (usd).
        for j in pctl_lt:
            for k, l in j.items(): 

                # Append to combine_lt if the top keyword matches so that frequency, bitcoin price change (%), bitcoin price (usd) will be grouped together.
                if i == k:
                    combine_lt.append(l)

        # Add the combine_lt into grp_tkword_freq_pctchg_price_dict with the key word being top keyword.
        grp_tkword_freq_pctchg_price_dict[i] = combine_lt
        
    return grp_tkword_freq_pctchg_price_dict 


# Subfunction of key_sum_mean_median_freq_pctchg_price_tp func. 
def srt_tkword_freq_pctchg_price_dict(grp_tkword_freq_pctchg_price_dict): 
    
    '''Create a dictionary with key: top keywords of the day, items: list sorted based on frequency, bitcoin price change (%), bitcoin price (usd) within the percentile.'''

    kword_lt = [] 
    items_lt = []

    for key, items in grp_tkword_freq_pctchg_price_dict.items():

        # Append key into kword_tl. 
        kword_lt.append(key)

        freq_lt = []
        pctchg_lt = []
        price_lt = []

        # Append frequency, bitcoin price change (%), bitcoin price (usd) into their respective lists.
        for i in items: 
            freq_lt.append(i[0])
            pctchg_lt.append(i[1])
            price_lt.append(i[2])

        # Group frequency, bitcoin price change (%), bitcoin price (usd) together by appending into items_lt. 
        items_lt.append([freq_lt, pctchg_lt, price_lt])
    
    # Create a dictionary with key: top keywords of the day, items: list sorted based on frequency, bitcoin price change (%), bitcoin price (usd) within the percentile.
    srt_tkword_freq_pctchg_price_dict = dict(zip(kword_lt, items_lt))
    
    return srt_tkword_freq_pctchg_price_dict 


# Subfunction of freq_pctchg_price_df func. 
def key_sum_mean_median_freq_pctchg_price_tp(pctl_lt):
    
    '''Create a tuple with lists of key, sum_freq, sum_pctchg, sum_price, median_freq_lt, median_pctchg_lt, median_price_lt.'''
    
    key_lt = []
    sum_freq_lt = []
    sum_pctchg_lt = []
    sum_price_lt = [] 
    median_freq_lt = [] 
    median_pctchg_lt = []
    median_price_lt = [] 
    
    # Create a list of top keyword of the various dates within the chosen percentile.
    f_tkword_lt = tkword_lt(pctl_lt) 
    
    # Create a dictionary with key: top keywords, items: list of all the occurred frequency, bitcoin price change (%), bitcoin price (usd) within the percentile.
    f_grp_tkword_freq_pctchg_price_dict = grp_tkword_freq_pctchg_price_dict(pctl_lt, f_tkword_lt) 
    
    # Create a dictionary with key: top keywords, items: list sorted based on frequency, bitcoin price change (%), bitcoin price (usd) within the percentile.
    srt_dict = srt_tkword_freq_pctchg_price_dict(f_grp_tkword_freq_pctchg_price_dict)
    
    for key, items in srt_dict.items():
    
        # Append top keyword into key_lt. 
        key_lt.append(key)
        
        for i, j in enumerate(items):

            # Append sum and mean of frequencies into sum_freq_lt and median_lt respectively.
            if i == 0:
                sum_freq_lt.append(round(sum(j),2))
                median_freq_lt.append(round(np.median(j),2))

            # Append sum and mean of bitcoin percentage change into sum_pctchg_lt and median_lt respectively.
            if i == 1:
                sum_pctchg_lt.append(round(sum(j),2))
                median_pctchg_lt.append(round(np.median(j),2)) 

            # Append sum and mean of bitcoin price into sum_price_lt and median_lt respectively.
            if i == 2:
                sum_price_lt.append(round(sum(j),2)) 
                median_price_lt.append(round(np.median(j),2))
    
    return key_lt, sum_freq_lt, sum_pctchg_lt, sum_price_lt, median_freq_lt, median_pctchg_lt, median_price_lt 


# Subfunction of srt_freq_pctchg_price_df func. 
def freq_pctchg_price_df(pctl_lt):
    
    '''Create dataframe with columns: Top Keyword, Frequency (Sum), Frequency (Median), Bitcoin Percentage Change (%) (Sum), Bitcoin Percentage Change (%) (Median), Bitcoin Price (USD) (Sum), Bitcoin Price (USD) (Median).'''
    
    # Create the respective lists to create the dataframe. 
    key_lt, sum_freq_lt, sum_pctchg_lt, sum_price_lt, median_freq_lt, median_pctchg_lt, median_price_lt = key_sum_mean_median_freq_pctchg_price_tp(pctl_lt)
    
    # Create a dataframe with top keyword and frequency. 
    df = pd.DataFrame(sum_freq_lt, key_lt) 
    
    # Reset index of dataframe. 
    df.reset_index(inplace=True)
    
    # Rename columns dataframe. 
    df.rename(columns={df.columns[0]: 'Top Keyword', df.columns[1]:'Frequency (Sum)'}, inplace=True)
    
    # Create columns within the dataframe using the respective lists. 
    df['Frequency (Median)'] = median_freq_lt 
    df['Bitcoin Percentage Change (%) (Sum)'] = sum_pctchg_lt
    df['Bitcoin Percentage Change (%) (Median)'] = median_pctchg_lt
    df['Bitcoin Price (USD) (Sum)'] = sum_price_lt 
    df['Bitcoin Price (USD) (Median)'] = median_price_lt

    return df 


def srt_freq_pctchg_price_df(pctl_lt, col):
    
    '''Create a dataframe sorted based on the top values of the selected column.'''
    
    # Create dataframe with columns: Top Keyword, Frequency (Sum), Frequency (Median), Bitcoin Percentage Change (%) (Sum), Bitcoin Percentage Change (%) (Median), Bitcoin Price (USD) (Sum), Bitcoin Price (USD) (Median)
    df = freq_pctchg_price_df(pctl_lt)
    
    # Segregate based on column name. 
    if col == 'Frequency (Sum)':
        
        # Sort the dataframe based on selected column in descending order.
        df.sort_values(by=[col, 'Bitcoin Percentage Change (%) (Sum)'], ascending=False, inplace=True)
    
    if col == 'Frequency (Median)': 
        
        # Sort the dataframe based on selected column in descending order. 
        df.sort_values(by=[col, 'Bitcoin Percentage Change (%) (Median)'], ascending=False, inplace=True) 
    
    # Reset index dataframe. 
    df.reset_index(inplace=True)
    
    # Drop 'index' column from dataframe.
    df.drop(columns=['index'], inplace =True)
    
    return df 

# ---------------------------------------------------------------------------------------------- 

# Subfunction of comm_words_set func. 
def comm_tkword_lt(upp_tkword_lt, low_tkword_lt):
    
    '''Create a list of common top keywords of the day from lower and upper customized top keyword percentile lists.'''
    
    comm_tkword_lt= [] 
    
    # Iterate over upper customized top keyword percentile list.
    for i in upp_tkword_lt:
        
        # Iterate over lower customized top keyword percentile list.
        for j in low_tkword_lt:
            
            # Append top keyword to comm_tkword_lt when top keyword matches between lower and upper customized top keyword percentile lists.
            if i == j:
                comm_tkword_lt.append(i)
                
    return comm_tkword_lt 


def comm_words_set(upp_pctl_lt, low_pctl_lt):
    
    '''Create a set of common words between customized upper and lower percentile.'''
    
    # Find duplicate words to be removed from text. 
    # Create a list of lower customized percentile top keywords.
    low_tkword_lt = tkword_lt(low_pctl_lt) 

    # Create a list of upper customized percentile top keywords.
    upp_tkword_lt = tkword_lt(upp_pctl_lt)

    # Redudant words to be removed are common top keywords between lower and upper customized percentile top keywords.
    comm_words_set = set(comm_tkword_lt(upp_tkword_lt, low_tkword_lt))

    return comm_words_set

# ---------------------------------------------------------------------------------------------- 

def print_rmv_words(wtype, rmv_words):
    
    '''Print words to be removed.'''
    
    # No word to be removed. 
    if len(rmv_words) == 0:
        print('\033[1m' + 'No word to be removed.' + '\033[0m') 
    
    # 1 word to be removed. 
    elif len(rmv_words) == 1:
        print('\033[1m' + str(len(rmv_words)) + ' '  + str(wtype) + ' word to be removed:' + '\033[0m')
    
    # >1 word to be removed.
    elif len(rmv_words) > 1:
        print('\033[1m' + str(len(rmv_words)) + ' '  + str(wtype) + ' words to be removed:' + '\033[0m')
    
    # Print out the words to be removed. 
    for i in rmv_words:
        print(i)

# ---------------------------------------------------------------------------------------------- 

# Subfunction of tkw10_dup_words_set func.  
def sort_tkw10_lt(pctl_lt, col): 
    
    '''Create a top 10 keyword list of the respective chosen percentile.'''
    
    # Create dataframe based on top keyword, frequency, bitcoin precentage change (%) and their respective calculations.
    df = freq_pctchg_price_df(pctl_lt)
    
    # Sort values based on the column chosen. 
    df.sort_values(by=col, ascending=False, inplace=True)
    
    # Create a dataframe for only the top 10 keywords in the dataframe. 
    df = df.nlargest(10, col) 
    
    tkword_lt = [] 
    
    # Append the top 10 keywords into tkwords_lt. 
    for i in df['Top Keyword']:
        tkword_lt.append(i)
    
    return tkword_lt 


def tkw10_dup_words_set(upp_pctl_lt, low_pctl_lt, col):
    
    '''Create a set of duplicate words after comparing the top 10 keywords of customized upper and lower percentiles.'''
    
    # Create lists of top 10 keywords for customized upper and lower percentiles respectively.
    upp10_tkword_lt = sort_tkw10_lt(upp_pctl_lt, col)
    low10_tkword_lt = sort_tkw10_lt(low_pctl_lt, col) 
    
    # Create a set of common top keywords among the customized upper and lower percentiles. 
    dup_words_set = set(comm_tkword_lt(upp10_tkword_lt, low10_tkword_lt))
    
    return dup_words_set 


# ---------------------------------------------------------------------------------------------- 

def comm_words_lt(arr_1, arr_2):
    
    '''List of common words.'''
    
    comm_lt = []
    
    # Iterate over arr_1.
    for i in arr_1:
        
        # Iterate over arr_2.
        for j in arr_2:
            
            # Append common words into comm_lt.  
            if (i == j) and (i not in comm_lt):
                comm_lt.append(i)
                
    return comm_lt 


def print_comm_words(comm_words):
    
    '''Print common words.'''
    
    # No common word. 
    if len(comm_words) == 0:
        print('\033[1m' + 'No common word.' + '\033[0m')
    
    # 1 common word. 
    elif len(comm_words) == 1:
        print('\033[1m' + str(len(comm_words)) + ' common word:' + '\033[0m')
    
    # >1 common words. 
    elif len(comm_words) > 1:
        print('\033[1m' + str(len(comm_words)) + ' common words:' + '\033[0m')
    
    # Print out the common words. 
    for i in comm_words:
        print(i) 


def fred_btc_fedbsdf(df_1, df_2):
    
    '''Create a dataframe from Fed based on Bitcoin Price (USD) and Federal Reserve Balance Sheet (Millions of USD).'''
    
    # Reset dataframes. 
    df_1.reset_index(inplace=True)
    df_2.reset_index(inplace=True)
    
    # Merge dataframes into one. 
    df = df_1.merge(df_2, on='DATE', how='left')
    
    # Rename dataframe. 
    df.rename(columns={df.columns[0]: 'Date', df.columns[1]: 'Bitcoin Price (USD)', df.columns[2]: 'Federal Reserve Balance Sheet (Millions of USD)'}, inplace=True)

    return df


