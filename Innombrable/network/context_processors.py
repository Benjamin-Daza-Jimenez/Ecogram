from .forms import PosteoForm

def posteo_form(request):
    postear = PosteoForm()
    return {
        'posteoForm': postear,
    }