from django.http import HttpResponse
from django.shortcuts import render
import os
import PyPDF2

from django.shortcuts import render

def index(request):
    """Render the index page."""
    return render(request, 'score/index.html', {'qa_history': []})

# Dummy model generation (replace with real AI service if available)
def generate_answer(file_content, question):
    """Simulate an AI response based on the file content and question."""
    return f"Response to: {question}"


def process_input(request):
    if request.method == 'POST':
        # Handle file deletion
        if 'delete_file' in request.POST:
            if 'file_path' in request.session:
                file_path = request.session.pop('file_path')
                if os.path.exists(file_path):
                    os.remove(file_path)
            request.session.pop('qa_history', None)  # Clear question-answer history
            return render(request, 'score/index.html', {
                'response': "File deleted successfully.",
                'file_uploaded': None,
                'qa_history': []
            })

        # Retrieve the question
        question = request.POST.get('question', '')

        # Check whether to keep using the same file
        keep_file = request.POST.get('keep_file', 'no') == 'yes'

        # Handle file upload or reuse
        if keep_file and 'file_path' in request.session:
            file_path = request.session['file_path']
        else:
            uploaded_file = request.FILES.get('file', None)
            if not uploaded_file:
                return render(request, 'score/index.html', {
                    'response': "No file uploaded.",
                    'qa_history': request.session.get('qa_history', [])
                })

            # Save the uploaded file temporarily
            os.makedirs('temp', exist_ok=True)
            file_path = os.path.join('temp', uploaded_file.name)
            with open(file_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            # Save the file path in the session
            request.session['file_path'] = file_path

        # Process the file to extract content
        try:
            if file_path.endswith('.txt'):
                with open(file_path, 'r') as file:
                    file_content = file.read()
            elif file_path.endswith('.pdf'):
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    file_content = ''.join(page.extract_text() for page in reader.pages)
            else:
                return render(request, 'score/index.html', {
                    'response': "Unsupported file type.",
                    'qa_history': request.session.get('qa_history', [])
                })
        except Exception as e:
            return render(request, 'score/index.html', {
                'response': f"Error processing file: {e}",
                'qa_history': request.session.get('qa_history', [])
            })

        # Generate the response
        response = generate_answer(file_content, question)

        # Update question-answer history
        qa_history = request.session.get('qa_history', [])
        qa_history.append({'question': question, 'response': response})
        request.session['qa_history'] = qa_history

        # Render the template with updated history
        return render(request, 'score/index.html', {
            'response': response,
            'file_uploaded': os.path.basename(file_path),
            'qa_history': qa_history,
            'keep_file': True
        })

    # Render initial template
    return render(request, 'score/index.html', {'qa_history': []})