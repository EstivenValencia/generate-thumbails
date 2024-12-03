import boto3
from PIL import Image
import io
import json
import os
import datetime

# Configuraciones
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

size_resize = (100,100)
destination_bucket = 'thumnails-storage'
table_name = 'metadata_thumbnails'

def send_metada_to_dynamo(metada):
    """
    Envía los metadatos de la imagen a DynamoDB.

    Args:
        metada (dict): Diccionario con los metadatos de la imagen.

    Returns:
        None
    """
    table = dynamodb.Table(table_name)
    response = table.put_item(Item=metada)
    print("Ítem insertado exitosamente:", response)

def read_image(record):
    """
    Lee la información de la imagen desde el registro SQS y obtiene la imagen de S3.

    Args:
        record (dict): Registro SQS que contiene la información de la imagen.

    Returns:
        tuple: Contiene los datos de la imagen, nombre del bucket, nombre del archivo y ruta del archivo.
    """
    body = record['body']
    data = json.loads(body)
    bucket = data['bucket']
    file_path = data['file_path']

    response = s3_client.get_object(Bucket=bucket, Key=file_path)
    image_data = response['Body'].read()
    filename = os.path.basename(file_path)

    print(f"Bucket: {bucket}")
    print(f"Archivo: {file_path}")

    return image_data, bucket, filename, file_path

def save_thumbnail_image(destination_bucket, file_path, data):
    """
    Guarda la imagen miniatura en el bucket de destino de S3.

    Args:
        destination_bucket (str): Nombre del bucket de destino.
        file_path (str): Ruta del archivo en S3.
        data (bytes): Datos de la imagen miniatura.

    Returns:
        int: Tamaño del archivo guardado.
    """
    try:
        s3_client.put_object(
            Bucket=destination_bucket,  
            Key=file_path,        
            Body=data,              
            ContentType='image/png'
        )
        print(f"Imagen subida exitosamente a {destination_bucket}/{file_path}")
    except Exception as e:
        print(f"Error al subir la imagen: {e}")

    response = s3_client.head_object(Bucket=destination_bucket, Key=file_path)
    file_size = response['ContentLength']
    return file_size

def lambda_handler(event, context):
    """
    Función principal de Lambda que procesa los mensajes de SQS, crea miniaturas de imágenes y guarda los metadatos.

    Args:
        event (dict): Evento de Lambda que contiene los registros de SQS.
        context (object): Objeto de contexto de Lambda.

    Returns:
        dict: Respuesta de la función Lambda con código de estado y mensaje.
    """
    try:
        for record in event['Records']:
            image_data, bucket, filename, file_path = read_image(record)

            image = Image.open(io.BytesIO(image_data))
            image.thumbnail(size_resize)  

            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            buffer.seek(0)

            file_size = save_thumbnail_image(destination_bucket, file_path, buffer)
            buffer.close()
            del buffer

            metada_thumbnail = {
                "filename": filename,
                "URL": f"https://{destination_bucket}.s3.amazonaws.com/{file_path}",
                "size": file_size,
                "date_created": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "height": image.size[1],
                "width": image.size[0],  
            }
            print("Entra a dinamo")
            send_metada_to_dynamo(metada_thumbnail)

        return {
            'statusCode': 200,
            'body': 'Mensajes procesados exitosamente'
        }

    except Exception as e:
        print(f"Error procesando el mensaje: {e}")
        return {
            'statusCode': 500,
            'body': f'Error procesando el mensaje: {e}'
        }