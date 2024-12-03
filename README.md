# Proyecto Thumbnails en AWS

Esta documentación describe cómo ejecutar el proyecto de generación de thumbnails en AWS.

## Configuración Inicial

1. **Crear un ambiente virtual de Python e instalar las dependencias del proyecto:**

 ```bash
   python -m venv .env
   pip install -r requirements.txt
```
2. **Configurar las credenciales de AWS:**

   Las credenciales necesarias (`aws_access_key_id`, `aws_secret_access_key`) deben configurarse en el script de configuración. Estas credenciales se obtienen al iniciar el laboratorio.

## Descripción del Proyecto

El proyecto utiliza la clase `Thumbnails` del script `tools.py` para gestionar la creación de los servicios en la nube (SaaS). Esta clase incluye métodos para:

- Crear la cola de mensajes SQS.
- Crear la función Lambda.
- Crear la tabla de DynamoDB.
- Crear los buckets de S3.

## Ejecución del Proyecto

Para ejecutar el proyecto, simplemente ejecute el siguiente comando:

```bash
python main_aws.py
```

## Probar datos de DynamoDB

Para probar el correcto funcionamiento de los metadatos insertados en dynamodb, ejecute el siguiente comando

```bash
    python scan_db.py
```

## Visualización de Imágenes

Para observar las imágenes, se utiliza una interfaz que permite seleccionar y visualizar las imágenes procesadas.

## Funcionamiento del Proyecto

1. **Creación de Clientes:**

   Se crean los clientes necesarios para los procesos.

2. **Creación de Buckets:**

   Se crean los buckets de S3 para almacenar las imágenes originales y los thumbnails procesados.

3. **Creación de la Tabla de DynamoDB:**

   Se crea una tabla en DynamoDB para almacenar los metadatos de las imágenes.

4. **Creación de la Cola de Mensajes SQS:**

   Se configura una cola de mensajes SQS para gestionar las tareas de procesamiento.

5. **Creación de la Función Lambda:**

   - Se desarrolla el script de Lambda.
   - Se agregan los paquetes necesarios utilizando PIP.
   - Se comprime la carpeta y se despliega el archivo ZIP en AWS Lambda.
   - Se configura un trigger de SQS para que la función Lambda se ejecute cada vez que llegue un mensaje.

6. **Despliegue de la Aplicación:**

   La aplicación se despliega utilizando AWS Amplify.

7. **Subida de Imágenes:**

   Se utiliza un método para leer las imágenes de la carpeta `images`, subirlas al bucket `media-images-storage` y crear un mensaje en SQS.

Esta documentación proporciona una guía completa para configurar y ejecutar el proyecto de generación de thumbnails en AWS. Asegúrese de seguir cada paso cuidadosamente para garantizar un despliegue exitoso.

