#!/usr/bin/python

# Copyright: (c) 2020, Mark Ciecior <mciecior@carrieraccessit.com>
# GNU General Public License v3.0+

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: duo_admin_settings

short_description: Create a Duo account within an MSP portal.

version_added: "2.9"

description:
    - This is used to add/change the settings of Duo accounts

options:
    app_name:
        description:
            - The name of the integration to create
        type: str
        required: true
    type:
        description:
            - The type of the integration to create. Refer to Retrieve Integrations for a list of valid values. Note that integrations of type "azure-ca" may not be created via the API.
        type: str
        required: true
    self_service_allowed:
        description:
            - Set to 1 to grant an integration permission to allow users to manage their own devices. This is only supported by integrations which allow for self service configuration.
        type: bool
        required: false
        default: false

author:
    - Mark Ciecior (mciecior@carrieraccessit.com)
'''

EXAMPLES = '''
# Create a new integration
- name: Create integration
  duo_admin_integrations:
    ikey: ABCDEFGH
    skey: ABCDEFGH12345678
    host: api-123XYZ.duosecurity.com
    app_name: New App
    type: websdk
    state: present

# Update the name of a child account's integration
- name: Update app name
  duo_admin_integrations:
    ikey: ABCDEFGH
    skey: ABCDEFGH12345678
    host: api-123XYZ.duosecurity.com
    name: Awesome Test Account
    state: present
    app_ikey: ABC123456DEF
    app_name: New App Name

# Retrieve the integrations of a child account
  duo_admin_integrations:
    ikey: ABCDEFGH
    skey: ABCDEFGH12345678
    host: api-123XYZ.duosecurity.com
    name: Awesome Test Account
    state: query
'''

RETURN = '''
integrationList:
    description: list of integrations
    type: list

ikey:
    description: integration key of the integration
    type: str

skey:
    description: secret key of the integration
    type: str
'''

import duo_client
from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        ikey=dict(type='str', required=True),
        skey=dict(type='str', required=True, no_log=True),
        host=dict(type='str', required=True),
        name=dict(type='str', required=False),
        state=dict(type='str', required=True),
        app_name=dict(type='str', required=False),
        app_ikey=dict(type='str', required=False),
        app_type=dict(type='str', required=False),
        self_service_allowed=dict(type=bool, required=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        settings={}
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    ikey = module.params.get('ikey')
    skey = module.params.get('skey')
    host = module.params.get('host')
    name = module.params.get('name')
    state = module.params.get('state')
    app_name = module.params.get('app_name')
    app_ikey = module.params.get('app_ikey')
    app_type = module.params.get('app_type')
    self_service_allowed = module.params.get('self_service_allowed')
    newSettings = {}
    if app_name is not None:
        newSettings['name'] = app_name
    if app_type is not None:
        newSettings['integration_type'] = app_type
    if self_service_allowed is not None:
        newSettings['self_service_allowed'] = '1' if self_service_allowed else '0'
    admin_api = duo_client.Admin(
        ikey=ikey,
        skey=skey,
        host=host,
        )

    '''
    If name is specified, update the API object to reference the child account ID
    '''
    if name:
        accounts_api = duo_client.Accounts(
          ikey=ikey,
          skey=skey,
          host=host,
          )
        accountList = accounts_api.get_child_accounts()
        for account in accountList:
            if account['name'] == name:
                admin_api.account_id = account['account_id']
                break
        if not admin_api.account_id:
            module.fail_json(msg='Could not find child account {}'.format(name), **result)

    '''
    If app_ikey is specified, find the settings for the specific integration
    '''
    if app_ikey:
        currentSettings = {}
        try:
            currentSettings = admin_api.get_integration(app_ikey)
        except Exception as e:
            module.fail_json(msg='Could not retrieve current integration: {}'.format(str(e)), **result)
        if state == 'query':
            result['changed'] = False
            try:
                for k, v in currentSettings.items():
                    result['settings'][k] = v
                module.exit_json(**result)
            except Exception as e:
                module.fail_json(msg=str(e), **result)

        if state == 'present':
            result['changed'] = False
            for k, v in newSettings.items():
                if newSettings[k] and (newSettings[k] != currentSettings[k]):
                    result['changed'] = True
                    break
            if result['changed'] is False:
                module.exit_json(**result)
            else:
                for k, v in newSettings.items():
                    if newSettings[k]:
                        result['settings'][k] = v
                if not module.check_mode:
                    try:
                        admin_api.update_integration(app_ikey, **newSettings)
                    except Exception as e:
                        result['changed'] = False
                        module.fail_json(msg=str(e), **result)

        module.exit_json(**result)

    elif not app_ikey:
        try:
            integrationList = admin_api.get_integrations()
        except Exception as e:
            module.fail_json(msg='Cound not retrieve list of integrations: {}'.format(str(e)), **result)
        if state == 'query':
            result['integrationList'] = integrationList
            module.exit_json(**result)
        elif state == 'present':
            for i in integrationList:
                if i['name'] == app_name:
                    result['changed'] = False
                    result['ikey'] = i['ikey']
                    result['skey'] = i['skey']
                    module.exit_json(**result)
            result['changed'] = True
            if module.check_mode:
                module.exit_json(**result)
            else:
                try:
                    newIntegration = admin_api.create_integration(
                      **newSettings
                    )
                except Exception as e:
                    result['changed'] = False
                    module.fail_json(msg='Could not create integration: {}'.format(str(e)), **result)
            result['ikey'] = newIntegration['integration_key']
            result['skey'] = newIntegration['secret_key']
            module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
