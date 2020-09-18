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
module: duo_account

short_description: Create a Duo account within an MSP portal.

version_added: "2.9"

description:
    - "This is used by MSPs to create child accounts within their portals"

options:
    ikey:
        description:
            - Integration Key for the Duo Accounts API applications
        type: str
        required: true
    skey:
        description:
            - Secret Key for the Duo Accounts API applications
        type: str
        required: true
    host:
        description:
            - API Host for the Duo Accounts API applications
        type: str
        required: true
    name:
        description:
            - Name of the new child account to be created
        type: str
        required: true
    state:
        description:
            - Whether this child account should exist or not
        type: str
        required: true

author:
    - Mark Ciecior (mciecior@carrieraccessit.com)
'''

EXAMPLES = '''
# Create a child account
- name: Create child account
  duo_account:
    ikey: ABCDEFGH
    skey: ABCDEFGH12345678
    host: api-123XYZ.duosecurity.com
    name: Awesome Test Account
    state: present

# Remove a child account
- name: Remove child account
  duo_account:
    ikey: ABCDEFGH
    skey: ABCDEFGH12345678
    host: api-123XYZ.duosecurity.com
    name: Awesome Test Account
    state: absent

'''

RETURN = '''
account_id:
    description: The Duo-assigned account_id variable
    type: str
    returned: always

api_hostname:
    description: The Duo-assigned API hostname
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
        name=dict(type='str', required=True),
        state=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        account_id=''
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
    accounts_api = duo_client.Accounts(
        ikey=ikey,
        skey=skey,
        host=host,
        )
    if state == 'present':
        result['changed'] = False
        accountList = accounts_api.get_child_accounts()
        for account in accountList:
            if account['name'] == name:
                result['changed'] = False
                result['account_id'] = account['account_id']
                result['api_hostname'] = account['api_hostname']
                module.exit_json(**result)
        if not module.check_mode:
            try:
                resp = accounts_api.create_account(name)
                result['account_id'] = resp['account_id']
                result['api_hostname'] = resp['api_hostname']
            except Exception as e:
                module.fail_json(msg=str(e), **result)
        result['changed'] = True
        module.exit_json(**result)

    if state == 'absent':
        result['changed'] = False
        accountList = accounts_api.get_child_accounts()
        for account in accountList:
            if account['name'] == name:
                result['account_id'] = account['account_id']
                if not module.check_mode:
                    try:
                        accounts_api.delete_account(account['account_id'])
                    except Exception as e:
                        module.fail_json(msg=str(e), **result)
                result['changed'] = True
                module.exit_json(**result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
