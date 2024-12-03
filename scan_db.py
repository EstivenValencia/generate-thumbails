import boto3
from config import *

# Crear cliente de DynamoDB
dynamodb = boto3.client('dynamodb',
                                aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                aws_session_token=AWS_SESSION_TOKEN,
                                region_name=AWS_REGION)

# Parámetros de la tabla
table_name = 'metadata_thumbnails'

# Escanear la tabla
response = dynamodb.scan(TableName=table_name)

# Leer los elementos encontrados
items = response.get('Items', [])
for item in items:
    print(item)