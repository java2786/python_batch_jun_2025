from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def welcome(request):
    return HttpResponse("<h1>Welcome to my App</h1>")

def student_list(request):
    html = """
    <!DOCTYPE html>
    <head>
        <title>Student List</title>
    </head>
    <body>
        <h1>Students</h1>    
        <ul>
            <li>Ramesh - CS162</li>
            <li>Mahesh - CS894</li>
            <li>Suresh - IT714</li>
            <li>Mukesh - AIML8673</li>
        </ul>
    </body>
    </html>
    """
    return HttpResponse(html)

