import nltk
import pandas as pd
from utility import custom_stop_words, complex_word_count, syllable_per_word, personal_word_count, avg_word_len
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from nltk.tokenize import RegexpTokenizer
import os
from tqdm import tqdm

nltk.download('punkt')
nltk.download('wordnet')
lemma = WordNetLemmatizer()

# nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# stop_words = nltk.corpus.stopwords.words('english')
c_stop_words = custom_stop_words()


# set(stopwords.words('english'))


def analysis(dir_list, df, extracted_path):
    print('Analysing..')
    for i in tqdm(dir_list):
        try:
            r = i.split('.')[0]
            row = df.loc[df['URL_ID'] == r].index[0]
            f = open(extracted_path + i, 'r', encoding='utf-8')
            text = f.read()
            word_tokens = word_tokenize(text)

            filtered_sentence = []

            for w in word_tokens:
                if w not in c_stop_words:
                    filtered_sentence.append(w)

            preprocessed_txt = (" ".join(filtered_sentence))

            file = open('utility_files/negative-words.txt', 'r')
            neg_words = file.read().split()
            file = open('utility_files/positive-words.txt', 'r')
            pos_words = file.read().split()

            num_pos = len([i for i in filtered_sentence if i.lower() in pos_words])
            num_neg = len([i for i in filtered_sentence if i.lower() in neg_words])
            df.loc[row, 'POSITIVE SCORE'] = num_pos
            df.loc[row, 'NEGATIVE SCORE'] = num_neg
            # sentiment = round((num_pos - num_neg) / len(filtered_sentence), 2)

            Polarity_Score = (num_pos - num_neg) / ((num_pos + num_neg) + 0.000001)
            df.loc[row, 'POLARITY SCORE'] = Polarity_Score
            Subjectivity_Score = (num_pos + num_neg) / ((len(filtered_sentence)) + 0.000001)
            df.loc[row, 'SUBJECTIVITY SCORE'] = Subjectivity_Score

            ### Text Analysis Started Here
            tokenizer = RegexpTokenizer(r'\w+')
            tokens = tokenizer.tokenize(str(filtered_sentence))
            word_Count = len(tokens)
            number_of_sentences = sent_tokenize(str(filtered_sentence))
            num_sentences = len(number_of_sentences)

            Average_Sentence_Length = word_Count / num_sentences
            df.loc[row, 'AVG SENTENCE LENGTH'] = Average_Sentence_Length
            # Averagge Number Of Words Per Sentence
            Average_Number_Words_Per_Sentence = len(text) / num_sentences
            df.loc[row, 'AVG NUMBER OF WORDS PER SENTENCE'] = Average_Number_Words_Per_Sentence

            # percentage of complex words With Complex Word Count

            complex_word_cnt, percentage_complex_words = complex_word_count(tokens, word_Count)
            df.loc[row, 'PERCENTAGE OF COMPLEX WORDS'] = percentage_complex_words
            df.loc[row, 'COMPLEX WORD COUNT'] = complex_word_cnt

            # Fog Index Count

            Fog_Index = 0.4 * (Average_Sentence_Length + percentage_complex_words)
            df.loc[row, 'FOG INDEX'] = Fog_Index
            syllable_per_wrd = syllable_per_word(word_tokens, word_Count)
            df.loc[row, 'SYLLABLE PER WORD'] = syllable_per_wrd

            personal_wrd_count = personal_word_count(text)
            df.loc[row, 'PERSONAL PRONOUNS'] = personal_wrd_count
            avg_wrd_length = avg_word_len(word_tokens)

            df.loc[row, 'AVG WORD LENGTH'] = avg_wrd_length
        except:
            pass

    return df



