import pytest
from flatDict.flatDict import *

import logging
logger = logging.getLogger(__name__)

success = {
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
}

successSmall = {
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
}

successGroup0 = {
    "referenceNumber": "demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": {
        'transactionCountD': 0,
        "branchNumber": "1234",
        'group0': [1, 2, 3, 4],
        "after": "group"
    }
}

successGroupL = {
    "referenceNumber": "demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": {
        'grouplL': []
    }
}

successGroupD = {
    "referenceNumber": "demo: :AccountDetailsResponse",
    "status": "SUCCESS",
    "accountDetail": {
        'grouplD': {'a':1},
        "dmgAccount": False
    }
}

successGroup = {
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
}

successApplication = {
    "referenceNumber": "220659464291945925",
    "status": "SUCCESS",
    "creditOffer": {
        "uniqueId": "001358438581231020180619095922286",
        "uniqueIdSeq": 1,
        "existingCustomerType": "NEW",
        "decision": "DECLINED",
        "springleafReferenceNumber": "52302461",
        "appReferenceNumber": "153510843",
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


@pytest.fixture()
def log_config():
    logging.basicConfig(level=logging.WARNING)


class TestGetKeys(object):
    def testGetKeysGroup(self, log_config):
        successGroupKeys = FlatDict(successGroup).getKeys()
        assert 6 == len(successGroupKeys)

    def testGetKeysGroupQ(self, log_config):
        successGroupKeys = FlatDict(successGroup0).getKeys()
        assert 6 == len(successGroupKeys)

    def testGetKeysSuccess(self, log_config):
        successKeys = FlatDict(successGroupD).getKeys()
        assert 4 == len(successKeys)

    def testGetKeyssuccessSmall(self, log_config):
        successKeys = FlatDict(successSmall).getKeys()
        assert 10 == len(successKeys)

    def testGetKeyssuccess(self, log_config):
        successKeys = FlatDict(success).getKeys()
        assert 57 == len(successKeys)

    def testGetKeysApplicant(self, log_config):
        successKeys = FlatDict(successApplication).getKeys()
        assert 16 == len(successKeys)


class TestGetValue(object):
    def testComplexKeyValueExists(self, log_config):
        key = 'accountDetail:group:0:termInMonths'
        fd = FlatDict(successGroup)
        fieldValue = fd.getValue(key)
        assert fieldValue == 25

    def testSimpleKeyValueExists(self, log_config):
        key = 'referenceNumber'
        fd = FlatDict(successGroup)
        fieldValue = fd.getValue(key)
        assert fieldValue == "demo: :AccountDetailsResponse"

    def testComplexKeyDict(self, log_config):
        key = 'accountDetail:dmgAccount'
        fd = FlatDict(successGroup)
        fieldValue = fd.getValue(key)
        assert fieldValue == False

    def testKeyEmpty(self, log_config):
        # todo: Consider raising failure for empty and None key
        key = ''
        fd = FlatDict(successGroup)
        fieldValue = fd.getValue(key)
        assert fieldValue == ''

    def testKeyIncomplete(self, log_config):
        key = 'accountDetail:group'
        fd = FlatDict(successGroup)
        fieldValue = fd.getValue(key)
        assert isinstance(fieldValue, list)

    def testKeyMissFormated(self, log_config):
        # todo: Consider raising failure for missformated key
        key = 'accountDetail:group:'
        fd = FlatDict(successGroup)
        fieldValue = fd.getValue(key)
        assert fieldValue == ''

    def testComplexKeyListBounds(self, log_config):
        key = 'accountDetail:group:6:termInMonths'
        fd = FlatDict(successGroup)
        with pytest.raises(IndexError):
            fd.getValue(key)

    def testComplexKeyBad(self, log_config):
        key = 'accountDetail:group6'
        fd = FlatDict(successGroup)
        with pytest.raises(KeyError):
            fd.getValue(key)


class TestAddValue(object):
    def testSimpleKeyValueExists(self, log_config):
        key = 'referenceNumber'
        fd = FlatDict(successGroup)
        fd.addValue(key, 'new reference number')
        fieldValue = fd.getValue(key)
        assert fieldValue == "new reference number"

    def testListKey(self, log_config):
        key = 'accountDetail:dmgAccount'
        fd = FlatDict(successGroup)
        fd.addValue(key, 42)
        fieldValue = fd.getValue(key)
        assert fieldValue == 42

    # def testListKey(self, log_config):
    #     key = 'accountDetail:group:0:termInMonths'
    #     successGroup.addValue(key, '42')
    #     fieldValue = successGroup.getValue(key)
    #     # assert fieldValue == 42
    #
    # def testAddListEntry(self, log_config):
    #     key = 'accountDetail:group:3:termInMonths'
    #     successGroup.addValue(key, '42')
    #     fieldValue = successGroup.getValue(key)
    #     # assert fieldValue == 42
    #
    # def testAddDictEntry(self, log_config):
    #     key = 'accountDetail:group'
    #     successGroup.addValue(key, {'new key': 'value'}
    #     fieldValue = successGroup.getValue(key+':kew key')
    #     # assert fieldValue == 'value'

