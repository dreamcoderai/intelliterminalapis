# app/core/storage.py

import os
from pathlib import Path
from uuid import uuid4

import boto3
from dotenv import load_dotenv
from fastapi import HTTPException, UploadFile

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def _get_spaces_settings():
    settings = {
        "region": os.getenv("SPACE_REGION"),
        "bucket": os.getenv("SPACE_BUCKET"),
        "secret": os.getenv("SPACE_SECRET"),
        "key": os.getenv("SPACE_ID"),
        "endpoint_url": os.getenv("SPACE_URL"),
        "public_endpoint": os.getenv("SPACE_END_POINT"),
    }

    missing = [name for name, value in settings.items() if name != "public_endpoint" and not value]
    if missing:
        raise HTTPException(
            status_code=500,
            detail=f"Missing Space configuration: {', '.join(missing)}",
        )

    if not settings["public_endpoint"]:
        settings["public_endpoint"] = (
            f"https://{settings['bucket']}.{settings['region']}.digitaloceanspaces.com"
        )

    return settings


def upload_patient_file(file: UploadFile, patient_id: int, category: str) -> str:
    settings = _get_spaces_settings()

    client = boto3.client(
        "s3",
        region_name=settings["region"],
        endpoint_url=settings["endpoint_url"],
        aws_access_key_id=settings["key"],
        aws_secret_access_key=settings["secret"],
    )

    file_extension = Path(file.filename or "").suffix
    object_key = (
        f"intelliterminal/patientdata/{category}/{patient_id}-{uuid4().hex}{file_extension}"
    )

    extra_args = {"ACL": "public-read"}
    if file.content_type:
        extra_args["ContentType"] = file.content_type

    try:
        client.upload_fileobj(file.file, settings["bucket"], object_key, ExtraArgs=extra_args)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload {category} to object storage",
        ) from exc

    return f"{settings['public_endpoint'].rstrip('/')}/{object_key}"


def upload_user_file(file: UploadFile, user_id: int) -> str:
    """Upload a user profile picture to intelliterminal/users/profiles/."""
    settings = _get_spaces_settings()

    client = boto3.client(
        "s3",
        region_name=settings["region"],
        endpoint_url=settings["endpoint_url"],
        aws_access_key_id=settings["key"],
        aws_secret_access_key=settings["secret"],
    )

    file_extension = Path(file.filename or "").suffix
    object_key = f"intelliterminal/users/profiles/{user_id}-{uuid4().hex}{file_extension}"

    extra_args = {"ACL": "public-read"}
    if file.content_type:
        extra_args["ContentType"] = file.content_type

    try:
        client.upload_fileobj(file.file, settings["bucket"], object_key, ExtraArgs=extra_args)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to upload profile picture to object storage",
        ) from exc

    return f"{settings['public_endpoint'].rstrip('/')}/{object_key}"


def delete_patient_files(urls: list[str]) -> None:
    """Delete a list of DO Spaces objects given their public URLs. Silently skips None/empty."""
    file_urls = [u for u in urls if u]
    if not file_urls:
        return

    settings = _get_spaces_settings()
    public_base = settings["public_endpoint"].rstrip("/")

    client = boto3.client(
        "s3",
        region_name=settings["region"],
        endpoint_url=settings["endpoint_url"],
        aws_access_key_id=settings["key"],
        aws_secret_access_key=settings["secret"],
    )

    objects = []
    for url in file_urls:
        if url.startswith(public_base):
            key = url[len(public_base):].lstrip("/")
            objects.append({"Key": key})

    if not objects:
        return

    try:
        client.delete_objects(
            Bucket=settings["bucket"],
            Delete={"Objects": objects, "Quiet": True},
        )
    except Exception as exc:
        print(f"Warning: failed to delete files from object storage: {exc}")
