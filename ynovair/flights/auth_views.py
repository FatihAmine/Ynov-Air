from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    """Extended user registration form with email and additional fields"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    first_name = forms.CharField(required=True, max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Prénom'
    }))
    last_name = forms.CharField(required=True, max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nom'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom d\'utilisateur'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form with styled fields"""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nom d\'utilisateur'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mot de passe'
    }))


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bienvenue {user.username}! Votre compte a été créé avec succès.')
            return redirect('home')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'flights/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {username}!')
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'flights/login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté avec succès.')
    return redirect('home')


@login_required
def profile_view(request):
    """User profile view showing user info and bookings"""
    from flights.models import Booking
    
    # Get user's bookings
    user_bookings = Booking.objects.filter(
        passenger__email=request.user.email
    ).select_related('flight', 'flight__origin', 'flight__destination', 'passenger').order_by('-booking_date')
    
    context = {
        'user': request.user,
        'bookings': user_bookings,
    }
    
    return render(request, 'flights/profile.html', context)


class UserUpdateForm(forms.ModelForm):
    """Form for updating user profile"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


@login_required
def profile_update_view(request):
    """Update user profile information"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès!')
            return redirect('profile')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'flights/profile_update.html', {'form': form})
