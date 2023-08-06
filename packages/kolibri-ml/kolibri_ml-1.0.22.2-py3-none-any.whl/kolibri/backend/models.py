# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief:

from kdmt.file import read_json_file
from pathlib import Path
from kolibri.data.ressources import resources

sklearn_models_path= resources.get(str(Path('models','sklearn','models.json'))).path
sklearn_models=read_json_file(sklearn_models_path)

n_estimators = 10

def get_model(model_name, weights=None, bakend='tensorflow'):
    if isinstance(model_name, list):
        models_ = [sklearn_models.get(model, None) for model in model_name]
        if weights is None:
            weights = [1 for model in model_name]
        model_cict={
      "class": "mlxtend.classifier.EnsembleVoteClassifier",
      "parameters": {
        "clfs": {
          "value": models_
        },
        "voting": {
          "value": "soft",
          "type": "categorical",
          "values": ["soft", "hard"]
        },
        "weights": {
          "value": weights
        }
      }
    }

        return model_cict

    else:
        model= sklearn_models.get(model_name, None)

    return model



if __name__=="__main__":
    models_=["LogisticRegression", "knn"]
    models_=[get_model_(m) for m in models_]
    print(models_)