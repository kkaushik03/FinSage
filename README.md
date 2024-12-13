# FinSage

Many financial documents are riddled with complicated jargon that is overwhelming for people who do not have a financial background. This serves as a significant disadvantage considering that these documents may have detrimental financial consequences to the receiver if not understood properly. 

Finsage aims to solve this problem by providing a chatbot where users receive direct answers to questions on their specific documents so that they can take action appropriately. 

## Getting Started

### Dependencies

Prior to running the application, the following libraries must be installed via these commands:
```
pip install PyPDF2
pip install django
pip install google-generativeai
```

### Executing program

To run the program, clone the repository and enter the Finsage/project directory. Then run the following to start the server:
```
python3 manage.py runserver
```


## Folder Structure

Finsage/project
* contains all code files
Finsage/project/finsage
* contains code for Django application to run
Finsage/project/score
* contains the UI templates in index.html. The structure goes from CSS at the beginning, HTML in the middle, to JavaScript near the end of the file.
* contains the AI code in view.py. The process_input function is run whenever the user enters input, either by uploading a file or by submitting a question.

## Authors

Contributors:
Khushi Kaushik
Huyen Nguyen
Hiba Mughal

