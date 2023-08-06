import pathlib

import regression_model

import pandas as pd




pd.options.display.max_rows = 10
pd.options.display.max_columns = 10


PACKAGE_ROOT = pathlib.Path(regression_model.__file__).resolve().parent
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"
TRAINED_ENCODER_DIR= PACKAGE_ROOT / "trained_encoders"
DATASET_DIR = PACKAGE_ROOT / "datasets"

# data
TESTING_DATA_FILE = "test.csv"
TRAINING_DATA_FILE = "train.csv"
TARGET = "Class"

#categorical not allowed
CATEGORICAL_NA_NOT_ALLOWED=['Gene','Variation','TEXT']
#variables
FEATURES = ['Gene','Variation','TEXT']

# text variable
TEXT_FEATURE = ["TEXT"]

# categorical variables

CAT_FEATURES=['Gene','Variation']

PIPELINE_NAME = "logistic_regression"
PIPELINE_SAVE_FILE = f"{PIPELINE_NAME}_output_v"
ONE_HOT_GENE_SAVE_FILE = TRAINED_ENCODER_DIR/'one_hot_gene.pkl'
ONE_HOT_VARIATION_SAVE_FILE = TRAINED_ENCODER_DIR/'one_hot_variation.pkl'
ONE_HOT_TEXT_SAVE_FILE = TRAINED_ENCODER_DIR/'one_hot_text.pkl'
SCALER_SAVE_FILE=TRAINED_ENCODER_DIR/'standardscaler.pkl'

# used for differential testing
ACCEPTABLE_MODEL_DIFFERENCE = 0.05
