from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    CfnOutput
)
from constructs import Construct

class Tarea1Stack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Definir el VPC
        vpc = ec2.Vpc(self, "MyVpc", max_azs=3)

        # Definir el rol IAM
        role = iam.Role.from_role_arn(self, "LabRole", "arn:aws:iam::086310855935:role/LabRole")

        # AMI y tipo de instancia
        machine_image = ec2.MachineImage.generic_linux({
            'us-east-1': 'ami-0aa28dab1f2852040'
        })
        instance_type = ec2.InstanceType.of(
            ec2.InstanceClass.BURSTABLE2, 
            ec2.InstanceSize.MICRO
        )
        
        # Crear el grupo de seguridad
        security_group = ec2.SecurityGroup(self, "MySecurityGroup",
            vpc=vpc,
            description="Allow SSH and HTTP access",
            allow_all_outbound=True
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), 
            ec2.Port.tcp(22), 
            "Permitir acceso SSH"
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), 
            ec2.Port.tcp(80), 
            "Permitir acceso HTTP"
        )

        # Referenciar el par de llaves existente
        key_pair = ec2.KeyPair.from_key_pair_name(self, "KeyPair", "vockey")

        # Crear la instancia EC2
        instance = ec2.Instance(self, "EC2Instance",
            instance_type=instance_type,
            machine_image=machine_image,
            vpc=vpc,
            role=role,
            security_group=security_group,
            vpc_subnets={"subnet_type": ec2.SubnetType.PUBLIC},
            key_pair=key_pair,  # Usar el par de llaves referenciado
            block_devices=[ec2.BlockDevice(
                device_name="/dev/sda1",
                volume=ec2.BlockDeviceVolume.ebs(20)  # Tamaño del volumen de acuerdo al .yml
            )]
        )

        # Script de usuario para clonar repositorios
        user_data = ec2.UserData.custom("""
            #!/bin/bash
            cd /var/www/html/
            git clone https://github.com/utec-cc-2024-2-test/websimple.git
            git clone https://github.com/utec-cc-2024-2-test/webplantilla.git
            ls -l
        """)
        instance.add_user_data(user_data.render())

        # Salidas del stack
        CfnOutput(self, "InstanceId",
            value=instance.instance_id,
            description="ID de la instancia EC2"
        )

        CfnOutput(self, "InstancePublicIP",
            value=instance.instance_public_ip,
            description="IP pública de la instancia"
        )

        CfnOutput(self, "websimpleURL",
            value=f"http://{instance.instance_public_ip}/websimple",
            description="URL de websimple"
        )

        CfnOutput(self, "webplantillaURL",
            value=f"http://{instance.instance_public_ip}/webplantilla",
            description="URL de webplantilla"
        )
