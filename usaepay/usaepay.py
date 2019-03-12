import re
import random
import time
import base64
import hashlib
import urllib
import urllib2
try:
	from urllib.parse import parse_qs
except ImportError:
	from urlparse import parse_qs

import fieldmap

class UmTransaction():

	def __init__(self):
		self.key = ''
		self.card = ''
		self.exp = ''
		self.amount = ''
		self.invoice = ''
		self.usesandbox = True
		# defaults
		self.magstripe = ''
		self.command = "sale"
		self.result = "Error"
		self.resultcode = "E"
		self.error = "Transaction not processed yet."
		self.timeout = 45
		self.cardpresent = False
		self.lineitems = []
		self.isrecurring = False
		self.nontaxable = False
		self.checkimage_front = ''
		self.checkimage_back = ''
		self.billsourcekey = False
		self.cardpresent = False
		self.allowpartialauth = False
		self.savecard = False
		self.orderid = ''
		self.cvv2 = ''
		self.cavv = ''
		self.tip = ''
		self.billstate = ''
		self.shipstate  = ''
		self.billphone = ''
		self.tax = ''
		self.subtotal = ''
		self.accounttype = ''
		self.shipcompany = ''
		self.magsupport = ''
		self.custreceiptname = ''
		self.numleft = ''
		self.start = ''
		self.shipfromzip = ''
		self.billcompany = ''
		self.duty = ''
		self.billzip = ''
		self.fax= ''
		self.ponum = ''
		self.zip = ''
		self.dlnum = ''
		self.refnum = ''
		self.discount = ''
		self.shipstreet = ''
		self.xid = ''
		self.inventorylocation = ''
		self.ignoreduplicate = ''
		self.account = ''
		self.street = ''
		self.checknum = ''
		self.epccode = ''
		self.shiplname = ''
		self.billlname = ''
		self.billamount = ''
		self.shipcountry = ''
		self.billfname = ''
		self.custid = ''
		self.termtype = ''
		self.checkformat = ''
		self.ifauthexpired = ''
		self.custreceipt = ''
		self.restaurant_table = ''
		self.pares = ''
		self.cardholder = ''
		self.geolocation = ''
		self.ip = ''
		self.testmode = ''
		self.shipzip = ''
		self.cardauth = ''
		self.micr = ''
		self.session = ''
		self.billstreet = ''
		self.clerk = ''
		self.eci = ''
		self.shipping = ''
		self.contactless = ''
		self.addcustomer = ''
		self.signature = ''
		self.routing = ''
		self.auxonus = ''
		self.digitalgoods = ''
		self.ticketedevent = ''
		self.end = ''
		self.shipphone = ''
		self.reasoncode = ''
		self.shipcity = ''
		self.recurring = ''
		self.dukpt = ''
		self.billcity = ''
		self.currency = ''
		self.dlstate = ''
		self.terminal = ''
		self.authexpiredays = ''
		self.schedule = ''
		self.billstreet2 = ''
		self.website = ''
		self.shipfname = ''
		self.custemail = ''
		self.billtax = ''
		self.comments = ''
		self.billcountry = ''
		self.shipstreet2 = ''
		self.software = ''
		self.origauthcode = ''
		self.email = ''
		self.description = ''
		self.softdescriptor = ''
		self.ssn = ''
		self.lineitems = []
		self.pin = False

	def process(self):
		err = self.check_data()
		if err:
			self.result = "Error"
			self.resultcode = "E"
			self.error = err
			self.errorcode = "10129"
			return False

		map = fieldmap.get_field_map()

		data = {}
		for field in map:
			if map[field] == 'isrecurring':
				if self.isrecurring:
					data['UMisRecurring'] = 'Y'
			elif map[field] == 'nontaxable':
				if self.nontaxable:
					data['UMnontaxable'] = 'Y'
			elif map[field] == 'checkimage_front' or map[field] == 'checkimage_back':
				data[field] = base64.b64encode(getattr(self, map[field]))
			elif map[field] == 'billsourcekey':
				if self.billsourcekey:
					data['UMbillsourcekey'] = 'yes'
			elif map[field] == 'cardpresent':
				if self.cardpresent:
					data['UMcardpresent'] = '1'
			elif map[field] == 'allowpartialauth':
				if self.allowpartialauth:
					data['UMallowPartialAuth'] = 'Yes'
			elif map[field] == 'savecard':
				if self.savecard:
					data['UMsaveCard'] = 'y'
			else:
				data[field] = getattr(self, map[field])

		if 'UMcheckimagefront' in data or 'UMcheckimageback' in data:
			data['UMcheckimageencoding'] = 'base64'

		# tack on custom fields
		for i in range (1, 20):
			if hasattr(self, "custom" + str(i)):
				data["UMcustom"+str(i)] = getattr(self, "custom" + str(i))

		# tack on line level detail
		c = 1
		for lineitem in self.lineitems:

			if 'sku' in lineitem:
				data["UMline" + str(c) + "sku"] = lineitem['sku']
			if 'name' in lineitem:
				data["UMline" + str(c) + "name"] = lineitem['name']
			if 'description' in lineitem:
				data["UMline" + str(c) + "description"] = lineitem['description']
			if 'cost' in lineitem:
				data["UMline" + str(c) + "cost"] = lineitem['cost']
			if 'taxable' in lineitem:
				data["UMline" + str(c) + "taxable"] = lineitem['taxable']
			if 'qty' in lineitem:
				data["UMline" + str(c) + "qty"] = lineitem['qty']
			if 'refnum' in lineitem:
				data["UMline" + str(c) + "prodRefNum"] = lineitem['refnum']
			# optional level 3 	data
			if 'um' in lineitem:
				data["UMline" + str(c) + "um"] = lineitem['um']
			if 'taxrate' in lineitem:
				data["UMline" + str(c) + "taxrate"] = lineitem['taxrate']
			if 'taxamount' in lineitem:
				data["UMline" + str(c) + "taxamount"] = lineitem['taxamount']
			if 'taxclass' in lineitem:
				data["UMline" + str(c) + "taxclass"] = lineitem['taxclass']
			if 'commoditycode' in lineitem:
				data["UMline" + str(c) + "commoditycode"] = lineitem['commoditycode']
			if 'discountrate' in lineitem:
				data["UMline" + str(c) + "discountrate"] = lineitem['discountrate']
			if 'discountamount' in lineitem:
				data["UMline" + str(c) + "discountamount"] = lineitem['discountamount']

			c +=1

		# Create hash if pin has been set.
		if self.pin:
			# generate random seed value
			seed = str(int(time.time()* random.random()))

			# assemble prehash data
			prehash = self.command + ":" + trim(self.pin) + ":" + self.amount + ":" + self.invoice + ":" + seed

			# create sha1 hash
			sha_1 = hashlib.sha1()
			hash = 's/' + seed + '/' + sha_1.update(prehash).hexdigest() + '/n'

			# populate hash value
			data['UMhash'] = hash

		# Tell the gateway what the client side timeout is
		if self.timeout > 0:
			data['UMtimeout'] = int(self.timeout)

		# Figure out URL
		url =  "https://www.usaepay.com/gate"
		if hasattr(self, "gatewayurl"):
			url = self.gatewayurl
		if self.usesandbox:
			url = "https://sandbox.usaepay.com/gate"

		# Post data to Gateway
		result=self.http_post(url, data)
		if result is False:
			return false

		parsed_res = parse_qs(result)
		#check to make sure we received the	correct fields

		if not "UMversion" in parsed_res or not "UMstatus" in parsed_res:
			self.result = "Error"
			self.resultcode = "E"
			self.error = "Error parsing data from card processing gateway."
			self.errorcode = "10132"
			return False

		# store results
		self.result = parsed_res["UMstatus"][0] if "UMstatus" in parsed_res else "Error"
		self.resultcode = parsed_res["UMresult"][0] if "UMresult" in parsed_res else "E"
		self.authcode = parsed_res["UMauthCode"][0] if "UMauthCode" in parsed_res else ""
		self.refnum = parsed_res["UMrefNum"][0] if "UMrefNum" in parsed_res else ""
		self.batch = parsed_res["UMbatch"][0] if "UMbatch" in parsed_res else ""
		self.avs_result = parsed_res["UMavsResult"][0] if "UMavsResult" in parsed_res else ""
		self.avs_result_code = parsed_res["UMavsResultCode"][0] if "UMavsResultCode" in parsed_res else ""
		self.cvv2_result = parsed_res["UMcvv2Result"][0] if "UMcvv2Result" in parsed_res else ""
		self.cvv2_result_code = parsed_res["UMcvv2ResultCode"][0] if "UMcvv2ResultCode" in parsed_res else ""
		self.vpas_result_code = parsed_res["UMvpasResultCode"][0] if "UMvpasResultCode" in parsed_res else ""
		self.convertedamount = parsed_res["UMconvertedAmount"][0] if "UMconvertedAmount" in parsed_res else ""
		self.convertedamountcurrency = parsed_res["UMconvertedAmountCurrency"][0] if "UMconvertedAmountCurrency" in parsed_res else ""
		self.conversionrate = parsed_res["UMconversionRate"][0] if "UMconversionRate" in parsed_res else ""
		self.error = parsed_res["UMerror"][0] if "UMerror" in parsed_res else ""
		self.errorcode = parsed_res["UMerrorcode"][0] if "UMerrorcode" in parsed_res else ""
		self.custnum = parsed_res["UMcustnum"][0] if "UMcustnum" in parsed_res else ""
		self.authamount = parsed_res["UMauthAmount"][0] if "UMauthAmount" in parsed_res else ""
		self.balance = parsed_res["UMremainingBalance"][0] if "UMremainingBalance" in parsed_res else ""
		self.cardlevelresult = parsed_res["UMcardLevelResult"][0] if "UMcardLevelResult" in parsed_res else ""
		self.procrefnum = parsed_res["UMprocRefNum"][0] if "UMprocRefNum" in parsed_res else ""
		self.profiler_score = parsed_res["UMprofilerScore"][0] if "UMprofilerScore" in parsed_res else ""
		self.profiler_response = parsed_res["UMprofilerResponse"][0] if "UMprofilerResponse" in parsed_res else ""
		self.profiler_reason = parsed_res["UMprofilerReason"][0] if "UMprofilerReason" in parsed_res else ""
		self.cardref = parsed_res["UMcardRef"][0] if "UMcardRef" in parsed_res else ""
		self.isduplicate = parsed_res["UMisDuplicate"][0] if "UMisDuplicate" in parsed_res else ""

		if "UMcctransid" in parsed_res:
			self.cctransid = parsed_res["UMcctransid"][0]
		if "UMacsurl" in parsed_res:
			self.cctransid = parsed_res["UMacsurl"][0]
		if "UMpayload" in parsed_res:
			self.cctransid = parsed_res["UMpayload"][0]

		if self.resultcode == "A":
			return True
		return False


	def check_data(self):
		if not self.key:
			return "Source Key is required"

		if self.command.lower() in ["cc:capture", "cc:refund", "refund", "check:refund","capture", "creditvoid", 'quicksale', 'quickcredit','refund:adjust','void:release', 'check:void','void']:
			if not self.refnum:
				return "Reference Number is required"
		elif self.command.lower() in ["svp"]:
			if not self.svpbank:
				return "Bank ID is required"
			if  not self.svpreturnurl:
				return "Return URL is required"
			if not self.svpcancelurl:
				return "Cancel URL is required"
		else:
			if self.command.lower() in ["check:sale","check:credit", "check", "checkcredit","reverseach"]:
				if not self.account:
					return "Account Number is required"
				if not self.routing:
					return "Routing Number is required"
			elif self.command.lower() in ["cash", "cash:refund", "cash:sale", "external:check:sale", "external:cc:sale", "external:gift:sale"]:
				# nothing needs to be validated for cash
				pass
			else:
				if not self.magstripe and not re.match('~^enc://~', self.card):
					if not self.card:
						return "Credit Card Number is required"
					if not self.exp:
						return "Expiration Date is required"
			if self.command != "cc:save":
				self.amount = re.sub("/[^0-9\.]/", "", self.amount)
				if not self.amount:
					return "Amount is required"
				if not self.invoice and not self.orderid:
					return "Invoice number or Order ID is required"
		return None


	def http_post(self, url, data):

		postdata = urllib.urlencode(data)

		try:
			content = urllib2.urlopen(url=url, data=postdata).read()
			error = ''
		except urllib2.HTTPError, e:
			error = 'HTTPError = ' + str(e.code)
		except urllib2.URLError, e:
			error = 'URLError = ' + str(e.reason)
		except httplib.HTTPException, e:
			error = 'HTTPException'
		except Exception:
			import traceback
			error = 'generic exception: ' + traceback.format_exc()

		# check for a blank response
		if len(content) == 0:
			self.result = "Error"
			self.resultcode = "E"
			self.error = "Error reading from card processing gateway."
			self.errorcode = "10132"
			self.blank = 1
			return False

		return content