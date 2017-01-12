# -*- coding: utf-8 -*-
from setuptools import setup

setup(
	name='avahi-cname-aliases',
	version='1.0',
	description='Program for managing avahi aliases (systemd)',
	url='https://github.com/Dalee/avahi-cname-aliases',
	author='Dalee Dev Team',
	author_email='hello@dalee.ru',
	license='MIT',
	keywords='avahi cname alias systemd',
	packages=['avahi_cname_aliases'],
	scripts=['bin/avahi-cname-aliases'],
	zip_safe=False
)
