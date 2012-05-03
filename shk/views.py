from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

def loggedout(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/logout/')
    return render_to_response('registration/logout.html')
