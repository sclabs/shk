from .models import ExchangeContract, Bundle, IOU, RecallContract, Village
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.utils import timezone
from .forms import VillageForm, RecallForm

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
def ious(request):
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
        contractsByMe.extend(RecallContract.objects.filter(recipient=village))

    # use this dict to keep track of which contracts are failable
    failable = {}

    # fill in the dict
    for contract in contractsByMe:
        if contract.timeout < timezone.now():
            failable[contract.id] = True
        else:
            failable[contract.id] = False

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
    return render_to_response('addVillage.html', {'form': form}, RequestContext(request))

@login_required
def removeVillage(request, id):
    # get the village
    try:
        village = Village.objects.get(id=id)
        # make sure this is the user's village
        if village.user == request.user:
            # make sure this village is not involved in contracts
            if RecallContract.objects.filter(recipient=village):
                pass
            else:
                village.delete()
    except Village.DoesNotExist:
        pass
    return redirect('villages')

@login_required
def recall(request, id):
    # get the iou to be recalled or redirect to ious
    try:
        iou = IOU.objects.get(id=id)
    except IOU.DoesNotExist:
        return redirect('ious')
        
    if request.method == 'POST':
        # redirect to ious if you don't hold this iou
        if iou.holder != request.user:
            return redirect('ious')

        # make the bound form
        form = RecallForm(request.POST, iou=iou)

        # validate
        if form.is_valid():
            # clean
            cd = form.cleaned_data
            
            # if you recalled everything, the iou is gone 
            if cd['qty'] == iou.qty:
                iou.delete()

            # otherwise, decrement the quantity owed by the quantity contracted
            else:
                iou.qty -= cd['qty']
                iou.save()

            # create the contract
            contract = RecallContract(sender=iou.issuer,
                                      recipient=cd['recipient'],
                                      qty=cd['qty'],
                                      type=iou.type,
                                      timeout=cd['timeout'])
            contract.save()
            return redirect('ious')
    else:
        form = RecallForm(iou=iou)
    return render_to_response('recall.html', {'form': form}, RequestContext(request))

@login_required
def complete(request, id):
    # get the contract
    try:
        contract = RecallContract.objects.get(id=id)
        # check to see if it was issued by the user
        if contract.recipient.user == request.user:
            # delete the contract
            contract.delete()
    except RecallContract.DoesNotExist:
        pass
    return redirect('contracts')
    
