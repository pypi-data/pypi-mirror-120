#!/usr/bin/env python
# -*- coding: utf-8; -*-

# Copyright (c) 2021 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

import oci.data_science.models as data_science_models
import os
import tempfile
import shutil
import fsspec

from .common import utils
from .common.utils import OCIClientManager

from ads.common.oci_datascience import OCIDataScienceMixin
from typing import Any, Optional, Union


class ModelDeploymentProperties(
    OCIDataScienceMixin, data_science_models.ModelDeployment
):
    """Represents the details for a model deployment

    Attributes
    ----------
    swagger_types (dict): The property names and the corresponding types of OCI ModelDeployment model.
    model_id (str): the model artifact OCID in model catalog
    model_uri (str): uri to model files, can be local or in cloud storage

    Methods
    -------
    with_prop(property_name, value)
        Set the model deployment details `property_name` attribute to `value`
    with_instance_configuration(config)
        Set the configuration of VM instance.
    with_access_log(log_group_id, log_id)
        Config the access log with OCI logging service
    with_predict_log(log_group_id, log_id)
        Config the predict log with OCI logging service
    build()
        Return an instance of CreateModelDeploymentDetails for creating the deployment.
    """

    # These properties are supported by ModelDeploymentProperties but are not top-level attributes of ModelDeployment
    sub_properties = [
        "instance_shape",
        "instance_count",
        "bandwidth_mbps",
        "access_log_group_id",
        "access_log_id",
        "predict_log_group_id",
        "predict_log_id",
    ]

    def __init__(
        self,
        model_id: Optional[str] = None,
        model_uri: Optional[str] = None,
        oci_model_deployment: Union[
            data_science_models.ModelDeployment,
            data_science_models.CreateModelDeploymentDetails,
            data_science_models.UpdateModelConfigurationDetails,
            dict,
        ] = None,
        **kwargs,
    ):
        """Initialize a ModelDeploymentProperties object by specifying one of the followings:

        The model_id must be specified either explicitly or as an attribute of the OCI object.

        Args:
            model_id (str): Model Artifact OCID
            model_uri (str): uri to model files, can be local or in cloud storage
            oci_model_deployment: An OCI model or dict containing model deployment details.
                The OCI model can be an instance of either ModelDeployment, CreateModelDeploymentDetails or
                UpdateModelConfigurationDetails.
            kwargs: Users can also initialize the object by using keyword arguments.
                The following keyword arguments are supported by OCI models:
                    'display_name'
                    'description'
                    'project_id'
                    'compartment_id'
                    'model_deployment_configuration_details',
                    'category_log_details',
                    'freeform_tags',
                    'defined_tags',
                ModelDeploymentProperties also supports the following additional keyward arguments:
                    "instance_shape",
                    "instance_count",
                    "bandwidth_mbps",
                    "access_log_group_id",
                    "access_log_id",
                    "predict_log_group_id",
                    "predict_log_id",
                These additional arguments will be saved into approperate properties in the OCI model.

        Raises:
            ValueError: model_id is None AND not specified in
            oci_model_deployment.model_deployment_configuration_details.model_configuration_details
        """
        self.model_id = model_id
        self.model_uri = model_uri
        self.config = utils.load_config()
        self.ds_client = OCIClientManager.oci_ds_client(self.config)
        oci_kwargs = {}
        if oci_model_deployment:
            # User specified oci_model_deployment, which could be an OCI model object or a dict
            if isinstance(oci_model_deployment, dict):
                oci_kwargs = oci_model_deployment
                # If user specified properties defined in the sub_properties in oci_model_deployment (as dict),
                # move them to the kwargs so that they can be processed correctly.
                for key in list(oci_kwargs.keys()):
                    if key in self.sub_properties and not key in kwargs:
                        kwargs[key] = oci_kwargs.pop(key)
            else:
                # Extract properties from OCI model as a dict
                if hasattr(oci_model_deployment, "swagger_types"):
                    oci_kwargs = {
                        k: getattr(oci_model_deployment, k)
                        for k in oci_model_deployment.swagger_types.keys()
                    }
                elif oci_model_deployment:
                    raise ValueError(
                        "Invalid value for oci_model_deployment when initializing ModelDeploymentProperties: "
                        f"{oci_model_deployment}. "
                        "ModelDeploymentProperties should be initialized with an instance of OCI data science model, "
                        "a dictionary or keyword arguments."
                    )

        # Use kwargs to initialize OCI ModelDeployment attributes
        super().__init__(**oci_kwargs)

        # Get model ID from OCI object
        if self.model_id is None:
            try:
                self.model_id = (
                    self.model_deployment_configuration_details.model_configuration_details.model_id
                )
            except:
                self.model_id = None

        # Process additional kwargs
        # Convert all keys to lower case
        kwargs = {str(k).lower(): v for k, v in kwargs.items()}

        # Set ModelDeployment properties
        for key, val in kwargs.items():
            if key in self.swagger_types.keys():
                self.with_prop(key, val)

        # Config instance
        instance_config = {}
        for key in ["instance_shape", "instance_count", "bandwidth_mbps"]:
            if key in kwargs:
                instance_config[key] = kwargs[key]
        if instance_config:
            self.with_instance_configuration(config=instance_config)

        # Config logging
        if "access_log_group_id" in kwargs or "access_log_id" in kwargs:
            if not ("access_log_group_id" in kwargs and "access_log_id" in kwargs):
                raise ValueError(
                    "access_log_group_id and access_log_id must be specified at the same time."
                )
            self.with_access_log(kwargs["access_log_group_id"], kwargs["access_log_id"])

        if "predict_log_group_id" in kwargs or "predict_log_id" in kwargs:
            if not ("predict_log_group_id" in kwargs and "predict_log_id" in kwargs):
                raise ValueError(
                    "predict_log_group_id and predict_log_id must be specified at the same time."
                )
            self.with_predict_log(
                kwargs["predict_log_group_id"], kwargs["predict_log_id"]
            )

    def with_instance_configuration(self, config):
        """with_instance_configuration creates a ModelDeploymentDetails object with a specific config

        Args:
            config (dict): dictionary containing instance configuration about the deployment.
                The following keys are supported:
                    instance_shape,
                    instance_count,
                    bandwidth_mbps
                The instance_shape and instance_count are required when creating a new deployment.
                They are optional when updating an existing deployment.

        Returns:
            ModelDeploymentProperties: self
        """
        # Convert all keys to lower case for backward compatibility
        config = {str(k).lower(): v for k, v in config.items()}

        single_type_model_deployment_object = (
            data_science_models.SingleModelDeploymentConfigurationDetails()
        )

        model_configuration_details_object = (
            data_science_models.ModelConfigurationDetails()
        )
        model_configuration_details_object.model_id = self.model_id

        # instance_configuration is required even though it can be initialized with empty values
        instance_configuration_object = data_science_models.InstanceConfiguration()
        if "instance_shape" in config:
            instance_configuration_object.instance_shape_name = config["instance_shape"]
        model_configuration_details_object.instance_configuration = (
            instance_configuration_object
        )

        # scaling_policy is required even though it can be initialized with empty values
        scaling_policy_object = data_science_models.FixedSizeScalingPolicy()
        if "instance_count" in config:
            scaling_policy_object.instance_count = int(config["instance_count"])
        model_configuration_details_object.scaling_policy = scaling_policy_object

        if "bandwidth_mbps" in config:
            model_configuration_details_object.bandwidth_mbps = config["bandwidth_mbps"]

        single_type_model_deployment_object.model_configuration_details = (
            model_configuration_details_object
        )
        self.model_deployment_configuration_details = (
            single_type_model_deployment_object
        )
        return self

    def with_category_log(self, log_type: str, group_id: str, log_id: str):
        """Adds category log configuration

        Args:
            log_type (str): The type of logging to be configured. Must be "access" or "predict"
            group_id (str): Log group ID of OCI logging service
            log_id (str): Log ID of OCI logging service

        Returns:
            ModelDeploymentProperties: self

        Raises:
            ValueError: When log_type is invalid
        """
        if log_type not in ["access", "predict"]:
            raise ValueError(
                f'Invalid log type: {log_type}. Must be "access" or "predict".'
            )
        if not self.category_log_details:
            self.category_log_details = data_science_models.CategoryLogDetails()
        log_details = data_science_models.LogDetails()
        log_details.log_group_id = group_id
        log_details.log_id = log_id
        setattr(self.category_log_details, log_type, log_details)
        return self

    def with_access_log(self, log_group_id: str, log_id: str):
        """Adds access log config for OCI logging service

        Args:
            group_id (str): Log group ID of OCI logging service
            log_id (str): Log ID of OCI logging service

        Returns:
            ModelDeploymentProperties: self
        """
        return self.with_category_log("access", log_group_id, log_id)

    def with_predict_log(self, log_group_id: str, log_id: str):
        return self.with_category_log("predict", log_group_id, log_id)

    def with_logging_configuration(
        self,
        access_log_group_id: str,
        access_log_id: str,
        predict_log_group_id: Optional[str] = None,
        predict_log_id: Optional[str] = None,
    ):
        """Adds OCI logging configurations for OCI logging service

        Args:
            access_log_group_id (str): Log group ID of OCI logging service for access log
            access_log_id (str): Log ID of OCI logging service for access log
            predict_log_group_id (str): Log group ID of OCI logging service for predict log
            predict_log_id (str): Log ID of OCI logging service for predict log

        Returns:
            ModelDeploymentProperties: self
        """
        self.with_access_log(access_log_group_id, access_log_id)
        if predict_log_group_id and predict_log_id:
            self.with_predict_log(predict_log_group_id, predict_log_id)
        return self

    def with_prop(self, property_name: str, value: Any):
        """Sets model deployment's `property_name` attribute to `value`

        Args:
            property_name (str): string representing the property attribute to be changed
            value: new value for property attribute

        Returns:
            ModelDeploymentProperties: self

        Raises:
            Exception: if OCI ModelDeployment does not have the attribute `property_name`
        """
        if property_name not in self.swagger_types:
            raise AttributeError(
                f"OCI ModelDeployment does not have the attribute {property_name}"
            )
        setattr(self, property_name, value)
        return self

    def build(self):
        """Converts the deployment properties to OCI CreateModelDeploymentDetails object.
        Converts a model URI into a model OCID if user passed in a URI.
        """
        if self.model_uri:
            self.model_id = OCIClientManager._prepare_artifact(
                model_uri=self.model_uri,
                properties=dict(
                    display_name="testing",
                    project_id=self.project_id,
                    compartment_id=self.compartment_id,
                ),
                ds_client=self.ds_client,
            )
            self.model_deployment_configuration_details.model_configuration_details.model_id = (
                self.model_id
            )
        return self.to_oci_model(data_science_models.CreateModelDeploymentDetails)

    def to_update_deployment(self):
        """Converts the deployment properties to OCI UpdateModelDeploymentDetails object."""
        return self.to_oci_model(data_science_models.UpdateModelDeploymentDetails)
