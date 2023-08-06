

##### dictionary of commonly observed acronyms in microbiology reports. 
##note: these are highly dependant on institutional culture and writing styles, so these may need to be adjusted for a given institution. 
value_map_dict={
    'CANALB': 'Candida albicans',
    'STAEPI':'staphylococcus epidermidis',
    'YNCRY':' Many Yeast, Not Cryptococcus Species',
    'STACN': 'staphylococcus coagulase negative',
    'GPC': 'gram positive cocci',
    'CANTRO':'candida tropicalis',
    'STAHOM':'staphylococcus hominis',
    'STREP G':'Beta Hemolytic Streptococci',
    'GNR':'Gram Negative Rods',
    'STRPNE':'Streptococcus pneumoniae Growth',
    'STRP A':'Streptococcus pyogenes',
    'CANDUB':'Candida dubliniensis',
    'SA':'Staphylococcus aureus',
    'CANPARAP':'Candida parapsilosis',
    'PROMIR':'Proteus mirabilis',

    'STRMITIS':'Streptococcus mitis',
    'CANGLA':'Candida glabrata',
    'STREP C':'Beta Hemolytic Streptococci, Group C',
    'STREP A':'Streptococcus pyogenes (Group A)',
    'ENTCLOC':'Enterobacter cloacae',

    'KLEOXY':'Klebsiella oxytoca',
    'GORSPU':'Gordonia sputi',
    'CANKRU':'Candida krusei',
    'GPR':'Gram Positive Rods',
    'CANLUS':'Candida lusitaniae',

    'STEMAL':'Stenotrophomonas maltophilia',
    'SERMAR':'Serratia marcescens',
    'ASPER':'Aspergillus species',
    'STOMA':'Stomatococcus species',
    'MORMOR':'Morganella morganii',
    'ENTAVI':'Enterococcus avium',
    'CLOSDI':'clostridium difficile',
    'pmirbl': 'Proteus mirabilis',
    'PMIRBL': 'Proteus mirabilis',
    'organism identification: sa':'organism identification: staphylococcus aureus',
    'PROACN': 'propionibacterium acnes',
    
    'LACT': 'lactobacillus',
    'STACN': 'staphylococcus coagulase negative',
    'ENTFAECA': 'enterococcus faecalis',
    'CNS': 'coagulase negative staphylococci'   
}

# same idea as above but targets the most prevelent bacteria in the abbreviated species format to map to full name format
# value_map_dict2={
#     'k. pneumoniae': 'klebsiella pneumoniae',
#     'e. coli': 'escherichia coli',
#     'e. cloacae': 'enterobacter cloacae',
#     'a. baumannii': 'acinetobacter baumannii',
#     's. aureus': 'staphylococcus aureus',
#     's. pyogenes': 'streptococcus pyogenes',
#     'p. aeruginosa': 'pseudomonas aeruginosa',
#     'ps. aeruginosa': 'pseudomonas aeruginosa',
#     'h. influenzae': 'haemophilus influenzae',
#     'm. catarrhalis': 'moraxella catarrhalis',
#     'l. pneumophila': 'legionella pneumophila',
#     'la pneumophila': 'legionella pneumophila',
# }
value_map_dict2={
    
    r'\bk\.\b pneumoniae': 'klebsiella pneumoniae',
    r'\be\.\b coli': 'escherichia coli',
    r'\be\.\b cloacae': 'enterobacter cloacae',
    r'\ba\.\b baumannii': 'acinetobacter baumannii',
    r'\bs\.\b aureus': 'staphylococcus aureus',
    r'\bs\.\b pyogenes': 'streptococcus pyogenes',
    r'\bps?\.\b aeruginosa': 'pseudomonas aeruginosa',
    r'\bh\.\b influenzae': 'haemophilus influenzae',
    r'\bm\.\b catarrhalis': 'moraxella catarrhalis',
    r'\bla?\.?\b pneumophila': 'legionella pneumophila',
    
    ###updated regex below, included together to be comprehensive
    r'\bk\.\s?pneumoniae': 'klebsiella pneumoniae',
    r'\be\.\s?coli': 'escherichia coli',
    r'\be\.\s?cloacae': 'enterobacter cloacae',
    r'\ba\.\s?baumannii': 'acinetobacter baumannii',
    r'\bs\.\s?aureus': 'staphylococcus aureus',
    r'\bs\.\s?pyogenes': 'streptococcus pyogenes',
    r'\bps?\.\s?aeruginosa': 'pseudomonas aeruginosa',
    r'\bh\.\s?influenzae': 'haemophilus influenzae',
    r'\bm\.\s?catarrhalis': 'moraxella catarrhalis',
    r'\bla?\.?\s?pneumophila': 'legionella pneumophila',
}


########descriptive capture regex blocks########


#### synonyms for detected in cultures: (present|isolated|detected|grown|seen|cultured)


#####quant_regex_list: list of regular expressions designed to capture quantitative information regarding bacterial counts
##### note: the captured groups here are descriptive and do not impact infection status categorization.

quant_regex_list=[
    r'\b[\d,]{2,}\s?[\d,]*\b(\s?cfu\/ml)?', #most greedy, goes first and gets overwritten by more specific.
    r'[\d,\s]*\-\s?[\d,]+(\s?cfu\/ml)?',
    r'(>=?|greater than|gt)\s?\b[\d,\s]*\b(\s?cfu\/ml|colonies|colony)?',
    r'(<=?|less than|\blt\b)\s?\b[\d,\s]*\b(\s?cfu\/ml|colonies|colony)?',
    r'1[\*x]?e[2345678](\s?cfu\/ml)?',
    r'\d0,000-\d\d?0,000 cfu(\/ml)?',
    r'(few)\b',
    r'[\d,-]*\s?(colonies|colony)',
]

#####specimen_regex_list: list of regular expressions designed to capture info regarding sample type or sample specimen. eg blood culture.
##### note: the captured groups here are descriptive and do not impact infection status categorization.

specimen_regex_list= [
     r'\b\w*\b\sculture', #most greedy
     r'blood\sculture', #also fairly greedy
     r'(specimen|source|sample):\s?\w*',
     r'(csf|spinal)\s(culture)?',
     r'(tissue|biopsy|fluid|wound)\s(culture)?',
     r'(urine|joint|pleural|peritoneal)\s(culture)?'
     r'pcr',
     r'\bbal\b',
     r'bronchoalveolar\s?(lavage)?',
]


########classification-related capture regex blocks########

#####negative_regex_list: list of regular expressions designed to capture cultures without evidence of bacterial growth or only evidence of virus/fungus, which this classifier considers to be insufficient for a positive classification.
##### note: the captured groups here DO impact classification.

negative_regex_list=[
                    # r'negative for growth',
                     r'negative for', #making this a seperate one for debugging
                     r'no\sgrowth',
                     r'no acid fast bacilli',
                     r'acid fast bacilli negative',
    
                       ####8/23/21: changed to improve specificity. remove capturing "no normal flora"
#                      r'\bnormal\sflora\b',
                     r'(?<!\bno\b\s)(?<!\bnot\b\s)\bnormal\sflora\b',
    
    
#                      r'no\s+([a-zA-Z]+\s*){1,4}((\bisolated\b)|(\bfound\b)|(\bgrow[nth]{1,2}\b)|(\bseen\b)|(\bpresent\b)|(\bdetected\b)|(\bgrown\b)|(\bseen\b)|(\bcultured\b))',
                     #### 8/23/21: changed the \s*->\s+ so that it doesn't capture words starting with no... and requires a space and can't be no normal flora.
#                      r'no\s+([a-zA-Z]+\s*){1,4}((\bisolated\b)|(\bfound\b)|(\bgrow[nth]{1,2}\b)|(\bseen\b)|(\bpresent\b)|(\bdetected\b)|(\bgrown\b)|(\bseen\b)|(\bcultured\b))',
                    r'no\s+(?!normal flora)([a-zA-Z]+\s*){1,4}((\bisolated\b)|(\bfound\b)|(\bgrow[nth]{1,2}\b)|(\bseen\b)|(\bpresent\b)|(\bdetected\b)|(\bgrown\b)|(\bseen\b)|(\bcultured\b))',

                     #r'no\s*([a-zA-Z]+\s*){1,4}((\bisolated\b)|(\bfound\b)|(\bgrow[nth]{1,2}\b)|(\bseen\b))', #removed starting position parameter
    
                     ####8/23/21: changed to improve specificity. remove capturing "no normal xxx flora"
#                      r'normal\s(\s?\w{2,}\s)flora',
                     r'(?<!\bno\b\s)(?<!\bnot\b\s)\bnormal\s(\s?\w{2,}\s)flora',
                     r'no\s(\s?\b\w*[-()\s]*\b){0,6}\s?isolated', ###mildly greedy scrubber to find "no <bacteria species> isolated" 
                     r'culture\s(\s?\b\w*[-()]*\b){0,6}\s?negative',
                     r'no\sgrowth.*\(detection\slevel\sof\s\d+,?\d+\s?colonies', #no growth seen, highly specific to training set format
                     r'^negative$',
                     r'species\snot\sisolated',
                     r'mixed\s\w{0,}\s?flora',
                      ###8/23/21: increased specificity of not detected|indicated to avoid the results specifically referring to antibiotic resistance results. 
#                      r'not\sdetected|indicated',
                     r'(?<!resistance)(?<!susceptibility)\s+not\sdetected|indicated',
    
    
    
                     r':\snegative$', # added to account for a heading with the name of a species: negative. 
                     r'no\s(predominant|prevelant|identifyable|isolated)\s(organism|bacteria|colony|growth)', #covers some fairly niche language
                     r'parasite',
                     r'(?<!un)usual\s(\s?\w{2,}\s)flora', #usual respiratory flora, with protection against unusual
                     #r'normal\s(\s?\w{2,}\s)flora' #normal flora with accomodation of 
   
                       ### 8/23/21 adding a narrow catch for the single line of "no normal flora present", as this alone is inconclusive
                     r'^no normal flora\s?((\bisolated\b)|(\bfound\b)|(\bgrow[nth]{1,2}\b)|(\bseen\b)|(\bpresent\b)|(\bdetected\b)|(\bgrown\b)|(\bseen\b)|(\bcultured\b)|(\bidentified\b))?$',
                    ]

virus_regex_list=[r'virus|influenza[\s$^]+',
                  r'vzv|hsv|hpv',
                  r'herpes',
                  r'varicella'
                 ] #influenza needs to not grab influenzae

yeast_regex_list=[r'yeast',
                  r'candida',
                  r'mold',
                  r'aspergillus',
                  r'fusarium',
                  r'mucorales',
                  r'zygomycetes',
                  r'entomophtorales',
                  r'cryptococcus',
                  r'absidiaceae',
                  r'mucormycosis',
                  r'trichosporon',
                  r'penicillium',
                  r'paecilomyces',
                 ]





#####negative_regex_list: list of regular expressions designed to capture cultures without evidence of bacterial growth or only evidence of virus/fungus, which this classifier considers to be insufficient for a positive classification.


### dictionary of specific staph species[lock] : regex to capture the species [key]
staph_regex_dic={
    "staphylococcus_epidermidis": r'(?=.*\bstaph)(?=.*\b(epidermidis|epidermis))',#r'(?=.*\bstaph)(?=.*\bepidermidis)',
    "staphylococcus_hominis":r'(?=.*\bstaph)(?=.*\bhominis)',
    "staphylococcus_saprophyticus":r'(?=.*\bstaph)(?=.*\bsapro)',
    "staphylococcus_coag_neg":r'(?=.*\bstaph)(?=.*\bcoag\w*\sneg)',
    "staphylococcus_coag_pos":r'(?=.*\bstaph)(?=.*\bcoag\w*\spos)',
    "staphylococcus_aureus":r'(?=.*\bstaph)(?=.*\baureus)',
    "staphylococcus_oxacillin_r":r'(?=.*\bstaph)(?=.*\boxacillin[-\s]?resist|susceptible)',
    "staphylococcus_methicillin_r":r'((?=.*\bstaph)(?=.*\bmethicillin[-\s]?resist|susceptible))|(?=.*\bmrsa)',#r'((?=.*\bstaph)(?=.*\bmethicillin[-\s]?resist))|(?=.*\bmrsa)',
    "staphylococcus_lugdunensis":r'(?=.*\bstaph)(?=.*\blugdun)',
    "presumptive_staphylococcus":r'(?=(presumptive\s?staph)|(staph\w*\spresum))',
    #"staphylococcus_unspecified":r'staph',
}

### dictionary of specific staph species[lock] : classification assigned to the following. 
##note: negative staph can be converted to a positive classification if multiple instances occur. see staph_coag_neg_correction()
staph_classification_dic={
    "staphylococcus_epidermidis":'neg_staph' ,
    "staphylococcus_hominis":'neg_staph',
    "staphylococcus_saprophyticus":'neg_staph',
    "staphylococcus_coag_neg": 'neg_staph',
    "staphylococcus_coag_pos": 'pos_staph' ,
    "staphylococcus_aureus": 'pos_staph' ,
    "staphylococcus_oxacillin_r": 'pos_staph' ,
    "staphylococcus_methicillin_r": 'pos_staph' ,
    "staphylococcus_lugdunensis": 'neg_staph',
    "presumptive_staphylococcus": 'neg_staph',
    #"staphylococcus_unspecified": 'pos_staph_unspecified',
}       



staph_name_dic={
    "staphylococcus_epidermidis":'staphylococcus epidermidis' ,
    "staphylococcus_hominis":'staphylococcus hominis',
    "staphylococcus_saprophyticus":'staphylococcus saprophyticus',
    "staphylococcus_coag_neg": 'staphylococcus coagulase negative',
    "staphylococcus_coag_pos": 'staphylococcus coagulase positive' ,
    "staphylococcus_aureus": 'staphylococcus aureus' ,
    "staphylococcus_oxacillin_r": 'staphylococcus oxacillin resistant' ,
    "staphylococcus_methicillin_r": 'staphylococcus methicillin resistant' ,
    "staphylococcus_lugdunensis": 'staphylococcus lugdunensis',
    "presumptive_staphylococcus": 'presumptive staphylococcus',
    "staphylococcus_unspecified": 'staphylococcus unspecified',
}       



#####pos_quant_list + pos_qual_list: list of regular expressions designed to capture quantitative and qualitiative information that indicates a culture is likely positive for bacterial growth. 

pos_quant_list=[
                r'(moderate|heavy)\s?(?=growth)', ##replacing the above growth with a positive look ahead and capture groups, should improve sensitivity/specificity. removed light growth
                r'>=?\d{1,3},?0?00',
                r'1[\*x]?e[34567]',
                r'>=?100?,?000',
                r'([\d,\s]*cfu\/ml)',
                r'\d0,000-\d\d?0,000 cfu(\/ml)?',
               ]    

pos_qual_list=[ ###can be bolstered up.
                r'(multiple|many|numerous|\d\sor\smore|\d\+|\>\d)\s(organisms|orgs|species|bacteria)\s(present|isolated|detected|grown|seen|cultured)',
                #r'(multiple|many|numerous)\s(organisms|orgs|species|bacteria)\s(present|isolated|detected|grown|seen|cultured)',
                #r'(?<!not)\sdetected', 
                 r'(?<!not)\s(organisms|orgs|species|bacteria)\s(present|isolated|detected|grown|seen|cultured)',# included greedy here since i had the greedy match for this format in negatives. updated 8/10 to include all detected synonyms.
                r'\+\s?mixed bacterial morph',
                r'organism identification: \w+',
                r'^(positive|detected)$',
                r'no normal flora',
]

#multiple|many|numerous org[anisms]{0,6}\spresent|isolated|detected|grown|seen|cultured

###microbiome ontology, test recall. 


#####species_regex_list: list of regular expressions designed to capture occurances of bacterial species specific language. 
##note: unclear language is accounted for after this, so "unable to determine presence of pseudomonas" type notes are ultimately classified as negative. 

species_regex_list=[
                #drug resistance: ### commented out 7/22 to reduce noise and duplicate captures.
#                 r'carbapenem\-?\s?resistant\s?\b\w*\b',
#                 r'cephalosporin\-?\s?resistant\s?\b\w*\b',
#                 r'fluoroquinolone\-?\s?resistant\s?\b\w*\b',
#                 r'cefepime\-?\s?resistant\s?\b\w*\b',
#                 r'multidrug\-?\s?resistant\s?\b\w*\b',
#                 r'vancomycin[-\s]?resistant\s?\b\w*\b',

                #gram neg:
                r'gram\s(\bneg[ative]{0,5}\b)\s(rods|bacteria|organism|species|bacilli|flora)',
                r'pseudomonas\s?(aeruginosa)?',
                r'klebsiella\s?(pneumoniae)?',
                r'escherichia\s?\b\w*\b', #r'escherichia\s?(fergusonii)?',
                r'e\.?\s?coli',
                r'(pantoea)?\s?enterob[acter]*\s?(cloacae)?',
                r'acinetobacter\s?\b\w*\b', #r'acinetobacter/s?(baumannii)?',
                r'burkholderia', #burkholderia cepacia complex
                r'citrobacter\s?(freundii|koseri)?',
    
                #gram pos:
                r'leuconostoc',
                
                #gram variable:
                r'gram\s(\bvariable\b)\s(rods|bacteria|organism|species|bacilli|flora)',

                #gram pos +cocci and/or aerobes:
                r'gram\s(\bpos[itive]{0,5}\b)\s(rods|bacteria|organism|species|bacilli|flora)',
                r'neisseria', ##general nisseria, overwritten by more specific below
                r'(neisseria)?[ ]?gonorrhoeae|gonococci|diplococci',
                r'gram positive cocc[ius]{1,2}',
                r'peptostreptococc[ius]{1,2}', #anaerobic GP involved in mixed infections:
                r'viridans[ ]?(strep)?',
                r'streptococc[ius]{1,2}[ ]?[A-Za-z]*', #gallolyticus
                r'group\s\w\s?beta\sstrep\s', ##adding this to catch "group a beta strep" that is missed by below 
                r'(beta hem[olytic]{0,6} streptococc[ius]{1,2}|streptococc[ius]{1,2})',  #r'(beta hemolytic)?\s?streptococc[ius]{1,2}(,?\sgroup\s\w)?',
                r'gemella[ ]?(streptococc[ius]{1,2})?[ ]?(morbillorum)?',
                r'enterococc[ius]{1,2}', #faecium
                r'micrococc[ius]{1,2}',        
                r'aerococc[ius]{1,2}\s?(viridans)?',        
                r'peptococc[ius]{1,2}', ##anaerobic GP involved in mixed infections:
                r'stomatococc[ius]{1,2}',
                r'(gram positive)?\s?coccobacilli',
                r'(s\.|streptococc[ius]{1,2})\s?pneumoniae',
                r'lactococc[ius]{1,2}',
                r'pneumococci',
                r'meningococc[ius]{1,2}',
                r'cryptococc[ius]{1,2}',
                r'kytococc[ius]{1,2}',
                r'group [abcg] strep|strep \b\w*\b group [abcg]',
        
                r'nocardia[ ]?(farcinica)?',

                #gram-positive anaerobes: 
                    ##Anaerobic infections are typically suppurative, causing abscess formation and tissue necrosis and sometimes septic 
                    ##Usually, multiple species of anaerobes are present in infected tissues; aerobes are frequently also present (mixed anaerobic)
                r'actinomyces',
                r'clostridium',
                r'c.?\s?diff',
                r'clostridia',
                r'clostridioides',
                r'finegoldia', #Oral, respiratory, bone and joint, soft-tissue, and intra-abdominal infections
                r'cutibacterium',
                r'propioni?bacterium\s?(acnes)?', #Foreign body infections
                r'oligella',
                r'trueperella',


                #gram-negative anaerobes:
                r'bacteroides\s?\b\w*\b', #bacteroides capillosus\uniformis\etc. #involved in mixed infections
                r'fusobacterium\s?(nucleatum)?', #involved in mixed infections
                r'porphyromonas',
                r'prevotella', #involved in mixed infections

                ###########other:
                ##GP+ cocci:
                r'granulicatella',
                r'kocuria\s?(species)?',#generally non-pathogenic
                r'abiotrophia|granulicatella',
                r'propionibacterium\s?(acnes)?',
                r'rothia',
                r'brevibact',
    
                r'peptostrep',
                r'bifidobacterium',

                ##GP+ aerobic\rods: five medically important GP rods: Bacillus, Clostridium, Corynebacterium, Listeria, and Gardnerella. 
                #(see other sections for all)
                r'\bbacillus',
                r'corynebacterium',
                r'listeria\s?(monocytogenes)?',

                ##GN +aerobic:
                r'legionella',
                r'\w.?\s?pneumophila',
                r'(haemo[philus]*\s?influenzae|haemo[philus]*\s?parainfluenzae|[para]*influenzae|haemophilus)(?!(\s\w?\s?virus))',
#                 r'haemophilus',
#                 r'haemo[philus]*\s?influenzae|haemo[philus]*\s?parainfluenzae|[para]*influenzae|haemophilus',
#                 r"haemo[philus]*\sinfluenzae",#r"haemophilus influenzae",
#                 r'(haemophilus)?\s?parainfluenzae',      
                r'salmonella',
                r'diphtheroids',
                r'shigella',
                r'yersinia',
                r'cardiobacterium',
                r'typhi',
                r'providencia\s?(stuartii)?',
                r'(steno[trophomonas]*\s?maltophilia|stenotrophomonas|maltophilia)',
                r'(xanth[omonas]*\s?maltophilia|xanthomonas)',
                #r'(stenotrophomonas)?\s?(xanthomonas)?\s?(maltophilia)?', #r'(stenotrophomonas)?\s?(xanthomonas)?\s?maltophilia',
                r'eikenella\s?(corrodens)?',
                r'campylobact[er]{0,2}',
                r'(moraxella\scatarrhalis|moraxella)', #r'(moraxella)?\s?catarrhalis', #gonnorhea
                r'raoultella',
                r'brucella',
                r'alcaligenes',
                
                r'ochrobacterium',
                r'flavobacterium',

                ##GN+ anarobic
                r'lactobacil',
                r'serratia\s?(marcescens)?',
                r'proteus\s?(mirabilis|vulgaris)?',
                r'morganella\s?(morganii)?', #migt need to remove from neg.
                r'hafnia alvei|hafnia',
                r'aeromonas\s?(shigelloides)?',
                r'plesiomonas\s?(shigelloides)?',
                r'pantoea',
                r'pasteurella\s?(multocida)?',
                r'veillonella',
                r'elizabeth\skingella',
    
    
                r'bartonella', #cat scratch fever, other diseases and opportunistic infections

                ##Proteobacteria
                r'burkholderia\s?(cepacia)?',
                r'(achromobacter xylosoxidans|achromobacter)',
                r'bordetella',

                ##GN variable
                r'(gardnerella vaginalis|gardnerella)',
                r'gram variable rod',

                ##Actino
                r'mycobacteri[aum]{1,2}',
                r'tuberculosis',
                r'(?<!no\s)acid fast bacilli\s*(isolated|positive|detected|grown|seen|cultured)',
    

                r'capnocytophaga', #canine bacteria... 
    
                r'rhizobium', # plant based bacteria genus that was found on >1 list of clinically meaningful bacteria
    
                ##chylamydia
                r'chlamyd[iaophl]{2,6}\s?(trachomatis|pneumoniae|psittaci)?',
    
                ##rickets, nonmotile gram neg host-reliant and can't grow in artificial medium
                r'rickettsia',
    
                ##mycoplasma
                r'mycoplasma',
]


#####unclear_regex_list: list of regular expressions designed to capture either uncertain or indeterminate type language that would otherwise be classified as positive or not_captured by the above regex blocks. 

unclear_regex_list=[
    r'culture complete',
    #r'examination of smear for acid fast bacilli negative',
    #r'unable to determine',
    r'(?<!isolated)(?<!isolated )(?<!present)(?<!present )(?<!detected)(?<!detected )(unable to determine)(?!\s?colony count)', ##improved the specificity of the unable to determine. won't capture if a detected word infront or colony count behind.
    r'see (note|below|scanned|comment)',
    r'(left|right) hand',
    r'cannot be performed',
    r'test not performed',
    r'\d\+\s?(wbc|rbc)[\']?s\sseen',
    r'\+\sepithelial\scells',
    r'culture in progress',
    r'neutrop',
    r'contamin', #unconditional contamination, need to check this isn't being too greedy. 
    r'presence.{0,20}absence.{0,40}(cannot|can\'?t)\s?be\s?(determined|detected)', #presence or absence of x can't be determined
    r'comments:\s{0,5}validation studies at labcorp have demonstrated', ### text present in the footer of some notes
    r'comments:\s{0,4}this assay is specific for',
    r'^comments:',
    r'indeterminate',#this MAYYY be a bit greedy. will have to check. from my manual review, the ones that start w/ comments often don't discuss any fidnings, but rather context.
    r"cannot|can'?t be ruled out",
    r'below the detection|lod|limit of detection', 
    
    ##moved from likely_neg. while it likely more appropriately fits under likelyneg label, 
    r'no\s(?=.{0,75},).{0,75},(?=.{0,75}or).{0,75}or(?=(.*?\s.+?isolated)|(.*?\s.+?detected)).*?\.?' #updated multineg, now only works if , + or + 
]


#####likely_negative: list of regular expressions designed to capture either uncertain or indeterminate type language that would otherwise be classified as positive or not_captured by the above regex blocks. 
likely_negative_regex_list=[r'\b(few|rare)\b',
                 #r'<10?,?0?00\s?(colonies)?',
                r'(<=?|less than|\blt\b)\s?\b[\d,]*\s?\b(\s?cfu\/ml|colonies|colony)', #improved above regex to be more specific.
                r'(light)\s?(?=growth)',
                r'no\s(?=.{0,75},).{0,75},(?=.{0,75}or).{0,75}or(?=(.*?\s.+?isolated)|(.*?\s.+?detected)).*?\.?' #updated multineg, now only works if , + or + detected|isolated are within same sentence. 
                            #r'no\s(?=.{0,100},)(?=.{0,100}or)(?=.{0,100}\s(isolated|detected))'
                            #r'no\s(?=.*,)(?=.*or)(?=.*\s(isolated|detected))' #this was origionalyl labeled as a multi-neg. now moved to a likely neg for cohesion
                           ]



#####wiki_clinically_meaningful_bacteria: list of regular expressions designed to capture all bacteria listed in wikipedia's page of clinically important bacteria. https://en.wikipedia.org/wiki/List_of_clinically_important_bacteria

wiki_clinically_meaningful_bacteria=[
    r"acetobacter aurantius",
    r"acinetobacter baumannii",
    r"actinomyces israelii",
    r"agrobacterium radiobacter",
    r"agrobacterium tumefaciens",
    r"anaplasma",
    r"anaplasma phagocytophilum",
    r"azorhizobium caulinodans",
    r"azotobacter vinelandii",
    r"viridans streptococci",

    r"bacillus",
    r"bacillus anthracis",
    r"bacillus brevis",
    r"bacillus cereus",
    r"bacillus fusiformis",
    r"bacillus licheniformis",
    r"bacillus megaterium",
    r"bacillus mycoides",
    r"bacillus stearothermophilus",
    r"bacillus subtilis",
    r"bacillus thuringiensis",
    r"bacteroides",
    r"bacteroides fragilis",
    r"bacteroides gingivalis",
    r"prevotella melaninogenica",
    r"bartonella",
    r"bartonella henselae",
    r"bartonella quintana",
    r"bordetella",
    r"bordetella bronchiseptica",
    r"bordetella pertussis",
    r"borrelia burgdorferi",
    r"brucella",
    r"brucella abortus",
    r"brucella melitensis",
    r"brucella suis",
    r"burkholderia",
    r"burkholderia mallei",
    r"burkholderia pseudomallei",
    r"burkholderia cepacia",

    r"calymmatobacterium granulomatis",
    r"campylobacter",
    r"campylobacter coli",
    r"campylobacter fetus",
    r"campylobacter jejuni",
    r"campylobacter pylori",
    r"chlamydia ",
    r"chlamydia trachomatis",
    r"chlamydophila",
    r"chlamydophila pneumoniae",
    r"chlamydophila psittaci",
    r"clostridium",
    r"clostridium botulinum",
    r"clostridium difficile ",
    r"clostridium perfringens",
    r"clostridium tetani",
    r"corynebacterium",
    r"corynebacterium diphtheriae",
    r"corynebacterium fusiforme ",
    r"coxiella burnetii",

    r"ehrlichia chaffeensis",
    r"ehrlichiosis ewingii infection",
    r"eikenella corrodens",
    r"enterobacter cloacae",
    r"enterococcus",
    r"enterococcus avium",
    r"enterococcus durans",
    r"enterococcus faecalis",
    r"enterococcus faecium",
    r"enterococcus gallinarum",
    r"enterococcus maloratus ",
    r"escherichia coli",

    r"fusobacterium necrophorum",
    r"fusobacterium nucleatum",

    r"gardnerella vaginalis",

    r"haemophilus",
    r"haemophilus ducreyi",
    r"haemo[philus]*\sinfluenzae",#r"haemophilus influenzae",
    r"haemophilus parainfluenzae",
    r"haemophilus pertussis",
    r"haemophilus vaginalis",
    r"helicobacter pylori",

    r"klebsiella pneumoniae",

    r"lactobacillus",
    r"lactobacillus acidophilus",
    r"lactobacillus bulgaricus",
    r"lactobacillus casei",
    r"lactococcus lactis",
    r"legionella pneumophila",
    r"leishmania donovani",
    r"leptospira interrogans",
    r"leptospira noguchii",
    r"listeria monocytogenes",

    r"methanobacterium extroquens",
    r"microbacterium multiforme ",
    r"micrococcus luteus",
    r"moraxella catarrhalis",
    r"mycobacterium",
    r"mycobacterium avium",
    r"mycobacterium bovis",
    r"mycobacterium diphtheriae ",
    r"mycobacterium intracellulare",
    r"mycobacterium leprae",
    r"mycobacterium lepraemurium",
    r"mycobacterium phlei",
    r"mycobacterium smegmatis",
    r"mycobacterium tuberculosis",
    r"mycoplasma",
    r"mycoplasma fermentans",
    r"mycoplasma genitalium",
    r"mycoplasma hominis",
    r"mycoplasma penetrans",
    r"mycoplasma pneumoniae",
    r"mycoplasma mexican ",

    r"neisseria",
    r"neisseria gonorrhoeae",
    r"neisseria meningitidis",

    r"pasteurella",
    r"pasteurella multocida",
    r"pasteurella tularensis",
    r"peptostreptococcus",
    r"porphyromonas gingivalis",
    r"prevotella melaninogenica",
    r"pseudomonas aeruginosa",

    r"rhizobium radiobacter",
    r"rickettsia",
    r"rickettsia prowazekii",
    r"rickettsia psittaci",
    r"rickettsia quintana",
    r"rickettsia rickettsii",
    r"rickettsia trachomae",
    r"rochalimaea",
    r"rochalimaea henselae",
    r"rochalimaea quintana",
    r"rothia dentocariosa",

    r"salmonella",
    r"salmonella enteritidis",
    r"salmonella typhi",
    r"salmonella typhimurium",
    r"serratia marcescens",
    r"shigella dysenteriae",
    r"spirillum volutans",
    r"staphylococcus",
    r"staphylococcus aureus",
    r"staphylococcus epidermidis",
    r"stenotrophomonas maltophilia",
    r"streptococcus",
    r"streptococcus agalactiae",
    r"streptococcus avium",
    r"streptococcus bovis",
    r"streptococcus cricetus",
    r"streptococcus faceium",
    r"streptococcus faecalis",
    r"streptococcus ferus",
    r"streptococcus gallinarum",
    r"streptococcus lactis",
    r"streptococcus mitior",
    r"streptococcus mitis",
    r"streptococcus mutans",
    r"streptococcus oralis",
    r"streptococcus pneumoniae",
    r"streptococcus pyogenes",
    r"streptococcus rattus",
    r"streptococcus salivarius",
    r"streptococcus sanguis",
    r"streptococcus sobrinus",

    r"treponema",

    r"ureaplasma urealyticum",

    r"vibrio",
    r"vibrio cholerae",
    r"vibrio comma ",
    r"vibrio parahaemolyticus",
    r"vibrio vulnificus",

    r"wolbachia",

    r"yersinia",
    r"yersinia enterocolitica",
    r"yersinia pestis",
    r"yersinia pseudotuberculosis"
]


#list of all the unique bacteria in blood cultures at Lurie Children’s since 2012.
LCH_bact_list=[
"streptococcus",
"staphylococcus",
"staphylococcus epidermidis",
"staphylococcus aureus",
"staphylococcus coagulase negative",
"escherichia",
"enterococcus",
"enterobacter",
"klebsiella",
"acinetobacter",
"candida",
"citrobacter",
"corynebacterium",
"fusobacterium",
"haemophilus",
"lactobacillus",
"moraxella",
"propionibacterium",
"proteus",
"pseudomonas",
"stenotrophomonas",
"mycobacterium",
"serratia",
"bacillus",
"abiotrophia",
"clostridium",
"gram negative",
"gram positive",
"hafnia",
"salmonella",
"achromobacter",
"burkholderia",
"micrococcus",
"ochrobacterium",
"trueperella",
"capnocytophaga",
"cardiobacterium",
"eikenella",
"flavobacterium",
"gram variable",
"granulicatella",
"leuconostoc",
"listeria",
"rothia",
"lactococcus",
"brevibact",
"bacteroides",
"peptostrep",
"actinomyces",
"gardnerella",
"aeromonas",
"campylobact",
"fusarium",
"neisseria",
"rhizobium",
"gemella",
"bifidobacterium",
"prevotella",
"morganella",
"pantoea",
"veillonella",
"elizabeth kingella",
"brucella",
"legionella",
"aspergillus",
]