import pytest
from discoResponses.discoResponses import *

successGroup0 = FlatDict({
    "referenceNumber": "demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": {
        'transactionCountD': 0,
        "branchNumber": "1234",
        'group0': [1, 2, 3, 4],
        "after": "group"
    }
})

successGroup02 = FlatDict({
    "referenceNumber": "demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": {
        'transactionCount': 0,
        "branchNumber": "1234",
        'group0': [1, 2, 3, 4],
        "after": "group"
    }
})


class TestInsertTree(object):
    class MockTree(object):
        def __init__(self, *args, **kwargs):
            self.tree = []

        def insert(self, *args, **kwargs):
            self.tree.append((args, kwargs))

    def testGetKeysGroup(self):
        frame = ttk.Frame()
        tree = discoTree(frame, '')
        responses = dict()
        response = successGroup0
        allKeys = sorted(list(set(successGroup0.getKeys() + successGroup02.getKeys())))
        responses['success.json.erb'] = RESPONSE_ENTRY(response['status']=='SUCCESS', True, response, response.getKeys())
        responses['success2.json.erb'] = RESPONSE_ENTRY(response['status']=='SUCCESS', True, successGroup02, successGroup02.getKeys())

        # newTree = insertTree(allKeys, responses)
        newTree = tree.insertTree(allKeys, responses)
        assert 9 == len(newTree['success.json.erb'])
