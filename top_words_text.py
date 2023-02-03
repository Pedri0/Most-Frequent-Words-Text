import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import numpy as np
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from matplotlib import pyplot as plt
from absl import app
from absl import flags
#download stopwords
nltk.download('stopwords')
nltk.download('punkt')

FLAGS = flags.FLAGS

flags.DEFINE_integer('ngram_min', 1, 'Minimum n-gram size.')
flags.DEFINE_integer('ngram_max', 1, 'Maximum n-gram size.')
flags.DEFINE_list('custom_stopwords', ["eg", "etc", "usw", "also", "ever"],
         'List of stopwords to remove.')

def get_text_from_file(file_path):
    """Function to get text from file.

    Args:
        file_path (str): path to file
    """
    with open(file_path, 'r') as f:
        text = f.read()
    return text

def remove_stopwords(text, stopwords_list):
    """Function to remove stopwords from text given a list of stopwords.

    Args:
        text (str): text to remove stopwords from
        stopwords_list (list): list of stopwords to remove
    
    Returns:
        str: text with stopwords removed
    """
    #split text into list words
    processed_text = text.split()
    #remove stopwords
    processed_text = [word for word in processed_text if not word.lower() in stopwords_list]

    return ' '.join(processed_text)


def process_text(text):
    """Function to process or clean text.

    Args:
        text (str): text to process

    Returns:
        str: processed text (lower case, no numbers, no punctuation, no special characters, no stopwords)
    """    
    #to lower case
    processed_text = text.lower()
    #spaces between words and punctuation
    processed_text = re.sub(r'[]!"$%&\()*=#@+,./:;?[\\^_`{|}~-]+', r' \g<0> ', processed_text)
    #remove numbers, punctuation, extra spaces and special characters, except for apostrophes
    processed_text = re.sub(r"[^\w\d'\s]+", '', processed_text)
    processed_text = re.sub(r"\s+", ' ', processed_text)
    processed_text = processed_text.strip()
    #get english stopwords
    stopwords_eng = stopwords.words('english')
    #if custom stopwords are given, add them to the list
    if FLAGS.custom_stopwords:
        stopwords_eng.extend(FLAGS.custom_stopwords)

    #remove stopwords
    processed_text = remove_stopwords(processed_text, stopwords_eng)

    return processed_text, stopwords_eng

def save_plot_top_words(bow_sklearn_df):
    """Function to save plot of top words.

    Args:
        bow_sklearn_df (pd.DataFrame): dataframe with top words ordered by frequency (top to bottom)
    """    
    fig = plt.figure(figsize=(18, 18))
    ax = sns.barplot(bow_sklearn_df[:30], x='frecuencia', y='palabra')
    plt.xticks(rotation=45)
    ax.set_xticks(list(range(0, 10, 1)))
    ax.grid(True)
    plt.savefig('./results/top_words_ngram'+str(FLAGS.ngram_min)+str(FLAGS.ngram_max)+'.png')

def get_top_words(processed_text, stopwords_eng):
    """Function to get top words from text.

    Args:
        processed_text (str): processed text
        stopwords_eng (list): list of stopwords
    Returns:
        pd.DataFrame: dataframe with top words ordered by frequency (top to bottom)
    """       
    #configure count vectorizer
    vectorizer = CountVectorizer(stop_words=stopwords_eng, 
            ngram_range=(FLAGS.ngram_min,FLAGS.ngram_max))
    #fit transform vectorizer to text
    counts = vectorizer.fit_transform([processed_text])

    #Build and save dataframe with word counts
    bow_sklearn = pd.DataFrame(counts.toarray(), columns=vectorizer.get_feature_names_out())
    bow_sklearn = bow_sklearn.T.reset_index()
    bow_sklearn.rename(columns={'index':'palabra', 0:'frecuencia'}, 
        inplace=True)
    bow_sklearn.sort_values(by=['frecuencia', 'palabra'], 
        ignore_index=True, inplace=True, ascending=False)

    bow_sklearn.to_csv('./results/top_words_ngram'+str(FLAGS.ngram_min)+str(FLAGS.ngram_max)+'.csv', index=False)
    save_plot_top_words(bow_sklearn)
    return bow_sklearn

def main(argv):
    if len(argv) > 1:
        raise app.UsageError('Too many command-line arguments.')

    text = get_text_from_file('./text.txt')
    processed_text, stopwords = process_text(text)
    bow_df = get_top_words(processed_text, stopwords)
    print('Finished')

if __name__ == '__main__':
    app.run(main)