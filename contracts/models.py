from django.db import models

class Village(models.Model):
    name = models.CharField(max_length = 30)
    user = models.ForeignKey(models.User)

    def __unicode__(self):
        return self.name

class IOU(models.Model):
    issuer = models.ForeignKey(models.User)
    holder = models.ForeignKey(models.User)
    qty    = models.IntegerField()
    type   = models.CharField(max_length=10, choices=contracts.models.GOOD_TYPES)

    def __unicode__(self):
        return u'%s owes %s %s %s' % (self.issuer, self.holder, self.qty, self.type)

class RecallContract(models.Model):
    sender    = models.ForeignKey(models.User, null=True, blank=True)
    recipient = models.ForeignKey(Village, null=True, blank=True)
    qty       = models.IntegerField()
    type      = models.CharField(max_length=10, choices=contrats.models.GOOD_TYPES)
    timeout   = models.DateTimeField() 

    def __unicode__(self):
        return u'%s sending %s %s to %s for %s by %s' % (self.sender, self.qty,
                                                         self.type, self.recipient,
                                                         self.iou, self.timeout)

class ExchangeContract(models.Model):
    issuer = models.ForeignKey(models.User)

    def __unicode__(self):
        return u'exchange contract issued by %s' % (self.issuer,)

class Bundle(models.Model):
    send     = models.BooleanField()
    qty      = models.IntegerField()
    type     = models.CharField(max_length=10, choices=contracts.models.GOOD_TYPES)
    contract = models.ForeignKey(ExchangeContract)

    def __unicode__(self):
        if self.send:
            return u'send %s %s' % (self.qty, self.type)
        else:
            return u'receive %s %s' % (self.qty, self.type)

GOOD_TYPES (
    ('wood', 'Wood'),
    ('stone', 'Stone'),
    ('iron', 'Iron'),
    ('pitch', 'Pitch'),
    ('venison', 'Venison'),
    ('furniture', 'Furniture'),
    ('metalware', 'Metalware'),
    ('clothes', 'Clothes'),
    ('wine', 'Wine'),
    ('salt', 'Salt'),
    ('spices', 'Spices'),
    ('silk', 'Silk'),
    ('apples', 'Apples'),
    ('cheese', 'Cheese'),
    ('meat', 'Meat'),
    ('bread', 'Bread'),
    ('vegetables', 'Vegetables'),
    ('fish', 'Fish'),
    ('ale', 'Ale'),
    ('bows', 'Bows')
    ('pikes', 'Pikes')
    ('armour', 'Armour')
    ('swords', 'Swords')
    ('catapults', 'Catapults')
)
