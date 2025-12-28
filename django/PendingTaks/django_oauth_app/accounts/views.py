from django.shortcuts import render  
from django.contrib.auth.decorators import login_required  
  
  
def home(request):  
    """Home page view - shows login button or user info"""  
    return render(request, 'accounts/home.html')  
  
  
@login_required  
def dashboard(request):  
    """Dashboard view - only accessible after login"""  
    # Get social account info if exists  
    social_account = None  
    if request.user.socialaccount_set.exists():  
        social_account = request.user.socialaccount_set.first()  
      
    context = {  
        'social_account': social_account,  
    }  
    return render(request, 'accounts/dashboard.html', context)  