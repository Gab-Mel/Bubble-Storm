import spacy
from spacy.matcher import Matcher
import re
from collections import Counter
import random

nlp = spacy.load("pt_core_news_md")
matcher = Matcher(nlp.vocab)

meses = [
    "janeiro",
    "fevereiro",
    "março",
    "abril",
    "maio",
    "junho",
    "julho",
    "agosto",
    "setembro",
    "outubro",
    "novembro",
    "dezembro",
]

pattern_month_year = [{"LOWER": {"IN": meses}}, {"LOWER": "de"}, {"LIKE_NUM": True}]
pattern_day_month_year = [
    {"LIKE_NUM": True},
    {"LOWER": "de"},
    {"LOWER": {"IN": meses}},
    {"LOWER": "de"},
    {"LIKE_NUM": True},
]
matcher.add(
    "date",
    [pattern_day_month_year, pattern_month_year],
)


def get_token_morph(morph):
    gender = morph.get("Gender")
    number = morph.get("Number")

    feminine = gender[0] == "Fem" if len(gender) == 1 else False
    plural = number[0] == "Plur" if len(number) == 1 else False

    return feminine, plural


def get_determinant(feminine, plural):
    if plural:
        return "as" if feminine else "os"
    else:
        return "a" if feminine else "o"


def generate_relation_questions(doc, n):
    questions = set()
    entities = set((ent.text, ent[0].morph) for ent in doc.ents)

    for _ in range(n):
        ent1, morph1 = random.sample(entities, 1)[0]
        ent2, morph2 = random.sample(entities, 1)[0]

        if ent1 != ent2:
            feminine1, plural1 = get_token_morph(morph1)
            feminine2, plural2 = get_token_morph(morph2)

            det1 = get_determinant(feminine1, plural1)
            det2 = get_determinant(feminine2, plural2)

            questions.add(f"Qual a relação entre {det1} {ent1} e {det2} {ent2}?")

    return questions


def generate_who_questions(doc, n):
    questions = set()
    entities = set((ent.text, ent[0].morph) for ent in doc.ents if ent.label_ == "PER")

    if len(entities) == 0:
        return questions

    for _ in range(n):
        ent, morph = random.sample(entities, 1)[0]
        _, plural = get_token_morph(morph)

        if plural:
            questions.add(f"Quem foram {ent}?")
        else:
            questions.add(f"Quem foi {ent}?")

    return questions


def generate_date_questions(doc, n):
    questions = set()
    matches = matcher(doc)

    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]

        if string_id == "date":
            questions.add(f"O que ocorreu em {span.text}?")

    if len(questions) > n:
        return random.sample(questions, n)

    return questions


def generate_questions(text, n):
    text = re.sub(r"\[\d+\]", "", text)
    doc = nlp(text)

    questions = set()

    questions.update(generate_relation_questions(doc, n))
    questions.update(generate_who_questions(doc, n))
    questions.update(generate_date_questions(doc, n))

    entities = set((ent.text, ent[0].morph, ent.label_) for ent in doc.ents if ent.label_ != "PER")

    for text, morph, label in entities:
        feminine, plural = get_token_morph(morph)
        det = get_determinant(feminine, plural)

        questions.add(f"Explicar {det} {text} no contexto do texto.")
        if plural:
            questions.add(f"O que foram {det} {text}?")
        else:
            questions.add(f"O que foi {det} {text}?")

    if len(questions) > n:
        return random.sample(questions, n)

    return questions
