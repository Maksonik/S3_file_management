from fastapi import APIRouter, Depends

from sfm.core.permission.rate_limiter import check_rate_limit

files_api_v1 = APIRouter(prefix="/files", tags=["files"], dependencies=[Depends(check_rate_limit)])
