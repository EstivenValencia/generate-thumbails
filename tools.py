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
        client = self.session.client(type)
        return client

    def create_bucket(self, client, bucket_name) -> None:
        """
        Crea un bucket de S3 si no existe.
        
        Args:
            client (boto3.client): Cliente S3 de boto3
            bucket_name (str): Nombre del bucket a crear
        """
        try:
            # Primero, verificamos si el bucket ya existe
            try:
                client.head_bucket(Bucket=bucket_name)
                print(f"El bucket '{bucket_name}' ya existe.")
            except client.exceptions.ClientError as e:
                # Si el bucket no existe, lo creamos
                response = client.create_bucket(Bucket=bucket_name)
                print(f"Bucket '{bucket_name}' creado exitosamente. Respuesta: {response}")
        except Exception as e:
            print(f"Error al crear o verificar el bucket: {e}")

    def upload_file_to_bucket(self, client, bucket_name, file_path, object_name) -> None:
        """
        Sube un archivo al bucket de S3 especificado.
        
        Args:
            client (boto3.client): Cliente S3 de boto3
            bucket_name (str): Nombre del bucket
            file_path (str): Ruta local del archivo a subir
            object_name (str): Nombre del objeto en S3
        """
        try:
            response = client.upload_file(file_path, bucket_name, object_name)
            print(f"Respuesta de carga de archivo: {response}")
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")

    def create_table_dianamodb(self, client, table_name) -> None:
        """
        Crea una tabla en DynamoDB si no existe.
        
        Args:
            client (boto3.client): Cliente DynamoDB de boto3
            table_name (str): Nombre de la tabla a crear
        """
        try:
            table = client.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'filename',
                    'KeyType': 'HASH'  
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'filename',  
                    'AttributeType': 'S'  
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
            )
            print("Table status:", table)
        except client.exceptions.ClientError as e:
            print("La tabla ya existe")

    def create_sqs(self, client, sqs_name) -> tuple:
        """
        Crea una cola SQS FIFO y retorna su URL y ARN.
        
        Args:
            client (boto3.client): Cliente SQS de boto3
            sqs_name (str): Nombre de la cola SQS a crear
        
        Returns:
            tuple: (URL de la cola, ARN de la cola)
        """
        queue_name = sqs_name
        attributes = {
            'FifoQueue': 'true',                
            'ContentBasedDeduplication': 'true', 
        }

        try:
            self.sqs_client = client
            response = self.sqs_client.create_queue(
                QueueName=queue_name,
                Attributes=attributes
            )
            self.queue_url = response['QueueUrl'] 
            response = self.sqs_client.get_queue_attributes(
                QueueUrl=self.queue_url,
                AttributeNames=['QueueArn']
            )
            self.queue_arn = response['Attributes']['QueueArn']

            print(f"Cola FIFO creada: {queue_name}")
            return self.queue_url, self.queue_arn
        
        except Exception as e:
            print(f"Error creando la cola FIFO: {e}")
            return None

    def send_message_to_sqs(self, message_body, group_id) -> None:
        """
        Envía un mensaje a la cola SQS FIFO.
        
        Args:
            message_body (str): Cuerpo del mensaje a enviar
            group_id (str): ID del grupo de mensajes
        """
        try:
            response = self.sqs_client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=message_body,
                MessageGroupId=group_id
            )
            print(f"Mensaje enviado a la cola FIFO: {response['MessageId']}")
        except Exception as e:
            raise Exception(f'Error enviando el mensaje a la cola FIFO: {e}')
    
    def compress_lambda_folder(self, folder_path, zip_path) -> None:
        """
        Comprime una carpeta en un archivo zip para Lambda.
        
        Args:
            folder_path (str): Ruta de la carpeta a comprimir
            zip_path (str): Ruta donde se guardará el archivo zip
        """
        self.zip_path = zip_path 

        try:
            with zipfile.ZipFile(self.zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, folder_path)
                        if os.path.sep in arcname:  
                            zipf.write(file_path, arcname)
                        else:
                            zipf.write(file_path, file)
            print(f"{self.zip_path} creado exitosamente!")
        except Exception as e:
            raise Exception(f"Error al comprimir lambda_function.zip: {e}")

    def add_sqs_trigger_to_lambda(self, client, function_name) -> None:
        """
        Configura un trigger SQS para una función Lambda.
        
        Args:
            client (boto3.client): Cliente Lambda de boto3
            function_name (str): Nombre de la función Lambda
        """
        try:
            client.create_event_source_mapping(
                EventSourceArn= self.queue_arn,  
                FunctionName=function_name,  
                Enabled=True, 
                BatchSize=3,
            )
            print(f"Cola SQS configurada como trigger para la función Lambda '{function_name}'")
        except client.exceptions.ClientError as e:
            print(f"El trigger de SQS ya existe {e}")

    def deploy_lambda_fuction(self, client, folder_path, function_name, role_arn, timeout=30, memory_size=128):
        """
        Despliega una función Lambda.
        
        Args:
            client (boto3.client): Cliente Lambda de boto3
            folder_path (str): Ruta de la carpeta que contiene el código de la función
            function_name (str): Nombre de la función Lambda
            role_arn (str): ARN del rol de IAM para la función
            timeout (int): Tiempo de espera en segundos (por defecto 30)
            memory_size (int): Tamaño de memoria en MB (por defecto 128)
        
        Returns:
            dict: Respuesta de la creación de la función Lambda
        """
        try:
            self.compress_lambda_folder(folder_path, 'lambda.zip')

            with open(self.zip_path, 'rb') as zip_file:
                zip_content = zip_file.read()

            response = client.create_function(
                FunctionName=function_name,
                Runtime='python3.12',  
                Role=role_arn,  
                Handler='lambda_function.lambda_handler',  
                Code={
                    'ZipFile': zip_content  
                },
                Timeout=timeout,  
                MemorySize=memory_size  
            )

            print(f"Función Lambda '{function_name}' creada exitosamente!")

            self.add_sqs_trigger_to_lambda(client, function_name)
            return response
        
        except client.exceptions.ClientError as e:
            print(f"La funcion ya existe")

    def upload_folder_images(self, client, bucket_name, path):
        """
        Sube imágenes de una carpeta a un bucket S3 y envía mensajes a SQS.
        
        Args:
            client (boto3.client): Cliente S3 de boto3
            bucket_name (str): Nombre del bucket S3
            path (str): Ruta de la carpeta que contiene las imágenes
        """
        files = os.listdir(path)

        for file in files:
            if file.endswith('.jpg') or file.endswith('.png') or file.endswith(".jpeg"):
                try:
                    self.upload_file_to_bucket(client, bucket_name, f"{path}/{file}", f"{file}")

                    message = {
                        'bucket': bucket_name,
                        'file_path': f"{file}"
                    }
                    json_message = json.dumps(message)
                    # Enviar datos al SQS
                    self.send_message_to_sqs(json_message, 'upload_images')
                except Exception as e:
                    raise Exception(f"Error al cargar la imagen {file} [{e}]")


    def deploy_amplify_app(self, client, app_name, repository, branch, role_arn) -> str:
        """
        Despliega una aplicación en AWS Amplify y retorna la URL de la aplicación.

        Args:
            client (boto3.client): Cliente Amplify de boto3
            app_name (str): Nombre de la aplicación en Amplify
            repository (str): URL del repositorio de código fuente
            branch (str): Rama del repositorio a desplegar

        Returns:
            str: URL de la aplicación desplegada
        """
        try:
            response = client.create_app(
                name=app_name,
                repository=repository,
                platform='WEB',
                iamServiceRoleArn=role_arn
            )

            app_id = response['app']['appId']
            print(f"Aplicación '{app_name}' creada exitosamente con ID: {app_id}")

            client.create_branch(
                appId=app_id,
                branchName=branch,
            )

            app_url = response['app']['defaultDomain']
            print(f"Aplicación desplegada en: {app_url}")
            return app_url

        except Exception as e:
            raise Exception(f"Error al desplegar la aplicación en Amplify: {e}")    
