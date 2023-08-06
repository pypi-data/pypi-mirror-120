
#### this is an eample workflow I used to run rbcm_annotate locally on my two training and two validation datasets. 

import pandas as pd
import os
import numpy as np

import pathlib
import re
import sys, warnings
#import xlrd
from datetime import date

from .rbmce import *
import time  


### note for users looking to use as template: when running locally, I added a parameters.py file with all my desired filepaths. 
### the variables in parameters specified: data_path(where raw csv files stored)
### code_path (where I wanted to save code)
### output_path (where I wanted to save outputs such as annotated dataframe (in pkl format) and the markdown summary file)
### specified_date (date i wanted appended onto front of filename)
### n_latex_rows (int, default=10): for latex summary, specifies the top n counts for each specified category. essentially higher # = more examples of each output.
# from .parameters import *



def save_annotated_df(annotated_df, df_name, save_directory, specified_date):
    """saves workflow output (dataframe) with annotations, species captures, and infection status estimation as a pkl file. note pkl was chosen>csv to preserve datastructure formatting."""
#     specified_date=today.strftime("%d/%m/%Y") ##uncomment to save annotated df w/ todays date in filename
    
    save_directory=os.path.join(data_path,'annotated_data','{}_{}.pkl'.format(specified_date, df_name))
    print('saving annotated df ({}) to {}'.format(df_name, save_directory))
    annotated_df.to_pickle(save_directory)
    


def latex_report(annotated_df, df_name, save_directory, specified_date, n_latex_rows):
    """uses functions in latex_report.py to save a summary report from workflow in latex format (as a .txt file) """
    from .latex_report import *

    latex_filename=specified_date+'_'+df_name+'_latex_report'
    latex_filepath=os.path.join(data_path,'latex_reports',latex_filename)
    print('saving latex report to {}'.format(latex_filename))
    write_latex_report(latex_filepath, annotated_df, df_name, capture_table_len=n_latex_rows)
    
    
    
def preprocess_training1(output_path, data_path):
    """
    a list of operations used to pre-process our training_set1 prior to running rbcme on it.
    """
    tic = time.perf_counter()

    training1_import= pd.read_csv(os.path.join(output_path,'<file_name>.csv'),
                         parse_dates=['created_datetime','updated_datetime']
                        )
    ##data cleaning: all files with the word "screen", aka a microorganism screening>culture, were dropped for our training set.
    screen_cpt_drop_acute= list(training1_import.loc[training1_import['cpt_label'].apply(lambda x: re.search(r'screen', str(x).lower())is not None),'cpt_label'].unique())
    training1_import2= training1_import.loc[~training1_import['cpt_label'].isin(screen_cpt_drop_acute),].copy()

    print('####### Parsing culture note text into rows (if specified) #######')
    ##data cleaning: reports in trainingset 1 were often amalgamations of many different report components (eg gram stain, antibiotic screening, microbio report)
    ## to improve performance of workflow, we use the rbcme.parse_rows() to split the rows into 1 or many different lines in the dataframe, all tied to the same culture_id
    notes_parsed=training1_import2.groupby('note_key')['note_text'].apply(lambda x: parse_rows(x)).reset_index().rename(columns={'note_text':'parsed_note', 'level_1':'parse#'})
    training1_merged=pd.merge(training1_import2,notes_parsed, left_on='note_key',right_on='note_key')
    ##merged just indicates that all 

    toc = time.perf_counter() 
    print(f"data import, parsing, and cleaning: {toc - tic:0.4f} seconds") #useful timing output. sometimes the parsing function can take 5-20 min for 500,000+notes.
    return(training1_merged)






def run_t1():
    print('####### --------Training_set_1-------- #######') 
    
    df=preprocess_training1(output_path, data_path) # hidden on github, but here is where I ran all 
    
    tic = time.perf_counter()
    print('####### Extracting & Categorizing Parsed Row Via Regex Blocks #######')

    annotated_df= rbcme.run(df, 
                            text_col_main='parsed_note',
                            culture_id_main='procedure_order_key',
                            visit_id_main='visit_id',
                            staph_neg_correction=False,
                            notetype_main='parent_note_type',
                            likely_neg_to_neg_override=True) 
    
    
    toc = time.perf_counter()
    print(f"training1 result_categorize_main time: {toc - tic:0.4f} seconds, len: {len(annotated_df)}")  
    
    df_name='acute'
    save_annotated_df(df_name, annotated_df)
    latex_report(df_name, annotated_df,n_latex_rows )
    
        
    annotated_df= rbmce.run(df,
                                       text_col_main='lab_result',
                                       staph_nunique_col='culture_id',
                                       result_col_main='result_binary',
#                                        culture_id_main='encid',
                                       culture_id_main='culture_id',
                                       visit_id='encid', #this should be changed if there are multiple cultures per visit.

                                       staph_neg_correction=False,
                                       notetype_main='proc_desc',
                                       quant_col='lab_result', specimen_col='proc_desc',
                                       likely_neg_to_neg_override=True)
        
        
    
def main():
    print('####### Program Started #######')
    print(pd.__version__) #included to ensure high enough pd version (>0.25) to support pd.explode() is present.
    print('saving files with date: {}'.format(specified_date))

    #creating an annotated_data and latex report folder for the outputs to be stored. 
    if not os.path.exists(os.path.join(data_path,'annotated_data')):
        os.makedirs(os.path.join(data_path,'annotated_data'))
        
    if not os.path.exists(os.path.join(data_path,'latex_reports')):
        os.makedirs(os.path.join(data_path,'latex_reports'))
    
    run_t1()
    
    print('####### Program Finished #######')
    
    
        
if __name__ == "__main__":
    print('####### Program Started #######')
    print(pd.__version__)
    print('saving files with date: {}'.format(specified_date))

    #creating an annotated_data and latex report folder for the outputs to be stored. 
    if not os.path.exists(os.path.join(data_path,'annotated_data')):
        os.makedirs(os.path.join(data_path,'annotated_data'))
        
    if not os.path.exists(os.path.join(data_path,'latex_reports')):
        os.makedirs(os.path.join(data_path,'latex_reports'))    