#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 16:28:00 2022

@author: nelsonng
"""

# Import libraries. 
import matplotlib.pyplot as plt
import missingno as msno 
import seaborn as sns 

from datetime import date
from wordcloud import WordCloud 

# Import my packages. 
import my_Functions_btc_wrangle as myfbtc_wra

# ----------------------------------------------------------------------------------------------

def set_rcparams(): 
    
    '''Set rcParams setting for graph layout.'''
    
    # Reset layout to default. 
    plt.rcdefaults()  
    
    # Set rcParams settings.
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = 'Times New Roman' 
    plt.rcParams['figure.dpi'] = 600
    plt.rcParams['savefig.dpi'] = 600 

   
def set_sns_font_dpi(): 
    
    '''Set sns.setting for graph font and dpi.'''
    
    # Reset layout to default. 
    plt.rcdefaults() 
     
    # Set sns.set settings. 
    sns.set_style({'font.serif':'Times New Roman'}) 
    sns.set(rc = {"figure.dpi":600, 'savefig.dpi':600}) # Improve dpi. 


def set_sns_large_white(): 
    
    '''Set sns.setting to create a graph with large and whitegrid.'''
    
    # Reset layout to default. 
    plt.rcdefaults()  

    # Set style to times new roman.
    sns.set(rc = {'figure.figsize':(15, 10)}) # width x height. 
    sns.set_style('whitegrid') # Set background. 


def null_barchart(df, df_txt):

    '''Display bar chart to identify missing null values.'''
    
    # Reset layout to default. 
    set_rcparams() 
    
    # Set figure layout.  
    plt.subplots(figsize=(15, 6)) # width x height 
    
    # Plot bar chart. 
    df.isna().sum().plot(kind="bar", color='red')
    
    # Title of the bar chart. 
    plt.title('Bar Chart of Null values\n(' + str(df_txt) + ')', size=20)  
    
    # Display the bar chart. 
    plt.show() 


def null_heatmap(df, df_txt, fig_wid, fig_ht, ttl_siz):
    
    '''Display heatmap to identify missing null values.'''
    
    # Set graph layout. 
    set_rcparams() 
    
    # Set figure layout.  
    plt.subplots(figsize=(fig_wid, fig_ht)) # width x height
    
    # Colors for heatmap. 
    colours = ['springgreen', 'red'] # springgrean is non-null, red is null. 
    
    # Plot the heatmap. 
    cols = df.columns  
    g = sns.heatmap(df[cols].isnull(), cmap=sns.color_palette(colours), cbar_kws={'label': 'Red=Null, Green=Non-Null', 'orientation': 'vertical'})
    
    # Set title for the heatmap. 
    g.set_title('Heatmap of Non-null and Null Values\n(' + str(df_txt) + ')', size=ttl_siz)
    
    # Display the heatmap. 
    plt.show() 


def sorted_null_msno(df, df_txt, col, ttl_siz):
    
    '''Display null values sorted based on column.'''
    
    # Sort values based on selected column.
    sorted_df = df.sort_values(by = col)
    
    # Plot msno.matrix. 
    g = msno.matrix(sorted_df) 
    
    # Set title for the missingno. 
    g.set_title('Missingno of Non-null and Null Values Sorted By ' + col + '\n(' + str(df_txt) + ')', size=ttl_siz)
    
    # Display msno.matrix.
    plt.show()

# ----------------------------------------------------------------------------------------------

# Subfunction of scatterplot func, histplot func and word_cloud func. 
def dt_str_fmt(dt_str):
    
    '''Rearrange datetime str format.'''
    
    # Convert datetime str format to datetime. 
    dt_str = myfbtc_wra.cnvt_dt_str_to_datetime(dt_str) 
    
    # Convert datetime back to a new str format. 
    dt_str_fmt = dt_str.strftime("%d %B, %Y")
     
    return dt_str_fmt 


def scatterplot(df, col, start_date, end_date):
    
    '''Plot scatter plot.'''
    
    # Set graph layout. 
    set_rcparams()

    # Set figure layout.  
    plt.subplots(figsize=(15, 6)) # width x height 

    # Plot scatterplot.
    sns.scatterplot(data=df[col])

    # Convert date from datetime format to an arranged str format. 
    start_date_fmt = dt_str_fmt(start_date)
    end_date_fmt = dt_str_fmt(end_date)   

    # Title of the bar chart. 
    plt.title(str(col) + '\n(' + str(start_date_fmt) + ' - ' + str(end_date_fmt) + ')', size=20)  

    # Rotate the xticks to 90 degree.
    plt.xticks(rotation = 90)

    # Display plot. 
    plt.show() 


def histplot(df, col, bins, start_date, end_date):
    
    '''Plot histogram.'''
    
    # Set graph layout. 
    set_rcparams()
    
    # Find min and max values of the selected dataframe column.
    min_val = df[col].min()
    max_val = df[col].max()

    bins_lt = []
    
    # Create a list of bin values for sns.displot.
    for i in range(bins+1):
        bin_val = min_val + i*(max_val - min_val)/bins
        bins_lt.append(bin_val)

    # Set figure layout.  
    plt.subplots(figsize=(15, 6)) # width x height 

    sns.distplot(a=df[col], hist=True, 
                 kde=False, bins=bins_lt, 
                 hist_kws={'histtype': 'step', 
                           'linewidth': 1.5, 
                           'color': 'red'})
    
    # Convert date from datetime format to an arranged str format. 
    start_date_fmt = dt_str_fmt(start_date) 
    end_date_fmt = dt_str_fmt(end_date)  
    
    # Title of the bar chart. 
    plt.title(str(col) + '\n(' + str(start_date_fmt) + ' - ' + str(end_date_fmt) + ')', size=20)  

    # Display the bar chart. 
    plt.show() 


def word_cloud(df, col, pctl_cat, upper, lower, start_date, end_date):
    
    '''Create word cloud. '''
    
    # Set figure layout.
    set_rcparams() 
    plt.figure(figsize=(15, 6)) 
    
    # Perform deep copy.
    df = df.copy(deep=True)
    
    # Set index to 'Top Keyword'. 
    df.set_index('Top Keyword', inplace=True)
    
    # Variables for creating word cloud.
    tot_frq = df[col].sum()
    max_words = 100
    
    word_string = ''
    
    for i in df.index.values:
        if i.count(' ') == 0:
            
            # Create the magnitude of the word size, as max_words is the total number of keywords abled to be displayed on the wordcloud. 
            repeat_num_times = int(df.loc[i, col] / tot_frq * max_words)
            
            # Duplicate i in repeat_num_times. 
            word_string = word_string + ((i + ' ') * repeat_num_times)
    
    # Create the word cloud. 
    wordcloud = WordCloud(background_color='white', 
                          width=800, height=400).generate(word_string)
    plt.imshow(wordcloud, interpolation='bilinear')
    
    # Convert date from datetime format to an arranged str format. 
    start_date_fmt = dt_str_fmt(start_date)
    end_date_fmt = dt_str_fmt(end_date) 
    
    # Set x and y.
    x = 'Top Keyword' 
    
    # Set pctl_cat_txt.
    if pctl_cat == 'lower':
        pctl_cat_txt = str(lower) + ' percentile of ' + x + ': '
    elif pctl_cat == 'upper':
        pctl_cat_txt = str(upper) + ' percentile of ' + x + ': '
    
    # Set title. 
    title_strt = 'Top Keyword of ' + col 
    title_end = '(' + pctl_cat_txt + start_date_fmt + ' to ' + end_date_fmt + ')'  
    title_txt = title_strt + '\n' + title_end 
    plt.title(title_txt, size=20, y=1)
    
    # Shrink the size of the border. 
    plt.tight_layout(pad=0)
    
    # Switch off plt.axis. 
    plt.axis('off')
    
    # Display word cloud.
    plt.show()  

# ----------------------------------------------------------------------------------------------

def freq_pctchg_scatterplots(df, x, y, no_tkword, pctl_cat, upper, lower, start_date, end_date):
    
    '''Plot scatter plots based on Bitcoin Percentage Change (%) and Frequency.'''
    
    # Create a deepcopy of the dataframe. 
    df = df.copy(deep=True)
    
    # Slice the dataframe based on the number of top keywords. 
    df = df[:no_tkword]
    
    # Set graph layout.  
    set_rcparams() 
    
    # Set hue_1 and hue_2. 
    # Set hue_1. 
    hue_1 = 'Top Keyword'
    
    # Set hue_2.
    if x == 'Frequency (Sum)' and y == 'Bitcoin Percentage Change (%) (Sum)':
        hue_2 = 'Bitcoin Price (USD) (Sum)'

    if x == 'Frequency (Median)' and y == 'Bitcoin Percentage Change (%) (Median)':
        hue_2 = 'Bitcoin Price (USD) (Median)'

    # Combine Graphes 1 and 2.
    fig, ax = plt.subplots(2, 1, figsize=(15,12)) # width x height. 
    g_1 = sns.scatterplot(data=df, x=x, y=y, hue=hue_1, ax=ax[0])
    g_2 = sns.scatterplot(data=df, x=x, y=y, hue=hue_2, ax=ax[1])
    
    # Set hue_1_txt and hue_2_txt.
    hue_1_txt = 'Top ' + str(no_tkword) + ' Keywords'
    hue_2_txt = hue_1_txt
    
    # Set location for legend to be placed. 
    g_1.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), ncol=2, title=hue_1_txt)
    g_2.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), ncol=2, title=hue_2_txt)
    
    # Convert date from datetime format to an arranged str format. 
    start_date_fmt = dt_str_fmt(start_date)
    end_date_fmt = dt_str_fmt(end_date)  
    
    # Set pctl_cat_txt.
    if pctl_cat == 'lower':
        pctl_cat_txt = str(lower) + ' percentile of ' + x + ': '
    elif pctl_cat == 'upper':
        pctl_cat_txt = str(upper) + ' percentile of ' + x + ': '
    
    # Set title. 
    title_strt = y + ' VS ' + x
    title_end = pctl_cat_txt + start_date_fmt + ' to ' + end_date_fmt + ')' 

    title_1 = title_strt + '\n(' + hue_1_txt + ')\n(' + title_end
    title_2 = title_strt + '\n(' + hue_2_txt + ')\n(' + title_end
       
    # Set title_size.
    title_size = 20
    
    # Set title. 
    ax[0].set_title(title_1, size=title_size)
    ax[1].set_title(title_2, size=title_size)
    
    # Set proper spacing among graphs.  
    plt.tight_layout()
    
    # Display figures. 
    plt.show()  


def tkword_barplot(df, col, no_tkword, pctl_cat, upper, lower, start_date, end_date):
    
    '''Plot barplot for top keywords.'''
    
    # Create deepcopy for the dataframe.
    df = df.copy(deep=True)
    
    # Slice the dataframe to the respective no_tkword value. 
    df = df[:no_tkword]
    
    # Set graph layout. 
    set_rcparams() 
    plt.figure(figsize=(15, 6))
    
    # Set x and y.
    x = 'Top Keyword'
    y = col 
    
    # Plot barplot. 
    g = sns.barplot(data=df, x=x, y=y) 
    
    # Convert date from datetime format to an arranged str format. 
    start_date_fmt = dt_str_fmt(start_date)
    end_date_fmt = dt_str_fmt(end_date) 
    
    # Set pctl_cat_txt.
    if pctl_cat == 'lower':
        pctl_cat_txt = str(lower) + ' percentile of ' + x + ': '
    elif pctl_cat == 'upper':
        pctl_cat_txt = str(upper) + ' percentile of ' + x + ': '
    
    # Set title. 
    title_strt = y + ' VS ' + x
    title_end = pctl_cat_txt + start_date_fmt + ' to ' + end_date_fmt + ')'  
    title_txt = title_strt + '\n(' + 'Top ' + str(no_tkword) + ' Keywords' + ')\n(' + title_end

    # Set title.
    g.set_title(title_txt, size=20)

    # Rotate the xticks by 90 degrees. 
    plt.xticks(rotation=90)
    
    # Display graph. 
    plt.show() 


def fed_btc_graph(df, start_date, end_date):
    
    '''Plot a graph of Federal Reserve Balance Sheet \ Bitcoin Price.'''
    
    # Set graph layout. 
    set_sns_font_dpi()
    set_sns_large_white()

    # Custom_palette to set color for the lineplot. 
    custom_palette = sns.color_palette('tab10') 

    # Create the line plot for Federal Reserve Balance Sheet (Millions of USD).
    ax1 = sns.lineplot(data=df, y='Federal Reserve Balance Sheet (Millions of USD)', x='Date',
                       label='Federal Reserve Balance Sheet (Millions of USD)', 
                       legend=False, color=custom_palette[0])

    # Create an additional graph on the right. 
    ax2 = ax1.twinx()

    # Create the line plot for Bitcoin Price (USD).
    ax2 = sns.lineplot(data=df, y='Bitcoin Price (USD)', x='Date',
                       label='Bitcoin Price (USD)',
                       legend=False, color=custom_palette[1])

    # Create annotations. 
    text_1 = 'Bitcoin price started to collapse once the Federal Reserve did aggressive normalization of her balance sheet.'
    text_2 = 'Bitcoin price started to surge once the Federal Reserve expanded her balance sheet using large scale asset purchases.'
    text_3 = 'Grey shaded area: Bitcoin tweet text collection period'

    ax1.text(x=date(2017, 12, 30), y=5.25*10**6, s=text_1,  horizontalalignment='left', size=12, color=custom_palette[3]) 
    ax1.text(x=date(2020, 3, 28), y=3.8*10**6, s=text_2,  horizontalalignment='left', size=12, color=custom_palette[4]) 
    ax1.text(x=date(2021, 4, 20), y=4.8*10**6, s=text_3,  horizontalalignment='left', size=12, color='black') 

    # Create vertical lines. 
    ax1.axvline(x=date(2017, 12, 15), color=custom_palette[3], linestyle='--', alpha=0.8)
    ax1.axvline(x=date(2020, 3, 13), color=custom_palette[4], linestyle='--', alpha=0.8)

    # Convert end_date into tuple form of year, month and day.
    end_date_tp = myfbtc_wra.year_mth_day_tp(end_date)
    
    # Create shaded area. 
    plt.axvspan(start_date, end_date, color='grey', alpha=0.2) # Input start_date and end_date.  
    
    # Limit the x-axis. 
    plt.xlim([date(2017,7,1), date(end_date_tp[0],end_date_tp[1],end_date_tp[2])]) # Input end_date. 

    # Set title. 
    ax1.set_title('Federal Reserve Balance Sheet \ Bitcoin Price', size=20)

    # Display the legend outside the graph. 
    ax2.figure.legend()

    # Display the figure. 
    plt.show()
