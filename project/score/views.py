from django.http import HttpResponse
from django.shortcuts import render
import os
import google.generativeai as genai
import PyPDF2
import logging

# Configure the Gemini API
genai.configure(api_key="AIzaSyB1OC8atXoq3yloVL31BRJC2mUqO3NsJRI")
model = genai.GenerativeModel("gemini-1.5-flash")

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Define the index view
def index(request):
    """Render the main chatbot interface."""
    # Check if session already contains previous responses
    previous_responses = request.session.get('previous_responses', [])

    # Add the initial message if it's the first visit
    if not previous_responses:
        previous_responses.append({
            'question': None,
            'response': "How can I help you today?"
        })
        request.session['previous_responses'] = previous_responses

    return render(request, 'score/index.html', {
        'previous_responses': previous_responses,
        'file_uploaded': request.session.get('file_path', None)
    })


def process_input(request):
    """Process user input, handle file upload/reuse, and generate responses."""
    if request.method == 'POST':
        # Check if the user wants to delete the file
        if 'delete_file' in request.POST:
            if 'file_path' in request.session:
                file_path = request.session.pop('file_path')
                if os.path.exists(file_path):
                    os.remove(file_path)
            request.session.pop('previous_responses', None)  # Clear question-answer history
            return render(request, 'score/index.html', {
                'response': "File deleted successfully.",
                'file_uploaded': None,
                'previous_responses': []
            })

        # Get the question from the form
        question = request.POST.get('question', '').strip()
        if not question:
            return render(request, 'score/index.html', {
                'response': "Please enter a question.",
                'file_uploaded': request.session.get('file_path', None),
                'previous_responses': request.session.get('previous_responses', [])
            })

        # Check if the user wants to keep using the previous file
        keep_file = request.POST.get('keep_file', 'no') == 'yes'

        # Handle file upload or reuse
        if keep_file and 'file_path' in request.session:
            file_path = request.session['file_path']
        else:
            uploaded_file = request.FILES.get('file', None)
            if not uploaded_file:
                return render(request, 'score/index.html', {
                    'response': "No file uploaded.",
                    'file_uploaded': None,
                    'previous_responses': request.session.get('previous_responses', [])
                })

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
                    file_content = ''.join(page.extract_text() for page in reader.pages if page.extract_text())
            else:
                return render(request, 'score/index.html', {
                    'response': "Unsupported file type.",
                    'file_uploaded': os.path.basename(file_path),
                    'previous_responses': request.session.get('previous_responses', [])
                })
        except Exception as e:
            logging.error(f"Error processing file: {e}")
            return render(request, 'score/index.html', {
                'response': f"Error processing file: {e}",
                'file_uploaded': os.path.basename(file_path),
                'previous_responses': request.session.get('previous_responses', [])
            })

        # Generate a response using the Gemini API
        try:
            prompt = f"Please summarize the following financial document in 2-3 concise sentences:\n{file_content}\n\nQuestion: {question}"
            response = model.generate_content(prompt)
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return render(request, 'score/index.html', {
                'response': f"Error generating response: {e}",
                'file_uploaded': os.path.basename(file_path),
                'previous_responses': request.session.get('previous_responses', [])
            })

        # Get the previous responses from the session, or start a new list
        previous_responses = request.session.get('previous_responses', [])
        previous_responses.append({
            'question': question,
            'response': response.text
        })

        # Save the updated list of responses in the session
        request.session['previous_responses'] = previous_responses

        # Pass the response and file details to the template
        return render(request, 'score/index.html', {
            'response': response.text,
            'file_uploaded': os.path.basename(file_path),
            'keep_file': True,
            'submitted_question': question,
            'previous_responses': previous_responses
        })

    # Handle GET requests
    return render(request, 'score/index.html', {
        'previous_responses': request.session.get('previous_responses', []),
        'file_uploaded': request.session.get('file_path', None)
    })