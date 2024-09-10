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

@router.post("/upload/")
async def upload_video(
    file: UploadFile = File(...), 
    problemId: str = Form(...),
    review: str = Form(...),
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
    transcode_job_data = trigger_transcode_job(s3_filename, token, problemId, review)

    return {
        "filename": file.filename,
        "s3_filename": s3_filename,
        "transcode_job": transcode_job_data
    }


@router.patch("/members/")
async def update_member(
    file: Optional[UploadFile] = File(None),  # 이미지 파일 업로드
    token: str = Depends(validate_token),  # 로그인 토큰 확인
    nickName: str = Form(...),  # 닉네임
    instagramId: Optional[str] = Form(None),  # 인스타그램 ID
    height: Optional[float] = Form(None),  # 키 (소수점 포함)
    gender: Optional[str] = Form(None),  # 성별
    reach: Optional[float] = Form(None)  # 리치(팔 길이, 소수점 포함)
):
    # Step 1: Initialize member data with optional values
    member_data = {
        "nickName": nickName,
        "instagramId": instagramId,
        "height": height,
        "gender": gender,
        "reach": reach,
    }

    # Step 2: If a file is provided, get S3 presigned URL and upload the file
    if file:
        presigned_url_data = image_get_presigned_url()
        presigned_url = presigned_url_data["upload_url"]
        s3_filename = presigned_url_data["file_name"]
        
        # Upload image to S3 using presigned URL
        file.file.seek(0)
        upload_to_s3(presigned_url, file.file)
        
        # Add profile image URL to member data
        member_data["profileImageUrl"] = f"{settings.cdn_domain}/{s3_filename}"

    # Step 3: Send the member data to the API server
    response = await patch_member(token, member_data)

    return {
        "message": "Member updated successfully",
        "member_data": member_data,
        "response": response
    }


@router.get("/")
async def healthcheck():
    return {"status": "healthy"}
