# Mahanalobis_Detection_Outliers

Mahanalobis_Detection_Outliers is a method based on the inference of some parameters (means vertors and precisions matrice) of gaussian mixture with the EM algorithm to define mahanalobis distance 
and a scoring.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Mahanalobis_Detection_Outliers.

```bash
pip install Mahanalobis_Detection_Outliers
```

## Usage

```python
from outlier_detector.main import Mdo

params = { 
    "inference_type"='bayesian',
    "n_components" : 10,
    "covariance_type" : 'full',
    ...
    } #Parameters for bayesian Gaussian mixture or the usual one more explanations about parameters on sklearn

outliers_dectetion = Mdo()
X_scoring = outlier_detection.transform(X, **params)
 # Procede to inference for finding parameters (means and precision matrice)

List_scoring_global = outlier_detection.get_scoring() # returns global scoring 
List_scoring_local = outlier_detection.get_scoring("local") # returns local scoring
```


[Example of using](https://pip.pypa.io/en/stable/) 



## License
[MIT](https://choosealicense.com/licenses/mit/)