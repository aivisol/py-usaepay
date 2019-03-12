import unittest
from usaepay import usaepay
try:
	import test_data as test_data
except:
	import test_data_default as test_data

class UsaePayTestCase(unittest.TestCase):
	def setUp(self):
		self.txn_key = "_oL9jiwtFZcw697CDK4Pz5fqm7aWAqLU"

	def test_missing_card_no(self):
		tran = usaepay.UmTransaction()
		tran.key = test_data.txn_key
		tran.exp = "0120"
		tran.amount = "5.00"
		tran.invoice = '1212121212121212'
		tran.usesandbox = True
		res = tran.process()

		self.assertEqual(res, False)
		self.assertEqual(tran.result, "Error")
		self.assertEqual(tran.resultcode, "E")
		self.assertEqual(tran.errorcode, "10129")
		self.assertEqual(tran.error, "Credit Card Number is required")

	def test_missing_card_exp(self):
		tran = usaepay.UmTransaction()
		tran.key = self.txn_key
		tran.card = "4111111111111111"
		tran.amount = "5.00"
		tran.invoice = '1212121212121212'
		tran.usesandbox = True
		res = tran.process()

		self.assertEqual(res, False)
		self.assertEqual(tran.result, "Error")
		self.assertEqual(tran.resultcode, "E")
		self.assertEqual(tran.errorcode, "10129")
		self.assertEqual(tran.error, "Expiration Date is required")

	def test_missing_card_amount(self):
		tran = usaepay.UmTransaction()
		tran.key = self.txn_key
		tran.card = "4111111111111111"
		tran.exp = "0120"
		tran.invoice = '1212121212121212'
		tran.usesandbox = True
		res = tran.process()

		self.assertEqual(res, False)
		self.assertEqual(tran.result, "Error")
		self.assertEqual(tran.resultcode, "E")
		self.assertEqual(tran.errorcode, "10129")
		self.assertEqual(tran.error, "Amount is required")

	def test_lineitem(self):
		tran = usaepay.UmTransaction()
		tran.key = self.txn_key
		tran.card = "4111111111111111"
		tran.exp = "0120"
		tran.amount = "15.00"
		tran.invoice = '1212121212121212'
		tran.usesandbox = True
		tran.lineitems = [{"sku": "123"}, {"sku": "456"}]
		res = tran.process()

		self.assertEqual(res, True)
		self.assertEqual(tran.result, 'Approved')
		self.assertEqual(tran.resultcode, "A")
		self.assertEqual(tran.errorcode, "00000")
		self.assertEqual(tran.error, "Approved")


	def test_process_sandbox_1_ok(self):
		tran = usaepay.UmTransaction()
		tran.key = self.txn_key
		tran.card = "4111111111111111"
		tran.exp = "0120"
		tran.amount = "5.00"
		tran.invoice = '1212121212121212'
		tran.usesandbox = True
		res = tran.process()

		self.assertEqual(res, True)
		self.assertEqual(tran.result, 'Approved')
		self.assertEqual(tran.resultcode, "A")
		self.assertEqual(tran.errorcode, "00000")
		self.assertEqual(tran.error, "Approved")

	def test_process_sandbox_1_ok_sale(self):
		tran = usaepay.UmTransaction()
		tran.key = self.txn_key
		tran.card = "4111111111111111"
		tran.exp = "0120"
		tran.amount = "25.00"
		tran.invoice = '1212121212121212'
		tran.command = "cc:sale"
		tran.usesandbox = True
		res = tran.process()

		self.assertEqual(res, True)
		self.assertEqual(tran.result, 'Approved')
		self.assertEqual(tran.resultcode, "A")
		self.assertEqual(tran.errorcode, "00000")
		self.assertEqual(tran.error, "Approved")

	def test_process_sandbox_1_bad_card(self):
		tran = usaepay.UmTransaction()
		tran.key = self.txn_key
		tran.card = "9111111111111111"
		tran.exp = "0120"
		tran.amount = "5.00"
		tran.invoice = '1212121212121212'
		tran.usesandbox = True
		res = tran.process()

		self.assertEqual(res, False)
		self.assertEqual(tran.result, 'Error')
		self.assertEqual(tran.resultcode, "E")
		self.assertEqual(tran.errorcode, "00013")
		self.assertEqual(tran.error, "Invalid Card Number (3)")

	def test_process_sandbox_1_expired_card(self):
		tran = usaepay.UmTransaction()
		tran.key = self.txn_key
		tran.card = "4111111111111111"
		tran.exp = "0110"
		tran.amount = "15.00"
		tran.invoice = '1212121212121212'
		tran.usesandbox = True
		res = tran.process()

		self.assertEqual(res, False)
		self.assertEqual(tran.result, 'Declined')
		self.assertEqual(tran.resultcode, "D")
		self.assertEqual(tran.errorcode, "00017")
		self.assertEqual(tran.error, "Credit card has expired.")