#!/usr/bin/python
# -*- coding: utf-8 -*-

import color
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-v', action = 'store_false', dest = 'verbose', help = 'Enable verbose mode')
parser.add_argument('URL', nargs = 1)
results = parser.parse_args()
verbose = results.verbose
uRl = results.URL
uRl = ''.join(uRl)
uRl = str(uRl)
print """
_   __                          
| | / /                          
| |/ /  ___  _ __ _____   ____ _ 
|    \ / _ \| '__/ _ \ \ / / _` |
| |\  \ (_) | | | (_) \ V / (_| |
\_| \_/\___/|_|  \___/ \_/ \__,_|
                                 
"""
def separator():
    print '#' + '-' * 160 + '#'
programming_languages = ["AsciiDoc","C++","CFML","Dart","Elm","Erlang","Haskell","Java","Lua","node.js","PHP","Python","Ruby","Scala"]
separator()
print color.HEADER + 'Site selected: ' + uRl + color.WHITE
separator()
if verbose == False:
    verbose = False
else:
    verbose = True
cms = None

try:
    import sys
    import socket
    import requests
    import urllib2
    from Wappalyzer import Wappalyzer, WebPage
except ImportError:
    separator()
    print color.FAIL + 'Error while importing main libraries!' + color.DEFAULT
    print color.HEADER + 'Install from pip:  sudo pip install socket, python-Wappalyzer' + color.DEFAULT
    separator()

if len(sys.argv) == 1:
    print color.WARNING + 'Usage: ' + sys.argv[0] + ' <site>' + color.DEFAULT
elif uRl.startswith('http://'):
    uRl = uRl.replace('http://', '')
elif uRl.startswith('https://'):
    uRl = uRl.replace('https://', '')

def check_wordpress(url):
    
    try:
        code = requests.get('http://' + uRl + '/wp-login.php').status_code
    except urllib2.HTTPError:
        return None

    if code == 200:
        return 'Wordpress'
    result = None


def check_drupal(url):
    
    try:
        code = requests.get('http://' + uRl + '/user/login').status_code
    except urllib2.HTTPError:
        return None

    if code == 200:
        return 'Drupal'
    result = None


def check_joomla(url):
    
    try:
        code = requests.get('http://' + uRl + '/index.php?option=com_users&view=login')
    except urllib2.HTTPError:
        return None

    if code == 200:
        return 'Joomla'
    result = None


try:
    check_if_up = socket.gethostbyname(uRl)
    if check_if_up:
        print color.OKGREEN + 'Host ' + uRl + ' is up!' + color.WHITE
        separator()
        url = requests.get('http://' + uRl)
        out = url
        json = out.headers
        json = dict(json)
        server = json.get('server')
        if server == None:
            server = json.get('Server')
        else:
            server = json.get('server')
        if verbose == False:
            print color.HEADER + 'Headers:\n'
            print color.CYAN
            print json
            print color.WHITE
        
        wappalyzer = Wappalyzer.latest()
        webpage = WebPage.new_from_url('http://' + uRl)
        webpage = list(wappalyzer.analyze(webpage))
        language = json.get("x-powered-by")
        if language == None:
            language = ",".join(set(webpage) & set(programming_languages))

        if not webpage:
            print color.WARNING + 'No softwares found!' + color.DEFAULT
        else:
            separator()
            webpage = color.OKBLUE + 'Software used on ' + color.WHITE + color.HEADER + uRl + color.WHITE + ':\n' + '\n'.join(webpage)
            print color.OKBLUE + webpage + color.WHITE
            
            try:
                if check_wordpress('http://' + uRl):
                    cms = 'Wordpress'
                    cms_more = '%s is a Wordpress website!' % uRl
                    print color.OKGREEN + cms_more + color.WHITE
                else:
                    print (color.FAIL + '%s is not a Wordpress site!' + color.WHITE) % uRl
                if check_drupal('http://' + uRl):
                    cms = 'Drupal'
                    cms_more = '%s is a Drupal website!' % uRl
                    print color.OKGREEN + cms_more + color.WHITE
                else:
                    print (color.FAIL + '%s is not a Drupal site!' + color.WHITE) % uRl
                if check_joomla('http://' + uRl):
                    cms = 'Joomla'
                    cms_more = '%s is a Joomla website!' % uRl
                    print color.OKGREEN + cms_more + color.WHITE
                else:
                    print (color.FAIL + '%s is not a Joomla site!' + color.WHITE) % uRl
            except urllib2.HTTPError:
                print ' ' + uRl + ' login page does not exist or is forbidden' + color.DEFAULT

            print '\nWebServer: %s\nLanguage: %s\nCMS: %s' % (server, language, cms)
except socket.gaierror:
    socket.herror = None
    print color.FAIL + 'Host ' + uRl + " is down or doesn't exist!" + color.DEFAULT