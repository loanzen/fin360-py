import requests
from attrdict import AttrDict

SUPPORTED_BANKS = ['ICICI', 'SBI', 'KOTAK', 'YES', 'HDFC', 'AXIS', 'SYNDICATE', 'CORPORATION', 'PNB', 'UNITED_BANK',
                   'INDUSIND', 'CENTRAL_BANK', 'CITI', 'DBS', 'CANARA', 'STANDARD_CHARTERED', 'RBL', 'UNION_BANK',
                   'ALLAHABAD', 'BANK_OF_BARODA', 'STATE_BANK_PATIALA', 'STATE_BANK_MYSORE', 'STATE_BANK_TRAVANCORE',
                   'TAMILNAD_MERCANTILE', 'STATE_BANK_BIKANER_JAIPUR', 'STATE_BANK_HYDERABAD', 'BANK_OF_INDIA',
                   'BANK_OF_MAHARASHTRA', 'DENA_BANK', 'INDIAN_BANK', 'INDIAN_OVERSEAS', 'ORIENTAL_BANK', 'PUNJAB_SIND',
                   'UCO', 'VIJAYA', 'IDBI', 'BANDHAN', 'CATHOLIC_SYRIAN', 'CITY_UNION', 'DHANLAXMI', 'DCB', 'FEDERAL',
                   'IDFC', 'KARNATAKA', 'JAMMU_KASHMIR', 'KARUR_VYASA', 'LAKSHMI_VILAS', 'NAINITAL', 'SOUTH_INDIAN',
                   'RBS', 'SARASWAT_BANK', 'TJSB', 'DNB', 'DEUTSCHE_BANK', 'GREATER_BOMBAY', 'APNA_SAHAKARI_BANK',
                   'AKHAND_ANAND', 'BASSEIN_CATHOLIC', 'ANDHRA_BANK', 'PUNJAB_MAHARASHTRA_CO_OP_BANK', 'HSBC', 'BHARAT',
                   'SVC_BANK', 'SREENIDHI_SOUHARDA_SAHAKARI_BANK', 'OCEAN_FIRST']

SUPPORTED_ACCOUNT_TYPES = ['SAVING', 'CURRENT', 'CREDIT_CARD']


class Fin360ApiException(Exception):

    def __init__(self, status, **kwargs):
        description = kwargs.get('description', None)
        description_map = {
            400: "Bad Request",
            401: "Invalid Access Token",
            403: "Access Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
            503: "Service Unavailable",
        }
        self.status = status
        self.description = description_map[status] if description is None else description
        super(Fin360ApiException, self).__init__(self.description)

    def to_dict(self):
        return {
            'status': self.status,
            'description': self.description
        }

    def __str__(self):
        return super(Fin360ApiException, self).__str__()


class Fin360Client(object):

    BASE_URL = "https://www.fin360.in"

    def __init__(self, **kwargs):
        self.access_token = kwargs.get('access_token', None)

    def authenticate(self, email, password):
        url = '{}/bank-auth/api/v1/login'.format(self.BASE_URL)
        data = {"emailAddress": email, "password": password}
        response = requests.request("POST", url, data=data)

        if response.status_code is not 200:
            raise Fin360ApiException(response.status_code)

        self.access_token = response.json()['access_token']

        return AttrDict(response.json())

    def upload_statement(self, statement):
        url = "https://www.fin360.in/bank-connect/api/v1/uploadStatement"
        querystring = {"access_token": self.access_token}

        if statement['bank'].upper() not in SUPPORTED_BANKS:
            raise ValueError('{} is an unsupported bank'.format(statement['bank']))

        if statement['accountType'].upper() not in SUPPORTED_ACCOUNT_TYPES:
            raise ValueError('{} is an unsupported account type'.format(statement['accountType']))

        files = {'bankStmt': open(statement['bankStmt'], 'rb')}
        response = requests.request("POST", url, params=querystring, files=files, data=statement)

        if response.status_code is not 200:
            raise Fin360ApiException(response.status_code)

    def get_transactions_with_details(self, account_id):
        '''
            Returns transactions of a given statement (given account_id) in json format.

            Paramaters
            ----------
            arg1: account_id
                    account_id is returned from upload statement or upload multiple statements methods

            Returns
            -------
            json
                eg:
                {
                "bank_account": {
                    "accountHolder": "ACCOUNT_HOLDER_NAME",
                    "accountLimit": null,
                    "accountNo": "ACCOUNT_NUMBER",
                    "address": "N/A",
                    "availableCashLimit": null,
                    "availableCreditLimit": null,
                    "bank": {
                        "enumType": "",
                        "name": "BANK_NAME"
                    },
                    "bankAccountUID": "BANKACCOUNTUID",
                    "bankAddress": null,
                    "bankCredentialCO": null,
                    "bankTransactionList": [],
                    "branchAddress": null,
                    "cifNumber": null,
                    "client": null,
                    "creditCardNo": null,
                    "creditLimit": null,
                    "crnNo": null,
                    "currentCashAdvance": null,
                    "currentPurchaseCharges": null,
                    "customer": null,
                    "customerID": null,
                    "dueDate": null,
                    "email": null,
                    "fromDate": null,
                    "ifsCode": null,
                    "isValidBankStatement": true,
                    "lastPaymentReceived": null,
                    "micrCode": null,
                    "minAmountDue": null,
                    "openingBalance": null,
                    "pointsEarned": null,
                    "prevBalance": null,
                    "toDate": null,
                    "totalAmountDue": null,
                    "uploadBankStatementCO": null
                },
                "transactions": [
                    {
                        "amount": 500,
                        "balanceAfterTransaction": 1000.08,
                        "category": "RTGS",
                        "dateTime": "16/05/2016",
                        "description": "RTGS description",
                        "remark": null,
                        "type": "CREDIT",
                        "valueDate": null
                    }
                ]
            }
        '''
        url = '{0}/bank-account/api/v1/transactionsWithDetails/{1}.json'.format(self.BASE_URL, account_id)
        querystring = {"access_token": self.access_token}

        response = requests.request("GET", url, params=querystring)
        if response.status_code is not 200:
            raise Fin360ApiException(response.status_code)

        return AttrDict(response.json())
