from .models import ExchangeContract, Bundle, IOU, RecallContract, Village
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from .forms import VillageForm

@login_required
def exchange(request):
    # get all the contracts
    contracts = ExchangeContract.objects.all()
    
    # dictionaries that map contracts to lists of bundles
    sendBundles = {}
    receiveBundles = {}

    # fill in the dictionaries
    for contract in contracts:
        bundles = Bundle.objects.filter(contract=contract)
        sendBundles[contract.id] = []
        receiveBundles[contract.id] = []
        for bundle in bundles:
            if bundle.send:
                sendBundles[contract.id].append(bundle)
            else:
                receiveBundles[contract.id].append(bundle)
                
    return render_to_response('exchange.html', locals())

@login_required
def IOUs(request):
    # get all the IOUs held by the user
    iousHeld = IOU.objects.filter(holder=request.user)

    # get all the IOUs issued by the user
    iousIssued = IOU.objects.filter(issuer=request.user)

    return render_to_response('ious.html', locals())

@login_required
def contracts(request):
    # get all the contracts issued to the player
    contractsToMe = RecallContract.objects.filter(sender=request.user)

    # get all the contracts issued by the player
    # first get all the user's villages
    villages = Village.objects.filter(user=request.user)

    # list of all the contracts
    contractsByMe = []

    # fill in the list
    for village in villages:
        contractsByMe.append(RecallContract.objects.filter(recipient=village))

    return render_to_response('contracts.html', locals())

@login_required
def villages(request):
    # get all the user's villages
    villages = Village.objects.filter(user=request.user)

    # figure out which ones are involved in open contracts
    # a dictionary to keep track of this
    deletable = {}

    # fill in the dictionary
    for village in villages:
        if RecallContract.objects.filter(recipient=village):
            deletable[village.id] = False
        else:
            deletable[village.id] = True

    return render_to_response('villages.html', locals())

@login_required
def addVillage(request):
    if request.method == 'POST':
        form = VillageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            newVillage = Village(name=cd['name'], user=request.user)
            newVillage.save()
            return redirect('villages')
    else:
        form = VillageForm()
    return render_to_response('addVillage.html', {'form': form},   RequestContext(request))

@login_required
def removeVillage(request, id):
    try:
        village = Village.objects.get(id=id)
        if village.user == request.user:
            if RecallContract.objects.filter(recipient=village):
                pass
            else:
                village.delete()
    except Village.DoesNotExist:
        pass
    return redirect('villages')
