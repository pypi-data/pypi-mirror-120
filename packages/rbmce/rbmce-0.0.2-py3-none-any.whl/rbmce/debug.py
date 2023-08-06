from .rbmce import *    
from .regex_blocks import species_regex_list
import pandas as pd
pd.set_option('display.max_colwidth', None)

def rbmce_str_in(str_input, staph_neg_correction=False, likely_neg_to_neg_override=True):
    
    """
    function to take in a string argument, run concept extraction workflow, and display results

    """
    
    d={'parsed_note':[str_input],
    'culture_id':1,
   'visit_id':1
      }
    df=pd.DataFrame(data=d, index=[1])

    
    df= run(df, 
            text_col_main='parsed_note', 
            culture_id_main='culture_id',#'procedure_order_key',  ##formerly named staph_nunique_col
            visit_id_main='visit_id',   ##formerly named culture_id_main.  #this should be changed if there are multiple cultures per visit.
            staph_neg_correction=False, 
            notetype_main=None, 
            quant_col=None, 
            specimen_col=None,
            likely_neg_to_neg_override=True)
    
    
    df=df.drop(columns=['culture_id','visit_id'])
    print(df.iloc[:,:8])
    print()
    print(df.iloc[:,8:15])
    print()
    print(df.iloc[:,-15:-9])
    print()
    print(df.iloc[:,-9:])  
    
    
    
def main():
    import sys
    
    n = len(sys.argv[1:])
    
    arg_processed=''
    if n>1:
        for i in range(1, n+1):
            arg_string= str(sys.argv[i]).strip()
            arg_processed= arg_processed + ' ' + arg_string
            
    else:
        arg_processed= sys.argv[1]

    rbmce_str_in(arg_processed)
    
    
if __name__ == "__main__":
    main()