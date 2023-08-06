from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.calibration import CalibratedClassifierCV



from regression_model.processing import vect_preprocessors as pp
from regression_model.processing import features
from regression_model.config import config

import logging


_logger = logging.getLogger(__name__)


mutation_pipe = Pipeline(
    [
        (
            "categorical_imputer",
            pp.CategoricalImputer(variables=config.FEATURES),
        ),
        (
            "text_processor",
            pp.TextProcessor(variables=config.TEXT_FEATURE),
        ),
        (
            "categorical_processor",
            pp.CategoricalProcessor(
                variables=config.CAT_FEATURES
            ),
        ),
        
        (
            "categorical_encoder",
            pp.CategoricalEncoder(variables=config.FEATURES),
        ),
        
        
            ("meta_estimator",CalibratedClassifierCV(base_estimator=SGDClassifier(class_weight='balanced',alpha=0.0001,loss='log', 
                                       penalty='l2', random_state=0))  
            )
    ]
)