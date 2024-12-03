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
        # Lista solo los nombres de objetos, no descarga las imágenes
        response = s3_client.list_objects_v2(Bucket=BUCKET_THUMBNAILS)
        
        # Extrae solo los nombres de los archivos que son imágenes
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        images = [
            obj['Key'] for obj in response.get('Contents', []) 
            if any(obj['Key'].lower().endswith(ext) for ext in image_extensions)
        ]
        
        return images
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-image/{image_name}")
async def get_image(image_name: str):
    try:
        # Descarga la imagen específica solicitada
        response = s3_client.get_object(Bucket=BUCKET_THUMBNAILS, Key=image_name)
        
        # Devuelve la imagen como un flujo de bytes
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
