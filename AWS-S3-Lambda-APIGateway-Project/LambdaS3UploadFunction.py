import json
import boto3
import base64
import os

s3 = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        print("Received event: ", json.dumps(event))  # Log the incoming event
        
        # Extract the body and parse it
        body = json.loads(event['body'])
        folder_id = body['folder_id']  # Extract folder_id from the request body
        files = body['files']  # Expecting 'files' to be a list of dictionaries
        
        uploaded_files = []
        
        for file in files:
            file_content = base64.b64decode(file['file'])
            file_name = file['filename']
            
            # Create the full S3 key with the provided folder ID
            s3_key = f"{folder_id}/{file_name}"

            # Upload the file to the specified folder in S3
            s3.put_object(Bucket=bucket_name, Key=s3_key, Body=file_content)

            uploaded_files.append(s3_key)  # Store the uploaded file path

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Files uploaded successfully!', 'files': uploaded_files})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
