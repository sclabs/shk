from .models import ExchangeContract, Bundle, IOU, RecallContract, Village
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.utils import timezone
from .forms import *

@login_required
def exchange(request):
    # get all the contracts not issued by the user
    contracts = ExchangeContract.objects.all().exclude(issuer=request.user)

    # get all the contracts issued by the user
    myContracts = ExchangeContract.objects.filter(issuer=request.user)
    
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
                
    # dictionaries that map myContracts to lists of bundles
    mySendBundles = {}
    myReceiveBundles = {}

    # fill in the dictionaries
    for contract in myContracts:
        bundles = Bundle.objects.filter(contract=contract)
        mySendBundles[contract.id] = []
        myReceiveBundles[contract.id] = []
        for bundle in bundles:
            if bundle.send:
                mySendBundles[contract.id].append(bundle)
            else:
                myReceiveBundles[contract.id].append(bundle)
                
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

'''@login_required
def fail(request, id):
    # get the contract
    try:
        contract = RecallContract.objects.get(id=id)
        # check to see if it was issued by the user
        if contract.recipient.user == request.user:
            # check to see that the timeout has passed
            if contract.timeout < timezone.now():
                addOrCreate(contract.sender,
                            request.user,
                            contract.qty,
                            contract.type)
                # delete the contract
                contract.delete()
    except RecallContract.DoesNotExist:
        pass
    return redirect('contracts')'''

@login_required
def precreate(request):
    if request.method == 'POST':
        form = PrecreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return redirect('create', cd['send'], cd['receive'])
    else:
        form = PrecreateForm()
    return render_to_response('precreate.html', {'form': form}, RequestContext(request))

@login_required
def create(request, send, receive):
    if request.method == 'POST':
        form = CreateForm(request.POST, send=send, receive=receive)
        if form.is_valid():
            cd = form.cleaned_data
            # create an ExchangeContract
            contract = ExchangeContract(issuer=request.user)
            contract.save()
            # create the sendBundles
            for i in xrange(int(send)):
                sendBundle = Bundle(send=True,
                                    qty=cd['send_qty_%i' % i],
                                    type=cd['send_type_%i' % i],
                                    contract=contract)
                sendBundle.save()
            # create the receiveBundles
            for i in xrange(int(receive)):
                receiveBundle = Bundle(send=False,
                                       qty=cd['receive_qty_%i' % i],
                                       type=cd['receive_type_%i' % i],
                                       contract=contract)
                receiveBundle.save()
            return redirect('exchange')
    else:
        form = CreateForm(send=send, receive=receive)
    return render_to_response('create.html', {'form': form}, RequestContext(request))

@login_required
def cancel(request, id):
    # get the contract
    try:
        contract = ExchangeContract.objects.get(id=id)
        # check to see if it was issued by the user
        if contract.issuer == request.user:
            # delete the contract
            contract.delete()
    except ExchangeContract.DoesNotExist:
        pass
    return redirect('exchange')

'''@login_required
def accept(request, id):
    # get the contract
    try:
        contract = ExchangeContract.objects.get(id=id)
        # get the bundles
        bundles = Bundle.objects.filter(contract=contract)
        for bundle in bundles:
            if bundle.send:
                # how many IOUs short are we?
                held = countIOUs(contract.issuer, bundle.type)
                shortage = bundle.qty - held
                if shortage > 0:
                    addOrCreate(contract.issuer,
                                request.user,
                                shortage,
                                bundle.type)
                    transferIOUs(contract.issuer,
                                 request.user,
                                 held,
                                 bundle.type)
                else:
                    transferIOUs(contract.issuer,
                                 request.user,
                                 bundle.qty,
                                 bundle.type)
            else:
                # how many IOUs short are we?
                held = countIOUs(request.user, bundle.type)
                shortage = bundle.qty - held
                if shortage > 0:
                    addOrCreate(request.user,
                                contract.issuer,
                                shortage,
                                bundle.type)
                    transferIOUs(request.user,
                                 contract.issuer,
                                 held,
                                 bundle.type)
                else:
                    transferIOUs(request.user,
                                 contract.issuer,
                                 bundle.qty,
                                 bundle.type)
        contract.delete()
    except ExchangeContract.DoesNotExist:
        pass
    return redirect('exchange')

# helper methods
def countIOUs(user, type):
    # keep track of the quantity
    count = 0
    # get all the IOUs
    ious = IOU.objects.filter(holder=user, type=type)
    # count all the things
    for iou in ious:
        count += iou.qty
    return count
    
def transferIOUs(oldHolder, newHolder, qty, type):
    # keep track of this
    transferred = 0
    while transferred != qty:
        # first, see if we're already owed this
        try:
            iou = IOU.objects.get(issuer=newHolder,
                                  holder=oldHolder,
                                  type=type)
            excess = transferred + iou.qty - qty
            if excess <= 0:
                # go ahead with the transfer
                transferred += iou.qty
                iou.delete()
            else:
                # how much of this one we need to transfer?
                transfer = iou.qty - excess
                transferred += transfer
                iou.qty -= transfer
                iou.save()
        except IOU.DoesNotExist:
            # grab a random IOU of this type
            # make sure this exists!
            iou = IOU.objects.filter(holder=oldHolder, type=type)[0]
            excess = transferred + iou.qty - qty
            if excess <= 0:
                # go ahead with the transfer
                addOrCreate(iou.issuer, newHolder, iou.qty, type)
                transferred += iou.qty
                iou.delete()
            else:
                # how much of this one we need to transfer?
                transfer = iou.qty - excess
                addOrCreate(iou.issuer, newHolder, transfer, type)
                transferred += transfer
                iou.qty -= transfer
                iou.save()
    
def addOrCreate(issuer, holder, qty, type):
    # if an IOU like this already exists, add to it
    try:
        iou = IOU.objects.get(issuer=issuer,
                              holder=holder,
                              type=type)
        iou.qty += qty
        iou.save()
    # otherwise, create a new one
    except IOU.DoesNotExist:
        iou = IOU(issuer=issuer,
                  holder=holder,
                  qty=qty,
                  type=type)
        iou.save()'''
