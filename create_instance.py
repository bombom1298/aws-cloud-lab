import boto3
import os

REGION = "eu-north-1"

def create_key_pair():
    ec2_client = boto3.client("ec2", region_name=REGION)
    try:
        key_pair = ec2_client.create_key_pair(KeyName="python-lab-key")
        private_key = key_pair["KeyMaterial"]
        with os.fdopen(os.open("python_lab_key.pem", os.O_WRONLY | os.O_CREAT, 0o600), "w+") as handle:
            handle.write(private_key)
        print("Ключову пару створено: python_lab_key.pem")
    except ec2_client.exceptions.ClientError as e:
        print(f"Помилка створення ключа (можливо, вже існує): {e}")

def create_instance():
    ec2_client = boto3.client("ec2", region_name=REGION)
    try:
        instances = ec2_client.run_instances(
            ImageId="ami-0aba19e56f3eaec05",
            MinCount=1,
            MaxCount=1,
            InstanceType="t3.micro",
            KeyName="python-lab-key",
            TagSpecifications=[{
                "ResourceType": "instance",
                "Tags": [{"Key": "Name", "Value": "python-lab-demo"}]
            }]
        )
        instance_id = instances["Instances"][0]["InstanceId"]
        print(f"Створено інстанс: {instance_id}")
        return instance_id
    except Exception as e:
        print(f"Помилка створення інстансу: {e}")
        return None

if __name__ == "__main__":
    create_key_pair()
    create_instance()