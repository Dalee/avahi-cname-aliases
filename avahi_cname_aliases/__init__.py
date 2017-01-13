# -*- coding: utf-8 -*-

import time
import os
import os.path
import sys
import avahi
import dbus
import signal
import logging
from encodings.idna import ToASCII

CLASS_IN = 0x01
TYPE_CNAME = 0x05
TTL = 60

class Aliases:

	def __init__(self):
		self.running = True
		self.server = None
		self.group = None
		self.cname_dir = os.path.join("/etc", "avahi", "aliases.d")
		self.cname_list = []


	# set logging and signal handlers
	def set_handlers(self):
		logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
		signal.signal(signal.SIGINT, self.stop)
		signal.signal(signal.SIGTERM, self.stop)


	# load aliases list from /etc/avahi-aliases.d/ directory and
	# make simple validation
	def load_aliases(self):
		if os.path.exists(self.cname_dir) == False:
			return

		for list_name in os.listdir(self.cname_dir):
			file_name = os.path.join(self.cname_dir, list_name)
			fp = open(file_name, 'r')

			for cname_line in fp:
				if cname_line.startswith('#') == True:
					continue

				cname_line = cname_line.strip("\n")
				if cname_line == "":
					continue

				if cname_line.endswith('.local') == False:
					continue

				self.cname_list.append(cname_line)
			fp.close()


	# publish all aliases to avahi daemon
	def publish_aliases(self):
		if len(self.cname_list) == 0:
			return

		bus = dbus.SystemBus()
		bus_server = bus.get_object(avahi.DBUS_NAME, avahi.DBUS_PATH_SERVER)
		bus_group = bus.get_object(avahi.DBUS_NAME, bus_server.EntryGroupNew())

		self.server = dbus.Interface(bus_server, avahi.DBUS_INTERFACE_SERVER)
		self.group = dbus.Interface(bus_group, avahi.DBUS_INTERFACE_ENTRY_GROUP)

		for cname in self.cname_list:
			self.publish_cname(cname)
			logging.debug("CNAME: %s - published" % (cname,))

		self.group.Commit()

	# run and stay foreground
	def run(self):
		self.set_handlers()
		self.load_aliases()
		self.publish_aliases()

		# keep aliases published
		while self.running:
			time.sleep(TTL)

	# signale handler
	def stop(self, signum, frame):
		self.running = False

	# https://gist.github.com/gdamjan/3168336#file-avahi-alias-py-L29
	def publish_cname(self, cname):
		cname = self.encode_cname(cname)
		rdata = self.encode_rdata(self.server.GetHostNameFqdn())
		rdata = avahi.string_to_byte_array(rdata)
		self.group.AddRecord(
			avahi.IF_UNSPEC, avahi.PROTO_UNSPEC, dbus.UInt32(0),
			cname, CLASS_IN, TYPE_CNAME, TTL, rdata
		)

	# https://gist.github.com/gdamjan/3168336#file-avahi-alias-py-L47
	def encode_cname(self, name):
		return '.'.join( ToASCII(p) for p in name.split('.') if p )

	# https://gist.github.com/gdamjan/3168336#file-avahi-alias-py-L50
	def encode_rdata(self, name):
		def enc(part):
			a = ToASCII(part)
			return chr(len(a)), a

		return ''.join( '%s%s' % enc(p) for p in name.split('.') if p ) + '\0'

