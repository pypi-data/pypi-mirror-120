
import os
import numpy as np

import pathlib
import re
import sys, warnings
#import xlrd
from datetime import date

from .rbmce import *    
from .regex_blocks import species_regex_list
import pandas as pd
pd.set_option('display.max_colwidth', None)
import time

data_path='/share/fsmresfiles/gje1631/infection'
code_path='/home/gje1631/nmedw_py'
output_path= os.path.join(data_path, 'amalgam')
data_path= os.path.join(data_path, 'Nelson_files')

specified_date= '22_11_2021'
n_latex_rows=10




      

def descriptive_df(df, text_col_main,staph_nunique_col,result_col_main,
           culture_id_main,notetype_main,df_name):
    """
    makes a dataframe to present descriptive statistics of the parsing. 
    """
#     pd.options.display.max_rows
#     pd.set_option('display.max_colwidth', None)
    pd.options.display.max_rows
#     pd.set_option('display.max_colwidth', -1)
    pd.set_option('display.max_colwidth', 999)

    n_notes=int
    if 'note_key' in list(df):
        n_notes=df['note_key'].nunique()
    else:
        n_notes=np.nan
    
    dict1={r"n notekeys (can be $\geq$ n culture if parsed notes)":[n_notes],
        r"n cultures (can be many:visit)": [df[staph_nunique_col].nunique()],
        r"n visits":[df[culture_id_main].nunique()],
        r"n rows": [len(df)],
        r"n rows not parsed":[len(df[df['result_binary']=='not_captured'])]
        }
    return(pd.DataFrame.from_dict(dict1, orient='index', columns=[df_name]))



def describe_classification_latex(df,n, df_name,file_name,
                            text_col_main='parsed_note',
                            staph_nunique_col='procedure_order_key',
                            result_col_main='result_binary',
                            culture_id_main='visit_id',
                            notetype_main='parent_note_type',
                           ):
    
    """
    function to help standardize the desired outputs from the first non-aggregated result classification. writes latex output to a .txt file. 
    
    """
    pd.options.display.max_rows
#     pd.set_option('display.max_colwidth', -1)
    pd.set_option('display.max_colwidth', 999)
    
    f=open(os.path.join(output_path,'{}.txt'.format(file_name)),'a')   
    
    f.write('%############################')
    f.write('\n')
    
    df_title=str('\section{'+df_name+'}')
    f.write(df_title)
    f.write('\n')
    
    desc_df= descriptive_df(df, text_col_main,staph_nunique_col,result_col_main,
           culture_id_main,notetype_main,df_name)
    df_len=len(df)
    
    
    caption_str="Descriptive Statistics:"
    latex_out=desc_df.to_latex(#caption=caption_str,
                               escape=False#, longtable=True
                                )

    caption_str='{'+caption_str+'}'
    latex_out=latex_out.replace('\\begin{tabular}{lr}\n',
                            '\\begin{table}[H]\n\\centering\n\\caption'+caption_str+'\n\\begin{tabular}{lr}\n'
                           )
    latex_out=latex_out.replace('\\end{tabular}\n',
                            '\\end{tabular}\n\\end{table}\n'#.format(caption_str)
                           )

    f.write(latex_out)
    f.write('\n')
    
    caption_str= "top {} result binary2 (less granular than result binary1) distribution: (n unique: {}; n tot {}; \% of total {:.2f})".format(
                n,
                df['result_binary2'].nunique(),
                sum(df['result_binary2'].value_counts()),
                sum(df['result_binary2'].value_counts())*100/df_len
            )
    
    latex_out=df['result_binary2'].value_counts()[:n].to_latex(#longtable=True
                                                              )
    
    caption_str='{'+caption_str+'}'
    latex_out=latex_out.replace('\\begin{tabular}{lr}\n',
                            '\\begin{table}[H]\n\\centering\n\\caption'+caption_str+'\n\\begin{tabular}{lr}\n'
                           )
    latex_out=latex_out.replace('\\end{tabular}\n',
                            '\\end{tabular}\n\\end{table}\n'#.format(caption_str)
                           )
    
    f.write(latex_out)
    f.write('\n')
    
    
    caption_str="distribution of binary encoded infection status:"
    
    latex_out=df.groupby(staph_nunique_col)['result_num'].max().value_counts()[:n].to_latex(#caption=caption_str,
                                                           #longtable=True
                                                            )
    caption_str='{'+caption_str+'}'
    latex_out=latex_out.replace('\\begin{tabular}{lr}\n',
                            '\\begin{table}[H]\n\\centering\n\\caption'+caption_str+'\n\\begin{tabular}{lr}\n'
                           )
    latex_out=latex_out.replace('\\end{tabular}\n',
                            '\\end{tabular}\n\\end{table}\n'#.format(caption_str)
                           )
    f.write(latex_out)
    f.write('\n')
    
    caption_str="top {} SPECIES extracted by regex (where possible):(n unique: {}; n tot {}; \% of total {:.2f})".format(
                n,
                df['species_regex'].explode().nunique(),
                sum(df['species_regex'].explode().value_counts()),
                sum(df['species_regex'].explode().value_counts())*100/df_len
            )
    latex_out=df['species_regex'].explode().value_counts()[:n].to_latex(#caption=caption_str,
                                                              #longtable=True
                                                            )
    
    caption_str='{'+caption_str+'}'
    latex_out=latex_out.replace('\\begin{tabular}{lr}\n',
                            '\\begin{table}[H]\n\\centering\n\\caption'+caption_str+'\n\\begin{tabular}{lr}\n'
                           )
    latex_out=latex_out.replace('\\end{tabular}\n',
                            '\\end{tabular}\n\\end{table}\n'#.format(caption_str)
                           )
    f.write(latex_out)
    f.write('\n')
    
    caption_str="top {} SPECIMEN or SAMPLE regex captured:(n unique: {}; n tot {}; \% of total {:.2f})".format(
                n,
                df['regex_capture_specimen'].explode().nunique(),
                sum(df['regex_capture_specimen'].explode().value_counts()),
                sum(df['regex_capture_specimen'].explode().value_counts())*100/df_len
            )
    
    latex_out=df['regex_capture_specimen'].explode().value_counts()[:n].to_latex(#caption=caption_str,
                                                                       #longtable=True
                                                                        )
    caption_str='{'+caption_str+'}'
    latex_out=latex_out.replace('\\begin{tabular}{lr}\n',
                            '\\begin{table}[H]\n\\centering\n\\caption'+caption_str+'\n\\begin{tabular}{lr}\n'
                           )
    latex_out=latex_out.replace('\\end{tabular}\n',
                            '\\end{tabular}\n\\end{table}\n'#.format(caption_str)
                           )
    
    f.write(latex_out)
    f.write('\n')
    
    caption_str="top {} regex QUANTITATIVE entities captured:(n unique: {}; n tot {}; \% of total {:.2f})".format(
                n,
                df['regex_capture_quant'].explode().nunique(),
                sum(df['regex_capture_quant'].explode().value_counts()),
                sum(df['regex_capture_quant'].explode().value_counts())*100/df_len
            )
    
    latex_out=df['regex_capture_quant'].explode().value_counts()[:n].to_latex(#caption=caption_str,
                                                                    #longtable=True
                                                                   )
    
    caption_str='{'+caption_str+'}'
    latex_out=latex_out.replace('\\begin{tabular}{lr}\n',
                            '\\begin{table}[H]\n\\centering\n\\caption'+caption_str+'\n\\begin{tabular}{lr}\n'
                           )
    latex_out=latex_out.replace('\\end{tabular}\n',
                            '\\end{tabular}\n\\end{table}\n'#.format(caption_str)
                           )
    latex_out= latex_out.replace('>','$>$').replace('<','$<$') 
    f.write(latex_out)
    f.write('\n')
    
#     caption_str="top {} regex groups captured:(n unique: {}; n tot {}; \% of total {:.2f})".format(
#                 n,
#                 df['regex_text'].nunique(),
#                 sum(df['regex_text'].value_counts()),
#                 sum(df['regex_text'].value_counts())*100/df_len
#             )
    
#     latex_out=df['regex_text'].value_counts()[:n].to_latex(#caption=caption_str,
#                                                            #longtable=True
#                                                           )
    
#     caption_str='{'+caption_str+'}'
#     latex_out=latex_out.replace('\\begin{tabular}{lr}\n',
#                             '\\begin{table}[H]\n\\centering\n\\caption'+caption_str+'\n\\begin{tabular}{lr}\n'
#                            )
#     latex_out=latex_out.replace('\\end{tabular}\n',
#                             '\\end{tabular}\n\\end{table}\n'#.format(caption_str)
#                            )
#     f.write(latex_out)
#     f.write('\n')
    
    caption_str="distribution of which regex codeblocks assigned value (regex source):(n unique: {}; n tot {}; \% of total {:.2f})".format(
                df['regex_source'].nunique(),
                sum(df['regex_source'].value_counts()),
                sum(df['regex_source'].value_counts())*100/df_len
            )
    
    latex_out=df['regex_source'].value_counts()[:n].to_latex(#caption=caption_str, 
                                                             #longtable=True
                                                            )
    
    caption_str='{'+caption_str+'}'
    latex_out=latex_out.replace('\\begin{tabular}{lr}\n',
                            '\\begin{table}[H]\n\\centering\n\\caption'+caption_str+'\n\\begin{tabular}{lr}\n'
                           )
    latex_out=latex_out.replace('\\end{tabular}\n',
                            '\\end{tabular}\n\\end{table}\n'#.format(caption_str)
                           )
    f.write(latex_out)
    f.write('\n')
        
    caption_str="most frequent unclassified parsed note (input text):(n unique: {}; n tot {}; \% of total {:.2f})".format(
            df['result_binary'].nunique(),
            sum(df['result_binary'].value_counts()),
            sum(df['result_binary'].value_counts())*100/df_len
        )
    
    latex_out=df.loc[df['result_binary']=='not_captured',text_col_main].value_counts()[:n*2].to_latex(#caption=caption_str,
                                                                                                      #longtable=True
                                                                                                     )
#     latex_out=latex_out.replace('\\begin{tabular}{lr}','\\begin{tabular}{|*{1}{P{12.5cm}|}*{1}{P{2cm}|}}')

    
    caption_str='{'+caption_str+'}'
    latex_out=latex_out.replace('\\begin{tabular}{lr}',
                            '\\begin{table}[H]\n\\centering\n\\caption'+caption_str+'\n\\begin{tabular}{|*{1}{P{12.5cm}|}*{1}{P{2cm}|}}'
                           )
    latex_out=latex_out.replace('\\end{tabular}\n',
                            '\\end{tabular}\n\\end{table}\n'#.format(caption_str)
                           )
    
    f.write(latex_out)
    
    f.write('\n\n\n')

    f.close()

def write_latex_report(file_name_main,annotated_df, df_name, capture_table_len=10):
    
    f=open(os.path.join(output_path,'{}.txt'.format(file_name_main)),'w')
    from datetime import date

    today = date.today()
    today=today.strftime("%B %d, %Y")

    
    ###preamble
    f.write(r'\documentclass{article}')
    f.write('\n')
    f.write(r'\usepackage[utf8]{inputenc}')
    f.write('\n')
    f.write(r'\usepackage{comment}')
    f.write('\n')
    f.write(r'\usepackage{tabularx,caption,ragged2e}')
    f.write('\n')
    f.write(r'\usepackage{booktabs}')
    f.write('\n')
    f.write(r'\usepackage{float}')
    f.write('\n')
    f.write(r'\newcolumntype{L}{>{\RaggedRight\arraybackslash}X}')
    f.write('\n')
    f.write(r'\newcolumntype{P}[1]{>{\RaggedRight\arraybackslash}p{#1}}')
    f.write('\n')
    f.write(r'\usepackage{blindtext}')
    f.write('\n')
    f.write(r'\usepackage{rotating, makecell, cellspace}')
    f.write('\n')
    #f.write(r'\usepackage{longtable}') #added 7/1/21
    f.write('\n')
    f.write(r'\addparagraphcolumntypes{X}')
    f.write('\n')
    f.write(r'\title{microbio parser1}')
    f.write('\n')
    f.write(r'\author{garretteickelberg2023}')
    f.write('\n')
    f.write(r'\date{'+today+'}')
    f.write('\n')
    f.write(r'\begin{document}')
    f.write('\n')
    f.write('\maketitle')
    f.write('\n\n')
    f.close()
    
    

    
    if df_name=='acute':
        describe_classification_latex(annotated_df, n=capture_table_len, df_name='Clarity', file_name=file_name_main,
                                text_col_main='parsed_note',
                                staph_nunique_col='procedure_order_key',
                                result_col_main='result_binary',
                                culture_id_main='visit_id',
                                notetype_main='parent_note_type')
    elif df_name=='ss23':
        describe_classification_latex(annotated_df, n=capture_table_len, df_name='Cerner', file_name=file_name_main,
                                text_col_main='parsed_note',
                                staph_nunique_col='procedure_order_key',
                                result_col_main='result_binary',
                                culture_id_main='visit_id',
                                notetype_main='parent_note_type')
    elif df_name=='UC':
        describe_classification_latex(annotated_df, n=capture_table_len,df_name=' UC cultures', file_name=file_name_main,
                                text_col_main='lab_result',
                                staph_nunique_col='culture_id',
                                result_col_main='result_binary',
                                culture_id_main='encid',
                                notetype_main='proc_desc')
    elif df_name=='LCH':
        describe_classification_latex(annotated_df, n=capture_table_len, df_name='LCH culture', file_name=file_name_main,
                                text_col_main='lab_result',
                                staph_nunique_col='culture_id',
                                result_col_main='result_binary',
                                culture_id_main='encid',
                                notetype_main='proc_desc')

#     annotated_df
    ### little reformatting
    f=open(os.path.join(output_path,'{}.txt'.format(file_name_main)),'rt')
    data= f.read()
    #data = data.replace(r'\begin{table}', r'\begin{table}[H]')
    f.close()
    
    f=open(os.path.join(output_path,'{}.txt'.format(file_name_main)),'wt')
    f.write(data)
    f.write('\n')
    f.write(r'\end{document}')
    f.close()


def save_annotated_df(df_name, annotated_df):
    save_path=os.path.join(data_path,'annotated_data','{}_{}.pkl'.format(specified_date, df_name))
    print('saving annotated df ({}) to {}'.format(df_name, save_path))
    annotated_df.to_pickle(save_path)


def latex_report(df_name, annotated_df,n_latex_rows ):
#     from .latex_report import write_latex_report
    latex_filename=specified_date+'_'+df_name+'_latex_report'
    latex_filepath=os.path.join(data_path,'latex_reports',latex_filename)
    print('saving latex report to {}'.format(latex_filename))
    write_latex_report(latex_filepath, annotated_df, df_name, capture_table_len=n_latex_rows)




def preprocess_acute(output_path, data_path):

    tic = time.perf_counter()

    notes_acute_import= pd.read_csv(os.path.join(output_path,'120521_notes_acute_preproc.csv'),
                         parse_dates=['created_datetime','updated_datetime']
                        )
    ##main() making list of cpt_lables that need to be dropped from both por and notes.
    screen_cpt_drop_acute= list(notes_acute_import.loc[notes_acute_import['cpt_label'].apply(lambda x: re.search(r'screen', str(x).lower())is not None),'cpt_label'].unique())
    notes_acute_import2= notes_acute_import.loc[~notes_acute_import['cpt_label'].isin(screen_cpt_drop_acute),].copy()

    print('####### Parsing culture note text into rows (if specified) #######')
    ###main(): note parsing into rows of df
    notes_parsed=notes_acute_import2.groupby('note_key')['note_text'].apply(lambda x: parse_rows(x)).reset_index().rename(columns={'note_text':'parsed_note', 'level_1':'parse#'})
    notes_acute_merged=pd.merge(notes_acute_import2,notes_parsed, left_on='note_key',right_on='note_key')

    toc = time.perf_counter()
    print(f"data import, parsing, and cleaning: {toc - tic:0.4f} seconds")
    return(notes_acute_merged)



def run_acute():
    print('####### --------NOTES_ACUTE-------- #######')
    ############# acute and ss23:

    df=preprocess_acute(output_path, data_path)

    tic = time.perf_counter()
    print('####### Extracting & Categorizing Parsed Row Via Regex Blocks #######')
    annotated_df= run(df,
                                           text_col_main='parsed_note',
                                           culture_id_main='procedure_order_key',
#                                            result_col_main='result_binary',
#                                            culture_id_main='visit_id',
                                           visit_id_main='visit_id', #this should be changed if there are multiple cultures per visit.
                                           staph_neg_correction=False
                                        , notetype_main='parent_note_type',
                                          likely_neg_to_neg_override=True)

    toc = time.perf_counter()
    print(f"notes_acute result_categorize_main time: {toc - tic:0.4f} seconds, len: {len(annotated_df)}")
    print(annotated_df['result_num'].value_counts())


    df_name='acute'
#     save_annotated_df(df_name, annotated_df)
    latex_report(df_name, annotated_df,n_latex_rows )

def preprocess_ss23(output_path, data_path):
    tic = time.perf_counter()

    notes_ss23_import= pd.read_csv(os.path.join(output_path,'120521_notes_ss23_preproc.csv'),
                         parse_dates=['created_datetime','updated_datetime']
                        )

    ##SS23 main():preprocessing;  dropping note_type/cpt_labels for surveilence/screening.
    notes_ss23_import2=drop_notetypes(notes_ss23_import, text_col='cpt_label')
    notes_ss23_import2=drop_notetypes(notes_ss23_import2, text_col='parent_note_type')
    notes_ss23_import2=drop_notetypes(notes_ss23_import2, text_col='note_type')

    ### creating the composite note_type to address the nulls and -.  basically use parent_note_type>cpt_label>note_type
    notes_ss23_import2['composite_note_type']=notes_ss23_import2['parent_note_type']
    notes_ss23_import2.loc[notes_ss23_import2['parent_note_type'].isna(),'composite_note_type']=notes_ss23_import2.loc[notes_ss23_import2['parent_note_type'].isna(),'cpt_label']
    notes_ss23_import2.loc[notes_ss23_import2['composite_note_type']==' - ','composite_note_type']=notes_ss23_import2.loc[notes_ss23_import2['composite_note_type']==' - ','note_type']

    print('qc preparse')

    #### SS23 MAIN(): parsing
    notes_parsed_ss=notes_ss23_import2.groupby('note_key')['note_text'].apply(lambda x: parse_rows(x)).reset_index().rename(columns={'note_text':'parsed_note', 'level_1':'parse#'})
    print('parse_row fin')
    notes_ss23_merged=pd.merge(notes_ss23_import2,notes_parsed_ss, left_on='note_key',right_on='note_key')
    print('parse_row fin')
    notes_ss23_merged['parsed_note']=notes_ss23_merged['parsed_note'].apply(lambda x: str(x).split('ocf_blob')[0].strip()) ###removing some miscelanious tailing text present on the tail of some reports.
    print('formatting fin')
    toc = time.perf_counter()
    print(f"data import, parsing, and cleaning: {toc - tic:0.4f} seconds")
    return(notes_ss23_merged)




def run_ss23():
    print('####### --------NOTES_SS23-------- #######')
    print('qc start msg1')
    df= preprocess_ss23(output_path, data_path)

    print('####### Extracting & Categorizing Parsed Row Via Regex Blocks #######')
    tic = time.perf_counter()
#     notes_ss_merged
    print('qc start msg2')
    annotated_df= run(df,
                                       text_col_main='parsed_note',
                                       culture_id_main='procedure_order_key',
#                                        result_col_main='result_binary',
#                                        culture_id_main='visit_id',
                                       visit_id_main='visit_id', #this should be changed if there are multiple cultures per visit.
                                       staph_neg_correction=False,
                                       likely_neg_to_neg_override=True )

    print('qc start msg3')
                                        #, notetype_main=True)

    toc = time.perf_counter()

    print(f"ss23 result_categorize_main time: {toc - tic:0.4f} seconds, len: {len(annotated_df)}")


    df_name='ss23'
    save_annotated_df(df_name, annotated_df)
    latex_report(df_name, annotated_df,n_latex_rows )




def preprocess_LCH(output_path, data_path):
    tic = time.perf_counter()
    #### adding encoding accomodation because was getting error: 'utf-8' codec can't decode byte 0x94
    ###  importing and adding a culture_id col.
    LCH_culture= pd.read_csv(os.path.join(data_path,'culture_LCH.csv'), encoding= 'unicode_escape'
                )
    LCH_culture=LCH_culture.rename(columns={'EncID':'encid'})
    LCH_culture=LCH_culture.sort_values(['encid','specimn_taken_dttm'])
    LCH_culture=LCH_culture.reset_index().rename(columns={'index':'culture_id'})

    ## removing everything after comment and subbing multiple spaces for single spaces.
    LCH_culture['lab_result']= LCH_culture['lab_result'].apply(lambda x: re.split(r'comment', str(x),flags=re.IGNORECASE)[0])
    LCH_culture['lab_result']= LCH_culture['lab_result'].apply(lambda x: re.sub(' {2,}',' ',str(x)) )

    toc = time.perf_counter()
    print(f"data import, parsing, and cleaning: {toc - tic:0.4f} seconds")
    return(LCH_culture)



def run_LCH():
    print('####### --------NOTES_LCH-------- #######')

    df= preprocess_LCH(output_path, data_path)

    tic = time.perf_counter()
    annotated_df= run(df,
                                       text_col_main='lab_result',
                                       culture_id_main='culture_id',
#                                        result_col_main='result_binary',
                                       visit_id_main='encid', #this should be changed if there are multiple cultures per visit.
                                       staph_neg_correction=False, #staph_neg_correction False= no coag_neg correction
                                       notetype_main='proc_desc',
                                       quant_col='lab_result', specimen_col='proc_desc',
                                       likely_neg_to_neg_override=True) #override True= no likely neg influence on outcome

    toc = time.perf_counter()
    print(f"LCH result_categorize_main time: {toc - tic:0.4f} seconds, len: {len(annotated_df)}")
    
    print(annotated_df['result_num'].value_counts())

    df_name='LCH'
#     save_annotated_df(df_name, annotated_df)
    latex_report(df_name, annotated_df,n_latex_rows )
    
    
    
def preprocess_UC(output_path, data_path):
    tic = time.perf_counter()
    nocode_to_code_map_UC={
       'CULTURE & STAIN, CSF': 'csf',
        'CULTURE, URINE': 'urine',
         'CULTURE, BLOOD (BACTERIAL & FUNGUS)':'bloodbf',
         'CULTURE, BLOOD (BACTERIAL & FUNGAL)':'bloodbf',
         'CULTURE, VIRAL': 'vircul' ,
         'CULTURE & STAIN, AFB':'afb',
         'CULTURE & STAIN, ANAEROBE/AEROBE': 'cnsanaaer',
         'CULTURE & STAIN, QUANTITATIVE W/ ANAEROBES': 'cnsanaaer',
         'CULTURE & STAIN, FLUID': 'fluid',
         'CULTURE & STAIN, RESPIRATORY': 'respir',
         'CULTURE & STAIN, WOUND DRAINAGE': 'wounds',
         'CULTURE, BETA STREP SCREEN, THROAT': 'betathroat',
         'CULTURE, BLOOD (BACTERIAL & FUNGUS)': 'bloodbf',
         'CULTURE, CMV': 'cmv',
         'CULTURE, FUNGAL, MISC.': 'funmis',
         'CULTURE, FUNGAL, QUANT BX': 'funquant',
         'CULTURE, STOOL': 'stool',
         'CULTURE, URINE': 'urine',
         'CULTURE, URINE, PEDIATRIC PATIENT (LESS THAN 18 YEARS)':'urine',
         'CULTURE, URINE, REFLEXIVE FROM URINALYSIS':'urine',
         'CULTURE, VIRAL': 'vircul',
         'OVA AND PARASITES (O&P), DIRECT EXAM': 'ovaandpara'
    }


    UC_culture= pd.read_csv(os.path.join(data_path,'culture_UC.csv'), encoding= 'unicode_escape'
                    )
    UC_culture=UC_culture.rename(columns={'EncID':'encid','proc_desc':'proc_desc_raw'})

    UC_culture['proc_desc']=UC_culture['proc_desc_raw'].map(nocode_to_code_map_UC)

    UC_culture['culture_id']=UC_culture.groupby(['encid','specimen_day','proc_desc']).ngroup()+1
    
    
    
    ## removing everything after comment and subbing multiple spaces for single spaces.
    UC_culture['lab_result']= UC_culture['lab_result'].apply(lambda x: re.split(r'comment', str(x),flags=re.IGNORECASE)[0])
    UC_culture['lab_result']= UC_culture['lab_result'].apply(lambda x: re.sub(' {2,}',' ',str(x)) )

    ###concatenating a problematic example of poorly parsed string
    c1= UC_culture.loc[UC_culture['lab_result'].apply(lambda x: x.strip())=="Negative for Shiga Toxins 1 and 2. These toxins are present in some strains of",'culture_id']
    bool1=UC_culture.loc[UC_culture['culture_id'].isin(c1),'lab_result'].apply(lambda x: x.strip())=="enterohemorrhagic E. coli."

    replacement_str='Negative for Shiga Toxins 1 and 2. These toxins are present in some strains of enterohemorrhagic escherichia coli.'
    if len(bool1[bool1])==len(c1):
        UC_culture.loc[UC_culture['lab_result'].apply(lambda x: x.strip())=="Negative for Shiga Toxins 1 and 2. These toxins are present in some strains of",'lab_result']=replacement_str
        UC_culture.drop(bool1[bool1].index, inplace=True)
    else:
        print('##### PROBLEM: mismatch between lengths of each corresponding concatenation string for enterohemorrhagic ecoli ######')


    ###concatenating a problematic example of poorly parsed string
    c1= UC_culture.loc[UC_culture['lab_result'].apply(lambda x: x.strip())=="Previous results: Negative for Shiga Toxins 1 and 2. These toxins are present in",'culture_id'].to_list()
    bool1=UC_culture.loc[UC_culture['culture_id'].isin(c1),'lab_result'].apply(lambda x: x.strip())=="some strains of enterohemorrhagic E. coli."

    replacement_str='Previous results: Negative for Shiga Toxins 1 and 2. These toxins are present in some strains of enterohemorrhagic E. coli.'
    if len(bool1[bool1])==len(c1):
        UC_culture.loc[UC_culture['lab_result'].apply(lambda x: x.strip())=="Previous results: Negative for Shiga Toxins 1 and 2. These toxins are present in",'lab_result']=replacement_str
        UC_culture.drop(bool1[bool1].index, inplace=True)
    else:
        print('##### PROBLEM: mismatch between lengths of each corresponding concatenation string for enterohemorrhagic ecoli ######')


    ###concatenating a problematic example of poorly parsed string. this one is for qol as it removes a ton of wasteful parsed rows
    c1= UC_culture.loc[UC_culture['lab_result'].apply(lambda x: x.strip())=='Organism identification may have utilized MALDI-TOF mass spectrometry. The','culture_id'].to_list()
    bool1=UC_culture.loc[UC_culture['culture_id'].isin(c1),'lab_result'].apply(lambda x: x.strip())=='performance characteristics of the test were determined by the University of'
    bool2=UC_culture.loc[UC_culture['culture_id'].isin(c1),'lab_result'].apply(lambda x: x.strip())=='Chicago Medicine Clinical Microbiology Laboratory in a manner consistent with'
    bool3=UC_culture.loc[UC_culture['culture_id'].isin(c1),'lab_result'].apply(lambda x: x.strip())=='CLIA requirements. This test has not been cleared or approved by the U.S. Food'
    bool4=UC_culture.loc[UC_culture['culture_id'].isin(c1),'lab_result'].apply(lambda x: x.strip())=='and Drug Administration (FDA).'

    replacement_str='Organism identification may have utilized MALDI-TOF mass spectrometry. The performance characteristics of the test were determined by the University of Chicago Medicine Clinical Microbiology Laboratory in a manner consistent with CLIA requirements. This test has not been cleared or approved by the U.S. Food and Drug Administration (FDA).'

    UC_culture.loc[UC_culture['lab_result'].apply(lambda x: x.strip())=='Organism identification may have utilized MALDI-TOF mass spectrometry. The','lab_result']=replacement_str
    UC_culture.drop(bool1[bool1].index, inplace=True)
    UC_culture.drop(bool2[bool2].index, inplace=True)
    UC_culture.drop(bool3[bool3].index, inplace=True)
    UC_culture.drop(bool4[bool4].index, inplace=True)

    toc = time.perf_counter()
    print(f"data import, parsing, and cleaning: {toc - tic:0.4f} seconds")

    return(UC_culture)


def run_UC():
    print('####### --------NOTES_UC-------- #######')
    df= preprocess_UC(output_path, data_path)

    tic = time.perf_counter()

    annotated_df= run(df,
                                       text_col_main='lab_result',
                                       culture_id_main='culture_id',
                                       visit_id_main='encid', #this should be changed if there are multiple cultures per visit.

                                       staph_neg_correction=False,
                                       notetype_main='proc_desc',
                                       quant_col='lab_result', specimen_col='proc_desc',
                                       likely_neg_to_neg_override=True)
    
    


    toc = time.perf_counter()
    print(f"UC result_categorize_main time: {toc - tic:0.4f} seconds, len: {len(annotated_df)}")

    print(annotated_df['result_num'].value_counts())
    
#     df_name='UC'
#     save_annotated_df(df_name, annotated_df)
#     latex_report(df_name, annotated_df,n_latex_rows )
    
    
    
    
    
def main():
    print('####### Program Started #######')
    print(pd.__version__)
    print('saving files with date: {}'.format(specified_date))

#     #creating an annotated_data and latex report folder for the outputs to be stored.
#     if not os.path.exists(os.path.join(data_path,'annotated_data')):
#         os.makedirs(os.path.join(data_path,'annotated_data'))

#     if not os.path.exists(os.path.join(data_path,'latex_reports')):
#         os.makedirs(os.path.join(data_path,'latex_reports'))


#     run_acute()
#     run_ss23()
    run_LCH()
#     run_UC()
    run_acute()
#     run_ss23()

    print('####### Program Finished #######')




if __name__ == "__main__":
    main()
