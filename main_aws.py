from tools import Thumbnails
from config import *

if __name__ == "__main__":
    thumbnail = Thumbnails(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_REGION)

    # Creacion de los buckets
    s3_client = thumbnail.create_client('s3')  # Se crea el cliente de s3

    thumbnail.create_bucket(s3_client, BUCKET_THUMBNAILS)  # Se crea el bucket para las miniaturas
    thumbnail.create_bucket(s3_client, BUCKET_MEDIA_IMAGES)  # Se crea el bucket para las imagenes originales

    # Creacion de la cola de mensajes    
    sqs_client = thumbnail.create_client('sqs')
    thumbnail.create_sqs(sqs_client, 'convert_image_to_thumbnail.fifo') 

    # Creacion de la funcion lambda
    lambda_client = thumbnail.create_client('lambda')
    thumbnail.deploy_lambda_fuction(lambda_client, LAMBDA_FOLDER_PATH, FUNCTION_NAME, ROLE_ARN, timeout=30, memory_size=500)  # Se crea la función lambda

    # Creacion de la tabla DynamoDB
    dynamo_client = thumbnail.create_client('dynamodb')
    thumbnail.create_table_dianamodb(dynamo_client, TABLE_NAME)  # Se crea la tabla para almacenar los metadatos de las miniaturas

    # Carga de imagenes y mensajes a SQS
    thumbnail.upload_folder_images(s3_client, BUCKET_MEDIA_IMAGES, FOLDER_PATH)

    # Desplegar aplciacion web para visualizacion
    amplify_client = thumbnail.create_client('amplify')
    thumbnail.deploy_amplify_app(amplify_client, 'thumbnails-app', URL_REPOSITORY)  # Se despliega la aplicacion web en Amplify