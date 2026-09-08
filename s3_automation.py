import boto3
from botocore.exceptions import ClientError

REGION = "eu-north-1"

def create_bucket(bucket_name):
    s3_client = boto3.client("s3", region_name=REGION)
    try:
        location = {"LocationConstraint": REGION}
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        print(f"Бакет '{bucket_name}' успішно створено.")
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "BucketAlreadyExists" or error_code == "BucketAlreadyOwnedByYou":
            print(f"Бакет '{bucket_name}' вже існує.")
        else:
            print(f"Помилка створення бакета: {e}")

def upload_file(file_name, bucket_name, s3_key):
    s3_client = boto3.client("s3", region_name=REGION)
    try:
        s3_client.upload_file(file_name, bucket_name, s3_key)
        print(f"Файл '{file_name}' завантажено як '{s3_key}'.")
    except FileNotFoundError:
        print(f"Локальний файл '{file_name}' не знайдено.")
    except ClientError as e:
        print(f"Помилка завантаження файлу: {e}")

def read_file(bucket_name, s3_key):
    s3_client = boto3.client("s3", region_name=REGION)
    try:
        obj = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
        content = obj["Body"].read().decode("utf-8")
        print(f"Вміст '{s3_key}':\n{content[:200]}")
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchKey":
            print(f"Файл '{s3_key}' не знайдено в бакеті '{bucket_name}'.")
        else:
            print(f"Помилка читання файлу: {e}")

if __name__ == "__main__":
    bucket = "ctlab2onukevych"

    create_bucket(bucket)

    read_file(bucket, "неіснуючий_файл.csv")

    read_file(bucket, "usd_2022.csv")