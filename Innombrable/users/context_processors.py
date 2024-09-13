from .forms import UserLoginForm, UserSignUpForm

def login_form(request):
    login_form = UserLoginForm()
    signup_form = UserSignUpForm()
    return{
        'loginForm': login_form,
        'signupForm': signup_form
    }
