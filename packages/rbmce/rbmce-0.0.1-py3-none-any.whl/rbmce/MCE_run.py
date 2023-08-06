
#### this is an eample workflow I used to run rbcm_annotate

import pandas as pd
import os
import numpy as np

import pathlib
import re
import sys, warnings
#import xlrd
from datetime import date

from microbio_parser import *
import time  


from parameters import *



### todo:
## make a more appropriate run function
## figure out how to best setup data inport/export?

def save_annotated_df(annotated_df, df_name, save_directory, specified_date):
    """saves workflow output (dataframe) with annotations, species captures, and infection status estimation as a pkl file. note pkl was chosen>csv to preserve datastructure formatting."""
#     specified_date=today.strftime("%d/%m/%Y") ##uncomment to save annotated df w/ todays date in filename
    
    save_directory=os.path.join(data_path,'annotated_data','{}_{}.pkl'.format(specified_date, df_name))
    print('saving annotated df ({}) to {}'.format(df_name, save_directory))
    annotated_df.to_pickle(save_directory)
    


def latex_report(annotated_df, df_name, save_directory, specified_date, n_latex_rows):
    """uses functions in latex_report.py to save a summary report from workflow in latex format (as a .txt file) """
    from latex_report import *

    latex_filename=specified_date+'_'+df_name+'_latex_report'
    latex_filepath=os.path.join(data_path,'latex_reports',latex_filename)
    print('saving latex report to {}'.format(latex_filename))
    write_latex_report(latex_filepath, annotated_df, df_name, capture_table_len=n_latex_rows)
    
    
    
# def run_CME()



def run_acute():
    print('####### --------NOTES_ACUTE-------- #######')
    ############# acute and ss23:
    
    df=preprocess_acute(output_path, data_path)
    
    tic = time.perf_counter()
    print('####### Extracting & Categorizing Parsed Row Via Regex Blocks #######')
    annotated_df= result_categorize_main(df, 
                                           text_col_main='parsed_note',
                                           staph_nunique_col='procedure_order_key',
                                           result_col_main='result_binary',
                                           culture_id_main='visit_id',
                                         visit_id='visit_id', #this should be changed if there are multiple cultures per visit.
                                           staph_neg_correction=False 
                                        , notetype_main='parent_note_type',
                                          likely_neg_to_neg_override=True) 
    
    toc = time.perf_counter()
    print(f"notes_acute result_categorize_main time: {toc - tic:0.4f} seconds, len: {len(annotated_df)}")  
    
    
    df_name='acute'
    save_annotated_df(df_name, annotated_df)
    latex_report(df_name, annotated_df,n_latex_rows )
    
        
    
def main():
    print('####### Program Started #######')
    print(pd.__version__)
    print('saving files with date: {}'.format(specified_date))

    #creating an annotated_data and latex report folder for the outputs to be stored. 
    if not os.path.exists(os.path.join(data_path,'annotated_data')):
        os.makedirs(os.path.join(data_path,'annotated_data'))
        
    if not os.path.exists(os.path.join(data_path,'latex_reports')):
        os.makedirs(os.path.join(data_path,'latex_reports'))
    
    
    run_ss23()
    
    print('####### Program Finished #######')
    
    
    
    ####hmmmm how do i best allow users to run from cmd. 
    
if __name__ == "__main__":
    print('####### Program Started #######')
    print(pd.__version__)
    print('saving files with date: {}'.format(specified_date))

    #creating an annotated_data and latex report folder for the outputs to be stored. 
    if not os.path.exists(os.path.join(data_path,'annotated_data')):
        os.makedirs(os.path.join(data_path,'annotated_data'))
        
    if not os.path.exists(os.path.join(data_path,'latex_reports')):
        os.makedirs(os.path.join(data_path,'latex_reports'))    