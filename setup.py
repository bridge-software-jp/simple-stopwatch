# -*- coding: UTF-8 -*-

from distutils.core import setup
import py2exe

setup(
    windows = [{
		"script" : "Simple Stopwatch.pyw",
  		"name" : u"ストップウォッチ",
		"icon_resources" : [(1,"clock.ico")],
    		"version" : "1.0.2",
    		}],
    zipfile = "lib/library.zip")
