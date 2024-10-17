import xp_wrapper as xpw
from utils.aws_utils import load_ec2_config, setup_aws_config, load_aws_config
from sklearn.datasets import load_iris
import argparse
import mlflow
import os

iris = load_iris()
X = iris['data']
y = iris['target']

def parse_args():
    parser = argparse.ArgumentParser(description="MLXP-Wrapper tool setup and testing")
    parser.add_argument("-ccp", "--client_config_path", default='config/client_config.json', help='Path to client_config.json file')
    parser.add_argument("-pn", "--profile_name", default='mlxp-wrapper', help='AWS profile name (default: mlxp-wrapper)')
    parser.add_argument("-mlt", "--ml_type", type=str)
    parser.add_argument("-en", "--experiment_name", type=str)
    parser.add_argument("-mn", "--model_name", type=str)
    parser.add_argument("-rm", "--register_model", choices=['true', 'false'], default='false', type=str)
    args = parser.parse_args()
    return args

def mlxp_core_setup(config):
    instance_id = config['INSTANCE_ID']
    public_ip = config['PUBLIC_IP']
    mlflow_port = config['MLFLOW_PORT']
    
    print(f"Connecting to instance {instance_id} with public IP {public_ip} with MLflow port {mlflow_port}")

    train_server = f"http://{public_ip}:{mlflow_port}"
    mlflow.set_tracking_uri(train_server)
    print("MLflow tracking URI is ", mlflow.get_tracking_uri())


def main():
    print("""
    ======================================
    Welcome to the MLXP-Wrapper tool setup
    ======================================
    
    You need to provide a path for the client_config.json file.
    Optionally, you can specify a custom AWS profile (default is 'mlxp-wrapper').
    """)

    args = parse_args()

    client_config_path = args.client_config_path
    profile_name = args.profile_name
          
    #setup_aws_config(client_config_path, profile_name) 
    load_aws_config(client_config_path, profile_name)

    os.environ['AWS_PROFILE'] = profile_name # MLflow uses environment variables for credentials, not possible to force the use of boto3 session credentials

    config = load_ec2_config(client_config_path)
    mlxp_core_setup(config)

    xp = xpw.xp_wrapper()
    xp.train_model(X, y, ml_type=args.ml_type, experiment_name=args.experiment_name, model_name=args.model_name, register_model=args.register_model)

if __name__ == "__main__":
    main()

