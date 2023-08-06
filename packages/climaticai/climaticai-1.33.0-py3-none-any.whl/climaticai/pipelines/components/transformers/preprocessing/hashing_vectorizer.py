"""Base class for all transformers working with text features."""
from climaticai.pipelines.components.transformers import Transformer

from dask_ml.feature_extraction.text import HashingVectorizer
from climaticai.utils import infer_feature_types
import pandas as pd
import dask.array as da, dask.dataframe as dd

class TextHashingVectorizer(Transformer):
    """Base class for all transformers working with text features.

    Args:
        component_obj (obj): Third-party objects useful in component implementation. Defaults to None.
        random_seed (int): Seed for the random number generator. Defaults to 0.
    """
    name = "Text Hashing Vectorizer"
    hyperparameter_ranges = {}

    def __init__(self, n_features=2, random_seed=0, **kwargs):
        parameters = {'n_features':n_features}
        parameters.update(kwargs)

        component_obj = HashingVectorizer(**parameters)

        super().__init__(
            parameters=parameters, component_obj=component_obj, random_seed=random_seed
        )

    def _get_text_columns(self, X):
        """Returns the ordered list of columns names in the input which have been designated as text columns."""
        return list(X.ww.select("NaturalLanguage", return_schema=True).columns)

    def fit(self, X, y=None):
        """Fits component to data.

        Args:
            X (pd.DataFrame or np.ndarray): The input training data of shape [n_samples, n_features]
            y (pd.Series): The target training data of length [n_samples]

        Returns:
            self
        """
        X_t = infer_feature_types(X)
        self.n_features = self.parameters['n_features']
        self._text_columns = self._get_text_columns(X_t)
        return self

    def transform(self, X, y=None):
        """Transforms data X by creating new features using existing text columns.

        Args:
            X (pd.DataFrame): The data to transform.
            y (pd.Series, optional): Ignored.

        Returns:
            pd.DataFrame: Transformed X
        """
        X = infer_feature_types(X)
        l=[]
        for col in self._text_columns:
            X[col]=X[col].astype(str).fillna("")
            X_t = self._component_obj.fit_transform(X[col])
            X_t.compute_chunk_sizes()
            # ddf = infer_feature_types(ddf)
            # ddf = dd.concat([dd.from_dask_array(c) for c in [X_t]], axis=1)
            # cols = list(ddf.columns)
            # for n in range(len(cols)):
            #     try:
            #         ddf = ddf.rename({cols[n]:col+'_hash_'+str(n)})
            #         X[col+'_hash_'+str(n)]=ddf[col+'_hash_'+str(n)]
            #     except: pass
            l.append(X_t)
        X = X.repartition(1)
        x = dd.concat(l)
        for n in range(len(self._text_columns)*self.n_features):
            try: X['hash_'+str(n)] = x[n]
            except: pass
        # ddf = dd.concat(l, axis=1)
        # X[[col for col in ddf.columns]]=ddf[[col for col in ddf.columns]]
        # X = infer_feature_types(X)
        return X



