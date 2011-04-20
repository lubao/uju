# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Daemons(models.Model):
    start = models.TextField(db_column='Start') 
    info = models.TextField(db_column='Info') 
    class Meta:
        db_table = u'daemons'

class Gammu(models.Model):
    version = models.IntegerField(db_column='Version') 
    class Meta:
        db_table = u'gammu'

class Inbox(models.Model):
    update_in_db = models.DateTimeField(db_column='UpdatedInDB') 
    receiving_datetime = models.DateTimeField(db_column='ReceivingDateTime') 
    text = models.TextField(db_column='Text') 
    sender_number = models.CharField(max_length=60, db_column='SenderNumber') 
    coding = models.CharField(max_length=66, db_column='Coding') 
    udh = models.TextField(db_column='UDH') 
    smsc_number = models.CharField(max_length=60, db_column='SMSCNumber') 
    #Field renamed because it was a Python reserved word.
    class_field = models.IntegerField(db_column='Class')  
    text_decoded = models.TextField(db_column='TextDecoded') 
    _id = models.IntegerField(primary_key=True, db_column='ID') 
    recipient_id = models.TextField(db_column='RecipientID') 
    processed = models.CharField(max_length=15, db_column='Processed') 
    class Meta:
        db_table = u'inbox'

class Outbox(models.Model):
    update_in_db = models.DateTimeField(db_column='UpdatedInDB') 
    insert_into_db = models.DateTimeField(db_column='InsertIntoDB') 
    sending_datetime = models.DateTimeField(db_column='SendingDateTime') 
    text = models.TextField(db_column='Text', blank=True) 
    destination_number = models.CharField(max_length=60, 
        db_column='DestinationNumber'
    ) 
    coding = models.CharField(max_length=66, db_column='Coding') 
    udh = models.TextField(db_column='UDH', blank=True) 
    #Field renamed because it was a Python reserved word.
    class_field = models.IntegerField(null=True, 
        db_column='Class', blank=True
    )
    text_decoded = models.TextField(db_column='TextDecoded') 
    _id = models.IntegerField(primary_key=True, db_column='ID') 
    multipart = models.CharField(max_length=15, 
        db_column='MultiPart', blank=True
    ) 
    relative_validity = models.IntegerField(null=True, 
        db_column='RelativeValidity', blank=True
    ) 
    sender_id = models.CharField(max_length=765, 
        db_column='SenderID', blank=True
    ) 
    sending_timeout = models.DateTimeField(null=True, 
        db_column='SendingTimeOut', blank=True
    ) 
    delivery_report = models.CharField(max_length=21, 
        db_column='DeliveryReport', blank=True
    ) 
    creator_id = models.TextField(db_column='CreatorID') 
    class Meta:
        db_table = u'outbox'

class OutboxMultipart(models.Model):
    text = models.TextField(db_column='Text', blank=True) 
    coding = models.CharField(max_length=66, db_column='Coding') 
    udh = models.TextField(db_column='UDH', blank=True) 
    #Field renamed because it was a Python reserved word.
    class_field = models.IntegerField(null=True, 
        db_column='Class', blank=True
    ) 
    text_decoded = models.TextField(db_column='TextDecoded', blank=True) 
    _id = models.IntegerField(primary_key=True, db_column='ID') 
    sequence_position = models.IntegerField(primary_key=True, 
        db_column='SequencePosition') 
    class Meta:
        db_table = u'outbox_multipart'

class Pbk(models.Model):
    _id = models.IntegerField(primary_key=True, db_column='ID') 
    group_id = models.IntegerField(db_column='GroupID') 
    name = models.TextField(db_column='Name') 
    _number = models.TextField(db_column='Number') 
    class Meta:
        db_table = u'pbk'

class PbkGroups(models.Model):
    name = models.TextField(db_column='Name') 
    _id = models.IntegerField(primary_key=True, db_column='ID') 
    class Meta:
        db_table = u'pbk_groups'

class Phones(models.Model):
    _id = models.TextField(db_column='ID') 
    update_in_db = models.DateTimeField(db_column='UpdatedInDB') 
    insert_into_db = models.DateTimeField(db_column='InsertIntoDB') 
    timeout = models.DateTimeField(db_column='TimeOut') 
    send = models.CharField(max_length=9, db_column='Send') 
    receive = models.CharField(max_length=9, db_column='Receive') 
    imei = models.CharField(max_length=105, primary_key=True, db_column='IMEI') 
    client = models.TextField(db_column='Client') 
    battery = models.IntegerField(db_column='Battery') 
    signal = models.IntegerField(db_column='Signal') 
    sent = models.IntegerField(db_column='Sent') 
    received = models.IntegerField(db_column='Received') 
    class Meta:
        db_table = u'phones'

class SentItems(models.Model):
    update_in_db = models.DateTimeField(db_column='UpdatedInDB') 
    insert_into_db = models.DateTimeField(db_column='InsertIntoDB') 
    sending_datetime = models.DateTimeField(db_column='SendingDateTime') 
    delivery_datetime = models.DateTimeField(null=True, 
        db_column='DeliveryDateTime', blank=True
    ) 
    text = models.TextField(db_column='Text') 
    destination_number = models.CharField(
        max_length=60, db_column='DestinationNumber'
    ) 
    coding = models.CharField(max_length=66, db_column='Coding') 
    udh = models.TextField(db_column='UDH') 
    smsc_number = models.CharField(max_length=60, db_column='SMSCNumber') 
    #Field renamed because it was a Python reserved word.
    class_field = models.IntegerField(db_column='Class')  
    text_decoded = models.TextField(db_column='TextDecoded') 
    _id = models.IntegerField(primary_key=True, db_column='ID') 
    sender_id = models.CharField(max_length=765, db_column='SenderID') 
    sequence_position = models.IntegerField(primary_key=True, 
        db_column='SequencePosition') 
    status = models.CharField(max_length=51, db_column='Status') 
    status_error = models.IntegerField(db_column='StatusError') 
    tpmr = models.IntegerField(db_column='TPMR') 
    relative_validity = models.IntegerField(db_column='RelativeValidity') 
    creator_id = models.TextField(db_column='CreatorID') 
    class Meta:
        db_table = u'sentitems'

