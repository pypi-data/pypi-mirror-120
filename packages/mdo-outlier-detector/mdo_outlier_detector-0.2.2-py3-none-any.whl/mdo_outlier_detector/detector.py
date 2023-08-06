import pandas as pd
import numpy as np
from scipy.spatial import distance

from sklearn.mixture import BayesianGaussianMixture, GaussianMixture
from sklearn.base import BaseEstimator, TransformerMixin

import typing as t


class Mdo(BaseEstimator, TransformerMixin):
    """
    On utilise la distance de Mahanalobis pour definir un score pour chaque point,
    plus le score est eleve plus le point est aberrant
    """


    def __init__(self):
        return None

    def Frequentist_gmm_inference(
        self, data: pd.DataFrame, **params
    ) -> None:
        """
        Frequentist inference of parameters by the EM algorithms,
        accept only DataFrame with numerical data, please do the feature engineering before enter the Dataframe
        
        Parameters
        ----------
            Data: DataFrame
                Donnees a analyser

            **params: kwargs
                parametres du modele gaussian mixture

        Returns
        ----------
        None

        """
        gmm = GaussianMixture(**params)
        gmm.fit(data)

        self.means = gmm.means_
        self.precision = gmm.precisions_
        self.weight = gmm.weights_
        self.label = gmm.predict(data)
        self.nrb_comp = gmm.n_components

    def Bayesian_gmm_inference(
        self, data: t.Union[pd.DataFrame, np.ndarray], **params
    ) -> None:
        """
        Bayesian inference of parameters by the EM algorithms of sklearn,
        accept only DataFrame with numerical data, please do the feature engineering before enter the Dataframe
        
        Parameters
        ----------        
        Data: DataFrame
            Donnees a analyser
        **params: kwargs
            parametres du modele gaussianmixture

        Returns
        -------
        None
        """
        Bayesian_gmm = BayesianGaussianMixture(**params)
        Bayesian_gmm.fit(data)

        self.means = Bayesian_gmm.means_
        self.precision = Bayesian_gmm.precisions_
        self.weight = Bayesian_gmm.weights_
        self.label = Bayesian_gmm.predict(data)
        self.nrb_comp = Bayesian_gmm.n_components

    def global_mahanalobis(self, data: pd.DataFrame) -> t.List:
        """
        evaluate the weighted average distance from clusters
        
        Parameters
        ----------
        Data: DataFrame
            Donnees a analyser

        Returns
        -------
        List
            Liste des differentes distances
        """
        self.mahanalobis_global = []
        np_data_point = data.to_numpy()

        for i in range(data.shape[0]):

            for means, precision, weight in zip(
                self.means, self.precision, self.weight
            ):
                dist_point = weight * distance.mahalanobis(means, np_data_point[i], precision)
            self.mahanalobis_global.append(dist_point)

        self.scoring_global = True

        return self.mahanalobis_global

    def local_mahanalobis(self, data: pd.DataFrame) -> t.List:
        """
        Evaluate the distance of the nearest cluster (i.e  the cluster which the point belongs)
        
        Parameters
        ----------
            Data: DataFrame
                Donnees a analyser

        Returns
        -------
        List
            Liste des differentes distances
        """
        self.mahanalobis_local = []
        np_data_point = data.to_numpy()

        for i in range(data.shape[0]):
            means = self.means[self.label[i]]
            precision = self.precision[self.label[i]]
            dist_point = distance.mahalanobis(means, np_data_point[i], precision)
            self.mahanalobis_local.append(dist_point)

        self.scoring_local = True

        return self.mahanalobis_local

    def fit(self, data: pd.DataFrame, y=None):
        return self

    def transform(
        self,
        data: pd.DataFrame,
        inference_type: str = "bayesian",
        **params
    ) -> t.Union[None, pd.DataFrame]:
        """
        fitting of the distance

        Parameters
        ----------
        Data: DataFrame
            Donnees a analyser
        inference_type:Str
            Type d'inference
                bayesian : scoring issue du bayesian EM
                frequentist : scoring issue du EM basique        
                data_with_distance: None|Dataframe

        Returns
        -------
        DataFrame
            Renvoie un le dataframe de base avec les metriques s'il un dataframe en entree sinon None
        """
        if inference_type == "bayesian":
            self.Bayesian_gmm_inference(data, **params)
        if inference_type == "frequentist":
            self.Frequentist_gmm_inference(data, **params)

        self.global_mahanalobis(data)
        self.local_mahanalobis(data)

        if isinstance(data, pd.DataFrame):
            data_with_distance = data.copy()
            data_with_distance["local_metrics"] = self.mahanalobis_local
            data_with_distance["global_metrics"] = self.mahanalobis_global

            return data_with_distance

        else:
            return None

    def get_scoring(self, scoring: str = "global")-> t.List:
        """
        Get the scoring define by the mahanalobis distance (local or global)
        
        Parameters
        ----------

        scoring:Str
            definie le type de scoring qu'on veut en sortie
                global: scoring global
                local: scoring local
        
        Returns
        -------
        List
            retourne le score souhaite sous forme de liste
        """
        if scoring == "local" and self.scoring_local:
            return self.mahanalobis_local
        elif scoring == "global" and self.scoring_global:
            return self.mahanalobis_global

        else:
            raise Exception("neither local and global i've been permformed")