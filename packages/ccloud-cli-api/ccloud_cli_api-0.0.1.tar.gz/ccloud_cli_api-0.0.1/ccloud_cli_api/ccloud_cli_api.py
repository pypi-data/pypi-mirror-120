#  -*- coding: utf-8 -*-
# Copyright (C) 2021 John "Preston" Mille <john@compose-x.io>
# SPDX-License-Identifier: GPL-2.0

"""Main module."""

import json
import subprocess
import warnings
from copy import deepcopy
from os import environ


def login(email=None, password=None):
    if email and password:
        environ["CCLOUD_EMAIL"] = email
        environ["CCLOUD_PASSWORD"] = password
    if not environ.get("CCLOUD_EMAIL", None) or not environ.get(
        "CCLOUD_PASSWORD", None
    ):
        raise EnvironmentError(
            "You must specify CCLOUD_EMAIL and CCLOUD_PASSWORD to login"
        )
    base_cmd = ["ccloud", "login", "--save"]
    print(subprocess.run(base_cmd, capture_output=True, text=True).stdout)


def list_environments():
    base_cmd = "ccloud environment list -o json".split(" ")
    output = subprocess.run(base_cmd, capture_output=True, text=True).stdout
    return json.loads(output)


def list_clusters(all_environments=False):
    base_cmd = "ccloud kafka cluster list -o json".split(" ")
    if all_environments:
        clusters = []
        environments = list_environments()
        for env in environments:
            cmd = deepcopy(base_cmd)
            cmd.append("--environment")
            cmd.append(env["id"])
            output = subprocess.run(cmd, capture_output=True, text=True).stdout
            clusters += json.loads(output)
        return clusters
    else:
        output = subprocess.run(base_cmd, capture_output=True, text=True).stdout
        return json.loads(output)


def describe_schema_registry():
    """
    Function to list the schema registry of the environment
    :return:
    """
    base_cmd = "ccloud schema-registry cluster describe -o json".split(" ")
    output = subprocess.run(base_cmd, capture_output=True, text=True).stdout
    return json.loads(output)


def list_available_clusters():
    """
    Function to list the clusters (Kafka and Schema Registry)

    :return: The list of cluster IDs
    """
    clusters = [cluster["id"] for cluster in list_clusters(True)]
    clusters.append(describe_schema_registry()["cluster_id"])
    return clusters


def cluster_resource_exists(resource):
    """
    Validate that the resource exists.

    :param resource:
    :return:
    """
    if not isinstance(resource, str):
        raise TypeError("resource is", type(resource), "expected", str)
    clusters = list_available_clusters()
    if resource in clusters:
        return True
    return False


def list_service_accounts():
    """
    Function to list the Kafka clusters
    :return:
    """
    base_cmd = ["ccloud", "service-account", "list", "-o", "json"]
    output = subprocess.run(base_cmd, capture_output=True, text=True).stdout
    return json.loads(output)


def verify_service_account(service_account):
    """
    Function to validate that a given service account exists

    :param str service_account:
    :raises: TypeError
    :raises: LookupError
    """
    if not isinstance(service_account, str):
        raise TypeError("service_account is", type(service_account), "expected", str)
    service_accounts = list_service_accounts()
    if not str(service_account) in [str(acct["id"]) for acct in service_accounts]:
        raise LookupError(f"Service account {service_account} not found.")


def list_api_keys(service_account=None):
    """
    Function to list the API keys for service accounts

    :param str service_account: Specific service account you want the keys for
    :return: List of API keys
    :rtype: list
    """
    base_cmd = ["ccloud", "api-key", "list", "-o", "json"]
    if service_account:
        verify_service_account(service_account)
        service_accounts = list_service_accounts()
        if not str(service_account) in [str(acct["id"]) for acct in service_accounts]:
            raise LookupError(f"Service account {service_account} not found.")
        base_cmd.append("--service-account")
        base_cmd.append(service_account)
    output = subprocess.run(base_cmd, capture_output=True, text=True).stdout
    return json.loads(output)


def create_api_key(service_account, resource):
    """
    Function to create a new API key for a given service account for a specific resource

    :param str service_account:
    :param str resource:
    :return:
    """
    if not isinstance(service_account, str):
        raise TypeError("service_account is", type(service_account), "expected", str)
    verify_service_account(service_account)
    cluster_resource_exists(resource)
    base_cmd = [
        "ccloud",
        "api-key",
        "create",
        "--resource",
        resource,
        "--service-account",
        str(service_account),
        "-o",
        "json",
    ]
    output = subprocess.run(base_cmd, capture_output=True, text=True).stdout
    return json.loads(output)


def delete_api_key(api_key):
    """
    Function to delete an API key for a given service account for a specific resource

    :param str api_key:
    :return:
    """
    key = api_key_exists(api_key)
    if not key:
        warnings.warn(f"API Key {api_key} does not exist")
        return
    base_cmd = ["ccloud", "api-key", "delete", key["key"]]
    subprocess.run(base_cmd, capture_output=True, text=True)


def api_key_exists(api_key, service_account=None):
    """
    Function to verify that a given API key exists

    :param str api_key: The API key to lookup.
    :param str service_account: Specify the service account to look the key up for
    :return: The key if found, else None
    :rtype: dict|None
    :raises: TypeError
    """
    if not isinstance(api_key, str):
        raise TypeError("api_key is", type(service_account), "expected", str)
    if service_account and not isinstance(service_account, str):
        raise TypeError("service_account is", type(service_account), "expected", str)
    elif service_account:
        verify_service_account(service_account)
        api_keys = list_api_keys(service_account=service_account)
    else:
        api_keys = list_api_keys()

    for key in api_keys:
        if str(key["key"]) == api_key:
            return key
    return None
