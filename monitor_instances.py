import boto3

REGION = "eu-north-1"

def get_running_instances():
    ec2_client = boto3.client("ec2", region_name=REGION)
    try:
        reservations = ec2_client.describe_instances(Filters=[
            {"Name": "instance-state-name", "Values": ["running"]}
        ]).get("Reservations")

        if not reservations:
            print("Активних інстансів не знайдено.")
            return

        for reservation in reservations:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]
                instance_type = instance["InstanceType"]
                public_ip = instance.get("PublicIpAddress", "немає")
                private_ip = instance.get("PrivateIpAddress", "немає")
                name = next((tag["Value"] for tag in instance.get("Tags", []) if tag["Key"] == "Name"), "без імені")
                print(f"{instance_id} | {name} | {instance_type} | Public IP: {public_ip} | Private IP: {private_ip}")
    except Exception as e:
        print(f"Помилка отримання списку інстансів: {e}")

if __name__ == "__main__":
    get_running_instances()