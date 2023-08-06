
### main functions comprising the rule-based microbiology clinical concept extractor (RBMCE) 


import pandas as pd
import os
import numpy as np

import pathlib
import re
import sys, warnings
from datetime import date

import time
from .parameters import *
from .regex_blocks import species_regex_list


##### parsing rows and preparing df:


def drop_notetypes(notes, text_col):
    
    """
    function: optional function to drop certain notetypes from a df with notes. not currently generalized
    """

    drop_notetype_regexlist=[
        r'surveillance',
        r'screen'
    ]

    drop_notetype_boollist=[[False for i in range(len(notes[text_col]))] for x in range(len(drop_notetype_regexlist))]

    for i in range(0,len(drop_notetype_regexlist)):
        drop_notetype_boollist[i]=notes[text_col].apply( lambda x: re.search(drop_notetype_regexlist[i], str(x).lower()) != None)
    
        notes.loc[drop_notetype_boollist[i], 'result_binary']='drop_culture_type'
        
    drop_index=notes[notes['result_binary']=='drop_culture_type'].index
    
    #dropping rows:
    notes.drop(drop_index,inplace=True)
    notes.drop(columns='result_binary',inplace=True)
        
    return(notes)


def parse_rows(note_text,verbose=False, Return_bool=True, QC_mode=False, granular_newline=True):

    """
    function: parses gross microbiology notes into digestable rows to later classify.
    input: (string) raw microbiology note text in a single column. 
        NOTE: currently utilizes carriage returns/newline character patterns most often. utility of regular expressions here is highly dependent upon note format and structure. 

    output: (list of strings) list of parsed report rows
    
    QC_mode/verbose: (bool) optional parameters for debugging purposes useful in adding or modifying regular expressions
    granular_newline: (bool) parameter for a more aggressive row parsing of headings and subheadings. returns more rows than if False. 
    Return_bool: (bool) bool to output list of strings. useful in debugging. 
    """
    
    if type(note_text)!=pd.Series:
        note_text=pd.Series(note_text)
    remove_end_formatting=r'\r\n\r((\n)+(\r)){0,}\s*$' #remove carriage return\newline tails common on some types of reports
    lineparse1=r'\r\n\r(?:\n?\r?){0,}' #parses a \r\n\r with repeating pattern of \r\n as a new row.
    lineparse2=r'\n\s{1,2}\n\s{1,}(?=\w)' ### additional spaces and newline next to word splitting
    lineparse3=r'\s\n\s{1,}\n?'
    lineparse4=r'\s\n(?=\w)'
    lineparse5=r'(?<=\r\n(negative|positive|detected)\r\n)' ### helps maintain headings and results into one line. particularly useful for when species name is in the test name:
        ###eg:   \r\nE. coli:\nNegative
    lineparse6=r'\r\n(?=[A-Z a-z]+:\s)' ##parses out different column headers and results into one line. \r\nGRAM STAIN Results: no growth detected
    lineparse7=r'\r\n(?=\w)'
    heading_linebreak_remove= r'(?<=[A-Z]{2}:)\s?\r\n(?=[A-Z]+[A-Za-z\s]*)' #adding \s? to see if this solves
    
    ###trying to seperate headings vs non headings by removing some line breaks:
    regex_list_form0=[re.sub(heading_linebreak_remove,' ', str(x)) for x in note_text]
    regex_list_form1=[re.split(remove_end_formatting, str(x).lower())[0] for x in regex_list_form0] #removes the returncarriage and newlines at the end of a note
    string_to_parse=regex_list_form1[0]

    # all regex above are used to identify positions to sub in a unique tag which is then used to split into different rows. 
    string_to_parse2=re.sub(lineparse1,'--__--', str(string_to_parse)) 
    string_to_parse3=re.sub(lineparse2,'--__--', str(string_to_parse2)) 
    string_to_parse4=re.sub(lineparse5,'--__--', str(string_to_parse3))
    string_to_parse5=re.sub(lineparse6,'--__--', str(string_to_parse4),count=6) #count=6 added as a reasonable seeming upper #. 
    if granular_newline==True:
        string_to_parse6=re.sub(lineparse7,'--__--', str(string_to_parse5),count=12) #parses a new line carrage return followed by a word.  6/4/21
        parsed_list=string_to_parse6.split('--__--')
    else:
        parsed_list=string_to_parse5.split('--__--')
    
    regex_sub0= [re.sub(r'\r\n(?=\w)',' ',str(x)) for x in parsed_list ] #removes remaining single instances of \r\n that sometimes occur within lines. replaces w/ white space if occurs next to a word
    regex_sub1= [re.sub(r'\r\n','',str(x)) for x in regex_sub0 ] #removes remaining single instances of \r\n that sometimes occur within lines
    regex_sub2= [re.sub(lineparse3,' ',str(x)) for x in regex_sub1 ] #removes some more whitespace type repeating charactr gunk
    if QC_mode==True:
        regex_sub3= [re.sub(lineparse4,'!',str(x)) for x in regex_sub2 ] #removes some more whitespace type repeating charactr gunk
    else:
        regex_sub3= [re.sub(lineparse4,' ',str(x)) for x in regex_sub2 ] #removes some more whitespace type repeating charactr gunk
        
    #finally splitting comment and replacing multiple spaces with single spaces
    regex_sub4= [re.split(r'comment', str(x).lower())[0] for x in regex_sub3]
    regex_sub5= [re.sub(' {2,}',' ',str(x)) for x in regex_sub4 ]

    
    if verbose==True:
        print('#### removing tail return carrage/newlines: ####')
        display(regex_list_form1)
        print('#### parsing newlines: ####')
        display(regex_list_form2)
        print('#### subbing remaining \r\n occurances: ####')
        display(regex_sub1)
        print('#### removing whitspace char gunk1 ####')
        display(regex_sub2)
        print('#### removing whitspace char gunk2 ####')
        display(regex_sub3)

    
    if Return_bool==True:
        return(pd.Series(regex_sub5))
    
    
    

    
##### microbio parsing functions


#utility functions, split and concat.

def df_split_regex(df, result_binary_regex_split=None, result_col='result_binary'):
    """
    function to segregate a dataframe into two dataframes based a boolean list obtained from applying a regex_match to a col of results. intended to be used to sequester a dataframe of classified rows into positives and negatives
    """
    
    if result_binary_regex_split is not None:
        
        bool_list=df[result_col].apply(lambda x: re.search(result_binary_regex_split,str(x).lower()) is not None)
        df_unclass=df.loc[bool_list,:].copy()
        df=df.drop(df.loc[bool_list,:].index)
    else:
        df_unclass= df.loc[df[result_col]=='not_captured',:].copy()
        df=df.drop(df.loc[df[result_col]=='not_captured',:].index)
    
    return(df, df_unclass)


def df_concat(por,por_unclass):
    """
    concats split df back together. 
    """
    por=por.append(por_unclass, sort=True)
    
    return(por)



####   microbio parsing functions:


def regex_list_capture(df, regex_list, text_col_main, capture_col,
                       result_col='result_binary', regex_block='unspecified_regex_block',
                      regex_col=None,
                       default=True, QC=True,
                      override_result=False):
    """
    a generalized framework to iterate through a list of regular expressions, apply them to a text column ,
    make a dataframe of rows vs regex with values = capture groups, and assign values to the 
    origional dataframe w/ the list of regex captured, and possibly list of regex groups used.
    """
    from .regex_blocks import staph_regex_dic
    
    
    ### making # of boolean lists of length df for each entry in negative regex list
    bool_list=[[False for i in range(len(df[text_col_main]))] for x in range(len(regex_list))]
    #quant_capture_list=[['not_captured' for i in range(len(df[text_col_main]))] for x in range(len(regex_list))]

    capture_df= pd.DataFrame( index=df.index, columns= regex_list)
    capture_df[capture_df.isna()]='not_captured'
    
    ##testing this for result binary
    capture_df2= pd.DataFrame( index=df.index, columns= regex_list)
    col_list=list(capture_df)

    for i in range(0,len(bool_list)): ## looping through the regex list and vectorizing the regex captures across all rows
        bool_list[i]=df[text_col_main].apply( lambda x: re.search(regex_list[i], str(x).lower()) != None)
        capture= df.loc[bool_list[i], text_col_main].apply( lambda x: re.search(regex_list[i], str(x).lower()).group().strip(' ')) #
        capture_df.loc[bool_list[i], col_list[i]]=capture
        capture_df2.loc[bool_list[i], col_list[i]]='{}{}'.format(regex_block, i)
        
        if override_result==True: #storing the current result_col value to overwrite it after normal operation if override==True. Written this way such that normal use doesn't incure more operations.
             stored_value=df.loc[bool_list[i], result_col]
                
        df.loc[bool_list[i], result_col]='{}{}'.format(regex_block, i)
        
        if override_result==True:
             df.loc[bool_list[i], result_col]=stored_value
                
        df.loc[bool_list[i], 'regex_text']=regex_list[i]
        df.loc[bool_list[i], 'regex_source']=regex_block
    
    df_list = capture_df.values.tolist()
    df[capture_col]=[[x for x in y if x!='not_captured'] for y in df_list]
       
    ### adding spot for list of regex expressions that were triggered
    if regex_col!=None:
#         regex_activated=[list(capture_df.loc[:,[x!='not_captured' for x in y]]) for y in df_list]
#         df[regex_col]=regex_activated  
                ##7/27 fix to improve performance 100x on above line, which was a bottleneck that scaled non-linearly with df size. 
        t=np.where(capture_df != 'not_captured', capture_df.columns,'').tolist()
        df[regex_col]= [[x for x in y if x!='']for y in t]
        
    return(df)


def culture_abbreviation_map(df, text_col):
    """
    changes the value for the most prevelent abbreviations when available, else retain current value. 
    value_map_dic2 looks for most prevelent bacteria in an abbreviated species format (e. coli) to map to full name format (escherichia coli). note the casing is preserved in teh string besides the substitution.
    """
    from .regex_blocks import value_map_dict, value_map_dict2
    
    mapped=df[text_col].map(value_map_dict)
    df.loc[mapped.notna(),text_col]=mapped[mapped.notna()]
    
    ###
    for element in value_map_dict2.keys():
        df[text_col]=df[text_col].apply(lambda x: re.sub(element,value_map_dict2[element], str(x), flags=re.IGNORECASE))

    return(df)

def negative_classifier(df, text_col,result_col='result_binary',species_name='species'):
    """
    function: first classification step, searches for blatent negative results and non-bacterial species. 
    input:
        df: (dataframe)
        text_col: column with (parsed) microbio string to be classified 
        result_col: name of the first, most granular enumerated classification result col added
        species_name: (str) name of extracted species column to be added
    output: 
        df with result_col, species_name, and regex_capture columns added. 
    """
    
    from .regex_blocks import negative_regex_list,yeast_regex_list, virus_regex_list
    
    ##negative captures
    df= regex_list_capture(df,
                         negative_regex_list,
                         text_col,
                         capture_col='negative_capt',
                         regex_block='negative_classifying',
                          regex_col='negative_regex')
    
        
    #looking at negative for and also excluding current positives just incase note says "neg for x, pos for y..."
    neg_not_pos=(df[text_col].apply( lambda x: re.search(r'negative for', str(x).lower()) != None) &
            (df[result_col].apply(lambda x:re.search(r'pos',str(x)) != None))) #fixed, changed from is not none. 8/24
    df.loc[neg_not_pos, result_col]='negative_excluding_p'
    df.loc[neg_not_pos, 'regex_text']='negative_excluding_p'
    df.loc[neg_not_pos, 'regex_source']='negative_classifying'
    
    #yeast
    df= regex_list_capture(df,
                         yeast_regex_list,
                         text_col,
                         capture_col='yeast_capt',
                         regex_block='negative_classifying',
                          regex_col='yeast_regex')
    
    #virus
    df= regex_list_capture(df,
                         virus_regex_list,
                         text_col,
                         capture_col='virus_capt',
                         regex_block='negative_classifying',
                          regex_col='virus_regex')
    ##null values get an negative. 
    df.loc[df[text_col].isna(),result_col]='negative/null'
    df.loc[df[text_col].isna(),'regex_text']='negative/null'
    df.loc[df[text_col].isna(), 'regex_source']='negative/null'   
    
    return(df)



###### extracts that do not influence classification: quantatitive information, specimen/sampletype. 

def general_quant_extract(df, text_col):
    """
    fxn to extract general quantitative information from report, such as 10,000 cfu/ml. This info is difficult to tie to an exact species capture so for the time being the general quantitative info is extracted.
    """
    from .regex_blocks import quant_regex_list
    
    df= regex_list_capture(df,
                     quant_regex_list,
                     text_col,
                     capture_col='quant_descriptive_capt',
                     regex_block='quant_descriptive',
                     regex_col='quant_descriptive_regex')
    return(df)
    
def specimen_extract(df, text_col):
    """
    untested feature to try and extract specimen, aka sample type, from report. useful for cases where specimen is not a descrete info, as in our source system.
    """
    from .regex_blocks import specimen_regex_list
    
    df= regex_list_capture(df,
                     specimen_regex_list,
                     text_col,
                     capture_col='specimen_descriptive_capt',
                     regex_block='specimen_descriptive',
                      regex_col='specimen_descriptive_regex')
        
    df['specimen_descriptive_capt']= df['specimen_descriptive_capt'].apply(lambda x: [str(y).split('sample:')[-1].strip() for y in x] )
    df['specimen_descriptive_capt']= df['specimen_descriptive_capt'].apply(lambda x: [str(y).split('source:')[-1].strip() for y in x] )
    df['specimen_descriptive_capt']= df['specimen_descriptive_capt'].apply(lambda x: [str(y).split('specimen:')[-1].strip() for y in x] )
    return(df)


def selective_append(x, element):
    """
    simple append function with some if/then logic, slightly larger than ideal in a lamba fxn. 
    """
    from .regex_blocks import staph_name_dic
    if type(x)== list:
         x.append(staph_name_dic[element])

def staph_classifier(df, coag_neg_correction,  text_col, result_col, override_result=False):
    """
    function: staphylococcus have a diverse set of bacteria with different clinical interpretations/manifestations/severity. Notably, coag negative staph are common contaminants and are often required to have 
    repeat positive cultures for a confirmed positive. this function parses text for various staph regex and assigns species, binary classification, regex used, and regex category to parsed rows. 
    staph_coag_neg_correction() can be used as a followup to change neg_staph binary results -> pos_staph if duplicate neg_staph are present. 
    """
    from .regex_blocks import staph_regex_dic, staph_classification_dic

    for element in staph_regex_dic.keys():
        key_bool= df[text_col].apply( lambda x: re.search(staph_regex_dic[element], str(x).lower()) != None)      
        #df.loc[key_bool,'species']=element
        df.loc[key_bool,'species_regex'].apply(lambda x:selective_append(x, element))#=element
        df.loc[key_bool,'species_capt'].apply(lambda x:selective_append(x, element))
        
        #override_result: storing the current result_col value to overwrite it after normal operation if override==True. Written this way such that normal use doesn't incure more operations.
        #this is used to capture staph species in results classified as negative without changing the classification status.
        if override_result==True: 
             stored_value=df.loc[key_bool, result_col]
        
        df.loc[key_bool, result_col]=staph_classification_dic[element]
        
        if coag_neg_correction==False: ##if the coagulase negative correction if off, all staph pickups will be pos_staph rather than the staph_classification_dic value.
             df.loc[key_bool, result_col]='pos_staph'
        
        if override_result==True: #storing the current result_col value to overwrite it after normal operation if override==True. Written this way such that normal use doesn't incure more operations.
            df.loc[key_bool, result_col]=stored_value
            
                
        df.loc[key_bool,'regex_text']=staph_regex_dic[element]
        df.loc[key_bool,'regex_source']='species_specific_staph' 
        
    #final catchall for staph without a label of other staph
    key_bool= df[text_col].apply(lambda x: (re.search(r'staph[\w]*', str(x).lower()) is not None) & (
                                            re.search(r'epidermidis|hominis|saprophyticus|\bcoag[ulase]*\b|aureus|oxacillin|methicillin|lugdunensis', str(x).lower()) is None)) 
    df.loc[key_bool,'species_regex'].apply(lambda x:selective_append(x, 'staphylococcus_unspecified'))#=element
    df.loc[key_bool,'species_capt'].apply(lambda x:selective_append(x, 'staphylococcus_unspecified'))
    if override_result==False:
        df.loc[key_bool, result_col]='pos_staph_unspecified'
        df.loc[key_bool,'regex_text']='staph_unspecified'
        df.loc[key_bool,'regex_source']='species_specific_staph'       
    return(df)
    

def staph_coag_neg_correction(df, text_col, result_col, time_col='procedure_order_key', culture_id='visit_id'):
    """
    groups df by a visit/encounter identifier and counts the # of cultures classified as neg_staph. if >1, then changes the neg staph to a positive value. 
    this is performed to mirror the practice of requiring multiple neg_staph cultures to be considered positive (to rule out contamination).  
    
    """
    many_negstaph_bool=(df.loc[df[result_col]=='neg_staph',:].groupby(culture_id)[time_col].nunique()>1)  #n=30 -> 274 when changed from order-> result_datetime
    negstaph_vid=many_negstaph_bool[many_negstaph_bool].reset_index()[culture_id].to_list()

    df.loc[(df[culture_id].isin(negstaph_vid)) &(df[result_col]=='neg_staph'),result_col]='repeat_coagN_staph_pos'
    return(df)


def unspecific_pos_cat(df, text_col):
    """
    classifies text into non-specific positive, these are often overwritten by subsequent more specific when possible
    """
    from .regex_blocks import pos_quant_list, pos_qual_list

    df= regex_list_capture(df,
                 pos_quant_list,
                 text_col,
                 capture_col='pos_quant_capt',
                 regex_block='positive_unspecific',
                  regex_col='pos_quant_regex')
    
    df= regex_list_capture(df,
             pos_qual_list,
             text_col,
             capture_col='pos_qual_capt',
             regex_block='positive_unspecific',
              regex_col='pos_qual_regex')
    return(df)

########

def pos_species_cat(df, text_col, notetype_col=None, override_result_bool=False):
    """
    classifies text into species-specific positives, these are often overwritten by language signifying unclarity downstream
    """
    from .regex_blocks import species_regex_list
        
    df= regex_list_capture(df,
             species_regex_list,
             text_col,
             capture_col='species_capt',
             regex_block='species_positive',
             regex_col='species_regex', 
             override_result=override_result_bool)
    
    return(df)


def unclear_cat(df, text_col):
    """
    classifies text into uncertain categories based on presence of language signifying unclarity
    """
    from .regex_blocks import unclear_regex_list
        
    df= regex_list_capture(df,
             unclear_regex_list,
             text_col,
             capture_col='unclear_capt',
             regex_block='unclear',
             regex_col='unclear_regex')
    return(df)


def likelyneg_cat(df, text_col,override_result_bool=False):
    """
    classifies text into uncertain categories based on presence of language signifying unclarity
    """
    from .regex_blocks import likely_negative_regex_list
               
    df= regex_list_capture(df,
         likely_negative_regex_list,
         text_col,
         capture_col='likelyneg_capt',
         regex_block='likelyneg', 
         regex_col='likelyneg_regex',
         override_result=override_result_bool) ## i also moved the "multi-neg" instances, aka lists of no x, y, or z detected, to this for cohesion.
    return(df)


def df_result_binarize(df,staph_bool=True):
    """ 
    mapping enumerated result_binary values into more discrete binary values (0=neg/unclear/null; 1=likely positive)
    """

    neg_binary_bool=df['result_binary'].apply(lambda x: re.search(r'neg',str(x).lower()) is not None)
    pos_binary_bool=df['result_binary'].apply(lambda x: re.search(r'pos',str(x).lower()) is not None)
    desc_binary_bool=df['result_binary'].apply(lambda x: re.search(r'descriptive',str(x).lower()) is not None)
    
     
    df.loc[neg_binary_bool,'result_binary2']='negative'
    #df.loc[desc_binary_bool,'result_binary2']='negative'
    df.loc[pos_binary_bool,'result_binary2']='positive'
    
    df['result_binary2']= df['result_binary'].apply(lambda x: re.split(r'[\_]?x?\d{1,}',x)[0])
    
    df.loc[desc_binary_bool,'result_binary2']='negative'
    
    if staph_bool==False: #if the staph_neg_correction boolean is negative, aka no multiple coag neg staph required for pos, then this is applied as a correction.
        staph_binary_bool=df['result_binary'].apply(lambda x: re.search(r'staph',str(x).lower()) is not None) #including a staph 
        df.loc[staph_binary_bool,'result_binary2']='positive'
    
    df['result_binary2']= df['result_binary2'].apply(lambda x: re.split(r'\/null',x)[0])
    pos_bool= df['result_binary2'].apply(lambda x: re.search(r'pos',x)is not None)
    neg_bool= df['result_binary2'].apply(lambda x: re.search(r'neg',x)is not None)
    df.loc[pos_bool,'result_binary2']='positive'
    df.loc[neg_bool,'result_binary2']='negative'
    #result

    result2_mapper={
            'negative':0,
            'positive':1,
            'unclear':0,
            'not_captured':0,
            'yeast':0,
            'virus':0
        }

    df['result_num']= df['result_binary2'].map(result2_mapper)
    
    return(df)


def final_multiorg_adjustment(df,result_col):
    """
    adjusting final classification, and species_capt for those with the generalized multiple species present and no other info present. 
    ### taking the rows wwith a non-specific multipositive, and possibly some unclea rlanguage, and no species in species_capt. adding unspecified organisms to species list in this case. 
    ### note: i wanted this in the microbio_parser.py but cant get a higher version of pd to run on the cmd.
    """
    ### adding multiple_organisms present
    t1= df[['pos_qual_capt']].explode('pos_qual_capt')#[UC_culture_cat['pos_qual_capt'].explode()=='multiple organisms present']
    t1_index=t1[t1['pos_qual_capt']=='multiple organisms present'].index

    df.loc[t1_index,'result_num']=1 #adjusting the resultnum to be positive if multiorg is present. 
    df.loc[t1_index,result_col]='multiorg_pos1'

    ### taking the rows wwith a non-specific multipositive, and possibly some unclea rlanguage, and no species in species_capt. adding unspecified organisms to species list in this case. 
    t3=df.loc[t1_index,'species_capt'].explode()
    t3_index=t3[t3.isna()].index
    df.loc[t3_index,'species_capt'].apply(lambda x: x.append('unspecified organisms'))
    return(df)



def add_review_suggestion_flags(df,
                                text_col, #species_list=species_regex_list, 
                                result_col):
    
    """
    attempt to add on some logical "manual review suggested" flags onto cases to reduce false positive/negative classifications. currently
    flags cases with "flora" in text, >=1 species capture, and currently classifid as negative. inspired by some challenging to classify cases in our 2d validation set. 
    """
        ### flora flag testing
    flora_bool1=df[text_col].apply(lambda x: re.search(r'flora',str(x).lower())is not None)
    flora_bool2=df['species_capt'].apply(lambda x: len(x))>0
    flora_bool3= df['result_num']==0
    flora_flag= (flora_bool1) & (flora_bool2) & (flora_bool3) 
    
    df['flora_flag']=0
    df.loc[flora_flag,'flora_flag']=1
    return(df)



def OHDSI_ID_MAP(x):
    """
    function to map OHSDI concept ID based on the dictionary in OHDSI_MAP
    """
    from .OHDSI_MAP import OHDSI_MAP
    if x in OHDSI_MAP.keys():
        value= OHDSI_MAP[x]
    else:
        value=999999999
    return(value)

def OHDSI_NAME_MAP(x):
    """
    function to map OHSDI concept names based on the dictionary in OHDSI_MAP
    """
    from .OHDSI_MAP import OHDSI_NAME
    if x in OHDSI_NAME.keys():
        value= OHDSI_NAME[x]
    else:
        value='not_OHDSI_mapped'
    return(value)


def result_categorize_main(df, text_col_main='parsed_note', 
                           staph_nunique_col='procedure_order_key',
                           culture_id_main='visit_id', 
                           result_col_main='result_binary',
                           visit_id='visit_id', #this should be changed if there are multiple cultures per visit.
                           staph_neg_correction=True, 
                           notetype_main=None, 
                           quant_col=None, 
                           specimen_col=None,
                          likely_neg_to_neg_override=False):
    
    """
    retooled version of categorize 2 and 3 into same framework to help with more logical workflow.
    uses 6 step parsing now:
    
    1: parses blatent negative results and non-bacterial species.
    2: splitting the already parsed negatives out so "negative for x" type notes aren't included in downstream parsings
    3: parses unspecific positive rows. greedy but will be overwritten by more specific parsings later when possible
    4: parses species specific positives.
    5: parses staph positives into more granular info
    6: parses out any row with unclear language. eg "unable to determine presence or absence of staph..."
    staph_neg_correction: default True. True means the staph_neg correction runs, aka requires multiple instances of coag_neg to = outcome positive. False: all staph = Positive regardless of type or # of occurances.
    
    likely_neg_to_neg_override: default False for likelyneg, likelyneg captures impact classification -> negative. if True, likelyneg captures don't influence classification. 

    """
#     from .regex_blocks import species_regex_list
    import time  
    
    print('step0.1')
    #########step0.1: assign a baseline value for new columns to be overwritten:
    newcol_list=[result_col_main,
                 'regex_capture_quant',
             'regex_capture_specimen',
             'regex_text',
             'regex_source',
             'regex_capture',
             'species_regex',
             'result_binary2',
             'result_num']
    
    for element in newcol_list:
        df[element]='not_captured'
        
    print('step0.2') 
    ########step0.2: uses value_map_dic 1 and 2 to substitute out common abbreviations and formatting to more parser friendly formatting. 
    df=culture_abbreviation_map(df, text_col_main)
    
    print('step0.3')
    ########step0.3&0.4: parses quantitative info and specimen info when possible.
    if quant_col!=None:
        quant_col_param=quant_col
    else:
        quant_col_param=text_col_main
        
    df= general_quant_extract(df, text_col=quant_col_param)
        
    print('step0.4')
    if specimen_col!=None:
        specimen_col_param=specimen_col
    else:
        specimen_col_param=text_col_main
        
    df=specimen_extract(df, text_col=specimen_col_param)
        
    
    ########step1: parses blatent negative results and non-bacterial species.
    tic = time.perf_counter()
    print('step1')
    df =negative_classifier(df, text_col=text_col_main, result_col=result_col_main, species_name='species' )
    toc = time.perf_counter()
    print(f"negative_classifier: {toc - tic:0.4f} seconds")
    
    ########step2: splitting the parsed negatives out so "negative for x" type notes aren't flagged as false positives. also splits virus and yeast out as well    
    tic = time.perf_counter()
    print('step2')
    
    
    df, df_neg =df_split_regex(df, result_binary_regex_split=r'neg')  
    df, df_yeast =df_split_regex(df, result_binary_regex_split=r'yeast')
    df, df_virus =df_split_regex(df, result_binary_regex_split=r'virus')  
   
    ### combining df_neg + virus + yeast back together
    df_neg=df_concat(df_neg, df_yeast)
    df_neg=df_concat(df_neg, df_virus)
    
    toc = time.perf_counter()
    print(f"virus, neg, yeast, etc...: {toc - tic:0.4f} seconds")
    
        
    ########step2.1: adding species captures on negatives without changing result_col, aka binary outcome. 
    tic = time.perf_counter()
    print('step2.1')    
    df_neg= pos_species_cat(df_neg,
                        text_col=text_col_main, #species_list=species_regex_list, 
                        notetype_col=notetype_main,
                        override_result_bool=True)

    df_neg= staph_classifier(df=df_neg, coag_neg_correction=staph_neg_correction,
                             text_col=text_col_main,
                             result_col=result_col_main, override_result=True)    
    
    

        ####8/9/21 adding rows with a yeast/virus + no negative captures + >=1 other species present. 
#     elementwise_virusyeastlen= df_neg['yeast_capt'].apply(lambda x: len(x)).combine(df_neg['virus_capt'].apply(lambda x: len(x)), max)
    elementwise_yeastlen=df_neg['yeast_capt'].apply(lambda x: len(x))
    elementwise_viruslen=df_neg['virus_capt'].apply(lambda x: len(x))
    elementwise_virusyeastlen=pd.concat([elementwise_yeastlen, elementwise_viruslen], axis=1, sort=True).max(axis=1)

    elementwise_specieslen=df_neg['species_capt'].apply(lambda x: len(x))
    elementwise_neglen=df_neg['negative_capt'].apply(lambda x: len(x))
    

    exemption_cid= df_neg.loc[(elementwise_virusyeastlen>0) & (elementwise_specieslen>0) & (elementwise_neglen==0), culture_id_main].to_list()
    df_neg_exemption= df_neg[df_neg[culture_id_main].isin(exemption_cid)].copy()
    df_neg= df_neg[~df_neg[culture_id_main].isin(exemption_cid)].copy()

    
    df=df_concat(df, df_neg_exemption)
     
    
    #####todo figure out why some negs are making it over in the concat that are not in exemption. 
    


    print('n= {} rows ({} unique cultures) added back from the neg list via virus/yeast + bacerial species exemption'.format(len(df_neg_exemption),df_neg_exemption[culture_id_main].nunique()))
    
    toc = time.perf_counter()
    print(f"negative species capture...: {toc - tic:0.4f} seconds")
        
    ########step3: unspecific pos regex:
    tic = time.perf_counter()
    print('step3')
    df= unspecific_pos_cat(df, text_col=text_col_main)
    toc = time.perf_counter()
    print(f"unspecific positive: {toc - tic:0.4f} seconds")
    
    ########step4: specific species based pos regex:   
    tic = time.perf_counter()
    print('step4')
    df= pos_species_cat(df, text_col=text_col_main, #species_list=species_regex_list, 
                        notetype_col=notetype_main)
    toc = time.perf_counter()
    print(f"species specific captures: {toc - tic:0.4f} seconds")
    

    ########step5: specific staph parsings:
   
    tic = time.perf_counter()
    print('step5')
    df= staph_classifier(df,coag_neg_correction=staph_neg_correction,
                         text_col=text_col_main, result_col=result_col_main, override_result=False) #doing staph parsings
    if staph_neg_correction==True:
        df= staph_coag_neg_correction(df,
                                      text_col=text_col_main,
                                      result_col=result_col_main,
                                      time_col=staph_nunique_col,
                                      culture_id=visit_id
                                     ) ### accounting for multiple instances of staph coag negatives or other neg staph as contaminants
        toc = time.perf_counter()
        print(f"staph classifier: {toc - tic:0.4f} seconds")
        
    
    
    ########step6: final pass to categorize value col with unclear language:
    tic = time.perf_counter()
    print('step6')
    df=unclear_cat(df, text_col=text_col_main)
    #part of the unclear parsing: either likely negative or more nuanced negatives (eg "no x,y,z detected")
    df= likelyneg_cat(df, text_col=text_col_main,
                     override_result_bool=likely_neg_to_neg_override)
        
    df.loc[(df['result_binary']=='not_captured')&(df['regex_capture_quant'].notnull()),'regex_capture_quant']= 'note not otherwise categorized'
    toc = time.perf_counter()
    print(f"unclear and likely negative: {toc - tic:0.4f} seconds")
    

    
    ########step6.1: add unspecific_positive to species list for rows with only non-specific positive captures
    df.loc[df['result_binary'].apply(lambda x: re.search(r'unspecific',str(x))is not None),'species_capt'].apply(lambda x: x.append('positive_unspecific'))
    
                
    #concating the negative classified back in (yeast+virus+neg were concatenated previously)
    df=df_concat(df, df_neg)
    
    ### adding a unspecified organism marker for multipos cases without any specified species
    df=final_multiorg_adjustment(df,
                              result_col=result_col_main)
    
    ###making a all virus+yeast+bacteria species captured column.
    df['species_capt_all']=df['species_capt']+df['yeast_capt']
    df['species_capt_all']=df['species_capt_all']+df['virus_capt']
    
    
    ###9/10/21 OHDSI
    ### mapping to OHDSI
    df['OHDSI_ID']=df['species_capt_all'].apply(lambda x: [OHDSI_ID_MAP(y) for y in x])
    df['OHDSI_Concept']=df['species_capt_all'].apply(lambda x: [OHDSI_NAME_MAP(y) for y in x])
    
      
    
    ##binarizing parsed classification
    df=df_result_binarize(df)
    

    df= add_review_suggestion_flags(df,
                                    text_col=text_col_main, #species_list=species_regex_list, 
                                    result_col=result_col_main
                                   )
    
    
    return(df)



