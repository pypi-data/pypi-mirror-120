from .microbio_parser import *    
from .regex_blocks import species_regex_list
import pandas as pd
pd.set_option('display.max_colwidth', None)

def MCE_StrIn(str_input, staph_neg_correction=False, likely_neg_to_neg_override=True):
    
    """
    function to take in a string argument, run concept extraction workflow, and display results

    """
    import time  
    
    d={'parsed_note':[str_input],
    'culture_id':1,
   'visit_id':1
      }
    df=pd.DataFrame(data=d)
       
    df= result_categorize_main(df, 
                                       text_col_main='parsed_note',
                                       staph_nunique_col='procedure_order_key',
                                       result_col_main='result_binary',
                                       culture_id_main='visit_id',
                                       visit_id='visit_id', 
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
    str_input = input("Enter note text to process :")
    if str_input is None:
        str_input='No Salmonella, Shigella, Campylobacter, Aeromonas or Plesiomonas isolated.'
    MCE_StrIn(str_input)
    
    
    
if __name__ == "__main__":
    main()