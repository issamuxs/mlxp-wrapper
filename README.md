# MLXP-Wrapper

### Context

The MLXP-Wrapper repository is part of a machine learning platform demo project. The latter is composed of 3 parts:
1. MLXP-Core: An experiments tracking server based on MLflow hosted on AWS
2. MLXP-Wrapper: A wrapper over the MLflow server that enables config-based data science from any client machine
3. MLXP-Algo: A library that reproduces some of the key machine learning algorithms

### Description

Currently, the module is focused only on the training workflow. Data preparation as well as model deployment and monitoring are not handled.

This module is based on the xp_wrapper class, which provides an abstraction layer for experiments management over MLflow.

### Technical setup

1. Copy the client_config.json file provided by the MLXP-Core project into the config folder of the MLXP-Wrapper project.
