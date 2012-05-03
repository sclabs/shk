from .models import ExchangeContract, Bundle, IOU, RecallContract, Village
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

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
    contractsByMe = RecallContract.objects.filter(recipient.user=request.user)

    return render_to_response('contracts.html', locals())
