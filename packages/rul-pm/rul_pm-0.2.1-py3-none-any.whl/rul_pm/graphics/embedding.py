from rul_pm.iterators.iterators import LifeDatasetIterator
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def tsne(iterator: LifeDatasetIterator, subsample:int=1, perplexity:float=50, pca:bool=True, ax=None, **kwargs):
    """Plot the T-SNE embedding of the data provided by the iterator

    Parameters
    ----------
    iterator : LifeDatasetIterator
        [description]
    subsample : int, optional
        [description], by default 1
    perplexity : float, optional
        [description], by default 50
    pca : bool, optional
        Wether to use PCA before T-SNE, by default True
    ax : [type], optional
        Axis to make the plot. If it is not present a new figure will be created,
        By default None

    Returns
    -------
    [type]
        [description]
    """
    if ax is None:
        _, ax = plt.subplots(**kwargs)
    data = []
    labels =[]
    for i, (X, _,_) in enumerate(iterator):  
        d = X.iloc[::subsample, :]      
        data.append(d)
        labels.extend(np.ones(d.shape[0]) * i)
    X = np.vstack(data)
    print(X.shape)
    if pca:
        X = PCA(n_components=8).fit_transform(X)
    X_embedded = TSNE(n_components=2, perplexity=perplexity).fit_transform(X)    
    ax.scatter(X_embedded[:, 0], X_embedded[:, 1])
    return ax.figure, ax