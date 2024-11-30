import boto3

# Definir las credenciales de AWS
aws_access_key_id = 'TU_ACCESS_KEY_ID'
aws_secret_access_key = 'TU_SECRET_ACCESS_KEY'
aws_region = 'tu-region'  # por ejemplo, 'us-west-2'

# Crear un cliente de S3 con las credenciales
s3_client = boto3.client('s3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)
# Nombre del bucket que deseas crear
bucket_name = 'mi-nuevo-bucket'

# Crear el bucket
try:
    response = s3_client.create_bucket(Bucket=bucket_name)
    print(f"Bucket '{bucket_name}' creado exitosamente.")
    print(f"Respuesta: {response}")
except Exception as e:
    print(f"Error al crear el bucket: {e}")