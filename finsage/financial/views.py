from django.shortcuts import render
from google.cloud import documentai_v1beta3 as documentai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt  # Use with caution, ensure CSRF protection is in place for production
def parse_document(request):
    if request.method == "POST" and request.FILES.get('document'):
        # Initialize Document AI client
        client = documentai.DocumentUnderstandingServiceClient()

        # Read the uploaded file
        uploaded_file = request.FILES['document']
        content = uploaded_file.read()

        # Configure the request
        document = {
            "content": content,
            "mime_type": "application/pdf",  # Adjust if handling other file types
        }

        # Define features for Document AI processing
        request_data = {
            "document": document,
            "features": [{"type_": documentai.DocumentUnderstandingServiceClient.Feature.Type.TEXT_DETECTION}],
        }

        # Process the document
        try:
            response = client.process_document(request=request_data)
            # Extract text from the response
            extracted_text = response.document.text
            return JsonResponse({"extracted_text": extracted_text})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request. Please use POST with a file upload."}, status=400)