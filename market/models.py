from django.db import models
from django.contrib.auth.models import User
from .data import GOOD_TYPES

class Village(models.Model):
    name = models.CharField(max_length = 30)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

class IOU(models.Model):
    issuer = models.ForeignKey(User, related_name='issuer')
    holder = models.ForeignKey(User, related_name='holder')
    qty    = models.PositiveIntegerField()
    type   = models.CharField(max_length=10, choices=GOOD_TYPES)

    def __unicode__(self):
        return u'%s owes %s %s %s' % (self.issuer, self.holder, self.qty, self.type)

class RecallContract(models.Model):
    sender    = models.ForeignKey(User)
    recipient = models.ForeignKey(Village)
    qty       = models.PositiveIntegerField()
    type      = models.CharField(max_length=10, choices=GOOD_TYPES)
    timeout   = models.DateTimeField()

    def __unicode__(self):
        return u'%s sending %s %s to %s by %s' % (self.sender, self.qty,
                                                  self.type, self.recipient,
                                                  self.timeout)

class ExchangeContract(models.Model):
    issuer = models.ForeignKey(User)

    def __unicode__(self):
        return u'exchange contract issued by %s' % (self.issuer,)

class Bundle(models.Model):
    send     = models.BooleanField()
    qty      = models.PositiveIntegerField()
    type     = models.CharField(max_length=10, choices=GOOD_TYPES)
    contract = models.ForeignKey(ExchangeContract)

    def __unicode__(self):
        if self.send:
            return u'send %s %s' % (self.qty, self.type)
        else:
            return u'receive %s %s' % (self.qty, self.type)
