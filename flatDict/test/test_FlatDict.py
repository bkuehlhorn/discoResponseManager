import pytest
from flatDict.flatDict import *

success = FlatDict({
    "referenceNumber": "demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": {
        "branchNumber": "1234",
        "accountNumber": "00001234",
        "customerType": "BORROWER",
        "accountType": "LNS",
        "accountName": "Branch Account",
        "dateOfLoan": "1999-12-31",
        "amountFinanced": 6735.61,
        "accountBalance": 9876.54,
        "currentApr": 19.99,
        'group0': [1, 2, 3, 4],
        'grouplx': [],
        'groupdx': {},
        'group': [
            {
            "termInMonths": 25,
            "nextDueDate": "2018-09-11",
            "nextDueAmount": 140,
            "transactionCount": 0,
            "loanModString": "",
            "realEstateSecured": False,
            "lastPaymentReceivedDate": "2014-12-31",
            "lastPaymentReceivedAmount": 25,
            "bankruptcy": False}, {
            "termInMonths": 25,
            "nextDueDate": "2018-09-11",
            "nextDueAmount": 140,
            "transactionCount": 0,
            "loanModString": "",
            "realEstateSecured": False,
            "lastPaymentReceivedDate": "2014-12-31",
            "lastPaymentReceivedAmount": 25,
            "bankruptcy": False}, {
            "termInMonths": 25,
            "nextDueDate": "2018-09-11",
            "nextDueAmount": 140,
            "transactionCount": 0,
            "loanModString": "",
            "realEstateSecured": False,
            "lastPaymentReceivedDate": "2014-12-31",
            "lastPaymentReceivedAmount": 25,
            "bankruptcy": False}],
        "bankruptcyChapter": "Not bankrupt",
        "paperlessStatement": True,
        "paperlessStatusPending": True,
        "paperlessStatementTermsOfUse": True,
        "commoloco": False,
        "accountInterestType": "InterestBearing",
        "payOffRequestStatus": "ELIGIBLE",
        "customerStanding": "ITA_AUTO_LOAN_GOOD_STANDING",
        "paymentAllowed": True,
        "foreclosure": False,
        "repossession": False,
        "judgement": False,
        "nsfCount": 0,
        "lastStmtDue": "2018-08-29",
        "lastStmtAmt": 15181.83,
        "closingMethodCode": "",
        "guid": "",
        "appReferenceNumber": "8004520",
        "lateFeeAmount": 125.31,
        "nsfFeeAmount": 112.89,
        "delinquencyDays": 12,
        "pastDueBannerEligibility": True,
        "esigDocsDownload": False,
        "currentPaymentDueDate": "2018-09-29",
        "currentPaymentDueAmount": 556.92,
        "nextPaymentDueDate": "2018-08-29",
        "nextPaymentDueAmount": 999.99,
        "pastDueFlag": False,
        "pastDueAmount": 999.99,
        "paidAheadDate": "2018/08/22",
        "currentBalance": 9999,
        "paidInFull": False,
        "settledInFull": True,
        "borrowerAssistanceEligibility": True,
        "dmgAccount": False
    }
})

successSmall = FlatDict({
    "referenceNumber": "demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": {
        "branchNumber": "1234",
        "accountNumber": "00001234",
        'group0': [1, 2, 3, 4],
        'grouplx': [],
        'groupdx': {},
        'group': [{
            "termInMonths": 25,
            "nextDueDate": "2018-09-11",
            "bankruptcy": False}, {
            "termInMonths": 25,
            "nextDueDate": "2018-09-11",
            "bankruptcy": False}, {
            "termInMonths": 25,
            "nextDueDate": "2018-09-11",
            "bankruptcy": False}],
        "dmgAccount": False
    }
})

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

successGroupL = FlatDict({
    "referenceNumber": "demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": {
        'grouplL': []
    }
})

successGroupD = FlatDict({
    "referenceNumber": "demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": {
        'grouplD': {'a':1},
        "dmgAccount": False
    }
})

successGroup = FlatDict({
    "referenceNumber": "demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": {
        'group': [
            {"termInMonths": 25,
             "nextDueDate": "2018-09-11",
             "bankruptcy": False},
            {"termInMonths": 25,
             "nextDueDate": "2018-09-11",
             "bankruptcy": False},
            {"termInMonths": 25,
             "nextDueDate": "2018-09-11",
             "bankruptcy": False}
        ],
        "dmgAccount": False
    }
})


class TestGetKeys(object):
    def testGetKeysGroup(self):
        successGroupKeys = successGroup.getKeys()
        assert 6 == len(successGroupKeys)

    def testGetKeysGroupQ(self):
        successGroupKeys = successGroup0.getKeys()
        assert 6 == len(successGroupKeys)

    def testGetKeysSuccess(self):
        successKeys = successGroupD.getKeys()
        assert 4 == len(successKeys)

    def testGetKeyssuccessSmall(self):
        successKeys = successSmall.getKeys()
        assert 10 == len(successKeys)

    def testGetKeyssuccess(self):
        successKeys = success.getKeys()
        assert 57 == len(successKeys)


class TestGetValue(object):
    def testComplexKeyValueExists(self):
        key = 'accountDetail:group:0:termInMonths'
        fieldValue = successGroup.getValue(key)
        assert fieldValue == 25

    def testSimpleKeyValueExists(self):
        key = 'referenceNumber'
        fieldValue = successGroup.getValue(key)
        assert fieldValue == "demo: :AccountDetailsResponse"

    def testComplexKeyDict(self):
        key = 'accountDetail:dmgAccount'
        fieldValue = successGroup.getValue(key)
        assert fieldValue == False

    def testKeyEmpty(self):
        # todo: Consider raising failure for empty and None key
        key = ''
        fieldValue = successGroup.getValue(key)
        assert fieldValue == ''

    def testKeyIncomplete(self):
        key = 'accountDetail:group'
        fieldValue = successGroup.getValue(key)
        assert isinstance(fieldValue, list)

    def testKeyMissFormated(self):
        # todo: Consider raising failure for missformated key
        key = 'accountDetail:group:'
        fieldValue = successGroup.getValue(key)
        assert fieldValue == ''

    def testComplexKeyListBounds(self):
        key = 'accountDetail:group:6:termInMonths'
        with pytest.raises(IndexError):
            successGroup.getValue(key)

    def testComplexKeyBad(self):
        key = 'accountDetail:group6'
        with pytest.raises(KeyError):
            successGroup.getValue(key)


class TestAddValue(object):
    def testSimpleKeyValueExists(self):
        key = 'referenceNumber'
        successGroup.addValue(key, 'new reference number')
        fieldValue = successGroup.getValue(key)
        assert fieldValue == "new reference number"

    def testListKey(self):
        key = 'accountDetail:dmgAccount'
        successGroup.addValue(key, 42)
        fieldValue = successGroup.getValue(key)
        assert fieldValue == 42

    # def testListKey(self):
    #     key = 'accountDetail:group:0:termInMonths'
    #     successGroup.addValue(key, '42')
    #     fieldValue = successGroup.getValue(key)
    #     # assert fieldValue == 42
    #
    # def testAddListEntry(self):
    #     key = 'accountDetail:group:3:termInMonths'
    #     successGroup.addValue(key, '42')
    #     fieldValue = successGroup.getValue(key)
    #     # assert fieldValue == 42
    #
    # def testAddDictEntry(self):
    #     key = 'accountDetail:group'
    #     successGroup.addValue(key, {'new key': 'value'})
    #     fieldValue = successGroup.getValue(key+':kew key')
    #     # assert fieldValue == 'value'

