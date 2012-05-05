from django import forms
from .models import Village
from .data import GOOD_TYPES

class VillageForm(forms.Form):
    name = forms.CharField(max_length=30)

class RecallForm(forms.Form):
    qty       = forms.IntegerField()
    recipient = forms.ModelChoiceField(queryset=Village.objects.none())
    timeout   = forms.DateTimeField()

    # form needs to know this, will be set in constructor
    max_qty = 0
    
    def __init__(self, *args, **kwargs):
        # this kwarg is required
        # the iou you are making the contract from
        iou = kwargs.pop('iou')

        # call to super
        super(RecallForm, self).__init__(*args, **kwargs)

        # set the max_qty for validation
        self.max_qty = iou.qty

        # set the choices for the recipient
        self.fields['recipient'].queryset = Village.objects.filter(user=iou.holder)

    # custom validation code to make sure that qty is legal
    def clean_qty(self):
        qty = self.cleaned_data['qty']
        if qty > self.max_qty:
            raise forms.ValidationError('The maximum quantity is %s' % (self.max_qty,))
        return qty

class PrecreateForm(forms.Form):
    send    = forms.IntegerField()
    receive = forms.IntegerField()

class CreateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        send = kwargs.pop('send')
        receive = kwargs.pop('receive')
        super(CreateForm, self).__init__(*args, **kwargs)
        for i in xrange(int(send)):
            self.fields['send_qty_%i' % i] = forms.IntegerField()
            self.fields['send_type_%i' % i] = forms.ChoiceField(choices=GOOD_TYPES)
        for i in xrange(int(receive)):
            self.fields['receive_qty_%i' % i] = forms.IntegerField()
            self.fields['receive_type_%i' % i] = forms.ChoiceField(choices=GOOD_TYPES)
