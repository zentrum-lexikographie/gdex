__version__ = '0.1.0'

from .quax import (
    total_score,
    isa_knockout_criteria,
    factor_gradual_criteria,
    is_whole_sentence, 
    is_misparsed, 
    has_illegal_chars, 
    has_blacklist_words, 
    factor_graylist_rarechars, 
    factor_graylist_nongermankeyboardchars, 
    factor_graylist_words, 
    greylist_ne, 
    deixis_space, 
    deixis_time, 
    deixis_person, 
    optimal_interval
)
