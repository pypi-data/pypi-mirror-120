from .models.models import Hub

def basetest(request):

    hello = Hub.objects.values_list("display_name", "id")
    return {
        'testname': hello
    }
