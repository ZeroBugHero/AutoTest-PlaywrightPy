#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:ZX
@file:read_application.py
@time:2023/03/28
"""
import os
import yaml


def get_project_path():
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return project_path


def get_application_config() -> dict:
    config_path = get_project_path() + '/config/config.yaml'
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"The file {config_path} does not exist.")
    with open(config_path, 'r', encoding='utf-8') as f:
        active = yaml.load(f, Loader=yaml.FullLoader)['active']
    env_path = get_project_path() + f'/config/environments/{active}.yaml'
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"The file {env_path} does not exist.")
    with open(env_path, 'r', encoding='utf-8') as file:
        application = yaml.load(file, Loader=yaml.FullLoader)
    return application


def get_cases_path() -> str:
    cases_path = get_project_path() + '/cases'
    return cases_path


def aa() -> None: ...


if __name__ == '__main__':
    print(get_application_config())
    print(get_cases_path())
    print(get_project_path())
