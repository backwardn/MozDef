# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright (c) 2017 Mozilla Corporation

import json
from mozdef_util.utilities.key_exists import key_exists


class message(object):
    def __init__(self):
        '''
            Plugin used to fix object type discretions with cloudtrail messages
        '''
        self.registration = ['cloudtrail']
        self.priority = 10

        # Just add new entry to this dict to
        # automatically convert key mappings
        # which are mixed string and dict
        # into a dict with a raw_value key as the string value
        self.modify_keys = [
            'details.additionaleventdata',
            'details.apiversion',
            'details.serviceeventdetails',
            'details.requestparameters.attribute',
            'details.requestparameters.bucketpolicy.statement.principal.service',
            'details.requestparameters.bucketpolicy.statement.principal.aws',
            'details.requestparameters.callerreference',
            'details.requestparameters.description',
            'details.requestparameters.describecapacityreservationsrequest',
            'details.requestparameters.describecoippoolsrequest',
            'details.requestparameters.describeegressonlyinternetgatewaysrequest',
            'details.requestparameters.describefastsnapshotrestoresrequest',
            'details.requestparameters.describeflowlogsrequest',
            'details.requestparameters.describeflowlogsrequest.filter.value',
            'details.requestparameters.describehostsrequest',
            'details.requestparameters.describeinstancetypeofferingsrequest',
            'details.requestparameters.describeinstancetypesrequest',
            'details.requestparameters.describeipv6poolsrequest',
            'details.requestparameters.describenatgatewaysrequest',
            'details.requestparameters.describepublicipv4poolsrequest',
            'details.requestparameters.describescheduledinstancesrequest',
            'details.requestparameters.describespotfleetrequestsrequest',
            'details.requestparameters.describevpcendpointconnectionnotificationsrequest',
            'details.requestparameters.describevpcendpointsrequest',
            'details.requestparameters.describevpcendpointsrequest.filter',
            'details.requestparameters.describevpcendpointsrequest.filter.value',
            'details.requestparameters.describevpcendpointsrequest.vpcendpointid',
            'details.requestparameters.describevpcendpointserviceconfigurationsrequest',
            'details.requestparameters.describevpcendpointservicesrequest',
            'details.requestparameters.disableapitermination',
            'details.requestparameters.distributionconfig.callerreference',
            'details.requestparameters.domainname',
            'details.requestparameters.domainnames',
            'details.requestparameters.ebsoptimized',
            'details.requestparameters.filter',
            'details.requestparameters.groupdescription',
            'details.requestparameters.iaminstanceprofile',
            'details.requestparameters.invalidationbatch.callerreference',
            'details.requestparameters.imageid',
            'details.requestparameters.instancetype',
            'details.requestparameters.logging',
            'details.requestparameters.logstreamname',
            'details.requestparameters.metrics',
            'details.requestparameters.notification',
            'details.requestparameters.notificationconfiguration',
            'details.requestparameters.rule',
            'details.requestparameters.schema',
            'details.requestparameters.sort',
            'details.requestparameters.source',
            'details.requestparameters.tagging',
            'details.requestparameters.vpc',
            'details.responseelements.availabilityzones',
            'details.responseelements.createddate',
            'details.responseelements.creationdate',
            'details.responseelements.creationtime',
            'details.responseelements.credentials',
            'details.responseelements.dbsubnetgroup',
            'details.responseelements.distribution.distributionconfig.callerreference',
            'details.responseelements.endpoint',
            'details.responseelements.findings.service.additionalinfo.unusual',
            'details.responseelements.invalidation.invalidationbatch.callerreference',
            'details.responseelements.lastmodified',
            'details.responseelements.lastmodifieddate',
            'details.responseelements.policy',
            'details.responseelements.responseparameters.method.response.header.access-control-allow-headers',
            'details.responseelements.responseparameters.method.response.header.access-control-allow-methods',
            'details.responseelements.responseparameters.method.response.header.access-control-allow-origin',
            'details.responseelements.role',
            'details.responseelements.securitygroups',
            'details.responseelements.state',
            'details.responseelements.subnets',
        ]

    def convert_key_raw_str(self, needle, haystack):
        num_levels = needle.split(".")
        if len(num_levels) == 0:
            return False
        current_pointer = haystack
        for updated_key in num_levels:
            if updated_key == num_levels[-1]:
                current_pointer[updated_key] = {
                    'raw_value': json.dumps(current_pointer[updated_key])
                }
                return haystack
            if updated_key in current_pointer:
                current_pointer = current_pointer[updated_key]
            else:
                return haystack

    def onMessage(self, message, metadata):
        if 'source' not in message:
            return (message, metadata)

        if not message['source'] == 'cloudtrail':
            return (message, metadata)

        for modified_key in self.modify_keys:
            if key_exists(modified_key, message):
                message = self.convert_key_raw_str(modified_key, message)

        return (message, metadata)
