#!/usr/bin/env python3
import os
import sys
from aws_cdk import App
from aws_cdk import DefaultStackSynthesizer
from tarea1.tarea1_stack import Tarea1Stack  # Asegúrate de que el nombre del archivo sea correcto

app = App()

default_stack_synthesizer = DefaultStackSynthesizer(
    file_assets_bucket_name="cdk-${Qualifier}-assets-${AWS::AccountId}-${AWS::Region}",
    bucket_prefix="",
    image_assets_repository_name="cdk-${Qualifier}-container-assets-${AWS::AccountId}-${AWS::Region}",
    deploy_role_arn="arn:${AWS::Partition}:iam::${AWS::AccountId}:role/LabRole",
    file_asset_publishing_role_arn="arn:${AWS::Partition}:iam::${AWS::AccountId}:role/LabRole",
    image_asset_publishing_role_arn="arn:${AWS::Partition}:iam::${AWS::AccountId}:role/LabRole",
    cloud_formation_execution_role="arn:${AWS::Partition}:iam::${AWS::AccountId}:role/LabRole",
    lookup_role_arn="arn:${AWS::Partition}:iam::${AWS::AccountId}:role/LabRole",
    bootstrap_stack_version_ssm_parameter="/cdk-bootstrap/${Qualifier}/version",
    generate_bootstrap_version_rule=True,
)

Tarea1Stack(app, "AwsCdkHackForAwsAcademyLearnerLabStack", synthesizer=default_stack_synthesizer)

app.synth()
