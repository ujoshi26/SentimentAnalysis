import os
import csv
import io
from datetime import datetime, timezone

from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER", "atlas")
BLOB_NAME = os.getenv("BLOB_NAME", "data.csv")

def get_clients():
    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if conn_str:
        bsc = BlobServiceClient.from_connection_string(conn_str)
        append_client = AppendBlobClient.from_connection_string(
            conn_str, container_name=CONTAINER, blob_name=BLOB_NAME
        )
        return bsc, append_client

    # OIDC / Workload Identity path
    account = os.environ["AZURE_STORAGE_ACCOUNT"]  # required for account_url path
    account_url = f"https://{account}.blob.core.windows.net"
    cred = DefaultAzureCredential(exclude_shared_token_cache_credential=True)
    bsc = BlobServiceClient(account_url=account_url, credential=cred)
    append_client = AppendBlobClient(account_url=account_url,
                                     container_name=CONTAINER,
                                     blob_name=BLOB_NAME,
                                     credential=cred)
    return bsc, append_client

def main():
    bsc, append_client = get_clients()
    container_client = bsc.get_container_client(CONTAINER)

    # Ensure container exists (Terraform created it, but idempotent is nice)
    try:
        container_client.create_container()
    except ResourceExistsError:
        pass

    # Create the append blob with header if missing
    is_new = False
    try:
        append_client.get_blob_properties()
    except ResourceNotFoundError:
        append_client.create()
        is_new = True

    # Build a CSV line (example values; override with env if you like)
    ts = datetime.now(timezone.utc).isoformat()
    value1 = os.getenv("VALUE1", "42")
    value2 = os.getenv("VALUE2", "hello")

    sio = io.StringIO()
    writer = csv.writer(sio, lineterminator="\n")
    if is_new:
        writer.writerow(["timestamp", "value1", "value2"])
    writer.writerow([ts, value1, value2])
    data = sio.getvalue().encode("utf-8")

    append_client.append_block(data)
    print(f"Appended to {CONTAINER}/{BLOB_NAME}")

if __name__ == "__main__":
    main()

