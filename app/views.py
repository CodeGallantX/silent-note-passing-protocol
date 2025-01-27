import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as auth_logout, update_session_auth_hash
from django.http import JsonResponse
from .models import Note

# Create your views here.
def index(request):
    return render(request, 'index.html')

# Registration view
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not re.match(r'^[a-z0-9_]+$', username):
            messages.error(request, "Username must contain only lowercase letters, numbers, and underscores.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose a different username.")
        else:
            User.objects.create(username=username, password=password)
            messages.success(request, "Registration successful! Redirecting...")
            return redirect('/inbox')
    return render(request, 'register.html')

# Login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not re.match(r'^[a-z0-9_]+$', username):
            messages.error(request, "Username must contain only lowercase letters, numbers, and underscores.")
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect(inbox)
            else:
                messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def logout_user(request):
    auth_logout(request)
    messages.success("You have been logged out.")
    return redirect(index)

@login_required
def inbox(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to view your inbox.")
        return redirect(login)
    else:
        notes = Note.objects.filter(receiver=request.user)
        context= {
            'notes': notes
        }
    return render(request, 'inbox.html', context)

def write(request):
    if request.method == "POST":
        try:
            # Get sender and receiver as User instances
            sender_username = request.POST['sender']
            receiver_username = request.POST['receiver']
            sender = User.objects.get(username=sender_username)
            receiver = User.objects.get(username=receiver_username)

            # Get subject and body
            subject = request.POST['subject']
            body = request.POST['body']

            # Create the note
            Note.objects.create(sender=sender, receiver=receiver, subject=subject, body=body)

            # Return success message
            return render(request, 'write.html', {'message': 'Note sent successfully!'})
        except User.DoesNotExist:
            # Handle cases where the sender or receiver username does not exist
            return render(request, 'write.html', {'error': 'Sender or receiver username not found.'})
    return render(request, 'write.html')

@login_required
def sent(request): 
    sent_notes = Note.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, 'sent.html', {'sent_notes': sent_notes})

@csrf_exempt
def delete_note(request, note_id):
    if request.method == "POST":
        note = get_object_or_404(Note, id=note_id)
        note.delete()
        return messages.success({"success": True, "message": "Note deleted successfully"})
    return JsonResponse({"success": False, "message": "Invalid request method"})

def reset_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # Keep the user logged in after changing password
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'reset-password.html', {'form': form})
