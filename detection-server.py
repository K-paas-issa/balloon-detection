from fastapi import FastAPI, BackgroundTasks
from fastapi import Response, status
from ImageRequestDto import ImageRequest
from image_service import image_process
app = FastAPI()

@app.post("/api/process-image")
def get_climate_data(image_request : ImageRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(image_process, image_request)
    return Response(status_code=status.HTTP_202_ACCEPTED)