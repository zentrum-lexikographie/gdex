__version__ = '0.1.0'

from .quaxa import (
    total_score,
    isa_knockout_criteria,
    factor_gradual_criteria,
    has_finite_verb_and_subject,
    is_misparsed,
    has_illegal_chars,
    has_blacklist_words, BLACKLIST_WORDS_DE,
    factor_rarechars, RARE_CHARS_DE, ORD_RARE_CHARS_DE,
    factor_notkeyboardchar, QWERTZ_DE, ORDS_QWERTZ_DE,
    factor_graylist_words,
    factor_named_entity,
    deixis_space, DEFAULT_SPACE_DEIXIS_TERMS,
    deixis_time, DEFAULT_TIME_DEIXIS_TERMS,
    deixis_person,
    optimal_interval
)
