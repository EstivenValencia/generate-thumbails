import boto3
import os
import zipfile
import json

class Thumbnails():
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_session_token, aws_region):
        """
        Inicializa la sesión de AWS.
        
        Args:
            aws_access_key_id (str): ID de clave de acceso de AWS
            aws_secret_access_key (str): Clave de acceso secreta de AWS
            aws_session_token (str): Token de sesión de AWS
            aws_region (str): Región de AWS
        
        Returns:
            None
        """
        self.session = boto3.session.Session(
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key,
                                aws_session_token=aws_session_token,
                                region_name=aws_region)
    
    def create_client(self, type) -> boto3.client:
        """
        Crea y retorna un cliente de AWS del tipo especificado.
        
        Args:
            type (str): Tipo de cliente AWS (e.g., 's3', 'dynamodb')
        
        Returns:
            boto3.client: Cliente AWS del tipo especificado
        """
        return self.session.client(type)

    def create_bucket(self, client, bucket_name) -> None:
        """
        Crea un bucket de S3 si no existe.
        
        Args:
            client (boto3.client): Cliente S3 de boto3
            bucket_name (str): Nombre del bucket a crear
        
        Returns:
            None
        """
        # ... (código existente)

    def upload_file_to_bucket(self, client, bucket_name, file_path, object_name) -> None:
        """
        Sube un archivo al bucket de S3 especificado.
        
        Args:
            client (boto3.client): Cliente S3 de boto3
            bucket_name (str): Nombre del bucket
            file_path (str): Ruta local del archivo a subir
            object_name (str): Nombre del objeto en S3
        
        Returns:
            None
        """
        # ... (código existente)

    def create_table_dianamodb(self, client, table_name) -> None:
        """
        Crea una tabla en DynamoDB si no existe.
        
        Args:
            client (boto3.client): Cliente DynamoDB de boto3
            table_name (str): Nombre de la tabla a crear
        
        Returns:
            None
        """
        # ... (código existente)

    def create_sqs(self, client, sqs_name) -> tuple:
        """
        Crea una cola SQS FIFO y retorna su URL y ARN.
        
        Args:
            client (boto3.client): Cliente SQS de boto3
            sqs_name (str): Nombre de la cola SQS a crear
        
        Returns:
            tuple: (URL de la cola, ARN de la cola)
        """
        # ... (código existente)

    def send_message_to_sqs(self, message_body, group_id) -> None:
        """
        Envía un mensaje a la cola SQS FIFO.
        
        Args:
            message_body (str): Cuerpo del mensaje a enviar
            group_id (str): ID del grupo de mensajes
        
        Returns:
            None
        """
        # ... (código existente)
    
    def compress_lambda_folder(self, folder_path, zip_path) -> None:
        """
        Comprime una carpeta en un archivo zip para Lambda.
        
        Args:
            folder_path (str): Ruta de la carpeta a comprimir
            zip_path (str): Ruta donde se guardará el archivo zip
        
        Returns:
            None
        """
        # ... (código existente)

    def add_sqs_trigger_to_lambda(self, client, function_name) -> None:
        """
        Configura un trigger SQS para una función Lambda.
        
        Args:
            client (boto3.client): Cliente Lambda de boto3
            function_name (str): Nombre de la función Lambda
        
        Returns:
            None
        """
        # ... (código existente)

    def deploy_lambda_fuction(self, client, folder_path, function_name, role_arn, timeout=30, memory_size=128):
        """
        Despliega una función Lambda.

        Args:
            client (boto3.client): Cliente Lambda de boto3
            folder_path (str): Ruta de la carpeta que contiene el código de la función
            function_name (str): Nombre de la función Lambda
            role_arn (str): ARN del rol IAM para la función Lambda
            timeout (int, optional): Tiempo de espera en segundos. Por defecto 30.
            memory_size (int, optional): Tamaño de memoria en MB. Por defecto 128.

        Returns:
            dict: Respuesta de la creación de la función Lambda
        """
        # ... (código existente)

    def upload_folder_images(self, client, bucket_name, path):
        """
        Sube imágenes de una carpeta a un bucket S3 y envía mensajes a SQS.

        Args:
            client (boto3.client): Cliente S3 de boto3
            bucket_name (str): Nombre del bucket S3
            path (str): Ruta de la carpeta que contiene las imágenes

        Returns:
            None
        """
        # ... (código existente)