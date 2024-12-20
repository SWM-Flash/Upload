from fastapi import APIRouter, File, UploadFile, Header, HTTPException, Depends, Form, Body
import shutil
import os
from typing import Optional
from app.dependencies.token_validation import validate_token
from app.services.s3_upload import get_presigned_url, upload_to_s3, image_get_presigned_url
from app.services.transcode import trigger_transcode_job
from app.services.member_service import patch_member
from app.core.config import settings

router = APIRouter()

@router.post("/videos/upload/")
async def upload_video(
    file: UploadFile = File(...), 
    problemId: str = Form(...),
    thumbnailImageUrl: str = Form(...),
    solvedDate: str = Form(...),
    perceivedDifficulty: str = Form('보통'),
    review: Optional[str] = Form(''),
    token: str = Depends(validate_token)
):
    # Step 2: Get S3 presigned URL from external API
    presigned_url_data = get_presigned_url()
    presigned_url = presigned_url_data["upload_url"]
    s3_filename = presigned_url_data["file_name"]
    
    # Step 3: Upload video to S3 using presigned URL
    file.file.seek(0)
    upload_to_s3(presigned_url, file.file)

    # Step 4: Trigger transcode job
    request_data = {
        "video_name": s3_filename,
        "problem_id": problemId,
        "perceivedDifficulty": perceivedDifficulty,
        "thumbnailImageUrl": thumbnailImageUrl,
        "solvedDate": solvedDate,
        "review": review,
        "token": token
    }
    transcode_job_data = trigger_transcode_job(request_data)

    return {
        "filename": file.filename,
        "s3_filename": s3_filename,
        "transcode_job": transcode_job_data
    }

@router.post("/videos/upload/new/")
async def upload_video_with_problem(
    file: UploadFile = File(...),
    thumbnailImageUrl: str = Form(...),
    gymId: int = Form(...),
    sectorId: int = Form(...),
    holdId: int = Form(...),
    difficulty: str = Form(...),
    perceivedDifficulty: str = Form('보통'),
    solvedDate: str = Form(...),
    review: Optional[str] = Form(''),
    token: str = Depends(validate_token)
):
    # Step 2: Get S3 presigned URL from external API
    presigned_url_data = get_presigned_url()
    presigned_url = presigned_url_data["upload_url"]
    s3_filename = presigned_url_data["file_name"]
    
    # Step 3: Upload video to S3 using presigned URL
    file.file.seek(0)
    upload_to_s3(presigned_url, file.file)

    # Step 4: Trigger transcode job
    request_data = {
        "video_name": s3_filename,
        "thumbnailImageUrl": thumbnailImageUrl,
        "gymId": gymId,
        "sectorId": sectorId,
        "holdId": holdId,
        "difficulty": difficulty,
        "solvedDate": solvedDate,
        "perceivedDifficulty": perceivedDifficulty,
        "review": review,
        "token": token
    }
    transcode_job_data = trigger_transcode_job(request_data)

    return {
        "filename": file.filename,
        "s3_filename": s3_filename,
        "transcode_job": transcode_job_data
    }

@router.post("/admin/upload/")
async def upload_video(
    file: UploadFile = File(...), 
    problemId: str = Form(...),
    nickName: str = Form(...),
    instagramId: str = Form(...),
    review: Optional[str] = Form(''),
    thumbnailImageUrl: str = Form(...),
    solvedDate: str = Form(...),
    token: str = Depends(validate_token)
):
    # Step 2: Get S3 presigned URL from external API
    presigned_url_data = get_presigned_url()
    presigned_url = presigned_url_data["upload_url"]
    s3_filename = presigned_url_data["file_name"]
    
    # Step 3: Upload video to S3 using presigned URL
    file.file.seek(0)
    upload_to_s3(presigned_url, file.file)

    # Step 4: Trigger transcode job
    request_data = {
        "video_name": s3_filename,
        "problem_id": problemId,
        "perceivedDifficulty": '보통',
        "thumbnailImageUrl": thumbnailImageUrl,
        "solvedDate": solvedDate,
        "review": review,
        "token": token,
        "nickname": nickName,
        "instagramId": instagramId
    }
    transcode_job_data = trigger_transcode_job(request_data)

    return {
        "filename": file.filename,
        "s3_filename": s3_filename,
        "transcode_job": transcode_job_data
    }

@router.post("/admin/upload/new/")
async def upload_video(
    file: UploadFile = File(...),
    gymId: int = Form(...),
    sectorId: int = Form(...),
    holdId: int = Form(...),
    difficulty: str = Form(...),
    thumbnailImageUrl: str = Form(...),
    solvedDate: str = Form(...),
    nickName: str = Form(...),
    instagramId: str = Form(...),
    review: Optional[str] = Form(''),
    token: str = Depends(validate_token)
):
    # Step 2: Get S3 presigned URL from external API
    presigned_url_data = get_presigned_url()
    presigned_url = presigned_url_data["upload_url"]
    s3_filename = presigned_url_data["file_name"]
    
    # Step 3: Upload video to S3 using presigned URL
    file.file.seek(0)
    upload_to_s3(presigned_url, file.file)

    # Step 4: Trigger transcode job
    request_data = {
        "video_name": s3_filename,
        "gymId": gymId,
        "sectorId": sectorId,
        "holdId": holdId,
        "difficulty": difficulty,
        "perceivedDifficulty": '보통',
        "review": review,
        "token": token,
        "nickname": nickName,
        "instagramId": instagramId,
        "solvedDate": solvedDate,
        "thumbnailImageUrl": thumbnailImageUrl
    }
    transcode_job_data = trigger_transcode_job(request_data)

    return {
        "filename": file.filename,
        "s3_filename": s3_filename,
        "transcode_job": transcode_job_data
    }



@router.post("/images/")
async def update_member(
    file: Optional[UploadFile] = File(None)
):
    presigned_url_data = image_get_presigned_url()
    presigned_url = presigned_url_data["upload_url"]
    s3_filename = presigned_url_data["file_name"]
    
    # Upload image to S3 using presigned URL
    file.file.seek(0)
    upload_to_s3(presigned_url, file.file)

    return {
        "message": "Member updated successfully",
        "profileImageUrl": f"{settings.cdn_domain}/{s3_filename}"
    }


@router.get("/")
async def healthcheck():
    return {"status": "healthy"}
