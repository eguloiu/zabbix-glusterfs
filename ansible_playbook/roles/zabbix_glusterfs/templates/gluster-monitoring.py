#!/usr/bin/env python

__author__   = "Eduard Dragan"
__email__    = "eduard.guloiu@gmail.com"
__license__  = "GPL"
__version__  = "1.13"
_status__    = "Production"

import json
import subprocess
import sys
import re
import time
from xml.dom import minidom
import xmltodict
# https://docs.gluster.org/en/v3/Administrator%20Guide/Geo%20Replication/#status
# Plugin is written for a SINGLE volume - XML output may change for multiple volumes but nowhere to test

def get_gluster( gluster_command, printxml=False ):
  for i in range(1,3):
    command_output = subprocess.check_output('/usr/bin/sudo /usr/sbin/gluster ' + gluster_command + ' --xml', shell=True)
    xml = minidom.parseString( command_output )
    data = xmltodict.parse( xml.toxml() )
    if data['cliOutput']['opRet'] == '0':
      break
    time.sleep(3)

  if printxml==True:
    return xml.toxml()
  else:
    return data
    #return json.dumps( {"data":replication_status} )

def get_volumes():
  data = get_gluster( 'volume list' )
  volumes = data['cliOutput']['volList']['volume']
  result = []
  for i in volumes:
    element = {}
    element['{#NAME}'] = i
    result.append( element )
  return json.dumps( {"data": result} )

def get_volume_info(volume):
  data = get_gluster( 'volume info ' + volume, True )
  return data

def get_volume_status(volume):
  data = get_gluster( 'volume status ' + volume + ' detail', True )
  return data

def get_peers():
  data = get_gluster( 'pool list' )
  peers = data['cliOutput']['peerStatus']['peer']
  result = []
  for i in peers:
    element = {}
    element['{#UUID}'] = i['uuid']
    element['{#HOSTNAME}'] = i['hostname']
    if i['connected'] == '1':
      element['{#STATE}'] = 'Connected'
    else:
      element['{#STATE}'] = 'Disconnected'
    result.append( element )
  return json.dumps( {"data": result} )

def get_peers_status():
  data = get_gluster('peer status',True)
  return data

def get_georep_discovery():
  data = get_gluster('volume geo-replication status')
  volume = data['cliOutput']['geoRep']['volume']['name']
  replication_sessions = data['cliOutput']['geoRep']['volume']['sessions']['session']['pair']
  result = []
  for i in replication_sessions:
    element = {}
    element['{#MASTERUUID}'] = i['master_node_uuid']
    element['{#MASTERHOSTNAME}'] = i['master_node']
    result.append( element )
  return json.dumps( {"data": result} )

def get_georep():
  data = get_gluster('volume geo-replication status', True)
  return data

def get_heal_entries( volume ):
  entries_to_heal = 0
  command_output = subprocess.check_output('/usr/bin/sudo /usr/sbin/gluster volume heal ' + volume + ' statistics heal-count', shell=True)
  for i in command_output.split('\n'):
    if re.search("Number of entries:.*",i):
      tmp = int( i.split(':')[1].strip() )
      entries_to_heal += tmp
  return entries_to_heal

if ( len(sys.argv)==1 ):
  print( 'Please provide at least one argument' )

if ( len(sys.argv)>=2 ):
  if sys.argv[1]=='georep-status-xml':
    print( get_georep() )
  elif sys.argv[1]=='discovery':
    print( get_volumes() )
  elif sys.argv[1]=='peers-discovery':
    print( get_peers() )
  elif sys.argv[1]=='peers-status':
    print( get_peers_status() )
  elif sys.argv[1]=='info' and sys.argv[2]!=None:
    print( get_volume_info(sys.argv[2]) )
  elif sys.argv[1]=='status' and sys.argv[2]!=None:
    print( get_volume_status(sys.argv[2]) )
  elif sys.argv[1]=='georep-discovery':
    print( get_georep_discovery() )
  elif sys.argv[1]=='healentries' and sys.argv[2]!=None:
    print( get_heal_entries(sys.argv[2]) )
  else:
   print( 'end' )

