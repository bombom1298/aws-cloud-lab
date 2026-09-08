import boto3
import sys

REGION = "eu-north-1"

def stop_instance(instance_id):
    ec2_client = boto3.client("ec2", region_name=REGION)
    try:
        response = ec2_client.stop_instances(InstanceIds=[instance_id])
        state = response["StoppingInstances"][0]["CurrentState"]["Name"]
        print(f"Інстанс {instance_id}: статус — {state}")
    except Exception as e:
        print(f"Помилка зупинки інстансу: {e}")

def terminate_instance(instance_id):
    ec2_client = boto3.client("ec2", region_name=REGION)
    try:
        response = ec2_client.terminate_instances(InstanceIds=[instance_id])
        state = response["TerminatingInstances"][0]["CurrentState"]["Name"]
        print(f"Інстанс {instance_id}: статус — {state}")
    except Exception as e:
        print(f"Помилка видалення інстансу: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Використання: python manage_instance.py <stop|terminate> <instance_id>")
        sys.exit(1)

    action = sys.argv[1]
    instance_id = sys.argv[2]

    if action == "stop":
        stop_instance(instance_id)
    elif action == "terminate":
        terminate_instance(instance_id)
    else:
        print("Невідома дія. Використовуй 'stop' або 'terminate'.")