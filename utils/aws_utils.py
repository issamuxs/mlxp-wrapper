import json
import os
from pathlib import Path
import configparser
import boto3

def load_ec2_config(client_config_path):    
    with open(client_config_path, 'r') as f:
        config = json.load(f)

        # Extract EC2 params
        instance_id = config['INSTANCE_ID']
        public_ip = config['PUBLIC_IP']
        mlflow_port = config['MLFLOW_PORT']

    return config

def setup_aws_config(client_config_path, profile_name):
    with open(client_config_path, 'r') as f:
        config = json.load(f)
        
        # Extract AWS parameters
        access_key_id = config['AWS_PARAM']['AccessKeyId']
        secret_access_key = config['AWS_PARAM']['SecretAccessKey']
        aws_region = config['AWS_PARAM']['Region']
        aws_output = config['AWS_PARAM']['Output']

    home = str(Path.home())
    aws_credentials_path = os.path.join(home, '.aws', 'credentials')
    aws_config_path = os.path.join(home, '.aws', 'config')

    # Ensure relevant AWS directories exist
    os.makedirs(os.path.dirname(aws_credentials_path), exist_ok=True)
    os.makedirs(os.path.dirname(aws_config_path), exist_ok=True)

    # Update credentials file
    credentials = configparser.ConfigParser()
    credentials.read(aws_credentials_path)

    if profile_name not in credentials:
        credentials[profile_name] = {}

    credentials[profile_name]['aws_access_key_id'] = access_key_id
    credentials[profile_name]['aws_secret_access_key'] = secret_access_key

    with open(aws_credentials_path, 'w') as f:
            credentials.write(f)
        
    # Update config file
    config = configparser.ConfigParser()
    config.read(aws_config_path)

    profile_section = f"profile {profile_name}"

    if profile_section not in config:
        config[profile_section] = {}

    config[profile_section]['Region'] = aws_region
    config[profile_section]['Output'] = aws_output 

    with open(aws_config_path, 'w') as f:
            config.write(f)

    print(f"AWS profile {profile_name} has been added to ~/.aws/credentials and ~/.aws/config files.")

def load_aws_config(client_config_path, profile_name):
    try:
        session = boto3.Session(profile_name=profile_name)
        print(f"AWS configuration using {profile_name} successfully loaded.")
    except:
        print(f"AWS profile {profile_name} not found. Adding AWS profile in ~/.aws/credentials and ~/.aws/config.")
        setup_aws_config(client_config_path=client_config_path, profile_name=profile_name)
        load_aws_config(client_config_path, profile_name)
        

