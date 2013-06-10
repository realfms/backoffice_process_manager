'''
Created on 31/05/2013

@author: mac@tid.es
'''

ACTIVATION_STATUS = (
    ('PENDING',   'PENDING'),
    ('VALIDATED', 'VALIDATED'),
    ('ERROR',     'ERROR'),
    ('CANCELED',  'CANCELED'),
)

SUBSCRIPTION_STATUS = (
    ('ACTIVE',   'ACTIVE'),
    ('CANCELED', 'CANCELED'),
)


BILLING_TYPE = (
    ('ONE SHOT',   'ONE SHOT'),
    ('RECURRENT',  'RECURRENT'),
)

COMPLETION_STATUS = (
    ('PENDING',   'PENDING'),
    ('COMPLETED', 'COMPLETED'),
    ('ERROR',     'ERROR'),
    ('CANCELED',  'CANCELED'),
)

CHANNEL = (
    ('ONLINE',       'ONLINE'),
    ('DIRECT_SALES', 'DIRECT_SALES'),
)

DATE_FORMAT = '%d/%m/%Y'

