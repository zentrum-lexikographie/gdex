import subprocess

import spacy

import gdex

spacy_model_packages = {
    "de_core_news_sm": (
        "de-core-news-sm @ https://github.com/explosion/spacy-models/"
        "releases/download/de_core_news_sm-3.8.0/"
        "de_core_news_sm-3.8.0-py3-none-any.whl"
        "#sha256=fec69fec52b1780f2d269d5af7582a5e28028738bd3190532459aeb473bfa3e7"
    ),
    "de_hdt_dist": (
        "de_hdt_dist @ https://huggingface.co/zentrum-lexikographie/de_hdt_dist/"
        "resolve/main/de_hdt_dist-any-py3-none-any.whl"
        "#sha256=02ba1b5db8c15a06aeea46bab1e248704e4a33aab11ef7846b68fa622393c330"
    ),
}


def spacy_model(model):
    try:
        return spacy.load(model)
    except OSError:
        assert model in spacy_model_packages, model
        subprocess.check_call(["pip", "install", "-qqq", spacy_model_packages[model]])
        return spacy.load(model)


de_core_nlp = spacy_model("de_core_news_sm")
de_hdt_nlp = spacy_model("de_hdt_dist")


def scores(s):
    return (gdex.de_core(de_core_nlp(s)), gdex.de_hdt(de_hdt_nlp(s)))


def assert_knockout(s):
    for doc in scores(s):
        for sent in doc.sents:
            assert sent._.gdex <= 0.5


def assert_penalty(factor_method, s):
    for nlp, scorer in ((de_core_nlp, gdex.de_core), (de_hdt_nlp, gdex.de_hdt)):
        doc = nlp(s)
        for sent in doc.sents:
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
            assert sent._.gdex >= 0.0 and sent._.gdex <= 1.0


def test_hypotaxis_hdt():
    test_sents = [
        ("Hause", "Leider verpasste sie den Anruf, weil sie später nach Hause kam."),
        ("gewittert", "Dass es im Sommer gewittert, kommt nicht selten vor."),
        (None, "Herbstspaziergänge sind besonders schön, wenn es nicht regnet."),
        (
            None,
            (
                "Der uralte Baum, der schon damals hier stand, "
                "gehörte fest in das Stadtbild."
            ),
        ),
        (
            None,
            (
                "Um besser sehen zu können, braucht man eventuell eine Brille, "
                "auch Sehhilfe genannt."
            ),
        ),
        (
            "Pinguine",
            (
                "Alle Pinguine sind flugunfähig, wobei nicht "
                "alle flugunfähigen Vögel Pinguine sind."
            ),
        ),
    ]
    nlp, scorer = de_hdt_nlp, gdex.de_hdt
    for hit, s in test_sents:
        doc = nlp(s)
        if hit is not None:
            for token in doc:
                if token.text == hit:
                    token._.is_hit = True
        for sent in doc.sents:
            score = scorer.factor_hypotaxis(sent)
            if hit == "Hause":
                assert score == 1.0 - 2 * scorer.penalty_hypotaxis
            else:
                assert score == 1.0 - scorer.penalty_hypotaxis


def test_illegal_chars():
    assert_knockout("Das ist ein Satz mit unzulässigen Zeichen [1].")
    assert_knockout("Gleiches gilt für diesen Satz mit test@test.de.")
    assert_knockout("Gleiches gilt für Sonderzeichen wie\nZeilenumbrüche.")


def test_misparsed():
    assert_knockout("Ein Satz ohne Satzzeichen")
    assert_knockout("ein Satz, der mit Kleinbuchstaben beginnt.")
    assert_knockout(": Ein Satz mit Interpunktion am Anfang.")
    assert_knockout("Ein Satz, der nach einem Komma geteilt wurde,")
    assert_knockout("Der nächste Satz gehört inhaltlich eng zu diesem:")
    assert_knockout(
        (
            '"Durch das Kriterium werden auch alle Sätze, die mit '
            'Anführungszeichen beginnen und/oder enden, ausgeschlossen."'
        )
    )
    assert_knockout('Die Kulisse habe "eine malerische Qualität."')


def test_finite_verb_and_subject():
    assert_knockout("Achtung!")
    assert_knockout("Jetzt kaufen!")
    assert_knockout("Über uns.")


def test_rarechars():
    factor_method = gdex.SentenceScorer.factor_rarechars
    assert_penalty(factor_method, "Für Zeichen wie + & € gibt es Punktabzug.")
    assert_penalty(factor_method, "Auch Klammern (Parenthese) sind nicht ideal.")


def test_notkeyboardchar():
    factor_method = gdex.SentenceScorer.factor_notkeyboardchar
    assert_penalty(factor_method, "Gute Medizin schmeckt, 良药苦口。")


def test_named_entities():
    factor_method = gdex.SentenceScorer.factor_named_entities
    assert_penalty(factor_method, "Beispiele aus Berlin brauchen wir nicht.")


def test_blacklist():
    factor_method = gdex.SentenceScorer.factor_blacklist
    assert_penalty(factor_method, "Manche Sätze sind Trash.")


def test_rarelemmas():
    factor_method = gdex.SentenceScorer.factor_rarelemmas
    assert_penalty(factor_method, "Wir sind alle Idiosynkrasien.")


def test_optimal_interval():
    factor_method = gdex.SentenceScorer.factor_optimal_interval
    assert_penalty(factor_method, "Kurz ist doof!")
    assert_penalty(factor_method, "Lang ist auch doof, " * 5 + ", wirklich!")
    assert_penalty(factor_method, "Lang ist auch doof, " * 10 + ", ehrlich!")


def test_deixis():
    factor_method = gdex.SentenceScorer.factor_deixis
    assert_penalty(factor_method, "Hier ist es schlecht!")
    assert_penalty(factor_method, "Unten und oben ist es auch schlecht!")
    assert_penalty(factor_method, "Jetzt bitte nicht!")
