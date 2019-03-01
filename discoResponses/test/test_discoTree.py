import pytest
from discoResponses.discoResponses import *
delimiter = FlatDict.delimiter
# delimiter = '\0'
# delimiter = '/'
# FlatDict.delimter = delimiter

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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

successGroup0Array = {
    "referenceNumber": "demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": {
        'transactionCountD': 0,
        "branchNumber": "1234",
        'group0': [1, 2, 3, 4],
        "after": "group"
    }
}

successGroup02Array = {
    "referenceNumber": "demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": {
        'transactionCount': 0,
        "branchNumber": "1234",
        'group0': [1, 2, 3, 4],
        "after": "group"
    }
}


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
        responses['success.json.erb'] = RESPONSE_ENTRY(response['status']=='SUCCESS', True, response, response.getKeys())
        responses['success2.json.erb'] = RESPONSE_ENTRY(response['status']=='SUCCESS', True, sg02, sg02.getKeys())

        # newTree = insertTree(allKeys, responses)
        newTree = tree.insertTree(allKeys, responses)
        assert 6 == len(newTree['success.json.erb'])

    def testGetKeysGroupArray(self):
        frame = ttk.Frame()
        tree = DiscoTree(frame, '')
        responses = dict()
        sg0 = FlatDict(successGroup0Array)
        sg02 = FlatDict(successGroup02Array)
        response = sg0
        allKeys = sorted(list(set(sg0.getKeys() + sg02.getKeys())))
        responses['success.json.erb'] = RESPONSE_ENTRY(response['status']=='SUCCESS', True, response, response.getKeys())
        responses['success2.json.erb'] = RESPONSE_ENTRY(response['status']=='SUCCESS', True, sg02, sg02.getKeys())

        # newTree = insertTree(allKeys, responses)
        newTree = tree.insertTree(allKeys, responses)
        assert 9 == len(newTree['success.json.erb'])

    def testGetKeysGroupApplication(self):
        frame = ttk.Frame()
        tree = DiscoTree(frame, '')
        responses = dict()
        sg0 = FlatDict(successApplication)
        sg02 = FlatDict(successBranch)
        responses = {}
        responses['success.json.erb'] = RESPONSE_ENTRY(sg0['status']=='SUCCESS', True, sg0, sg0.getKeys())
        responses['success2.json.erb'] = RESPONSE_ENTRY(sg02['status']=='SUCCESS', True, sg02, sg02.getKeys())
        all_keys = set()
        for response in responses:
            all_keys = all_keys.union(responses[response].allKeys)

        all_keys = sorted(all_keys)
        newTree = tree.insertTree(all_keys, responses)
        assert 22 == len(newTree['success.json.erb'])

    def testGetKeysGroupGetOffer(self):
        frame = ttk.Frame()
        tree = DiscoTree(frame, '')
        responses = dict()
        sg0 = FlatDict(GetOfferSuccess)
        sg02 = FlatDict(GetOfferDirect)
        responses = {}
        responses['success.json.erb'] = RESPONSE_ENTRY(sg0['status']=='SUCCESS', True, sg0, sg0.getKeys())
        responses['success2.json.erb'] = RESPONSE_ENTRY(sg02['status']=='SUCCESS', True, sg02, sg02.getKeys())
        all_keys = set()
        for response in responses:
            all_keys = all_keys.union(responses[response].allKeys)

        all_keys = sorted(all_keys)
        # newTree = insertTree(allKeys, responses)
        newTree = tree.insertTree(all_keys, responses)
        assert 25 == len(newTree['success.json.erb'])
        assert 25 == len(newTree['success2.json.erb'])
