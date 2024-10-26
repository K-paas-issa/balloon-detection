from pydantic import BaseModel

class ImageRequest(BaseModel):
    balloonReportId : int
    serialCode : str
    path : str
