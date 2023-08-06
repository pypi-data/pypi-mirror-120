"""A transformer that imputes missing values."""
import numpy as np
import pandas as pd
import woodwork as ww

from blocktorch.pipelines.components.transformers.transformer import Transformer
from blocktorch.utils import infer_feature_types
from dask_ml.preprocessing import BlockTransformer
from dask_ml.preprocessing import DummyEncoder
from dask_ml.preprocessing import Categorizer, DummyEncoder
from sklearn.pipeline import make_pipeline

from dask_ml.compose import make_column_transformer, ColumnTransformer
from dask_ml.preprocessing import OneHotEncoder as DaskOneHotEncoder
from dask_ml.wrappers import Incremental
from dask_ml.impute import SimpleImputer as DaskSimpleImputer
import dask.array as da
from blocktorch.utils import infer_feature_types





class Imputer(Transformer):
    """A transformer that encodes categorical features in a one-hot numeric array.

    Args:
        top_n (int): Number of categories per column to encode. If None, all categories will be encoded.
            Otherwise, the `n` most frequent will be encoded and all others will be dropped. Defaults to 10.
        features_to_encode (list[str]): List of columns to encode. All other columns will remain untouched.
            If None, all appropriate columns will be encoded. Defaults to None.
        random_seed (int): Seed for the random number generator. Defaults to 0.
    """

    name = "Imputer"
    hyperparameter_ranges = {}
    """{}"""

    def __init__(
        self,
        top_n=10,
        logical_types = {},
        random_seed=0,
        **kwargs,
    ):
        parameters = {
            "top_n": top_n,
            "logical_types": logical_types
        }
        parameters.update(kwargs)


        super().__init__(
            parameters=parameters, component_obj=None, random_seed=random_seed
        )


    def _get_cat_cols(self, X):
        """Get names of categorical columns in the input DataFrame."""
        return list(X.ww.select(include=["category"], return_schema=True).columns)

    def _get_num_cols(self, X):
        """Get names of categorical columns in the input DataFrame."""
        return list(X.ww.select(include=["numeric"], return_schema=True).columns)


    def fit(self, X, y=None):
        """Fits the one-hot encoder component.

        Args:
            X (pd.DataFrame): The input training data of shape [n_samples, n_features].
            y (pd.Series, optional): The target training data of length [n_samples].

        Returns:
            self

        Raises:
            ValueError: If encoding a column failed.
        """
        return self

    def transform(self, X, y=None):
        """One-hot encode the input data.

        Args:
            X (pd.DataFrame): Features to one-hot encode.
            y (pd.Series): Ignored.

        Returns:
            pd.DataFrame: Transformed data, where each categorical feature has been encoded into numerical columns using one-hot encoding.
        """


        def func(X):

            logical_types = self.parameters['logical_types']
            X_ww = infer_feature_types(X, logical_types)

            column_transformer = make_column_transformer(
                (DaskSimpleImputer(strategy='most_frequent'), self._get_cat_cols(X_ww)),
                (DaskSimpleImputer(strategy='mean'), self._get_num_cols(X_ww)),
                remainder='passthrough',
            )

            for col in self._get_cat_cols(X_ww):
                try:
                    X_ww[col] = X_ww[col].astype('category')
                    X_ww[col] = X_ww[col].cat.as_known()
                except: pass

            return column_transformer.fit_transform(X_ww)

        xformer = BlockTransformer(func)

        X_t = xformer.fit_transform(X)

        return X_t



