import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Set

from spacy.tokens.doc import Doc
from spacy.tokens.span import Span
from spacy.tokens.token import Token

from .version import __version__

_DEFAULT_ILLEGAL_CHARS = "<>|[]{}/\\^@·•"
_DEFAULT_RARE_CHARS = "'’‘)(_+*~#°§%&€£$¥…©®™"

Span.set_extension("gdex", default=0.0)
if not Token.has_extension("is_hit"):
    Token.set_extension("is_hit", default=False)


@dataclass
class SentenceScorer:
    illegal_chars: Set[str] = field(
        default_factory=lambda: set(_DEFAULT_ILLEGAL_CHARS), repr=False
    )
    keyboard_chars: Set[str] = field(default_factory=set, repr=False)
    rare_chars: Set[str] = field(
        default_factory=lambda: set(_DEFAULT_RARE_CHARS), repr=False
    )

    has_finite_verb_and_subject: Callable[[Span], bool] = lambda sent: True
    is_misparsed: Callable[[Span], bool] = lambda sent: False
    is_deixis: Callable[[Token], bool] = lambda token: False
    num_entities: Callable[[Span], int] = lambda sent: 0
    is_hypotactic: Callable[[Span], bool] = lambda sent: False
    hit_in_subordinate_clause: Callable[[Span], bool] = lambda sent: False

    whitelist: Set[str] = field(default_factory=set, repr=False)
    blacklist: Set[str] = field(default_factory=set, repr=False)

    optimal_min_len: int = 10
    optimal_max_len: int = 20

    penalty_blacklist: float = 0.1667  # 1/6
    penalty_named_entity: float = 0.1667  # 1/6
    penalty_rare_char: float = 0.125  # 1/(2**3)
    penalty_hypotaxis: float = 0.0625  # 1/(2**4), doubled if hit_in_subordinate_clause
    penalty_deixis: float = 0.03125  # 1/(2**5)

    def score_sentence(self, sent: Span) -> float:
        score = 0.5 * self.has_no_knockout_criterion(sent)
        score += 0.5 * self.factor_gradual_criteria(sent)
        return score

    def __call__(self, doc: Doc) -> Doc:
        for sent in doc.sents:
            sent._.gdex = self.score_sentence(sent)
        return doc

    def has_no_knockout_criterion(self, sent):
        if self.has_illegal_chars(sent):
            return False
        if self.is_misparsed(sent):
            return False
        if not self.has_finite_verb_and_subject(sent):
            return False
        return True

    def factor_gradual_criteria(self, sent):
        factor = 1.0
        if self.penalty_blacklist is not None:
            factor *= self.factor_blacklist(sent)
        if len(self.whitelist) > 0:
            factor *= self.factor_rarelemmas(sent)
        if self.penalty_rare_char is not None:
            factor *= self.factor_rarechars(sent)
        if len(self.keyboard_chars) > 0:
            factor *= self.factor_notkeyboardchar(sent)
        if self.penalty_named_entity is not None:
            factor *= self.factor_named_entities(sent)
        if self.optimal_min_len is not None and self.optimal_max_len is not None:
            factor *= self.factor_optimal_interval(sent)
        if self.penalty_deixis is not None:
            factor *= self.factor_deixis(sent)
        if self.penalty_hypotaxis is not None:
            factor *= self.factor_hypotaxis(sent)
        return factor

    def has_illegal_chars(self, sent: Span):
        for c in sent.text:
            if ord(c) < 32:
                # any ASCII/Unicode control characers, e.g. newline \n
                return True
            if c in self.illegal_chars:
                return True
        return False

    def factor_rarechars(self, sent: Span):
        num_matches = len([c for c in sent.text if c in self.rare_chars])
        return max(0.0, 1.0 - self.penalty_rare_char * num_matches)

    def factor_notkeyboardchar(self, sent: Span):
        txt = sent.text
        return (sum((1 for c in txt if c in self.keyboard_chars)) / len(txt)) ** 2

    def factor_named_entities(self, sent: Span):
        return max(0.0, 1.0 - self.penalty_named_entity * self.num_entities(sent))

    def factor_tokens(
        self,
        sent: Span,
        pred: Callable[[Token], bool],
        penalty_factor: float,
    ) -> float:
        num_matches = sum((1 for t in sent if not t._.is_hit and pred(t)))
        return max(0.0, 1.0 - penalty_factor * num_matches)

    def factor_blacklist(self, sent: Span):
        return self.factor_tokens(
            sent, lambda t: t.lemma_ in self.blacklist, self.penalty_blacklist
        )

    def factor_rarelemmas(self, sent: Span):
        return sum(
            (
                1
                for t in sent
                if t._.is_hit
                or t.pos_ in {"PUNCT", "DET", "PRON", "ADP", "CCONJ", "SCONJ"}
                or t.tag_ == "PROAV"
                or t.lemma_ in self.whitelist
            )
        ) / len(sent)

    def factor_optimal_interval(self, sent: Span) -> float:
        low = self.optimal_min_len
        high = self.optimal_max_len
        num_tokens = len(sent)

        if low <= num_tokens <= high:
            return 1.0
        elif num_tokens < low:
            if num_tokens < low / 2.0:
                return 0.0
            else:
                diff = low - num_tokens
                return 1 - diff * (1.0 / (low / 2.0))
        else:
            if num_tokens > (2 * high):
                return 0.0
            diff = (2 * high) - num_tokens
            return diff / high

    def factor_deixis(self, sent: Span):
        return self.factor_tokens(sent, self.is_deixis, self.penalty_deixis)

    def factor_hypotaxis(self, sent: Span) -> float:
        factor = 1.0
        if self.hit_in_subordinate_clause(sent):  # implies hypotaxis
            factor -= 2 * self.penalty_hypotaxis
        elif self.is_hypotactic(sent):
            factor -= self.penalty_hypotaxis
        return max(0.0, factor)


def _de_has_finite_verb_and_subject(sent: Span) -> bool:
    for root in sent:
        if root.dep_ != "ROOT":
            continue
        for finite_verb in (root, *root.children):
            if finite_verb.pos_ not in {"AUX", "VERB"}:
                continue
            if "Fin" not in finite_verb.morph.get(
                "VerbForm", []
            ) and not finite_verb.tag_.endswith("FIN"):
                continue
            for subject in (*finite_verb.children, *root.children):
                if subject.dep_ in {"sb", "nsubj"} and subject.pos_ in {
                    "NOUN",
                    "PROPN",
                    "PRON",
                }:
                    return True
    return False


def _de_is_misparsed(sent: Span) -> bool:
    tokens = list(sent)

    first_token = tokens[0]
    if first_token.pos_ == "PUNCT":
        return True

    first_token_text = first_token.text
    if first_token_text.isspace() or first_token_text.islower():
        return True

    last_token = tokens[-1]
    if last_token.text not in {".", "?", "!"}:
        return True

    if (sum((1 for t in tokens if t.tag_ == "$(")) % 2) != 0:
        return True

    return False


# spatial/directional and temporal deixis terms
_DE_SPACE_TIME_DEIXIS_TERMS = {
    "hier",
    "dort",
    "dorthin",
    "da",  # not if SCONJ
    "dahin",
    "jetzt",
    "gestern",
    "daraufhin",
    "bald",
    "anschließend",
    "damals",
    "einst",
    "kürzlich",
    "neulich",
}

# additional deictic expressions — to be penalized only if token.is_sent_start
_DE_DEIXIS_TERMS_AT_START = {
    "später",
    "spätere",
    "heute",
    "vorgestern",
    "morgen",
    "übermorgen",
    "dann",
    "danach",
    "hinterher",
    "deshalb",  # causal
    "deswegen",  # causal
    "damit",  # instrumental; not if SCONJ
}
# reference: https://grammis.ids-mannheim.de/terminologie/717

_DE_PERSON_DEIXIS_PRON_TYPES = {"Prs", "Dem", "Ind", "Neg", "Tot"}


def _de_is_deixis(token: Token) -> bool:
    if (
        token.pos_ == "PRON"
        and token.morph.get("PronType", [""])[0] in _DE_PERSON_DEIXIS_PRON_TYPES
    ):
        return True
    if token.pos_ == "SCONJ":
        return False
    if token.text.lower() in _DE_SPACE_TIME_DEIXIS_TERMS:
        return True
    if token.is_sent_start and token.text.lower() in _DE_DEIXIS_TERMS_AT_START:
        return True
    return False


def _de_core_num_entities(sent: Span):
    return len(sent.ents)


def _de_hdt_num_entities(sent: Span):
    return sum((1 for t in sent if t.pos_ == "PROPN"))


# aim: identify sentences with VL subordinate clauses
_DE_HDT_HYPO_DEPS = {"acl", "advcl", "ccomp", "csubj"}


def _de_hdt_is_hypotactic(sent: Span) -> bool:
    deps = {t.dep_ for t in sent}
    if deps.isdisjoint(_DE_HDT_HYPO_DEPS):
        return False
    return True


def _de_hdt_hit_in_subordinate_clause(sent: Span) -> bool:
    hit_indices = {t.i for t in sent if t._.is_hit}
    if not hit_indices:
        return False
    subclause_indices = set()
    for token in sent:
        if token.dep_ in _DE_HDT_HYPO_DEPS:
            subtree_indices = {t.i for t in token.subtree}
            if sent[0].i in subtree_indices:
                # exempt from this penalty, as a prominent placement is likely
                continue
            subclause_indices.update(subtree_indices)
    if hit_indices.issubset(subclause_indices):
        return True
    return False  # at least one hit in main clause or in exempted sub. clause


_QWERTZ_DE = set(
    (
        "^1234567890ß'qwertzuiopü+asdfghjklöä#<yxcvbnm,.-°!\"§$%&/()=?`"
        "QWERTZUIOPÜ*ASDFGHJKLÖÄ'>YXCVBNM;:_′¹²³¼½¬{[]}\\¸@ł€¶ŧ←↓→øþ\""
        "~æſðđŋħ̣ĸł˝^’|»«¢„“”µ·…–″¡⅛£¤⅜⅝⅞™±°¿˛ΩŁ€®Ŧ¥↑ıØÞ°¯ÆẞÐªŊĦ˙&Ł̣̣˘›‹©‚‘’º×÷— "
    )
)

# most frequent DWDS lemmata (disjoint with vulgar words)
_de_whitelist_file = (Path(__file__) / ".." / "de_whitelist.txt").resolve()
_de_whitelist = set(_de_whitelist_file.read_text(encoding="utf-8").splitlines())

_de_vulger_file = (Path(__file__) / ".." / "VulGer.csv").resolve()
_de_vulger_blacklist = set()

with _de_vulger_file.open(encoding="utf-8") as vulger:
    for n, (word, score) in enumerate(csv.reader(vulger)):
        if n == 0:
            continue
        if float(score) > 0:
            continue
        _de_vulger_blacklist.add(word)

de_core = SentenceScorer(
    has_finite_verb_and_subject=_de_has_finite_verb_and_subject,
    is_misparsed=_de_is_misparsed,
    is_deixis=_de_is_deixis,
    num_entities=_de_core_num_entities,
    keyboard_chars=_QWERTZ_DE,
    whitelist=_de_whitelist,
    blacklist=_de_vulger_blacklist,
)

de_hdt = SentenceScorer(
    has_finite_verb_and_subject=_de_has_finite_verb_and_subject,
    is_misparsed=_de_is_misparsed,
    is_deixis=_de_is_deixis,
    num_entities=_de_hdt_num_entities,
    keyboard_chars=_QWERTZ_DE,
    whitelist=_de_whitelist,
    blacklist=_de_vulger_blacklist,
    is_hypotactic=_de_hdt_is_hypotactic,
    hit_in_subordinate_clause=_de_hdt_hit_in_subordinate_clause,
)

__all__ = ["SentenceScorer", "de_core", "de_hdt"]
