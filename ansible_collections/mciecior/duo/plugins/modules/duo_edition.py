#!/usr/bin/python

# Copyright: (c) 2021, Mark Ciecior <mciecior@carrieraccessit.com>
# GNU General Public License v3.0+

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: duo_edition

short_description: Get or set a Duo account edition within an MSP portal.

version_added: "2.9"

description:
    - "This is used by MSPs to get/set child account editions"

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
    account_id:
        description:
            - Duo-provided ID of the child account
        type: str
        required: true
    edition:
        description:
            - Billing edition of this child account
            - One of: ['ENTERPRISE', 'PLATFORM', or 'BEYOND']
            - These correspond to Duo MFA, Duo Access, and Duo Beyond, respectively
        type: str
        required: false

author:
    - Mark Ciecior (mciecior@carrieraccessit.com)
'''

EXAMPLES = '''
# Get a child account's edition
- name: Get child account edition
  duo_edition:
    ikey: ABCDEFGH
    skey: ABCDEFGH12345678
    host: api-123XYZ.duosecurity.com
    account_id: DAABCDEFGH12345678

# Set a child account's edition
- name: Set child account edition
  duo_edition:
    ikey: ABCDEFGH
    skey: ABCDEFGH12345678
    host: api-123XYZ.duosecurity.com
    account_id: DAABCDEFGH12345678
    edition: BEYOND

'''

RETURN = '''
edition:
    description: Billing edition of this child account
    type: str
    returned: always
'''


# import duo_client
from ansible.module_utils.basic import AnsibleModule


# This import and class can be removed once the duo_client library supports
#   the billing edition endpoint (https://github.com/duosecurity/duo_client_python/pull/133)
from duo_client.client import Client


class OverrideAdmin(Client):
    account_id = None

    def api_call(self, method, path, params):
        if self.account_id is not None:
            params['account_id'] = self.account_id
        return super(OverrideAdmin, self).api_call(method, path, params)

    def get_billing_edition(
        self,
    ):
        """
        Returns the billing edition for a child account.

        Returns dict including edition.

        Raises RuntimeError on error.
        """
        params = {
            'account_id': self.account_id,
        }
        response = self.json_api_call(
            'GET',
            '/admin/v1/billing/edition',
            params
        )
        return response

    def set_billing_edition(self, edition):
        """
        Sets the billing edition for a child account.

        edition - <str:the edition to set> One of: ENTERPRISE, PLATFORM, or BEYOND

        Returns empty string on success.

        Raises RuntimeError on error.
        """
        params = {
            'account_id': self.account_id,
            'edition': edition
        }
        response = self.json_api_call(
              'POST',
              '/admin/v1/billing/edition',
              params
        )
        return response


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        ikey=dict(type='str', required=True),
        skey=dict(type='str', required=True, no_log=True),
        host=dict(type='str', required=True),
        account_id=dict(type='str', required=True),
        edition=dict(type='str', required=False)
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
    account_id = module.params.get('account_id')
    edition = module.params.get('edition', None)
    # admin_api = duo_client.Admin(
    admin_api = OverrideAdmin(
        ikey=ikey,
        skey=skey,
        host=host,
        )
    admin_api.account_id = account_id

    try:
        resp = admin_api.get_billing_edition()
        result['edition'] = resp['edition']
    except Exception as e:
        module.fail_json(msg=str(e), **result)
    if not edition:
        result['changed'] = False
        module.exit_json(**result)
    elif edition == result['edition']:
        result['changed'] = False
        module.exit_json(**result)
    else:
        if edition not in ['ENTERPRISE', 'PLATFORM', 'BEYOND']:
            module.fail_json(msg="edition must be one of ['ENTERPRISE', 'PLATFORM', 'BEYOND'], not {}".format(edition), **result)
        result['changed'] = True
        if not module.check_mode:
            try:
                resp = admin_api.set_billing_edition(edition)
                result['edition'] = edition
            except Exception as e:
                module.fail_json(msg=str(e), **result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
