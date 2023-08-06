#!/usr/bin/env python
# -*- coding: utf-8; -*-

# Copyright (c) 2021 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/
"""Utilities used by the model deployment package
"""

# Standard lib
import fsspec
import json
# Copyright (c) 2021 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

import logging
import oci
import os
import shutil
import sys
import tempfile
import time
import yaml
from typing import Dict

from enum import Enum, auto
from oci.data_science.models import CreateModelDetails
from oci.signer import Signer
from oci.util import get_signer_from_authentication_type, AUTHENTICATION_TYPE_FIELD_NAME
from .progress_bar import TqdmProgressBar, DummyProgressBar


SERVICE_ENDPOINT_CONFIG = "oci_odsc_service_endpoint"
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("ODSC-ModelDeployment")


def get_logger():
    return logger


def load_config(source=None):
    """Loads SDK config from YAML or dict

    Args:
        source (str or dict, optional): Path to config YAML or a dict containing the configurations.
            Defaults to None. Source will be ignored if it is not str or dict.

    Returns:
        dict: Dictionary containing the configurations
    """
    # Empty config dict
    config = {}

    # source will be ignore if it is not str or dict
    if isinstance(source, dict):
        # source is dict
        config = source
    elif isinstance(source, str):
        # source is path to yaml file
        if "yaml" in source:
            with open(source) as cf:
                try:
                    config = yaml.load(cf, Loader=yaml.CLoader)
                except:
                    config = yaml.load(cf, Loader=yaml.Loader)
        else:
            logger.error("Pass in a valid config yaml file")
            raise ValueError(f"Not a valid yaml file: {source}")

    # Load service endpoint from environment variable if it is not specified in config
    # Default service endpoint in OCI SDK will be used if service endpoint is not in config or environment variables.
    if not config.get(SERVICE_ENDPOINT_CONFIG) and os.environ.get(
        "OCI_ODSC_SERVICE_ENDPOINT"
    ):
        config[SERVICE_ENDPOINT_CONFIG] = os.environ["OCI_ODSC_SERVICE_ENDPOINT"]
    config = {str(k).lower(): v for k, v in config.items()}
    return config


def set_log_level(level="INFO"):
    """set_log_level sets the logger level

    Args:
        level (str, optional): The logger level. Defaults to "INFO"

    Returns:
        Nothing
    """

    level = logging.getLevelName(level)
    logger.setLevel(level)


def seconds_since(t):
    """seconds_since returns the seconds since `t`. `t` is assumed to be a time
    in epoch seconds since time.time() returns the current time in epoch seconds.

    Args:
        t (int) - a time in epoch seconds

    Returns
        int: the number of seconds since `t`
    """

    return time.time() - t


def is_notebook():
    """is_notebook returns True if the environment is a Jupyter notebook and
    False otherwise

    Args:
        None

    Returns:
        bool: True if Jupyter notebook; False otherwise

    Raises:
        NameError: If retrieving the shell name from get_ipython() throws an error

    """

    try:
        from IPython import get_ipython

        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":  # pragma: no cover
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except ImportError:
        # IPython is not installed
        return False
    except NameError:
        return False  # Probably standard Python interpreter


def get_progress_bar(max_progress, description="Initializing"):
    """get_progress_bar return an instance of ProgressBar, sensitive to the runtime environment

    Args:
        max_progress (int): Progress bar max
        description (str, optional): Progress bar description (defaults to "Initializing")

    Returns:
        An instance of ProgressBar. Either a DummyProgressBar (non-notebook) or TqdmProgressBar
        (notebook environement)
    """

    if is_notebook():  # pragma: no cover
        return TqdmProgressBar(max_progress, description=description, verbose=False)
    else:
        return DummyProgressBar()


# State Constants
class State(Enum):
    ACTIVE = auto()
    CREATING = auto()
    DELETED = auto()
    DELETING = auto()
    FAILED = auto()
    INACTIVE = auto()
    UPDATING = auto()
    UNKNOWN = auto()

    @staticmethod
    def _from_str(state):
        if state == None:
            return State.UNKNOWN
        elif state.upper() == "ACTIVE":
            return State.ACTIVE
        elif state.upper() == "CREATING":
            return State.CREATING
        elif state.upper() == "DELETED":
            return State.DELETED
        elif state.upper() == "DELETING":
            return State.DELETING
        elif state.upper() == "FAILED":
            return State.FAILED
        elif state.upper() == "INACTIVE":
            return State.INACTIVE
        elif state.upper() == "UPDATING":
            return State.UPDATING
        else:
            return State.UNKNOWN

    def __call__(self):
        # This will provide backward compatibility.
        # In previous release, ModelDeployment has state() as method instead of property
        return self


class OCIClientManager:
    """OCIClientManager is a helper class used for accessing DataScienceClient and
    DataScienceCompositeClient objects

    Attributes
    ----------
    ds_client - class attribute for data science client
    ds_composite_client - class attribute for data science composite client

    Methods
    -------
    oci_ds_client(config)
        returns the OCI DataScienceClient
    oci_ds_composite_client(ds_client)
        returns the OCI DataScienceCompositeClient
    """

    @staticmethod
    def get_oci_config_path_and_profile(sdk_config=None):
        """Determines the OCI config path and profile from SDK config

        Args:
            sdk_config (dict, optional): A dictionary containing MD SDK config. Defaults to None.

        Returns:
            dict: A dictionary containing file_path and/or profile if it is specified in the SDK config.
                This dictionary can be used as kwargs for oci.config.from_file(**kwargs)
        """
        if sdk_config is None:
            sdk_config = {}
        sdk_config = {k.lower(): v for k, v in sdk_config.items()}
        # Get API key config if signer is not obtained
        # Use default OCI config and profile when the value of oci_config_profile/oci_config_file is None or empty
        profile = sdk_config.get("oci_config_profile")
        file_path = sdk_config.get("oci_config_file")
        # Pass file_path/profile to oci.config.from_file only if there is value
        # OCI SDK will handle the default values.
        kwargs = {}
        if file_path:
            kwargs["file_path"] = file_path
        if profile:
            kwargs["profile"] = profile
        return kwargs

    @staticmethod
    def get_oci_config(sdk_config=None):
        oci_config = oci.config.from_file(
            **OCIClientManager.get_oci_config_path_and_profile(sdk_config)
        )
        return oci_config

    @staticmethod
    def get_oci_config_signer(sdk_config=None):
        """Gets OCI signer from SDK config"""
        oci_config = {}
        signer = None
        if not sdk_config:
            sdk_config = {}

        # Get resource principal signer if user specified resource principal as authentication method
        if sdk_config.get("auth") == "resource_principal":
            # EnvironmentError will be raise if resource principal is not available.
            signer = oci.auth.signers.get_resource_principals_signer()
            return oci_config, signer
        # Try to get signer from OCI config
        try:
            oci_config = OCIClientManager.get_oci_config(sdk_config)

            if AUTHENTICATION_TYPE_FIELD_NAME in oci_config:
                signer = get_signer_from_authentication_type(oci_config)
            else:
                signer = Signer.from_config(oci_config)
            return oci_config, signer
        except oci.exceptions.ConfigFileNotFound:
            if "oci_api_keys" in sdk_config or sdk_config.get("auth") == "api_key":
                # If OCI_API_KEYS are specified in config,
                #   raise error to let user know config file is not found.
                raise

        # Try to get signer from resource principal only if OCI_API_KEYS are not specified in config
        try:
            signer = oci.auth.signers.get_resource_principals_signer()
        except EnvironmentError:
            raise EnvironmentError(
                "Unable to obtain OCI credentials. Please setup API Keys."
            )

        return oci_config, signer

    @staticmethod
    def oci_ds_client(sdk_config=None):
        """Returns the OCI DataScienceClient

        Returns:
            DataScienceClient: DataScienceClient
        """
        if not sdk_config:
            sdk_config = {}

        oci_config, signer = OCIClientManager().get_oci_config_signer(sdk_config)

        kwargs = {}
        if SERVICE_ENDPOINT_CONFIG in sdk_config:
            kwargs["service_endpoint"] = sdk_config[SERVICE_ENDPOINT_CONFIG]

        ds_client = oci.data_science.DataScienceClient(
            oci_config,
            signer=signer,
            retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY,
            **kwargs,
        )
        return ds_client

    @staticmethod
    def oci_ds_composite_client(ds_client):
        """oci_ds_composite_client returns the OCI DataScienceCompositeClient

        Args:
            ds_client (DataScienceClient): OCI DataScienceClient

        Returns:
            DataScienceCompositeClient: DataScienceCompositeClient
        """
        return oci.data_science.DataScienceClientCompositeOperations(ds_client)

    @staticmethod
    def default_compartment_id(config=None):
        """Determines the default compartment OCID
        This method finds the compartment OCID from (in priority order):
        an environment variable, an API key config or a resource principal signer.

        Parameters
        ----------
        config : dict, optional
            The model deployment config, which contains the following keys:
            auth: Authentication method, must be either "resource_principal" or "api_key".
            If auth is not specified:
                1. api_key will be used if available.
                2. If api_key is not available, resource_principal will be used.
            oci_config_file: OCI API key config file location. Defaults to "~/.oci/config"
            oci_config_profile: OCI API key config profile name. Defaults to "DEFAULT"

        Returns
        -------
        str or None
            The compartment OCID if found. Otherwise None.
        """
        # Try to get compartment ID from environment variable.')
        if os.environ.get('NB_SESSION_COMPARTMENT_OCID'):
            return os.environ.get('NB_SESSION_COMPARTMENT_OCID')
        # Try to get compartment ID from OCI config, then RP signer
        # Note: we assume compartment_ids can never be: 0, False, etc.
        oci_config, signer = OCIClientManager.get_oci_config_signer(config)
        return oci_config.get("compartment_id") or oci_config.get("tenancy") or \
               getattr(signer, "tenancy_id", None)


    @staticmethod
    def _prepare_artifact(model_uri: str, properties: Dict, ds_client=None) -> str:
        """
        Prepare model artifact. Returns model ocid.

        Args:
            model_uri (str): uri to model files, can be local or in cloud storage
            properties (dict): dictionary of properties that are needed for creating a model.
            ds_client (DataScienceClient): OCI DataScienceClient

        Returns:
            str: model ocid
        """
        if not ds_client:
            ds_client = OCIClientManager.oci_ds_client()
        if properties:
            properties_dict = (
                properties
                if isinstance(properties, dict)
                else json.loads(repr(properties))
            )
        with tempfile.TemporaryDirectory() as d:
            fhandlers = fsspec.open_files(
                model_uri,
                config=OCIClientManager.get_oci_config(),
                mode="rb",
            )
            if len(fhandlers) == 0:
                raise FileNotFoundError("No files found under this path.")
            for fh in fhandlers:
                with fh as fin:
                    with open(os.path.join(d, os.path.basename(fh.path)), "wb") as fout:
                        fout.write(fin.read())
            shutil.make_archive(
                os.path.join(os.path.dirname(d), "model_files"),
                "zip",
                os.path.dirname(d),
                os.path.basename(d),
            )
            return OCIClientManager._upload_artifact(
                ds_client,
                f"{os.path.join(os.path.dirname(d), 'model_files')}.zip",
                properties_dict,
            )

    @staticmethod
    def _upload_artifact(ds_client, model_zip: str, properties: dict) -> str:
        """Uploads the model artifact to cloud storage.

        Args:
            ds_client (DataScienceClient): OCI DataScienceClient
            model_zip (str): path to model artifact zip file
            properties (dict): dictionary of properties

        Returns:
            str: model ocid
        """
        create_model_details = CreateModelDetails(
            display_name=properties.get("display_name", None),
            project_id=properties["project_id"],
            compartment_id=properties["compartment_id"],
        )

        model = ds_client.create_model(create_model_details).data
        with open(model_zip, "rb") as data:
            ds_client.create_model_artifact(
                model.id,
                data,
                content_disposition=f'attachment; filename="{model.id}.zip"',
            )
        return model.id
