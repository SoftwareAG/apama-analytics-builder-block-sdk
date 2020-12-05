#!/usr/bin/env python3

# $Copyright (c) 2019 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or its subsidiaries and/or its affiliates and/or their licensors.$
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG
import os, urllib, buildExtension

def add_arguments(parser):
    """ Add parser arguments. """
    #these are optional arguments, requires at least one of them to perform upload or delete
    remote = parser.add_argument_group(
        'upload or delete (requires at least the following arguments: --cumulocity_url, --username, --password, (--input or --name))')
    remote.add_argument('--cumulocity_url', metavar='URL', help='the base Cumulocity URL')
    remote.add_argument('--username',
                        help='the Cumulocity tenant identifier and the username in the <tenantId>/<username> format')
    remote.add_argument('--password', help='the Cumulocity password')

def run(args):
    # Support remote operations and whether they are mandatory.
    remote = {'cumulocity_url': True, 'username': True, 'password': True}

    # checks if all manadatory remote options are provided
    buildExtension.isAllRemoteOptions(args,remote)
    connection = buildExtension.C8yConnection( args.cumulocity_url, args.username,args.password)
    try:
        extension_mos = connection.do_get('/inventory/managedObjects', {'fragmentType': "pas_extension", "pageSize": 2000})
        for mo in extension_mos['managedObjects']: 
            print(mo['pas_extension'])
    except urllib.error.HTTPError as err:
        if err.code == 404:
	        raise Exception(
		        f'Failed to perform REST request for resource /inventory/managedObjects on url {connection.base_url}. Verify that the base Cumulocity URL is correct.')
        raise err

