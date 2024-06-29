import logging
import time

from fastapi import APIRouter, File, UploadFile, BackgroundTasks

from api.application_layer.use_cases.upload import (
    ProcessFileException,
    UploadUseCase
)

router = APIRouter()

logger = logging.getLogger("billing_api." + __name__)


@router.post("/upload/")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    start_time = time.time()
    logger.info("File received, processing started.")

    try:
        data = await file.read() if file else None
        background_tasks.add_task(UploadUseCase.process_file, data)
    except ProcessFileException as error:
        logger.error(f"Error processing file: {error}")
    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Endpoint responded in {execution_time:.4f} seconds.")    

    return {"detail": "File received, processing started."}
