from django import forms
from .models import Village, IOU

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
