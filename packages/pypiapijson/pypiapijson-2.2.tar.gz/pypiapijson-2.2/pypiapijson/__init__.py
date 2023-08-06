from . import asyncs
from types import Optional
"""Hello! If you are seeing this. Welcome to built in help!"""

class CannotFindPackage(Exception):
	"""Exception for things"""
	pass
	
class CannotFindPackagewithVersionProvided(Exception):
	"""Also exception for understandable reason"""
	pass
class ErrorToGetStatus(Exception):
	"""For Somehow Can't Get Stats"""
	pass
try:
	import urllib.request
	print("You are using Python 3.x that\'s great!")
except ModuleNotFoundError or ImportError:
	import sys
	sys.exit("You using python 2 and this module is not supported")
import json
"""I want most of functions are not async that you need await for god damn reason"""
def get(name):
	"""Get the information about package with that name provided if that was not exist or pypi api down then say error"""
	try:
		re = urllib.request.Request(f"https://pypi.org/pypi/{name}/json")
		s = urllib.request.urlopen(re)
		r = s.read()
	except Exception:
		raise CannotFindPackage("Error occured!\nI can\'t get the package info check your connection if you check it was all right, pypi api may gone maintenance.")
	if s.getcode() != 200:
		raise CannotFindPackage("Error occured!\nI can\'t get the package info maybe check your typo or check your connection if you check it was all right, pypi api may gone maintenance.")
	else:
		return json.loads(r.decode("utf-8"))
def getbyv(name,ver:Optional[str,int]):
	"""Get the information about package with that name provided if that was not exist or pypi api down then say error"""
	try:
		re = urllib.request.Request(f"https://pypi.org/pypi/{name}/{ver}/json")
		s = urllib.request.urlopen(re)
		r = s.read()
	except Exception:
		raise CannotFindPackagewithVersionProvided("Error occured!\nI can\'t get the package info with provided version maybe check your typo or check your connection if you check it was all right, pypi api may gone maintenance.")
	if s.getcode() != 200:
		raise CannotFindPackagewithVersionProvided("Error occured!\nI can\'t get the package info with provided version maybe check your typo or check your connection if you check it was all right, pypi api may gone maintenance.")
	else:
		return json.loads(r.decode("utf-8"))

def status():
	r = urllib.request.Request("https://pypi.org/stats")
	r.add_header("Accept","application/json")
	r.add_header("Content-type","application/json")
	try:
		content = urllib.request.urlopen(r).read()
	except:
		raise ErrorToGetStatus("I could not get stats")
	return json.loads(content.decode("utf-8"))
def helpme():
	print("Hello!\nUsage:\nget(packagename : string)\nGet information the paclage name that you provided and get the information in lastest version if there\'s no package it\'ll return none and raise error\ngetbyv(packagename : string,version : float or string) Do everything like get but you\'ll need to specify version the package have if there\'s wrong return None and raise error\nstatus()This will retrieve what package take most space and this fucntion is asynchronous function so run it with asyncio or await it.")
global listfunc
listfunc = ["get","getbyv","status"]
print("Hello! Want to get help what available function? execute helpme()\n:D")
