import pytest
from discoResponses.discoResponses import *
delimiter = FlatDict.DELIMITER
# delimiter = '\0'
# delimiter = '/'
# FlatDict.DELIMITER = delimiter

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)

# \n\s+([vNt])
successApplication = {
  "referenceNumber": "220659464291945925",
  "status": "SUCCESS",
  "creditOffer": {
    "uniqueId": "001358438581231020180619095922286",
    "uniqueIdSeq": 1,
    "existingCustomerType": "NEW",
    "decision": "DECLINED",
    "springleafReferenceNumber": "52302461",
    "appReferenceNumber":"153510843",
    "centralizedPhoneNumber": "8007411043",
    "cig": "YES"
  },
  "users": [
    {
      "customerId": "164749289"
    }
  ],
  "contactApplcntAllwd": True,
  "enhancedAppEligible": False,
  "emailAddressPresent": True,
  "custIdPresent": True,
  "activeOrPendAcct": "Unknown"
}
successBranch = {
  "referenceNumber": "454036239149082349",
  "status": "SUCCESS",
  "creditOffer": {
    "uniqueId": "000837544805953220161028105854798",
    "uniqueIdSeq": 1,
    "existingCustomerType": "NEW",
    "decision": "AUTO_APPROVED_COUNTER",
    "springleafReferenceNumber": "52302638",
    "appReferenceNumber":"153510843",
    "approvedSecuredAmount": 7000,
    "approvedUnsecuredAmount": 2000,
    "branchNumber": "35"
  },
  "branch": {
    "branchNumber": "35",
    "location": "SANTA ROSA, CA",
    "branchManager": "AutoAppCounter Manager",
    "branchEmailAddress": "br0035@onemainfinancial.com",
    "addressLine1": "1175 W STEELE LN",
    "city": "SANTA ROSA",
    "state": "CA",
    "zip": "95403",
    "phoneNumber": "7075428775",
    "longitude": -122.730141,
    "latitude": 38.460464,
    "speaksSpanish": True
  }
}
successApplicationTree = {'activeOrPendAcct': TABLE_ENTRY(parent='', text='activeOrPendAcct', values=['Unknown', None], tags=[None, 'missing']), 'branch': TABLE_ENTRY(parent='', text='branch', values=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], tags=['missing', None]), 'branch:addressLine1': TABLE_ENTRY(parent='branch', text='addressLine1', values=[None, '1175 W STEELE LN'], tags=['missing', None]), 'branch:branchEmailAddress': TABLE_ENTRY(parent='branch', text='branchEmailAddress', values=[None, 'br0035@onemainfinancial.com'], tags=['missing', None]), 'branch:branchManager': TABLE_ENTRY(parent='branch', text='branchManager', values=[None, 'AutoAppCounter Manager'], tags=['missing', None]), 'branch:branchNumber': TABLE_ENTRY(parent='branch', text='branchNumber', values=[None, '35'], tags=['missing', None]), 'branch:city': TABLE_ENTRY(parent='branch', text='city', values=[None, 'SANTA ROSA'], tags=['missing', None]), 'branch:latitude': TABLE_ENTRY(parent='branch', text='latitude', values=[None, 38.460464], tags=['missing', None]), 'branch:location': TABLE_ENTRY(parent='branch', text='location', values=[None, 'SANTA ROSA, CA'], tags=['missing', None]), 'branch:longitude': TABLE_ENTRY(parent='branch', text='longitude', values=[None, -122.730141], tags=['missing', None]), 'branch:phoneNumber': TABLE_ENTRY(parent='branch', text='phoneNumber', values=[None, '7075428775'], tags=['missing', None]), 'branch:speaksSpanish': TABLE_ENTRY(parent='branch', text='speaksSpanish', values=[None, True], tags=['missing', None]), 'branch:state': TABLE_ENTRY(parent='branch', text='state', values=[None, 'CA'], tags=['missing', None]), 'branch:zip': TABLE_ENTRY(parent='branch', text='zip', values=[None, '95403'], tags=['missing', None]), 'contactApplcntAllwd': TABLE_ENTRY(parent='', text='contactApplcntAllwd', values=[True, None], tags=[None, 'missing']), 'creditOffer': TABLE_ENTRY(parent='', text='creditOffer', values=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], tags=[None, None]), 'creditOffer:appReferenceNumber': TABLE_ENTRY(parent='creditOffer', text='appReferenceNumber', values=['153510843', '153510843'], tags=[None, None]), 'creditOffer:approvedSecuredAmount': TABLE_ENTRY(parent='creditOffer', text='approvedSecuredAmount', values=[None, 7000], tags=['missing', None]), 'creditOffer:approvedUnsecuredAmount': TABLE_ENTRY(parent='creditOffer', text='approvedUnsecuredAmount', values=[None, 2000], tags=['missing', None]), 'creditOffer:branchNumber': TABLE_ENTRY(parent='creditOffer', text='branchNumber', values=[None, '35'], tags=['missing', None]), 'creditOffer:centralizedPhoneNumber': TABLE_ENTRY(parent='creditOffer', text='centralizedPhoneNumber', values=['8007411043', None], tags=[None, 'missing']), 'creditOffer:cig': TABLE_ENTRY(parent='creditOffer', text='cig', values=['YES', None], tags=[None, 'missing']), 'creditOffer:decision': TABLE_ENTRY(parent='creditOffer', text='decision', values=['DECLINED', 'AUTO_APPROVED_COUNTER'], tags=[None, None]), 'creditOffer:existingCustomerType': TABLE_ENTRY(parent='creditOffer', text='existingCustomerType', values=['NEW', 'NEW'], tags=[None, None]), 'creditOffer:springleafReferenceNumber': TABLE_ENTRY(parent='creditOffer', text='springleafReferenceNumber', values=['52302461', '52302638'], tags=[None, None]), 'creditOffer:uniqueId': TABLE_ENTRY(parent='creditOffer', text='uniqueId', values=['001358438581231020180619095922286', '000837544805953220161028105854798'], tags=[None, None]), 'creditOffer:uniqueIdSeq': TABLE_ENTRY(parent='creditOffer', text='uniqueIdSeq', values=[1, 1], tags=[None, None]), 'custIdPresent': TABLE_ENTRY(parent='', text='custIdPresent', values=[True, None], tags=[None, 'missing']), 'emailAddressPresent': TABLE_ENTRY(parent='', text='emailAddressPresent', values=[True, None], tags=[None, 'missing']), 'enhancedAppEligible': TABLE_ENTRY(parent='', text='enhancedAppEligible', values=[False, None], tags=[None, 'missing']), 'referenceNumber': TABLE_ENTRY(parent='', text='referenceNumber', values=['220659464291945925', '454036239149082349'], tags=[None, None]), 'status': TABLE_ENTRY(parent='', text='status', values=['SUCCESS', 'SUCCESS'], tags=[None, None]), 'users': TABLE_ENTRY(parent='', text='users', values=[None, None], tags=[None, 'missing']), 'users:0': TABLE_ENTRY(parent='users', text=0, values=[None, None], tags=[None, 'missing']), 'users:0:customerId': TABLE_ENTRY(parent='users:0', text='customerId', values=['164749289', None], tags=[None, 'missing'])}


successGroup0Array = {
    "referenceNumber": "000 demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": {
        'transactionCountD': 0,
        "branchNumber": "5678",
        'group0': [11, 22, 33, 4],
        "after": "group"
    }
}
successGroup02Array = {
    "referenceNumber": "demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": {
        'transactionCount': 0,
        "branchNumber": "1234",
        'group0': [1, 2, 34],
        "after": "group"
    }
}
successGroup0ArrayTree = {'accountDetail': TABLE_ENTRY(parent='', text='accountDetail',values=[None, None, None, None, None, None, None, None, None, None], tags=[None, None]),
                          'accountDetail:after': TABLE_ENTRY(parent='accountDetail', text='after',values=['group', 'group'], tags=[None, None]),
                          'accountDetail:branchNumber': TABLE_ENTRY(parent='accountDetail', text='branchNumber',values=['5678', '1234'], tags=[None, None]),
                          'accountDetail:group0': TABLE_ENTRY(parent='accountDetail', text='group0',values=[None, None], tags=[None, None]),
                          'accountDetail:group0:0': TABLE_ENTRY(parent='accountDetail:group0', text=0, values=[11, 1],tags=[None, None]),
                          'accountDetail:group0:1': TABLE_ENTRY(parent='accountDetail:group0', text=1, values=[22, 2],tags=[None, None]),
                          'accountDetail:group0:2': TABLE_ENTRY(parent='accountDetail:group0', text=2, values=[33, 34],tags=[None, None]),
                          'accountDetail:group0:3': TABLE_ENTRY(parent='accountDetail:group0', text=3, values=[4, None],tags=[None, 'missing']),
                          'accountDetail:transactionCount': TABLE_ENTRY(parent='accountDetail', text='transactionCount',values=[None, 0], tags=['missing', None]),
                          'accountDetail:transactionCountD': TABLE_ENTRY(parent='accountDetail',text='transactionCountD', values=[0, None],tags=[None, 'missing']),
                          'referenceNumber': TABLE_ENTRY(parent='', text='referenceNumber',values=['000 demo: :AccountDetailsResponse', 'demo: :AccountDetailsResponse'], tags=[None, None]),
                          'status': TABLE_ENTRY(parent='', text='status', values=['SUCCESS', 'SUCCESS'],tags=[None, None])}


successGroup0ArrayNest = {
    "referenceNumber": "demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": [
        {
            'transactionCountD': 0,
            "branchNumber": "1234",
            'agroup0': [1, 2, 3, 4],
            "after": "group"
        },
        {
            'transactionCountD': 0,
            "branchNumber": "1234",
            'agroup0': [1, 2, 3, 4],
            "after": "group"
        }
    ]
}
successGroup02ArrayNest = {
    "referenceNumber": "demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": [
        {
            'transactionCountD': 0,
            "branchNumber": "1234",
            'agroup0': [1, 2, 3, 4],
            "after": "group"
        },
        {
            'transactionCountD': 0,
            "branchNumber": "1234",
            # 'agroup0': [1, 2, 3, 4],
            "after": "group"
        }
    ]
}
successGroup0ArrayTreeNest = {'accountDetail': TABLE_ENTRY(parent='', text='accountDetail', values=[None, None, None, None, None, None, None, None], tags=[None, None]),
                              'accountDetail:0': TABLE_ENTRY(parent='accountDetail', text=0, values=[None, None, None, None, None, None, None, None], tags=[None, None]),
                              'accountDetail:0:after': TABLE_ENTRY(parent='accountDetail:0', text='after', values=['group', 'group'], tags=[None, None]),
                              'accountDetail:1': TABLE_ENTRY(parent='accountDetail', text=1, values=[None, None, None, None, None, None, None, None], tags=[None, None]),
                              'accountDetail:1:after': TABLE_ENTRY(parent='accountDetail:1', text='after', values=['group', 'group'], tags=[None, None]),
                              'accountDetail:0:agroup0': TABLE_ENTRY(parent='accountDetail:0', text='agroup0', values=[None, None], tags=[None, None]),
                              'accountDetail:0:agroup0:0': TABLE_ENTRY(parent='accountDetail:0:agroup0', text=0, values=[1, 1], tags=[None, None]),
                              'accountDetail:0:agroup0:1': TABLE_ENTRY(parent='accountDetail:0:agroup0', text=1, values=[2, 2], tags=[None, None]),
                              'accountDetail:0:agroup0:2': TABLE_ENTRY(parent='accountDetail:0:agroup0', text=2, values=[3, 3], tags=[None, None]),
                              'accountDetail:0:agroup0:3': TABLE_ENTRY(parent='accountDetail:0:agroup0', text=3, values=[4, 4], tags=[None, None]),
                              'accountDetail:1:agroup0': TABLE_ENTRY(parent='accountDetail:1', text='agroup0', values=[None, None], tags=[None, 'missing']),
                              'accountDetail:1:agroup0:0': TABLE_ENTRY(parent='accountDetail:1:agroup0', text=0, values=[1, None], tags=[None, 'missing']),
                              'accountDetail:1:agroup0:1': TABLE_ENTRY(parent='accountDetail:1:agroup0', text=1, values=[2, None], tags=[None, 'missing']),
                              'accountDetail:1:agroup0:2': TABLE_ENTRY(parent='accountDetail:1:agroup0', text=2, values=[3, None], tags=[None, 'missing']),
                              'accountDetail:1:agroup0:3': TABLE_ENTRY(parent='accountDetail:1:agroup0', text=3, values=[4, None], tags=[None, 'missing']),
                              'accountDetail:0:branchNumber': TABLE_ENTRY(parent='accountDetail:0', text='branchNumber', values=['1234', '1234'], tags=[None, None]),
                              'accountDetail:1:branchNumber': TABLE_ENTRY(parent='accountDetail:1', text='branchNumber', values=['1234', '1234'], tags=[None, None]),
                              'accountDetail:0:transactionCountD': TABLE_ENTRY(parent='accountDetail:0', text='transactionCountD', values=[0, 0], tags=[None, None]),
                              'accountDetail:1:transactionCountD': TABLE_ENTRY(parent='accountDetail:1', text='transactionCountD', values=[0, 0], tags=[None, None]),
                              'referenceNumber': TABLE_ENTRY(parent='', text='referenceNumber', values=['demo: :AccountDetailsResponse',
                                                                     'demo: :AccountDetailsResponse'], tags=[None, None]),
                              'status': TABLE_ENTRY(parent='', text='status', values=['SUCCESS', 'SUCCESS'], tags=[None, None])}


successGroup41ArrayNest = {
    "referenceNumber": "1demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": [
        {
            'transactionCountD': 0,
            "branchNumber": "1234",
            'agroup0': [1, 2, 3, 4, 5],
            "after": "group"
        }
    ]
}
successGroup40ArrayNest = {
    "referenceNumber": "1demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": [
        {
            'transactionCountD': 0,
            "branchNumber": "1234",
            'agroup0': [1, 2, 3, 4],
            "after": "group"
        },
        {
            'transactionCountD': 1,
            "branchNumber": "1234",
            'agroup0': [1, 2, 3, 4],
            "after": "group"
        },
        {
            'transactionCountD': 2,
            "branchNumber": "1234",
            'agroup0': [1, 2, 3, 4],
            "after": "group"
        },
        {
            'transactionCountD': 3,
            "branchNumber": "1234",
            'agroup0': [1, 2, 3, 4],
            "after": "group"
        }
    ]
}
successGroup42ArrayNest = {
    "referenceNumber": "3demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": [
        {
            'transactionCountD': 0,
            "branchNumber": "1234",
            'agroup0': [1, 2, 3, 4],
            "after": "group"
        },
        {
            'transactionCountD': 1,
            "branchNumber": "1234",
            'agroup0': [1, 2, 3, 4],
            "after": "group"
        },
        {
            'transactionCountD': 2,
            "branchNumber": "1234",
            'agroup0': [1, 2, 3, 4],
            "after": "group"
        },
        {
            'transactionCountD': 3,
            "branchNumber": "1234",
            'agroup0': [1, 2, 3, 4],
            "after": "group"
        }
    ]
}
successGroup43ArrayNest = {
    "referenceNumber": "2demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": [
        {
            'transactionCountD': 0,
            "branchNumber": "1234",
            # 'agroup0': [1, 2, 3, 4],
            "after": "group"
        },
        {
            'transactionCountD': 0,
            "branchNumber": "1234",
            'agroup0': [1, 2, 3, 4],
            "after": "group"
        }
    ]
}
successGroup4ArrayTreeNest = {'accountDetail': TABLE_ENTRY(parent='', text='accountDetail', values=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], tags=[None, None, None, None]),
                              'accountDetail:0': TABLE_ENTRY(parent='accountDetail', text=0, values=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], tags=[None, None, None, None]),
                              'accountDetail:0:after': TABLE_ENTRY(parent='accountDetail:0', text='after', values=['group', 'group', 'group', 'group'], tags=[None, None, None, None]),
                              'accountDetail:1': TABLE_ENTRY(parent='accountDetail', text=1, values=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], tags=[None, 'missing', None, None]),
                              'accountDetail:1:after': TABLE_ENTRY(parent='accountDetail:1', text='after', values=['group', None, 'group', 'group'], tags=[None, 'missing', None, None]),
                              'accountDetail:2': TABLE_ENTRY(parent='accountDetail', text=2, values=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], tags=[None, 'missing', None, 'missing']),
                              'accountDetail:2:after': TABLE_ENTRY(parent='accountDetail:2', text='after', values=['group', None, 'group', None], tags=[None, 'missing', None, 'missing']),
                              'accountDetail:3': TABLE_ENTRY(parent='accountDetail', text=3, values=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], tags=[None, 'missing', None, 'missing']),
                              'accountDetail:3:after': TABLE_ENTRY(parent='accountDetail:3', text='after', values=['group', None, 'group', None], tags=[None, 'missing', None, 'missing']),
                              'accountDetail:0:agroup0': TABLE_ENTRY(parent='accountDetail:0', text='agroup0', values=[None, None, None, None], tags=[None, None, None, 'missing']),
                              'accountDetail:0:agroup0:0': TABLE_ENTRY(parent='accountDetail:0:agroup0', text=0, values=[1, 1, 1, None], tags=[None, None, None, 'missing']),
                              'accountDetail:0:agroup0:1': TABLE_ENTRY(parent='accountDetail:0:agroup0', text=1, values=[2, 2, 2, None], tags=[None, None, None, 'missing']),
                              'accountDetail:0:agroup0:2': TABLE_ENTRY(parent='accountDetail:0:agroup0', text=2, values=[3, 3, 3, None], tags=[None, None, None, 'missing']),
                              'accountDetail:0:agroup0:3': TABLE_ENTRY(parent='accountDetail:0:agroup0', text=3, values=[4, 4, 4, None], tags=[None, None, None, 'missing']),
                              'accountDetail:0:agroup0:4': TABLE_ENTRY(parent='accountDetail:0:agroup0', text=4, values=[None, 5, None, None], tags=['missing', None, 'missing', 'missing']),
                              'accountDetail:1:agroup0': TABLE_ENTRY(parent='accountDetail:1', text='agroup0', values=[None, None, None, None], tags=[None, 'missing', None, None]),
                              'accountDetail:1:agroup0:0': TABLE_ENTRY(parent='accountDetail:1:agroup0', text=0, values=[1, None, 1, 1], tags=[None, 'missing', None, None]),
                              'accountDetail:1:agroup0:1': TABLE_ENTRY(parent='accountDetail:1:agroup0', text=1, values=[2, None, 2, 2], tags=[None, 'missing', None, None]),
                              'accountDetail:1:agroup0:2': TABLE_ENTRY(parent='accountDetail:1:agroup0', text=2, values=[3, None, 3, 3], tags=[None, 'missing', None, None]),
                              'accountDetail:1:agroup0:3': TABLE_ENTRY(parent='accountDetail:1:agroup0', text=3, values=[4, None, 4, 4], tags=[None, 'missing', None, None]),
                              'accountDetail:2:agroup0': TABLE_ENTRY(parent='accountDetail:2', text='agroup0', values=[None, None, None, None], tags=[None, 'missing', None, 'missing']),
                              'accountDetail:2:agroup0:0': TABLE_ENTRY(parent='accountDetail:2:agroup0', text=0, values=[1, None, 1, None], tags=[None, 'missing', None, 'missing']),
                              'accountDetail:2:agroup0:1': TABLE_ENTRY(parent='accountDetail:2:agroup0', text=1, values=[2, None, 2, None], tags=[None, 'missing', None, 'missing']),
                              'accountDetail:2:agroup0:2': TABLE_ENTRY(parent='accountDetail:2:agroup0', text=2, values=[3, None, 3, None], tags=[None, 'missing', None, 'missing']),
                              'accountDetail:2:agroup0:3': TABLE_ENTRY(parent='accountDetail:2:agroup0', text=3, values=[4, None, 4, None], tags=[None, 'missing', None, 'missing']),
                              'accountDetail:3:agroup0': TABLE_ENTRY(parent='accountDetail:3', text='agroup0', values=[None, None, None, None], tags=[None, 'missing', None, 'missing']),
                              'accountDetail:3:agroup0:0': TABLE_ENTRY(parent='accountDetail:3:agroup0', text=0, values=[1, None, 1, None], tags=[None, 'missing', None, 'missing']),
                              'accountDetail:3:agroup0:1': TABLE_ENTRY(parent='accountDetail:3:agroup0', text=1, values=[2, None, 2, None], tags=[None, 'missing', None, 'missing']),
                              'accountDetail:3:agroup0:2': TABLE_ENTRY(parent='accountDetail:3:agroup0', text=2, values=[3, None, 3, None], tags=[None, 'missing', None, 'missing']),
                              'accountDetail:3:agroup0:3': TABLE_ENTRY(parent='accountDetail:3:agroup0', text=3, values=[4, None, 4, None], tags=[None, 'missing', None, 'missing']),
                              'accountDetail:0:branchNumber': TABLE_ENTRY(parent='accountDetail:0', text='branchNumber', values=['1234', '1234', '1234', '1234'], tags=[None, None, None, None]),
                              'accountDetail:1:branchNumber': TABLE_ENTRY(parent='accountDetail:1', text='branchNumber', values=['1234', None, '1234', '1234'], tags=[None, 'missing', None, None]),
                              'accountDetail:2:branchNumber': TABLE_ENTRY(parent='accountDetail:2', text='branchNumber', values=['1234', None, '1234', None], tags=[None, 'missing', None, 'missing']),
                              'accountDetail:3:branchNumber': TABLE_ENTRY(parent='accountDetail:3', text='branchNumber', values=['1234', None, '1234', None], tags=[None, 'missing', None, 'missing']),
                              'accountDetail:0:transactionCountD': TABLE_ENTRY(parent='accountDetail:0', text='transactionCountD', values=[0, 0, 0, 0], tags=[None, None, None, None]),
                              'accountDetail:1:transactionCountD': TABLE_ENTRY(parent='accountDetail:1', text='transactionCountD', values=[1, None, 1, 0], tags=[None, 'missing', None, None]),
                              'accountDetail:2:transactionCountD': TABLE_ENTRY(parent='accountDetail:2', text='transactionCountD', values=[2, None, 2, None], tags=[None, 'missing', None, 'missing']),
                              'accountDetail:3:transactionCountD': TABLE_ENTRY(parent='accountDetail:3', text='transactionCountD', values=[3, None, 3, None], tags=[None, 'missing', None, 'missing']),
                              'referenceNumber': TABLE_ENTRY(parent='', text='referenceNumber', values=['1demo: :AccountDetailsResponse',
                                                                     '1demo: :AccountDetailsResponse',
                                                                     '3demo: :AccountDetailsResponse',
                                                                     '2demo: :AccountDetailsResponse'], tags=[None, None, None, None]),
                              'status': TABLE_ENTRY(parent='', text='status', values=['SUCCESS', 'SUCCESS', 'SUCCESS', 'SUCCESS'], tags=[None, None, None, None])}


successGroupXArrayTreeNest = {'accountDetail': TABLE_ENTRY(parent='', text='accountDetail', values=[None, None, None, None, None, None, None, None, None, None, None, None], tags=[None, None, None]),
                              'accountDetail:0': TABLE_ENTRY(parent='accountDetail', text=0, values=[None, None, None, None, None, None, None, None, None, None, None, None], tags=[None, None, None]),
                              'accountDetail:0:after': TABLE_ENTRY(parent='accountDetail:0', text='after', values=['group', 'group', 'group'], tags=[None, None, None]),
                              'accountDetail:1': TABLE_ENTRY(parent='accountDetail', text=1, values=[None, None, None, None, None, None, None, None, None], tags=['missing', None, None]),
                              'accountDetail:1:after': TABLE_ENTRY(parent='accountDetail:1', text='after', values=[None, 'group', 'group'], tags=['missing', None, None]),
                              'accountDetail:2': TABLE_ENTRY(parent='accountDetail', text=2, values=[None, None, None, None, None, None, None, None, None], tags=['missing', None, 'missing']),
                              'accountDetail:0:agroup0': TABLE_ENTRY(parent='accountDetail:0', text='agroup0', values=[None, None, None], tags=[None, None, 'missing']),
                              'accountDetail:0:agroup0:0': TABLE_ENTRY(parent='accountDetail:0:agroup0', text=0, values=[1, 1, None], tags=[None, None, 'missing']),
                              'accountDetail:0:agroup0:1': TABLE_ENTRY(parent='accountDetail:0:agroup0', text=1, values=[2, 2, None], tags=[None, None, 'missing']),
                              'accountDetail:0:agroup0:2': TABLE_ENTRY(parent='accountDetail:0:agroup0', text=2, values=[3, 3, None], tags=[None, None, 'missing']),
                              'accountDetail:0:agroup0:3': TABLE_ENTRY(parent='accountDetail:0:agroup0', text=3, values=[4, 4, None], tags=[None, None, 'missing']),
                              'accountDetail:0:agroup0:4': TABLE_ENTRY(parent='accountDetail:0:agroup0', text=4, values=[5, None, None], tags=[None, 'missing', 'missing']),
                              'accountDetail:0:branchNumber': TABLE_ENTRY(parent='accountDetail:0', text='branchNumber', values=['1234', '1234', '1234'], tags=[None, None, None]),
                              'accountDetail:1:branchNumber': TABLE_ENTRY(parent='accountDetail:1', text='branchNumber', values=[None, '1234', '1234'], tags=['missing', None, None]),
                              'accountDetail:0:transactionCountD': TABLE_ENTRY(parent='accountDetail:0', text='transactionCountD', values=[0, 0, 0], tags=[None, None, None]),
                              'accountDetail:1:transactionCountD': TABLE_ENTRY(parent='accountDetail:1', text='transactionCountD', values=[None, 1, 0], tags=['missing', None, None]),
                              'referenceNumber': TABLE_ENTRY(parent='', text='referenceNumber', values=['1demo: :AccountDetailsResponse', '1demo: :AccountDetailsResponse', '2demo: :AccountDetailsResponse'], tags=[None, None, None]),
                              'status': TABLE_ENTRY(parent='', text='status', values=['SUCCESS', 'SUCCESS', 'SUCCESS'], tags=[None, None, None])}



successGroup0 = {
    "referenceNumber": "demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": {
        'transactionCount': 0,
        "branchNumber": "1234",
        "after": "group"
    }
}
successGroup02 = {
    "referenceNumber": "demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": {
        'transactionCount': 0,
        "branchNumber": "1234",
        "after": "group"
    }
}
successGroup0Tree = {'accountDetail': TABLE_ENTRY(parent='', text='accountDetail', values=[None, None, None, None, None, None], tags=[None, None]), 'accountDetail:after': TABLE_ENTRY(parent='accountDetail', text='after', values=['group', 'group'], tags=[None, None]), 'accountDetail:branchNumber': TABLE_ENTRY(parent='accountDetail', text='branchNumber', values=['1234', '1234'], tags=[None, None]), 'accountDetail:transactionCount': TABLE_ENTRY(parent='accountDetail', text='transactionCount', values=[0, 0], tags=[None, None]), 'referenceNumber': TABLE_ENTRY(parent='', text='referenceNumber', values=['demo: :AccountDetailsResponse', 'demo: :AccountDetailsResponse'], tags=[None, None]), 'status': TABLE_ENTRY(parent='', text='status', values=['SUCCESS', 'SUCCESS'], tags=[None, None])}


GetOfferSuccess = {
  "version":         "1.0",
  "status":          "success",
  "timeToExecute":   1920,
  "referenceNumber": None,
  "response": {
    "dupCounter":   "65",
    "customerFlag": "FC",
    "appStatus":    None,
    "name": {
      "last":   "JUNCOS",
      "suffix": None
    },
    "address": {
      "zipcode":      "46112",
      "zipcode4":     None,
      "countryCode":  "US"
    },
    "clientRequestId": "1478032435",
    "transactionId":   "17885329",
    "transactionStatus": {
      "status":   1000,
      "messages": None
    }
  }
}
GetOfferDirect = {
  "version":         "1.0",
  "status":          "success",
  "timeToExecute":   1920,
  "referenceNumber": None,
  "response": {
    "offer": [{
      "offerId":"99999999_1",
      "priority":"1",
      "expiration_date":"2016-02-11"
    }],
    "dupCounter":   "65",
    "customerFlag": "FC",
    "appStatus":    "B",
    "name": {
      "last":   "JUNCOS",
      "suffix": None
    },
    "address": {
      "zipcode":      "46112",
      "zipcode4":     None,
      "countryCode":  "US"
    },
    "clientRequestId": "1478032435",
    "transactionId":   "17885329",
    "transactionStatus": {
      "status":   1000,
      "messages": None
    }
  }
}
GetOfferSuccessTree = {'referenceNumber': TABLE_ENTRY(parent='', text='referenceNumber', values=[None, None], tags=[None, None]), 'response': TABLE_ENTRY(parent='', text='response', values=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], tags=[None, None]), 'response:address': TABLE_ENTRY(parent='response', text='address', values=[None, None, None, None, None, None], tags=[None, None]), 'response:address:countryCode': TABLE_ENTRY(parent='response:address', text='countryCode', values=['US', 'US'], tags=[None, None]), 'response:address:zipcode': TABLE_ENTRY(parent='response:address', text='zipcode', values=['46112', '46112'], tags=[None, None]), 'response:address:zipcode4': TABLE_ENTRY(parent='response:address', text='zipcode4', values=[None, None], tags=[None, None]), 'response:appStatus': TABLE_ENTRY(parent='response', text='appStatus', values=[None, 'B'], tags=[None, None]), 'response:clientRequestId': TABLE_ENTRY(parent='response', text='clientRequestId', values=['1478032435', '1478032435'], tags=[None, None]), 'response:customerFlag': TABLE_ENTRY(parent='response', text='customerFlag', values=['FC', 'FC'], tags=[None, None]), 'response:dupCounter': TABLE_ENTRY(parent='response', text='dupCounter', values=['65', '65'], tags=[None, None]), 'response:name': TABLE_ENTRY(parent='response', text='name', values=[None, None, None, None], tags=[None, None]), 'response:name:last': TABLE_ENTRY(parent='response:name', text='last', values=['JUNCOS', 'JUNCOS'], tags=[None, None]), 'response:name:suffix': TABLE_ENTRY(parent='response:name', text='suffix', values=[None, None], tags=[None, None]), 'response:offer': TABLE_ENTRY(parent='response', text='offer', values=[None, None, None, None, None, None], tags=['missing', None]), 'response:offer:0': TABLE_ENTRY(parent='response:offer', text=0, values=[None, None, None, None, None, None], tags=['missing', None]), 'response:offer:0:expiration_date': TABLE_ENTRY(parent='response:offer:0', text='expiration_date', values=[None, '2016-02-11'], tags=['missing', None]), 'response:offer:0:offerId': TABLE_ENTRY(parent='response:offer:0', text='offerId', values=[None, '99999999_1'], tags=['missing', None]), 'response:offer:0:priority': TABLE_ENTRY(parent='response:offer:0', text='priority', values=[None, '1'], tags=['missing', None]), 'response:transactionId': TABLE_ENTRY(parent='response', text='transactionId', values=['17885329', '17885329'], tags=[None, None]), 'response:transactionStatus': TABLE_ENTRY(parent='response', text='transactionStatus', values=[None, None, None, None], tags=[None, None]), 'response:transactionStatus:messages': TABLE_ENTRY(parent='response:transactionStatus', text='messages', values=[None, None], tags=[None, None]), 'response:transactionStatus:status': TABLE_ENTRY(parent='response:transactionStatus', text='status', values=[1000, 1000], tags=[None, None]), 'status': TABLE_ENTRY(parent='', text='status', values=['success', 'success'], tags=[None, None]), 'timeToExecute': TABLE_ENTRY(parent='', text='timeToExecute', values=[1920, 1920], tags=[None, None]), 'version': TABLE_ENTRY(parent='', text='version', values=['1.0', '1.0'], tags=[None, None])}


class TestInsertTree(object):
    class MockTree(object):
        def __init__(self, *args, **kwargs):
            self.tree = []

        def insert(self, *args, **kwargs):
            self.tree.append((args, kwargs))

    def testGetKeysGroup(self):
        frame = ttk.Frame()
        tree = DiscoTree(frame, '')
        responses = dict()
        sg0 = FlatDict(successGroup0)
        sg02 = FlatDict(successGroup02)
        response = sg0
        allKeys = sorted(list(set(sg0.getKeys() + sg02.getKeys())))
        responses['success.json.erb'] = RESPONSE_ENTRY(response['status']=='SUCCESS', True, response, response.getKeys(), 'json')
        responses['success2.json.erb'] = RESPONSE_ENTRY(response['status']=='SUCCESS', True, sg02, sg02.getKeys(), 'json')

        # newTree = insertTree(allKeys, responses)
        newTree = tree.insertTree(allKeys, responses)
        print(newTree)
        assert 6 == len(newTree)
        assert successGroup0Tree == newTree

    def testGetKeysGroupArray(self):
        frame = ttk.Frame()
        tree = DiscoTree(frame, '')
        responses = dict()
        sg0 = FlatDict(successGroup0Array)
        sg02 = FlatDict(successGroup02Array)
        response = sg0
        allKeys = sorted(list(set(sg0.getKeys() + sg02.getKeys())))
        responses['success.json.erb'] = RESPONSE_ENTRY(response['status']=='SUCCESS', True, response, response.getKeys(), 'json')
        responses['success2.json.erb'] = RESPONSE_ENTRY(response['status']=='SUCCESS', True, sg02, sg02.getKeys(), 'json')

        # newTree = insertTree(allKeys, responses)
        newTree = tree.insertTree(allKeys, responses)
        print(newTree)
        assert len(successGroup0ArrayTree) == len(newTree)
        assert successGroup0ArrayTree == newTree

    def testGetKeysGroupArrayNext(self):
        frame = ttk.Frame()
        tree = DiscoTree(frame, '')
        responses = dict()
        sg0 = FlatDict(successGroup0ArrayNest)
        sg02 = FlatDict(successGroup02ArrayNest)
        response = sg0
        allKeys = sorted(list(set(sg0.getKeys() + sg02.getKeys())))
        responses['success.json.erb'] = RESPONSE_ENTRY(response['status']=='SUCCESS', True, response, response.getKeys(), 'json')
        responses['success2.json.erb'] = RESPONSE_ENTRY(response['status']=='SUCCESS', True, sg02, sg02.getKeys(), 'json')

        # newTree = insertTree(allKeys, responses)
        newTree = tree.insertTree(allKeys, responses)
        print(newTree)
        assert len(successGroup0ArrayTreeNest) == len(newTree)
        assert successGroup0ArrayTreeNest == newTree

    def testGetKeys4GroupArrayNext(self):
        frame = ttk.Frame()
        tree = DiscoTree(frame, '')
        responses = dict()
        sg40 = FlatDict(successGroup40ArrayNest)
        sg41 = FlatDict(successGroup41ArrayNest)
        sg42 = FlatDict(successGroup42ArrayNest)
        sg43 = FlatDict(successGroup43ArrayNest)
        response = sg40
        allKeys = sorted(list(set(sg40.getKeys() + sg41.getKeys() + sg42.getKeys() + sg43.getKeys())))
        responses['success.json.erb'] = RESPONSE_ENTRY(response['status']=='SUCCESS', True, response, response.getKeys(), 'json')
        responses['success41.json.erb'] = RESPONSE_ENTRY(response['status']=='SUCCESS', True, sg41, sg41.getKeys(), 'json')
        responses['success42.json.erb'] = RESPONSE_ENTRY(response['status']=='SUCCESS', True, sg42, sg42.getKeys(), 'json')
        responses['success43.json.erb'] = RESPONSE_ENTRY(response['status']=='SUCCESS', True, sg43, sg43.getKeys(), 'json')

        # newTree = insertTree(allKeys, responses)
        newTree = tree.insertTree(allKeys, responses)
        print(newTree)
        assert len(successGroup4ArrayTreeNest) == len(newTree)
        assert successGroup4ArrayTreeNest == newTree

    def testGetKeysGroupApplication(self):
        frame = ttk.Frame()
        tree = DiscoTree(frame, '')
        responses = dict()
        sg0 = FlatDict(successApplication)
        sg02 = FlatDict(successBranch)
        responses = {}
        responses['success.json.erb'] = RESPONSE_ENTRY(sg0['status']=='SUCCESS', True, sg0, sg0.getKeys(), 'json')
        responses['success2.json.erb'] = RESPONSE_ENTRY(sg02['status']=='SUCCESS', True, sg02, sg02.getKeys(), 'json')
        all_keys = set()
        for response in responses:
            all_keys = all_keys.union(responses[response].allKeys)

        all_keys = sorted(all_keys)
        newTree = tree.insertTree(all_keys, responses)
        print(newTree)
        assert len(successApplicationTree) == len(newTree)
        assert successApplicationTree == newTree

    def testGetKeysGroupGetOffer(self):
        frame = ttk.Frame()
        tree = DiscoTree(frame, '')
        responses = dict()
        sg0 = FlatDict(GetOfferSuccess)
        sg02 = FlatDict(GetOfferDirect)
        responses = {}
        responses['success.json.erb'] = RESPONSE_ENTRY(sg0['status']=='SUCCESS', True, sg0, sg0.getKeys(), 'json')
        responses['success2.json.erb'] = RESPONSE_ENTRY(sg02['status']=='SUCCESS', True, sg02, sg02.getKeys(), 'json')
        all_keys = set()
        for response in responses:
            all_keys = all_keys.union(responses[response].allKeys)

        all_keys = sorted(all_keys)
        # newTree = insertTree(allKeys, responses)
        newTree = tree.insertTree(all_keys, responses)
        print(newTree)
        assert len(GetOfferSuccessTree) == len(newTree)
        assert GetOfferSuccessTree == newTree
