from django.http import HttpResponse
from django.shortcuts import render
import os
import google.generativeai as genai
import PyPDF2

# Configure the Gemini API
genai.configure(api_key="AIzaSyB1OC8atXoq3yloVL31BRJC2mUqO3NsJRI")
model = genai.GenerativeModel("gemini-1.5-flash")

def index(request):
    """
    Render the index.html template.
    """
    return render(request, 'score/index.html')

def hello_world(request):
    """
    Return a simple 'Hello World' message.
    """
    return HttpResponse("Hello World")
from django.shortcuts import render
import os
import google.generativeai as genai
import PyPDF2

# Configure the Gemini API
genai.configure(api_key="AIzaSyB1OC8atXoq3yloVL31BRJC2mUqO3NsJRI")
model = genai.GenerativeModel("gemini-1.5-flash")

def process_input(request):
    if request.method == 'POST':
        # Get the question from the form
        question = request.POST.get('question', '')

        # Get the uploaded file
        uploaded_file = request.FILES.get('file', None)
        if not uploaded_file:
            return render(request, 'score/index.html', {'response': "No file uploaded."})

        # Ensure the 'temp' directory exists
        os.makedirs('temp', exist_ok=True)

        # Save the uploaded file temporarily
        file_path = os.path.join('temp', uploaded_file.name)
        with open(file_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # Determine the file type and read content
        try:
            if file_path.endswith('.txt'):
                with open(file_path, 'r') as file:
                    file_content = file.read()
            elif file_path.endswith('.pdf'):
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    file_content = ''.join(page.extract_text() for page in reader.pages)
            else:
                return render(request, 'score/index.html', {'response': "Unsupported file type."})
        except Exception as e:
            return render(request, 'score/index.html', {'response': f"Error processing file: {e}"})

        # Generate a response using the Gemini API
        prompt = f"File Content:\n{file_content}\n\nQuestion: {question}"
        response = model.generate_content(prompt)
        
        # Clean up temporary file
        os.remove(file_path)

        # Pass the response to the template
        return render(request, 'score/index.html', {'response': response.text})

    return render(request, 'score/index.html', {'response': "Invalid request method."})