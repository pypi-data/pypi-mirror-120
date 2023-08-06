import os
import sys
import base64
import pprint
import code
import logging
import json
from datetime import datetime, timedelta

# Module Imports
import requests
from requests.auth import HTTPBasicAuth


class BTCPayServerAPIClient(object):
    def __init__(self, btcpay_url):
        self.base_url = btcpay_url

        # Store auth header
        self.auth_header = None
        self.active_store_id = None

    @classmethod
    def login_basic(cls, btcpay_url, username, password):
        uname = os.getenv("BTCPayUser")
        upass = os.getenv("BTCPayPass")

        # Exit if any creds missing
        if not any([uname, upass]):
            print("No Credentials Available!")
            print("Must export BTCPayUser and BTCPayPass before running this script.")
            sys.exit(-1)

        acode = f"{uname}:{upass}".encode()
        header_key = base64.b64encode(acode).decode()
        headers = {
            "Authorization": f"Basic {header_key}",
            "Content-Type": "application/json",
        }

        cls.auth_header = headers

        btcpay = cls.whoami(cls.auth_header)
        print(btcpay)
        return cls

    @classmethod
    def login_token(cls, btcpay_url, token):
        instance = cls(btcpay_url=btcpay_url)
        headers = {
            "Authorization": f"token {token}",
            "Content-Type": "application/json",
        }
        instance.auth_header = headers
        return instance

    def create_payment_request(self, request_data):
        url = f"{self.base_url}/api/v1/stores/{self.active_store_id}/payment-requests"
        print(url)
        create_request = requests.post(
            url=url,
            data=json.dumps(request_data),
            headers=self.auth_header,
        )
        if create_request.status_code != 200:
            print("There was a problem creating payment request")
            print(create_request.status_code)
            print(create_request.text)
            raise ValueError(create_request.text)

        request_result = create_request.json()
        return request_result

    def create_invoice(self, request_data):
        url = f"{self.base_url}/api/v1/stores/{self.active_store_id}/invoices"
        print(url)
        create_invoice = requests.post(
            url=url,
            data=json.dumps(request_data),
            headers=self.auth_header,
        )
        print(create_invoice.status_code)
        if create_invoice.status_code != 200:
            print("There was a problem creating invoice")
            print(create_invoice.status_code)
            print(create_invoice.text)
            raise ValueError(create_invoice.text)

        request_result = create_invoice.json()
        return request_result    

    def get_invoice_payment_methods(self, payment_id):
        url = f"{self.base_url}/api/v1/stores/{self.active_store_id}/invoices/{payment_id}/payment-methods"
        print(url)
        get_invoice_methods = requests.get(
            url=url,
            headers=self.auth_header,
        )
        # print(get_invoice_methods.json())
        for method in get_invoice_methods.json():
            if method['paymentMethod'] == "BTC":
                onchain_addr = method['destination']
            elif method['paymentMethod'] == "BTC-LightningNetwork":
                lightning_addr = method['destination']

        return onchain_addr, lightning_addr

    def set_store_id(self, store_id):
        self.active_store_id = store_id

    def get_token(self, label, plist=["unrestricted"]):
        if plist != None:
            permissions = plist

        payload = {
            "label": label,
            "permissions": permissions,
        }

        # Obtain the API Key
        url = f"{self.base_url}/api/v1/api-keys"
        r = requests.post(url, headers=self.basic_header, json=payload)
        print(r.text)
        print(f"API Key Status Code: {r.status_code}")
        new_token = r.json()["apiKey"]

        # Test API Key
        header = {"Authorization": f"token {new_token}"}
        url = f"{self.base_url}/api/v1/api-keys/current"
        r = requests.get(url, headers=header)

        self.token_header = header
        if self.token_header == None:
            return False
        return True

    # TODO:
    def get_pay_request_url(self):
        pass


    def get_current_key(self):
        url = f"{self.base_url}/api/v1/api-keys/current"
        r = requests.get(url, headers=self.token_header)
        try:
            key = r.json()
            return key
        except Exception as e:
            print(e)
            return None

    def get_server_info(self, header):
        if header is None:
            header = self.token_header
        # Get Server Info
        url = f"{self.base_url}/api/v1/server/info"
        r = requests.get(url, headers=self.token_header)
        print(f"STATUS CODE: {r.status_code}")
        return r.json()

    def create_new_user(self, uname, upass, header=None, isAdmin=False):
        if header is None:
            header = self.token_header
        # Create New Account
        payload = {"email": uname, "password": upass, "isAdministrator": isAdmin}
        url = f"{self.base_url}/api/v1/users"
        r = requests.post(url, headers=header, json=payload)

        sc = r.status_code
        print(f"STATUS CODE: {sc}")
        if sc == 403:
            print("Error: Permissions Issue")
            return
        return r.json()

    def create_new_store(self, store_name, header=None):
        if header is None:
            header = self.token_header
        # Create New Store
        payload = {
            "name": store_name,
            "website": "https://test.io",
            "invoiceExpiration": 900,
            "monitoringExpiration": 3600,
            "speedPolicy": "HighSpeed",
            "lightningDescriptionTemplate": "pay me really fast",
            "paymentTolerance": 0,
            "anyoneCanCreateInvoice": False,
            "requiresRefundEmail": False,
            "lightningAmountInSatoshi": False,
            "lightningPrivateRouteHints": False,
            "onChainWithLnInvoiceFallback": False,
            "redirectAutomatically": False,
            "showRecommendedFee": True,
            "recommendedFeeBlockTarget": 1,
            "defaultLang": "en",
            "htmlTitle": "Test!",
            "networkFeeMode": "MultiplePaymentsOnly",
            "payJoinEnabled": False,
            "defaultPaymentMethod": "BTC",
        }

        url = f"{self.base_url}/api/v1/stores"
        r = requests.post(url, headers=header, json=payload)

        sc = r.status_code
        print(f"STATUS CODE: {sc}")
        return r.json()

    def list_stores(self, header=None):
        if header is None:
            header = self.token_header
        # List Stores
        url = f"{self.base_url}/api/v1/stores"
        r = requests.get(url, headers=header)
        return r.json()

    def whoami(self):
        # Get ME
        url = f"{self.base_url}/api/v1/users/me"
        r = requests.get(url, headers=self.auth_header)

        if r.status_code == 200:
            return r.json()
        sc = r.status_code
        print(f"STATUS CODE: {sc}")
        return r.text

    def internal_node_info(self, header=None):
        if header is None:
            header = self.token_header

        # Get Lightning Node Info
        cryptoCode = "BTC"
        url = f"{self.base_url}/api/v1/server/lightning/{cryptoCode}/info"
        r = requests.get(url, headers=header)

        sc = r.status_code
        print(f"STATUS CODE: {sc}")
        return r.text

    def internal_node_connect(self, node_uri, header=None):
        if header is None:
            header = self.token_header

        # Connect Lightning Node
        cryptoCode = "BTC"
        url = f"{self.base_url}/api/v1/server/lightning/{cryptoCode}/connect"
        payload = {"nodeURI": node_uri}
        r = requests.post(url, headers=header, json=payload)

        sc = r.status_code
        print(f"STATUS CODE: {sc}")
        return r.text

    def internal_node_address(self, header=None):
        if header is None:
            header = self.token_header

        # Get Lightning Node On-Chain Address
        cryptoCode = "BTC"
        url = f"{self.base_url}/api/v1/server/lightning/{cryptoCode}/address"
        r = requests.post(url, headers=header)

        sc = r.status_code
        print(f"STATUS CODE: {sc}")
        return r.text


if __name__ == "__main__":
    a = BTCPayServerAPIClient()
    a.login()
    code.interact(local=locals())
