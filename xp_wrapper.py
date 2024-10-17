import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import mlflow
import joblib
from utils.mlflow_utils import get_next_version


class xp_wrapper:
    def __init__(self):
        #self.environment = {}
        self.data  = None
        self.model = None
        self.data_info = {}
        self.model_info = {}

    def load_data(self, data_path, data_type='csv'):
        """
        Returns a dictionary with 'X' mapped to features and optional 'y' mapped to target
        """
        if type == 'csv':
            self.data = pd.read_csv(data_path)
            self.data_info = {'variables': self.data.columns,
                                'shape': self.data.shape}
            
    def load_model(self, model_path, format='pickle'):
        self.model = joblib.load(model_path)
        self.model_info = {'model_type': type(self.model).__name__}

    def train_model(self, X, y, ml_type, experiment_name, model_name, register_model):

        self.data = {'X': X, 'y': y}

        if ml_type == 'supervised':

            X = self.data['X']
            y = self.data['y']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

            mlflow.set_experiment(experiment_name)

            with mlflow.start_run() as run:

                self.model_info['model_type'] = type(self.model).__name__
                self.model_info['version'] = get_next_version(model_name)
                self.model = LogisticRegression(max_iter=1000)
                print(f"Training model {model_name}...")
                self.model.fit(X, y)
                self.model_info['accuracy'] = self.model.score(X_test, y_test)

                mlflow.log_param("model_type", self.model_info['model_type'])
                mlflow.log_metric("accuracy", self.model_info['accuracy'])
                mlflow.sklearn.log_model(self.model, model_name)
                mlflow.set_tag("model version", self.model_info['version'])


            if register_model == 'true':
                print(f"Registering model {model_name} under version {self.model_info['version']} for this run")
                mlflow.register_model(f"runs:/{run.info.run_id}/model", model_name)
            else:
                print("No model registered for this run")

        else:
            print("ml_type not supported.")