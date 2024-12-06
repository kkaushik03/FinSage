from django.http import HttpResponse
from django.shortcuts import render
import os
import google.generativeai as genai
import PyPDF2

# Configure the Gemini API
genai.configure(api_key="AIzaSyB1OC8atXoq3yloVL31BRJC2mUqO3NsJRI")
model = genai.GenerativeModel("gemini-1.5-flash")

# Define the index view
def index(request):
    return render(request, 'score/index.html', {})

def process_input(request):
    if request.method == 'POST':
        # Check if the user wants to delete the file
        if 'delete_file' in request.POST:
            if 'file_path' in request.session:
                file_path = request.session.pop('file_path')
                if os.path.exists(file_path):
                    os.remove(file_path)
            return render(request, 'score/index.html', {'response': "File deleted successfully.", 'file_uploaded': None})

        # Get the question from the form
        question = request.POST.get('question', '')

        # Check if the user wants to keep using the previous file
        keep_file = request.POST.get('keep_file', 'no') == 'yes'

        # Handle file upload or reuse
        if keep_file and 'file_path' in request.session:
            file_path = request.session['file_path']
        else:
            uploaded_file = request.FILES.get('file', None)
            if not uploaded_file:
                return render(request, 'score/index.html', {'response': "No file uploaded."})

            # Save the uploaded file temporarily
            os.makedirs('temp', exist_ok=True)
            file_path = os.path.join('temp', uploaded_file.name)
            with open(file_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            # Save the file path in the session
            request.session['file_path'] = file_path

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

        # Pass the response and file details to the template
        return render(request, 'score/index.html', {
            'response': response.text,
            'file_uploaded': os.path.basename(file_path),
            'keep_file': True,
            'submitted_question': question  # Pass the submitted question to the template
        })

    return render(request, 'score/index.html', {})