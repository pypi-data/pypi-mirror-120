import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import pickle
from regression_model.config import config
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.preprocessing import normalize
from scipy.sparse import hstack
from sklearn.preprocessing import StandardScaler

from regression_model.config import config
from regression_model import __version__ as _version


class CategoricalImputer(BaseEstimator, TransformerMixin):
    """Categorical data missing value imputer."""
    """The individual dataframes had been left outer joined. Thus only text fields can be NA. They are filled as corresponding 'Gene'+'Variation'"""

    def __init__(self, variables=None) -> None:
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None) -> 'CategoricalImputer':
        """Fit statement to accomodate the sklearn pipeline."""

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Apply the transforms to the dataframe."""

        X = X.copy()
        X.loc[X['TEXT'].isnull(),'TEXT'] = X['Gene'] +' '+X['Variation']

        return X
 
    
class TextProcessor(BaseEstimator, TransformerMixin):
    """NLTK preprocessing of TEXT variable"""
    def __init__(self,variables=None) -> None:
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables
            
    def fit(self, X: pd.DataFrame, y: pd.Series = None) -> 'TextProcessor':
        """Fit statement to accomodate the sklearn pipeline."""

        return self
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Apply the transforms to the dataframe."""
        stop_words = set(stopwords.words('english'))
        X=X.copy()
        
        def nlp_preprocessing(total_text, index, column):
         if type(total_text) is not int:
            string = ""
            # replace every special char with space
            total_text = re.sub('[^a-zA-Z0-9\n]', ' ', total_text)
            # replace multiple spaces with single space
            total_text = re.sub('\s+',' ', total_text)
            # converting all the chars into lower-case.
            total_text = total_text.lower()
            
            for word in total_text.split():
            # if the word is a not a stop word then retain that word from the data
                if not word in stop_words:
                    string += word + " "
            
            X[column][index] = string
            
        for var in self.variables:
            for index, row in X.iterrows():
                if type(row[var]) is str:
                    nlp_preprocessing(row[var], index, var)
                else:
                    print("there is no text description for id:",index)
        
        return X
    
    
class CategoricalProcessor(BaseEstimator, TransformerMixin):
    """Preprocessing of Gene, Variation variable"""
    def __init__(self,variables=None) -> None:
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables
            
    def fit(self, X: pd.DataFrame, y: pd.Series = None) -> 'CategoricalProcessor':
        """Fit statement to accomodate the sklearn pipeline."""

        return self
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Apply the transforms to the dataframe."""
        
        X=X.copy()
        for var in self.variables:
            X[var]=X[var].str.replace('\s+', '_')
        
        return X
    
    
class CategoricalEncoder(BaseEstimator,TransformerMixin):
    """One-hot-encoding all features"""
    def __init__(self,variables=None,training=True) -> None:
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables
        self.training=training 
    def fit(self, X: pd.DataFrame, y: pd.Series = None) -> 'CategoricalEncoder':
        """Fit statement to accomodate the sklearn pipeline."""

        return self
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
            """Apply the transforms to the dataframe."""
        
        
        
            
            
        
            gene_vectorizer=CountVectorizer()
            gene_feature_onehotCoding=gene_vectorizer.fit_transform(X['Gene']) 
            pickle.dump(gene_vectorizer,open(config.ONE_HOT_GENE_SAVE_FILE,'wb'))
            
            variation_vectorizer=CountVectorizer()
            variation_feature_onehotCoding=variation_vectorizer.fit_transform(X['Variation'])
            pickle.dump(variation_vectorizer,open(config.ONE_HOT_VARIATION_SAVE_FILE,'wb'))
            
            text_vectorizer=CountVectorizer(min_df=3)
            text_feature_onehotCoding=text_vectorizer.fit_transform(X['TEXT'])
            pickle.dump(text_vectorizer,open(config.ONE_HOT_TEXT_SAVE_FILE,'wb'))
            
            train_gene_var_onehotCoding = hstack((gene_feature_onehotCoding,variation_feature_onehotCoding))
            train_x_onehotCoding = hstack((train_gene_var_onehotCoding, text_feature_onehotCoding)).tocsr()
            
            sc = StandardScaler(with_mean=False)
            train_x_onehotCoding = sc.fit_transform(train_x_onehotCoding) 
            pickle.dump(sc,open(config.SCALER_SAVE_FILE, 'wb'))
            
            
            return train_x_onehotCoding
       