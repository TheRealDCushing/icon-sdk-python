# -*- coding: utf-8 -*-
# Copyright 2018 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from tests.api_send.test_send_super import TestSendSuper
from IconService.builder.transaction_builder import IcxTransactionBuilder
from IconService.signed_transaction import SignedTransaction
from IconService.utils.validation import is_icx_transaction, is_T_HASH
from IconService.exception import JSONRPCException


class TestSendTransfer(TestSendSuper):

    def test_transfer(self):

        # When having an optional property, nonce
        icx_transaction = IcxTransactionBuilder().from_(self.setting["from"]).to(self.setting["to"]) \
            .value(self.setting["value"]).step_limit(self.setting["step_limit"]).nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]).build()
        tx_dict = SignedTransaction.to_dict(icx_transaction)
        self.assertTrue(is_icx_transaction(tx_dict))

        signed_transaction_dict = SignedTransaction(icx_transaction, self.wallet)
        result = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))

        # When not having an optional property, nonce
        icx_transaction = IcxTransactionBuilder().from_(self.setting["from"]).to(self.setting["to"]) \
            .value(self.setting["value"]).step_limit(self.setting["step_limit"]).nid(self.setting["nid"]).build()
        tx_dict = SignedTransaction.to_dict(icx_transaction)
        self.assertTrue(is_icx_transaction(tx_dict))

        signed_transaction_dict = SignedTransaction(icx_transaction, self.wallet)
        result = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))

        # When value is wrong not prefixed with '0x'
        wrong_value = "34330000000"
        icx_transaction = IcxTransactionBuilder().from_(self.setting["from"]).to(self.setting["to"]) \
            .value(wrong_value).step_limit(self.setting["step_limit"]).nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]).build()
        signed_transaction_dict = SignedTransaction(icx_transaction, self.wallet)
        self.assertRaises(JSONRPCException, self.icon_service.send_transaction, signed_transaction_dict)

        # When value is wrong which type is int
        wrong_value = 34330000000
        icx_transaction = IcxTransactionBuilder().from_(self.setting["from"]).to(self.setting["to"]) \
            .value(wrong_value).step_limit(self.setting["step_limit"]).nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]).build()
        signed_transaction_dict = SignedTransaction(icx_transaction, self.wallet)
        self.assertRaises(JSONRPCException, self.icon_service.send_transaction, signed_transaction_dict)

        # When address is wrong
        wrong_address = "hx5bfdb090f43a808005ffc27c25b213145e8"
        icx_transaction = IcxTransactionBuilder().from_(self.setting["from"]).to(wrong_address) \
            .value(self.setting["value"]).step_limit(self.setting["step_limit"]).nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]).build()
        signed_transaction_dict = SignedTransaction(icx_transaction, self.wallet)
        self.assertRaises(JSONRPCException, self.icon_service.send_transaction, signed_transaction_dict)

        # When not having a required property, nid
        icx_transaction = IcxTransactionBuilder().from_(self.setting["from"]).to(self.setting["to"]) \
            .value(self.setting["value"]).step_limit(self.setting["step_limit"]) \
            .nonce(self.setting["nonce"]).build()
        signed_transaction_dict = SignedTransaction(icx_transaction, self.wallet)
        self.assertRaises(JSONRPCException, self.icon_service.send_transaction, signed_transaction_dict)

        # When a sending address is wrong - not the wallet's address
        wrong_address = "hx5bfdb090f43a808005ffc27c25b213145e80b7cd"
        icx_transaction = IcxTransactionBuilder().from_(wrong_address).to(self.setting["to"]) \
            .value(self.setting["value"]).step_limit(self.setting["step_limit"]).nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]).build()
        signed_transaction_dict = SignedTransaction(icx_transaction, self.wallet)
        self.assertRaises(JSONRPCException, self.icon_service.send_transaction, signed_transaction_dict)

