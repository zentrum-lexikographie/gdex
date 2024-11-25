import spacy

import quaxa

de_core_nlp = spacy.load("de_core_news_sm")
de_hdt_nlp = spacy.load("de_hdt_lg")


def scores(s):
    return (quaxa.de_core(de_core_nlp(s)), quaxa.de_hdt(de_hdt_nlp(s)))


def assert_knockout(s):
    for doc in scores(s):
        for sent in doc.sents:
            assert sent._.quaxa <= 0.5


def assert_penalty(factor_method, s, headword=None):
    for nlp, scorer in ((de_core_nlp, quaxa.de_core), (de_hdt_nlp, quaxa.de_hdt)):
        doc = nlp(s)
        for sent in doc.sents:
            if headword is not None:
                assert factor_method(scorer, sent, headword) < 1.0
            else:
                assert factor_method(scorer, sent) < 1.0


def test_scoring():
    docs = scores(
        " ".join(
            (
                "Manasse ist ein einzigartiger Parfümeur.",
                "Ich hatte Gelegenheit eines seiner Seminare zu besuchen.",
                (
                    "7 Tage Erholung im Ferienhaus am Müritz See in einer idyllischen "
                    "Landschaft inmitten der Mecklenburgischen Seenplatte."
                ),
            )
        )
    )
    for doc in docs:
        for sent in doc.sents:
            assert sent._.quaxa >= 0.0 and sent._.quaxa <= 1.0


def test_illegal_chars():
    assert_knockout("Das ist ein Satz mit unzulässigen Zeichen [1].")
    assert_knockout("Gleiches gilt für diesen Satz mit test@test.de.")
    assert_knockout("Gleiches gilt für Sonderzeichen wie\nZeilenumbrüche.")


def test_misparsed():
    assert_knockout("Ein Satz ohne Satzzeichen")
    assert_knockout("ein Satz, der mit Kleinbuchstaben beginnt.")
    assert_knockout(": Ein Satz mit Interpunktion am Anfang.")


def test_finite_verb_and_subject():
    assert_knockout("Achtung!")
    assert_knockout("Jetzt kaufen!")
    assert_knockout("Über uns.")


def test_rarechars():
    factor_method = quaxa.SentenceScorer.factor_rarechars
    assert_penalty(factor_method, "1. Aufzählungen und Zahlen mögen wir nicht.")
    assert_penalty(factor_method, "Worte in Klammern (Paranthese) sind schlecht.")


def test_notkeyboardchar():
    factor_method = quaxa.SentenceScorer.factor_notkeyboardchar
    assert_penalty(factor_method, "Gute Medizin schmeckt, 良药苦口。")


def test_named_entities():
    factor_method = quaxa.SentenceScorer.factor_named_entities
    assert_penalty(factor_method, "Beispiele aus Berlin brauchen wir nicht.")


def test_blacklist():
    factor_method = quaxa.SentenceScorer.factor_blacklist
    assert_penalty(factor_method, "Manche Sätze sind Scheiße.", "Satz")


def test_whitelist():
    factor_method = quaxa.SentenceScorer.factor_whitelist
    assert_penalty(factor_method, "Wir sind alle Idiosynkrasien.", "sein")


def test_optimal_interval():
    factor_method = quaxa.SentenceScorer.factor_optimal_interval
    assert_penalty(factor_method, "Kurz ist doof!")
    assert_penalty(factor_method, "Lang ist auch doof, " * 5 + ", wirklich!")
    assert_penalty(factor_method, "Lang ist auch doof, " * 10 + ", ehrlich!")


def test_deixis():
    factor_method = quaxa.SentenceScorer.factor_deixis
    assert_penalty(factor_method, "Hier ist es schlecht!", "schlecht")
    assert_penalty(factor_method, "Unten und oben ist es auch schlecht!", "schlecht")
    assert_penalty(factor_method, "Jetzt bitte nicht!", "bitte")
