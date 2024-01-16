# -*- coding: utf-8 -*-
"""Text_Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1d0yDLSGpaaMw5JRJydX5X5M4PLiqTykz
"""
#Scraping Data through urls
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import nltk
nltk.download('punkt')
nltk.download('words')
nltk.download('stopwords')
from nltk.corpus import words
import codecs
from textblob import TextBlob
import string
import re

input_file_path = 'input.xlsx'
df = pd.read_excel(input_file_path)

for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']

    response = requests.get(url)

    if response.status_code == 200:#Request success
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text.strip() 
        if soup.find('title'):
            article_text = ""
        else:
            'No Title Found'
        
        article_text_element = soup.find('div', class_='td-post-content tagdiv-type')  #finding body texts
        if article_text_element:
            article_text = article_text_element.get_text().strip()

        # Saving the files
        output_file_path = f'{url_id}.txt'
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(f'{title}\n\n')
            file.write(f'\n{article_text}')

        print(f'Data extracted from {url} and saved to {output_file_path}')
    else:
        print(f'Failed to retrieve data from {url}')
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#TO IMPORT STOPWORDS AND CLEAN FILES
def clean_stopwords(text,stopword_files):
  stop_words=set()
  for file in stopword_files:
    with open(file,"r",encoding="latin-1") as File:
      stop_words.update(File.read().splitlines())

  words=nltk.word_tokenize(text)
  clean_words=(word for word in words if word.upper() not in stop_words)
  clean_text=" ".join(clean_words)
  return clean_text

stopword_files=["/content/drive/MyDrive/NLP/StopWords/StopWords_Auditor.txt","/content/drive/MyDrive/NLP/StopWords/StopWords_Currencies.txt",
"/content/drive/MyDrive/NLP/StopWords/StopWords_DatesandNumbers.txt","/content/drive/MyDrive/NLP/StopWords/StopWords_Generic.txt",
                "/content/drive/MyDrive/NLP/StopWords/StopWords_GenericLong.txt","/content/drive/MyDrive/NLP/StopWords/StopWords_Geographic.txt"
                ,"/content/drive/MyDrive/NLP/StopWords/StopWords_Names.txt"]

text_folder="/content/drive/MyDrive/NLP/Textfiles"
clean_files_folder="/content/drive/MyDrive/NLP/CleanFiles"

for filename in os.listdir(text_folder):
  file_path=os.path.join(text_folder,filename)

  with open(file_path,'r',encoding='latin-1') as file:
    text=file.read()

    cleaned_text=clean_stopwords(text,stopword_files)

    clean_file=os.path.join(clean_files_folder,f'cleaned_{filename}')
    with open(clean_file,'w',encoding='latin-1') as clean_File:
      clean_File.write("".join(cleaned_text))

      print(f"Cleaned words saved to {clean_file}")

#TO CREATE POSITIVE AND NEGATIVE WORDS DICTIONARY
def create_dict(postive_file,negative_file, stopword_files):
  with open(postive_file,'r',encoding='latin-1') as file:
    positive_words=set(file.read().splitlines())
  with open(negative_file,'r',encoding="latin-1") as file1:
    negative_words=set(file1.read().splitlines())

  stopwords=set()
  for stopword_file in stopword_files:
    with open(stopword_file,'r',encoding='latin-1') as File:
      stopwords.update(File.read().splitlines())
  positive_words=positive_words-stopwords
  negative_words=negative_words-stopwords
  positive_dict={word.lower() for word in positive_words}
  negative_dict={word.lower() for word in negative_words}

  return positive_dict,negative_dict

positive_file="/content/drive/MyDrive/NLP/MasterDictionary/positive-words.txt"
negative_file="/content/drive/MyDrive/NLP/MasterDictionary/negative-words.txt"
stopword_files=["/content/drive/MyDrive/NLP/StopWords/StopWords_Auditor.txt","/content/drive/MyDrive/NLP/StopWords/StopWords_Currencies.txt",
"/content/drive/MyDrive/NLP/StopWords/StopWords_DatesandNumbers.txt","/content/drive/MyDrive/NLP/StopWords/StopWords_Generic.txt",
                "/content/drive/MyDrive/NLP/StopWords/StopWords_GenericLong.txt","/content/drive/MyDrive/NLP/StopWords/StopWords_Geographic.txt"
                ,"/content/drive/MyDrive/NLP/StopWords/StopWords_Names.txt"]

positive_dict,negative_dict=create_dict(positive_file,negative_file,stopword_files)

def sentiment_scores(text,positive_dict,negative_dict):
  words=nltk.word_tokenize(text)
  #positive and negative score
  positive_score = sum(1 for word in words if word.lower() in positive_dict)
  negative_score = sum(-1 for word in words if word.lower() in negative_dict)

  negative_score=negative_score * (-1)

  blob = TextBlob(text)
  #polarity and subjectivity score
  polarity_score = blob.sentiment.polarity
  subjectivity_score = blob.sentiment.subjectivity

  return positive_score,negative_score,polarity_score,subjectivity_score


columns=["FileName","Positive_Score","Negative_Score","Polarity_Score","Subjectivity_Score"]
results_df=pd.DataFrame(columns=columns)

text_files_folder="/content/drive/MyDrive/NLP/CleanFiles"

for filename in os.listdir(text_files_folder):
    file_path = os.path.join(text_files_folder, filename)
    with open(file_path,'r',encoding='latin-1') as file:
      text=file.read()
    positive_score,negative_score,polarity_score,subjectivity_score=sentiment_scores(text,positive_dict,negative_dict)
    results_df = results_df.append({
        "Filename": filename,
        "Positive_Score": positive_score,
        "Negative_Score": negative_score,
        "Polarity_Score": polarity_score,
        "Subjectivity_Score": subjectivity_score}
        , ignore_index=True)

output_excel_path = '/content/drive/MyDrive/NLP/sentiment_result.xlsx'
results_df.to_excel(output_excel_path, index=False)
print(f"Sentiment scores saved to {output_excel_path}")

def text_analysis(text):
  sentences=nltk.sent_tokenize(text)
  Words=nltk.word_tokenize(text)
  english_words=words.words()

  def syllable(word):
    count=0
    for vowel in word:
      if vowel in "aeiouAEIOU":
        count+=1
    return count
  #average sentence length
  avg_sentence_length=len(Words)/len(sentences) if len(sentences)> 0 else 0
  #Complex words
  complex_words=[word for word in Words if syllable(word)>2]
  #percentage of Complex words
  complex_words_percent=(len(complex_words)/len(Words)) * 100 if len(Words) > 0 else 0
  #fog index
  fog_index=0.4 * (avg_sentence_length+complex_words_percent)
  #average words in a sentence
  avg_words_sentence=len(Words)/len(sentences) if len(sentences) > 0 else 0
  #total complex words
  complex_words_count=len(complex_words)
  #total clean words
  Stopwords=set(nltk.corpus.stopwords.words('english'))
  punctuation=set(string.punctuation)
  clean_words=[word for word in Words if word.lower() not in Stopwords and word not in punctuation]
  total_wordcount=len(clean_words)
  #syllables per word
  syllables_per_word=sum(syllable(word) for word in clean_words)
  #personal pronouns
  pers_pronouns_count=sum(1 for word in Words if re.match(r'\b(I|we|my|ours|us)\b', word, flags=re.IGNORECASE))
  #average length of a word
  avg_word_length=sum(len(word) for word in clean_words)/total_wordcount if total_wordcount > 0 else 0

  return avg_sentence_length,complex_words_percent,fog_index,avg_words_sentence,complex_words_count,total_wordcount,syllables_per_word,pers_pronouns_count,avg_word_length

text_files_folder="/content/drive/MyDrive/NLP/CleanFiles"

columns=["Filename","avg_sentence_length","Complex_word_percent","Fog_index","Avg_words_sentence","Complex_words_count","Total_wordcount","Syllables_per_word","pers_pronouns_count","Avg_word_length"]
results_df=pd.DataFrame(columns=columns)


for filename in os.listdir(text_files_folder):
    file_path = os.path.join(text_files_folder, filename)

    with open(file_path, 'r', encoding='latin-1') as file:
        text = file.read()

        avg_sentence_length,complex_word_percent,fog_index,avg_words_sentence,complex_words_count,total_wordcount,syllables_per_word,pers_pronouns_count,avg_word_length=text_analysis(text)

        results_df=results_df.append({
            "Filename":filename,
            "avg_sentence_length":avg_sentence_length,
            "complex_word_percent":complex_word_percent,
            "Fog_index":fog_index,
            "Avg_words_sentence":avg_words_sentence,
            "complex_words_count":complex_words_count,
            "total_wordcount":total_wordcount,
            "syllables_per_word":syllables_per_word,
            "pers_pronouns_count":pers_pronouns_count,
            "avg_word_length":avg_word_length},ignore_index=True)

output_file_path="/content/drive/MyDrive/NLP/text_analysis.xlsx"
results_df.to_excel(output_file_path,index=False)
print(f'Output is saved to {output_file_path}')
