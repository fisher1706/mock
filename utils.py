import json
import os
import random
import string
from pprint import pprint

from db_resource import get_trans_data
from settings import PATH


def unicode_convert(data, encoding='utf-8'):
    if isinstance(data, (str, bool, int, float)):
        return data
    else:
        return data.encode(encoding)


def randomStr(size=24, start_chars=None, chars=string.ascii_letters + string.digits):
    chars = unicode_convert(chars)
    _start_chars = ''

    if isinstance(start_chars, str):
        start_chars = unicode_convert(start_chars)

        if len(start_chars) < size:
            _start_chars = start_chars
    return _start_chars + ''.join(random.choice(chars) for _ in range(size - len(_start_chars)))


def generate_trans_data(data):
    trans_data = {
        "Transaction":
            {"Interchange": float('{:.2f}'.format(random.random() * 10)),
             "CashbackAmount": 0.0,
             "OriginalAmount": float(data.get('amount')),
             "TerminalID": data.get('terminal_id'),
             "PartnerID": randomStr(3, "", string.digits),
             "BatchNumber": randomStr(10, "", string.digits),
             "Scheme": "VISA",
             "MerchantID": data.get('timestart').strftime('%Y-%m-%d-%H.%M.%S.%f'),
             "BatchID": data.get('timeend').strftime('%Y-%m-%d-%H.%M.%S.%f'),
             "ReferenceData": "",
             "PaidDate": data.get('timeend').strftime('%Y-%m-%dT00:00:00'),
             "PurchaseDate": data.get('timestart').strftime('%Y-%m-%dT00:00:00'),
             "GrossAmount": 100000,
             # "OriginalCurrency": data.get('currency'),
             "OriginalCurrency": 'GBP',
             "TransactionCode": "SALE" + randomStr(2, "", string.digits),
             "CardNumber": data.get('card_bin') + "******" + data.get('card_last_digits'),
             "DbaName": "Fondy Ltd* FROMTHEMAKE",
             "TransactionID": data.get('ps_tran_id'),
             "RegistrationDate": data.get('timeend').strftime('%Y-%m-%dT00:00:00'),
             "NetAmount": float(data.get('actual_amount')),
             "SchemeFeeFixed": float('{:.4f}'.format(random.random())),
             "PhysicalTerminalID": randomStr(8, "", string.digits),
             "SystemSettlementType": randomStr(1, "", string.digits),
             "MerchantName": "Fondy Ltd",
             "SettlementID": data.get('timeend').strftime('%Y-%m-%d-%H.%M.%S.%f'),
             "SettlementType": "0",
             "AuthorizationNumber": "T" + randomStr(5, "", string.digits),
             "SchemeFeeBase": float('{:.3f}'.format(random.random())),
             "MerchantRegistrationNumber": randomStr(8, "", string.digits),
             "ReasonCode": "00",
                "ID": "2022-04-22-23.41.19.000570",
             "TransactionType": "TRTYPE_" + randomStr(2, "", string.digits),
             "AgreementID": randomStr(6, "", string.digits),
             "MerchantBucketName": None,
             "SettlementNumber": randomStr(8, "", string.digits),
             "SchemeFee": float('{:.4f}'.format(random.random())),
             "CardHolderCurrency": None,
             "Currency": 'EUR',
             "CardType": "CreditCard",
             "SchemeFeePercent": float('{:.4f}'.format(random.random())),
             "Fees": float('{:.4f}'.format(random.random() * 10)),
             "CardHolderAmount": 0.0,
             "MerchantBucketID": randomStr(7, "", string.digits),
             "SchemeFeeCurrency": data.get('currency'),
             "Arn": randomStr(23, "", string.digits),
             "TransactionLifeCycleID": "MCCTMB" + randomStr(7, "", string.digits),
             },
        "ResponseDateTime": data.get('timestart').strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
    }

    return trans_data


def generate_exception_data(data, code):
    exception_data = {
        "Exceptions": [
            {
                "MerchantReferenceNumber": None,
                "TerminalID": data.get('terminal_id'),
                "IssueNumber": None,
                "Scheme": "VISA",
                "Status": "B",
                "ReferenceData": "",
                "PurchaseDate": data.get('timestart').strftime('%Y-%m-%dT00:00:00'),
                "GrossAmount": float(data.get('amount')) * -1,
                "OriginalCurrency": data.get('currency'),
                "Agreement": randomStr(6, "", string.digits),
                "TransactionCode": code,
                "CardNumber": data.get('card_bin') + "******" + data.get('card_last_digits'),
                "ReasonCode": randomStr(4, "", string.digits),
                "RegistrationDate": data.get('timeend').strftime('%Y-%m-%dT00:00:00'),
                "SchemeFeeFixed": 0.0,
                "MerchantName": "Fondy Ltd",
                "SettlementID": data.get('timeend').strftime('%Y-%m-%d-%H.%M.%S.%f'),
                "ChargebackReferenceNumber": randomStr(10, "", string.digits),
                "AuthorizationNumber": "T" + randomStr(6, "", string.digits),
                "OriginalBatchID": randomStr(10, "", string.digits),
                "SchemeFeeBase": 0.0,
                "OriginalAmount": float(data.get('amount')),
                "SourceCurrency": data.get('currency'),
                "ID": data.get('timeend').strftime('%Y-%m-%d-%H.%M.%S.%f'),
                "TransactionType": "TRTYPE_" + randomStr(2, "", string.digits),
                "MessageText": "9130541827",
                "SchemeFee": 0.0,
                "SourceAmount": float(data.get('amount')),
                "Currency": data.get('currency'),
                "CardType": "CreditCard",
                "SchemeFeePercent": 0.0,
                    "OriginalTransactionID": "2022-04-22-23.41.19.000570",
                "SchemeFeeCurrency": "",
                "Arn": randomStr(23, "", string.digits)
            }
        ]
    }

    return exception_data


# def generate_exception_data(data, codes):
#     exception_data = {"Exceptions": ''}
#     inner = []
#
#     for code in codes:
#         row = {
#                 "MerchantReferenceNumber": None,
#                 "TerminalID": data.get('terminal_id'),
#                 "IssueNumber": None,
#                 "Scheme": "VISA",
#                 "Status": "B",
#                 "ReferenceData": "",
#                 "PurchaseDate": data.get('timestart').strftime('%Y-%m-%dT00:00:00'),
#                 "GrossAmount": float(data.get('amount')) * -1,
#                 "OriginalCurrency": data.get('currency'),
#                 "Agreement": randomStr(6, "", string.digits),
#                 "TransactionCode": code,
#                 "CardNumber": data.get('card_bin') + "******" + data.get('card_last_digits'),
#                 "ReasonCode": randomStr(4, "", string.digits),
#                 "RegistrationDate": data.get('timeend').strftime('%Y-%m-%dT00:00:00'),
#                 "SchemeFeeFixed": 0.0,
#                 "MerchantName": "Fondy Ltd",
#                 "SettlementID": data.get('timeend').strftime('%Y-%m-%d-%H.%M.%S.%f'),
#                 "ChargebackReferenceNumber": randomStr(10, "", string.digits),
#                 "AuthorizationNumber": "T" + randomStr(6, "", string.digits),
#                 "OriginalBatchID": randomStr(10, "", string.digits),
#                 "SchemeFeeBase": 0.0,
#                 "OriginalAmount": float(data.get('amount')),
#                 "SourceCurrency": data.get('currency'),
#                 "ID": data.get('timeend').strftime('%Y-%m-%d-%H.%M.%S.%f'),
#                 "TransactionType": "TRTYPE_" + randomStr(2, "", string.digits),
#                 "MessageText": "9130541827",
#                 "SchemeFee": 0.0,
#                 "SourceAmount": float(data.get('amount')),
#                 "Currency": data.get('currency'),
#                 "CardType": "CreditCard",
#                 "SchemeFeePercent": 0.0,
#                     "OriginalTransactionID": "2022-04-22-23.41.19.000570",
#                 "SchemeFeeCurrency": "",
#                 "Arn": randomStr(23, "", string.digits)
#             }
#         inner.append(row)
#
#     exception_data["Exceptions"] = inner
#
#     return exception_data


def writer(data, filename, path=PATH):
    json_object = json.dumps(data)

    with open(path + filename, "w") as outfile:
        try:
            outfile.write(json_object)
        except Exception:
            raise Exception(f'json data: {filename} is not created')


def cleaner(path=PATH):
    for file in os.listdir(path):
        os.remove(path + file)
        print(f"file: {file} - deleted")


if __name__ == '__main__':
    tran = 9001539162
    c = ['CHABAC', 'ZAPEL']

    d = get_trans_data(tran)

    x = generate_exception_data(d, c)
    pprint(x)
