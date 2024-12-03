# Variables de AWS
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_SESSION_TOKEN = ''
AWS_REGION = 'us-east-1'

# Carpeta de imagenes a procesar
FOLDER_PATH = 'images'

# Variables para almacenamiento en S3
BUCKET_THUMBNAILS = 'thumnails-storage'
BUCKET_MEDIA_IMAGES = 'media-images-storage'

# Variables de la funcion lambda y asociacion
LAMBDA_FOLDER_PATH = 'lambda'
FUNCTION_NAME = 'convert_image_to_thumbnail'
ROLE_ARN = 'arn:aws:iam::355629662964:role/LabRole'  # Se utiliza el rol lab de AWS ya que no se tiene permitido crear roles

# Variables de la tabla DynamoDB
TABLE_NAME = 'metadata_thumbnails'

# Repositorio de githu para despliegue de amplify
URL_REPOSITORY = 'https://github.com/EstivenValencia/generate-thumbails.git'