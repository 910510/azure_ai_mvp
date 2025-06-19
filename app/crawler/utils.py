import csv
from azure.storage.blob import BlobServiceClient

def save_to_csv(items, filename):
    with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=["rank", "title", "score", "genre", "year", "synopsis"])
        writer.writeheader()
        for item in items:
            writer.writerow(item)
    print(f"✅ CSV 저장 완료: {filename}")



def upload_csv_to_blob(local_path, container_name, blob_name, connection_string):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    try:
        container_client.create_container()
    except Exception:
        pass  # 이미 존재하는 경우 무시

    blob_client = container_client.get_blob_client(blob_name)

    with open(local_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    
    print(f"✅ Azure Blob 업로드 완료: {blob_name}")