#! /usr/bin/env python

import wakeonlan
from samsungtvws import SamsungTVWS

class TV:
	def __init__(self, ip, port, token, mac, name):
		self.ip = ip
		self.port = port
		self.token = token
		self.mac = mac
		self.name = name

		self.tv = SamsungTVWS(host=self.ip,
			port=self.port,
			token=self.token,
			timeout=10,
			name=self.name)

	def power_on(self):
		wakeonlan.send_magic_packet(self.mac, ip_address=self.ip)

	def power_off(self):
		self.tv.open()
		self.tv.shortcuts().power()
		self.tv.close()
