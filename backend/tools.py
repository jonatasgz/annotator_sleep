# This tools file refers to the classifiers in the nlp app. Unclean structure from developing on a parallel project

from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin
import spacy
import string
from gensim.models import Word2Vec
from gensim.utils import tokenize
import numpy as np

lemmatizer = spacy.load("pt_core_news_lg")

class RuleClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, variable, expressions, graded:list):
        """
        Custom text classifier based on rule-based categorization.
        
        Parameters:
        - variables: dict, mapping of a variable name to a keyword list.
        - graded: list of categories that require categorical classification.
        """
        self.variable = variable
        self.expressions = expressions
        self.graded = graded

    def fit(self, X, y=None):
        return self

    def predict(self, X):
        """
        Predict categories for a list of notes.
        
        Parameters:
        - X: list or array of text notes
        
        Returns:
        - List of predictions for a given variable in a given note
        """
        return [self._classify_text(note) for note in X]

    def _classify_text(self, note):
        """Applies classification rules to a single note."""
        
        if self.variable in self.graded:
            prediction = self._categoric_classifier(self.expressions, note)
        else:
            prediction = self._binary_classifier(self.expressions, note)

        return prediction

    def _categoric_classifier(self, words, note):
        split_note = note.split()
        index = self._first_match(words, split_note)

        try:
            next_word = split_note[index + 1]
        except:
            return 'missing'
        try:
            next_word_2 = split_note[index + 2]
        except:
            next_word_2 = ''
        
        if 'desconhece' in next_word:
            return 'dont know'
        elif 'nunca' in next_word:
            return 'never'
        elif 'às' in next_word and 'vezes' in next_word_2:
            return 'sometimes'
        elif 'frequente' in next_word:
            return 'frequent'
        elif 'sempre' in next_word:
            return 'always'
        else:
            return 'missing'

    def _binary_classifier(self, words, note):
        for word in words:
            if word in note:
                if self._is_negated(word, note):
                    return 'no'
                else:
                    return 'yes'
        return 'missing'

    def _first_match(self, words, split_note):
        for i in split_note:
            for word in words:
                if word in i:
                    return split_note.index(i)
        return None

    def _is_negated(self, word, note):
        split_note = note.split()
        index = self._first_match([word], split_note)

        try:
            if split_note[index - 1] == 'sem':
                return True
            elif split_note[index + 1] in ['nega', 'nunca']:
                return True
            else:
                return False
        except:
            return False


class CleanNotes(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return [self._clean_notes(note) for note in X]
        
    def _clean_notes(self, note):
        if isinstance(note, str):
            lowercase = note.lower()
            translate_table = str.maketrans(string.punctuation, ' '*len(string.punctuation))
            no_punctuation = lowercase.translate(translate_table)
            final = " ".join(no_punctuation.split())
            return final
        else:
            return ""
        
class MyLemmatizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return [self._lemmatize(note) for note in X]
    
    def _lemmatize(self, note):
        split_note = note.split(" ")
        lemmas = [tk.lemma_ for w in split_note for tk in lemmatizer(w)]
        lemma_note = " ".join(lemmas)
        return lemma_note
    
    def _stopwords(self, stopwords:list):
        stopwords_lemma = [tk.lemma_ for w in stopwords for tk in lemmatizer(w)]
        return list(set(stopwords_lemma))
    
class MyWord2Vec(BaseEstimator, TransformerMixin):
    def __init__(self, model, stopwords):
        self.model = model
        self.stopwords = stopwords

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return [self._get_mean_vector(note) for note in X]
    
    def _get_mean_vector(self, text):
        vectors = [self.model.wv[token] for token in tokenize(text) if token not in self.stopwords and token in self.model.wv]
        mean = np.mean(vectors, axis = 0)
        return mean

class Arraytomize(TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        return X.toarray()