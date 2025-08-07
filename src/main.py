from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import helpers

app= FastAPI()


@app.get("/")
def read_index():
    # helpers.generate_image()
    return {"hello" : "world"}


class ImageGenerationRequest (BaseModel):
    prompt : str


@app.post("/generate")
def generate_image(data: ImageGenerationRequest):
    try:

        pred_results= helpers.generate_image(data.prompt)
        return pred_results
    except Exception as e: 
        raise HTTPException(status_code = 500, detail= str(e))
    