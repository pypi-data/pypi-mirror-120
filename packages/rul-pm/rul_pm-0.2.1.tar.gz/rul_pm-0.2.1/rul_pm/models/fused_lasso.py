import numpy as np
import pandas as pd
from rul_pm.iterators.batcher import Batcher
from rul_pm.iterators.iterators import WindowedDatasetIterator
from rul_pm.models.model import TrainableModel
from tqdm.auto import tqdm

from sklearn.base import BaseEstimator
from sklearn.metrics import mean_squared_error


class FusedLasso(TrainableModel):
    """Wrapper around scikit-learn models

    Parameters
    ----------
    model: BaseEstimator
        A scikit-learn model
    """

    def __init__(self, model: BaseEstimator, **kwargs):
        super().__init__(**kwargs)
        self._model = model
        if not hasattr(self.model, "fit"):
            raise ValueError("Model must allow to fit")

    def build_model(self):
        return self._model

    def fit(self, train_iterator: WindowedDatasetIterator, **kwargs):
        """Fit the model with the given dataset iterator

        Parameters
        ----------
        train_iterator : WindowedDatasetIterator
            Dataset iterator from which obtain data to fit

        Keyword arguments
        -----------------
        kwargs:
            Arguments for the fit method

        Returns
        -------
        SKLearnModel
            self
        """
        X, y, sample_weight = train_iterator.get_data()

        loss = rr.quadratic.shift(-Y,coef=0.5)
        D = np.identity(X.shape[1])
        for i in range(n_features):
            for j in range(window_size-1):
                D[i + (j*window_size), i+((j+1)*window_size)] = -1

        for j in range(0, X.shape[1], train_iterator.window_size):
            D[]


        self.model.fit(X, y.ravel(), **kwargs, sample_weight=sample_weight)
        return self

    def predict(self, dataset_iterator: WindowedDatasetIterator):
        """Get the predictions for the given iterator

        Parameters
        ----------
        dataset_iterator : WindowedDatasetIterator
            Dataset iterator from which obtain data to predict

        Returns
        -------
        np.array
            Array with the predictiosn
        """
        X, _, _ = dataset_iterator.get_data()
        return self.model.predict(X)

    def get_params(self, deep: bool = False) -> dict:
        """Obtain the model parameters

        Parameters
        ----------
        deep : bool, optional
            Wether to obtain the parameters for each element, by default False

        Returns
        -------
        dict
            Model parameters
        """
        out = super().get_params(deep=deep)
        out["model"] = self.model
        if deep and hasattr(self.model, "get_params"):
            for key, value in self.model.get_params(deep=True).items():
                out["model__%s" % key] = value
        return out

    def set_params(self, **params):
        ## TODO Check invalid parameters
        model_params = {}
        for name, value in params.items():
            if "__" in name:
                model_params[name.split("__")[1]] = value
        for name in model_params.keys():
            params.pop(f"model__{name}")

        super().set_params(**params)
        self.model.set_params(**model_params)
        return self
