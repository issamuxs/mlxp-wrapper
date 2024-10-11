import xp_wrapper as xpw
import utils
from sklearn.datasets import load_iris
import json
import argparse
import mlflow

iris = load_iris()
X = iris['data']
y = iris['target']

xp = xpw.xp_wrapper()

def main():
    with open('config/ec2_params.json', 'r') as f:
        config = json.load(f)
        instance_id = config['INSTANCE_ID']
        public_ip = config['PUBLIC_IP']
        mlflow_port = config['MLFLOW_PORT']
    print(f"Connecting to instance {instance_id} with public IP {public_ip} with MLflow port {mlflow_port}")
    mlflow.set_tracking_uri(f"http://{public_ip}:{mlflow_port}")
    parser = argparse.ArgumentParser(description="Train and log a logistic regression model in MLflow")
    parser.add_argument("-mlt", "--ml_type", type=str)
    parser.add_argument("-en", "--experiment_name", type=str)
    parser.add_argument("-mn", "--model_name", type=str)
    parser.add_argument("-r", "--register", choices=['true', 'false'], default='false', type=str)
    args = parser.parse_args()
    xp.train_model(X, y, ml_type=args.ml_type, experiment_name=args.experiment_name, model_name=args.model_name, register=args.register)

if __name__ == "__main__":
    main()

