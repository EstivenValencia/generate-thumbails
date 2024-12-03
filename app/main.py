import os
import io
import boto3
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from config import *
import uvicorn

app = FastAPI()

# Configuración de S3
s3_client = boto3.client(
    's3', 
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
    region_name=AWS_REGION
)

@app.get("/", response_class=HTMLResponse)
async def serve_html():
    with open("index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/list-images")
async def list_images():
    try:
        images = []
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET_THUMBNAILS)
        print(pages)
        for page in pages:
            print(page)
            if 'Contents' in page:
                for obj in page['Contents']:
                    if obj['Key'].lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
                        images.append(obj['Key'])

        if not images:
            return {"message": "No se encontraron imágenes en el bucket", "images": []}

        return {"images": images}

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@app.get("/get-image/{image_name}")
async def get_image(image_name: str):
    try:
        response = s3_client.get_object(Bucket=BUCKET_THUMBNAILS, Key=image_name)
        return StreamingResponse(
            io.BytesIO(response['Body'].read()), 
            media_type=response['ContentType']
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Imagen no encontrada: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )