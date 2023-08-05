import os
import sys
from typing import List
from tqatest.app.core.errors import PredictException, ModelLoadException
from tqatest.app.core.config import MODEL_NAME, MODEL_PATH, MODEL_ID
from loguru import logger
from tqatest.ml.libs import annhub


class MachineLearningModel(object):
    def __init__(self) -> None:
        super().__init__()
        self.load()

    def load(self):
        # if MODEL_PATH.endswith("/"):
        #     path = f"{MODEL_PATH}{MODEL_NAME}"
        # else:
        #     path = f"{MODEL_PATH}/{MODEL_NAME}"

        # path = os.path.abspath(os.path.join(os.getcwd(), path))

        # if not os.path.exists(path):
        #     message = f"Machine learning model at {path} not exists!"
        #     logger.error(message)
        #     raise FileNotFoundError(message)
        package_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(package_dir,'../../ml/model/TrainedModel_c++.ann')

        self.load_model(path)
    
    def load_model(self, path : str):
        self.model = annhub.ANNHUB(int(MODEL_ID))
        self.model.LoadWeightFile(path)
        if not self.model:
            message = f"Model {MODEL_ID} could not load!"
            logger.error(message)
            raise ModelLoadException(message)

    def predict(self, data_input : List[float]) -> List[float]:
        self.model.Predict(data_input)
        output = self.model.GetOutput()
        if not output:
            raise PredictException(f"Error when predict input:'{data_input}'")
        return output


