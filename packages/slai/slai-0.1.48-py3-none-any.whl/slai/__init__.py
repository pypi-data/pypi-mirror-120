from slai.model_version import ModelVersion
from slai.types import ModelTypes
from slai.base_handler import BaseModelHandler
from slai.login import Login
from slai import loaders
from slai.model import Model
from slai.dataset import DataSet

__version__ = "0.1.48"


# most used slai actions go here
model = Model
model_version = ModelVersion
loaders = loaders
types = ModelTypes
login = Login
dataset = DataSet
BaseModelHandler = BaseModelHandler

__all__ = [
    "__version__",
    "model_version",
    "dataset",
    "model",
    "types",
    "base_handler",
    "loaders",
    "login",
]
