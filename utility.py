import glob
import string
import re


def custom_stop_words():
    l = []
    path = 'utility_files/StopWords/*'
    files = glob.glob(path)
    for i in files:
        f = open(i, 'r')
        text_org = str(f.read())
        res = [word.strip(string.punctuation) for word in text_org.split() if
               word.strip(string.punctuation).isalnum()]
        l.extend(res)
    return l


def complex_word_count(tokens, word_Count):
    complex_word_cnt = 0
    for token in tokens:
        vowels = 0
        if token.endswith(('es', 'ed')):
            pass
        else:
            for l in token:
                if (l == 'a' or l == 'e' or l == 'i' or l == 'o' or l == 'u'):
                    vowels += 1
            if vowels > 2:
                complex_word_cnt += 1
    if len(tokens) != 0:
        percentage_complex_words = (complex_word_cnt / word_Count)

    return complex_word_cnt, percentage_complex_words


def syllable_per_word(word_tokens, word_Count):
    ## Syllable Per Word
    vowels = 0
    for x in word_tokens:
        if x.endswith(('es', 'ed')):
            pass
        else:
            for i in x:
                if (i == 'a' or i == 'e' or i == 'i' or i == 'o' or i == 'u'):
                    vowels += 1
    syllable_per_word = vowels / word_Count
    return syllable_per_word


def personal_word_count(text):
    ### Count Of Personal Pronoun

    pronoun_re = r'\b(I|my|we|us|ours)\b'
    matches = re.findall(pronoun_re, text)
    count_of_personal_pronoun = len(matches)
    return count_of_personal_pronoun


def avg_word_len(word_tokens):
    ### Average Word Length
    charcnt = 0
    for word in word_tokens:
        charcnt += len(word.strip())
    if len(word_tokens) != 0:
        Avg_Word_Length = charcnt / len(word_tokens)

    return Avg_Word_Length
