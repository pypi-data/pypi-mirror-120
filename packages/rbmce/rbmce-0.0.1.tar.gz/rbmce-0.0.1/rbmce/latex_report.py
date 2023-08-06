
import pandas as pd
import os
import numpy as np
import re
#import xlrd

from parameters import *


################# summary output:




# def descriptive_df(df, text_col_main,staph_nunique_col,result_col_main,
#            culture_id_main,notetype_main,df_name):
#     """
#     makes a dataframe to present descriptive statistics of the parsing. 
#     """
# #     pd.options.display.max_rows
# #     pd.set_option('display.max_colwidth', None)
#     pd.options.display.max_rows
# #     pd.set_option('display.max_colwidth', -1)
#     pd.set_option('display.max_colwidth', 999)

#     n_notes=int
#     if 'note_key' in list(df):
#         n_notes=df['note_key'].nunique()
#     else:
#         n_notes=np.nan
    
#     dict1={r"n notekeys (can be $\geq$ n culture if parsed notes)":[n_notes],
#         r"n cultures (can be many:visit)": [df[staph_nunique_col].nunique()],
#         r"n visits":[df[culture_id_main].nunique()],
#         r"n rows": [len(df)],
#         r"n rows not parsed":[len(df[df['result_binary']=='not_captured'])]
#         }
#     return(pd.DataFrame.from_dict(dict1, orient='index', columns=[df_name]))



# def describe_classification_latex(df,n, df_name,file_name,
#                             text_col_main='parsed_note',
#                             staph_nunique_col='procedure_order_key',
#                             result_col_main='result_binary',
#                             culture_id_main='visit_id',
#                             notetype_main='parent_note_type',
#                            ):
    
#     """
#     function to help standardize the desired outputs from the first non-aggregated result classification. writes latex output to a .txt file. 
    
#     """
#     pd.options.display.max_rows
# #     pd.set_option('display.max_colwidth', -1)
#     pd.set_option('display.max_colwidth', 999)
    
#     f=open(os.path.join(output_path,'{}.txt'.format(file_name)),'a')   
    
#     f.write('%############################')
#     f.write('\n')
    
#     df_title=str('\section{'+df_name+'}')
#     f.write(df_title)
#     f.write('\n')
    
#     desc_df= descriptive_df(df, text_col_main,staph_nunique_col,result_col_main,
#            culture_id_main,notetype_main,df_name)
#     df_len=len(df)
    
    
#     caption_str="Descriptive Statistics:"
#     latex_out=desc_df.to_latex(#caption=caption_str,
#                                escape=False#, longtable=True
#                                 )

#     caption_str='{'+caption_str+'}'
#     latex_out=latex_out.replace('\\begin{tabular}{lr}\n',
#                             '\\begin{table}[H]\n\\centering\n\\caption'+caption_str+'\n\\begin{tabular}{lr}\n'
#                            )
#     latex_out=latex_out.replace('\\end{tabular}\n',
#                             '\\end{tabular}\n\\end{table}\n'#.format(caption_str)
#                            )

#     f.write(latex_out)
#     f.write('\n')
    
#     caption_str= "top {} result binary2 (less granular than result binary1) distribution: (n unique: {}; n tot {}; \% of total {:.2f})".format(
#                 n,
#                 df['result_binary2'].nunique(),
#                 sum(df['result_binary2'].value_counts()),
#                 sum(df['result_binary2'].value_counts())*100/df_len
#             )
    
#     latex_out=df['result_binary2'].value_counts()[:n].to_latex(#longtable=True
#                                                               )
    
#     caption_str='{'+caption_str+'}'
#     latex_out=latex_out.replace('\\begin{tabular}{lr}\n',
#                             '\\begin{table}[H]\n\\centering\n\\caption'+caption_str+'\n\\begin{tabular}{lr}\n'
#                            )
#     latex_out=latex_out.replace('\\end{tabular}\n',
#                             '\\end{tabular}\n\\end{table}\n'#.format(caption_str)
#                            )
    
#     f.write(latex_out)
#     f.write('\n')
    
    
#     caption_str="distribution of binary encoded infection status:"
    
#     latex_out=df['result_num'].value_counts()[:n].to_latex(#caption=caption_str,
#                                                            #longtable=True
#                                                             )
#     caption_str='{'+caption_str+'}'
#     latex_out=latex_out.replace('\\begin{tabular}{lr}\n',
#                             '\\begin{table}[H]\n\\centering\n\\caption'+caption_str+'\n\\begin{tabular}{lr}\n'
#                            )
#     latex_out=latex_out.replace('\\end{tabular}\n',
#                             '\\end{tabular}\n\\end{table}\n'#.format(caption_str)
#                            )
#     f.write(latex_out)
#     f.write('\n')
    
#     caption_str="top {} SPECIES extracted by regex (where possible):(n unique: {}; n tot {}; \% of total {:.2f})".format(
#                 n,
#                 df['species_regex'].nunique(),
#                 sum(df['species_regex'].value_counts()),
#                 sum(df['species_regex'].value_counts())*100/df_len
#             )
#     latex_out=df['species_regex'].value_counts()[:n].to_latex(#caption=caption_str,
#                                                               #longtable=True
#                                                             )
    
#     caption_str='{'+caption_str+'}'
#     latex_out=latex_out.replace('\\begin{tabular}{lr}\n',
#                             '\\begin{table}[H]\n\\centering\n\\caption'+caption_str+'\n\\begin{tabular}{lr}\n'
#                            )
#     latex_out=latex_out.replace('\\end{tabular}\n',
#                             '\\end{tabular}\n\\end{table}\n'#.format(caption_str)
#                            )
#     f.write(latex_out)
#     f.write('\n')
    
#     caption_str="top {} SPECIMEN or SAMPLE regex captured:(n unique: {}; n tot {}; \% of total {:.2f})".format(
#                 n,
#                 df['regex_capture_specimen'].nunique(),
#                 sum(df['regex_capture_specimen'].value_counts()),
#                 sum(df['regex_capture_specimen'].value_counts())*100/df_len
#             )
    
#     latex_out=df['regex_capture_specimen'].value_counts()[:n].to_latex(#caption=caption_str,
#                                                                        #longtable=True
#                                                                         )
#     caption_str='{'+caption_str+'}'
#     latex_out=latex_out.replace('\\begin{tabular}{lr}\n',
#                             '\\begin{table}[H]\n\\centering\n\\caption'+caption_str+'\n\\begin{tabular}{lr}\n'
#                            )
#     latex_out=latex_out.replace('\\end{tabular}\n',
#                             '\\end{tabular}\n\\end{table}\n'#.format(caption_str)
#                            )
    
#     f.write(latex_out)
#     f.write('\n')
    
#     caption_str="top {} regex QUANTITATIVE entities captured:(n unique: {}; n tot {}; \% of total {:.2f})".format(
#                 n,
#                 df['regex_capture_quant'].nunique(),
#                 sum(df['regex_capture_quant'].value_counts()),
#                 sum(df['regex_capture_quant'].value_counts())*100/df_len
#             )
    
#     latex_out=df['regex_capture_quant'].value_counts()[:n].to_latex(#caption=caption_str,
#                                                                     #longtable=True
#                                                                    )
    
#     caption_str='{'+caption_str+'}'
#     latex_out=latex_out.replace('\\begin{tabular}{lr}\n',
#                             '\\begin{table}[H]\n\\centering\n\\caption'+caption_str+'\n\\begin{tabular}{lr}\n'
#                            )
#     latex_out=latex_out.replace('\\end{tabular}\n',
#                             '\\end{tabular}\n\\end{table}\n'#.format(caption_str)
#                            )
#     latex_out= latex_out.replace('>','$>$').replace('<','$<$') 
#     f.write(latex_out)
#     f.write('\n')
    
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
    
#     caption_str="distribution of which regex codeblocks assigned value (regex source):(n unique: {}; n tot {}; \% of total {:.2f})".format(
#                 df['regex_source'].nunique(),
#                 sum(df['regex_source'].value_counts()),
#                 sum(df['regex_source'].value_counts())*100/df_len
#             )
    
#     latex_out=df['regex_source'].value_counts()[:n].to_latex(#caption=caption_str, 
#                                                              #longtable=True
#                                                             )
    
#     caption_str='{'+caption_str+'}'
#     latex_out=latex_out.replace('\\begin{tabular}{lr}\n',
#                             '\\begin{table}[H]\n\\centering\n\\caption'+caption_str+'\n\\begin{tabular}{lr}\n'
#                            )
#     latex_out=latex_out.replace('\\end{tabular}\n',
#                             '\\end{tabular}\n\\end{table}\n'#.format(caption_str)
#                            )
#     f.write(latex_out)
#     f.write('\n')
        
#     caption_str="most frequent unclassified parsed note (input text):(n unique: {}; n tot {}; \% of total {:.2f})".format(
#             df['result_binary'].nunique(),
#             sum(df['result_binary'].value_counts()),
#             sum(df['result_binary'].value_counts())*100/df_len
#         )
    
#     latex_out=df.loc[df['result_binary']=='not_captured',text_col_main].value_counts()[:n*2].to_latex(#caption=caption_str,
#                                                                                                       #longtable=True
#                                                                                                      )
# #     latex_out=latex_out.replace('\\begin{tabular}{lr}','\\begin{tabular}{|*{1}{P{12.5cm}|}*{1}{P{2cm}|}}')

    
#     caption_str='{'+caption_str+'}'
#     latex_out=latex_out.replace('\\begin{tabular}{lr}',
#                             '\\begin{table}[H]\n\\centering\n\\caption'+caption_str+'\n\\begin{tabular}{|*{1}{P{12.5cm}|}*{1}{P{2cm}|}}'
#                            )
#     latex_out=latex_out.replace('\\end{tabular}\n',
#                             '\\end{tabular}\n\\end{table}\n'#.format(caption_str)
#                            )
    
#     f.write(latex_out)
    
#     f.write('\n\n\n')

#     f.close()
    
      

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