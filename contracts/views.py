from .models import ExchangeContract, Bundle
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

#def availableContracts(request):

#def outstandingIOUs(request):

#def heldIOUs(request):

#def issuedContracts(request):

#def acceptedContracts(request):

@login_required
def exchange(request):
    # get all the contracts
    #contracts = []
    try:
        #contracts.append(ExchangeContract.objects.get())
        contracts = ExchangeContract.objects.all()
    except ExchangeContract.DoesNotExist:
        contracts = None
        return render_to_response('exchange.html', locals())
    
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

#def IOUs(request):

#def contracts(request):
