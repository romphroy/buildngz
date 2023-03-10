from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User

def registerUser(request):
    # Request is POST. 
    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        
        # Valid form, Save form.
        if form.is_valid():
            
            # Create user using the form            
            # Assign user role
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.role = User.CUSTOMER
            # user.save()
            
            # create the user using the create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email,username=username,password=password)
            user.role = User.CUSTOMER
            user.save()
            print('The User was created')
            return redirect('registerUser')
        else:
            print('Invalid Form')
            print(form.errors)
    # Not POST, show the registration form
    else:
        form = UserForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/registerUser.html', context)
