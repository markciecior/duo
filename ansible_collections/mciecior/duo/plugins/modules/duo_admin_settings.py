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
    - "This is used to add/change the settings of Duo accounts"

options:
    ikey:
        description:
            - Integration Key for the Duo Admin/Accounts API application
        type: str
        required: true
    skey:
        description:
            - Secret Key for the Duo Admin/Accounts API application
        type: str
        required: true
    host:
        description:
            - API Host for the Duo Admin/Accounts API application
        type: str
        required: true
    name:
        description:
            - Name of the new child account to be modified.  This is only used by MSP accounts to modify child accounts.
        type: str
        required: false
    state:
        description:
            - Operation to perform.  "query" will retrieve settings.  "present" will update settings.  settings variable is required if state=present
        type: str
        required: true
    lockout_threshold:
        description:
            - The number of consecutive failed authentication attempts before the user’s status is set to “Locked Out” and the user is denied access.
        type: bool
        required: false
    lockout_expire_duration:
        description:
            - If non-zero, the time in minutes until a locked-out user’s status reverts to “Active”. If 0, a user remains locked out until their status is manually changed (By an admin or API call). Minimum: 5 minutes. Maximum: 30000 minutes
        type: bool
        required: false
    inactive_user_expiration:
        description:
            - Users will be automatically deleted if they are inactive (no successful logins) for a this amount of days. Minimum: 30 days. Maximum: 365 days.
        type: bool
        required: false
    sms_batch:
        description:
            - How many passcodes to send at one time, up to 10.
        type: bool
        required: false
    sms_expiration:
        description:
            - The time in minutes to expire and invalidate SMS passcodes, or empty if they should not expire.
        type: bool
        required: false
    sms_refresh:
        description:
            - If 1, a new set of SMS passcodes will automatically be sent after the last one is used. If 0, a new set will not be sent.
        type: bool
        required: false
    sms_message:
        description:
            - Description sent with every batch of SMS passcodes.
        type: bool
        required: false
    fraud_email:
        description:
            - The email address to be notified when a user reports a fraudulent authentication attempt or is locked out due to failed authentication attempts, or empty for all administrators will be notified. If fraud_email is set to a specific email address and fraud_email_enabled is set to false, the specific email address value is cleared.
        type: bool
        required: false
    fraud_email_enabled:
        description:
            - Set to true to enable fraudulent authentication notification emails. False disables the fraud email functionality. If fraud_email is set to a specific email address and fraud_email_enabled is set to false, the specific email address value is cleared.
        type: bool
        required: false
    keypress_confirm:
        description:
            - The key for users to press to authenticate, or empty if any key should be pressed to authenticate. If this is empty, keypress_fraud must be as well.
        type: bool
        required: false
    keypress_fraud:
        description:
            - The key for users to report fraud, or empty if any key should be pressed to authenticate. If this is empty, keypress_confirm must be as well.
        type: bool
        required: false
    timezone:
        description:
            - This is the timezone used when displaying timestamps in the administrative interface. Timezones must be entries in the IANA Time Zone Database, for example, “US/Eastern”, “Australia/Darwin”, “GMT”.
        type: bool
        required: false
    telephony_warning_min:
        description:
            - Configure a alert to be sent when the account has fewer than this many telephony credits remaining.
        type: bool
        required: false
    caller_id:
        description:
            - Automated calls will appear to come from this number. This does not apply to text messages.
        type: bool
        required: false
    push_enabled:
        description:
            - If true, users will be able to use Duo Push to authenticate. If false, users will not be able to use Duo Push to authenticate. Note that if false, this will override push_enabled for any groups.
        type: bool
        required: false
    sms_enabled:
        description:
            - If true, users will be able to use SMS passcodes to authenticate. If false, users will not be able to use SMS passcodes to authenticate. Note that if false, this will override sms_enabled for any groups.
        type: bool
        required: false
    voice_enabled:
        description:
            - If true, users will be able to authenticate using voice callback. If false, users will not be able to authenticate using voice callback. Note that if false, this will override voice_enabled for any groups.
        type: bool
        required: false
    mobile_otp_enabled:
        description:
            - If true, users will be able to use authenticate with a passcode generated by Duo Mobile. If false, users will not be able to authenticate with a passcode generated by Duo Mobile. Note that if false, this will override Duo Mobile passcodes for any groups.
        type: bool
        required: false
    u2f_enabled:
        description:
            - If true, users will be able to use authenticate with a U2F device. If false, users will not be able to authenticate with a U2F device. Default: false.
        type: bool
        required: false
    user_telephony_cost_max:
        description:
            - The maximum number of telephony credits a user may consume in a single authentication event. This excludes Duo administrators authenticating to the Duo administration panel. Default: 20.
        type: bool
        required: false
    minimum_password_length:
        description:
            - The minimum number of characters that an administrator’s Duo Admin Panel password must contain. This is only enforced on password creation and reset; existing passwords will not be invalidated. Default: 12.
        type: bool
        required: false
    password_requires_upper_alpha:
        description:
            - If true, administrator passwords will be required to contain an upper case alphabetic character. If false, administrator passwords will not be required to contain an upper case alphabetic character. This is only enforced on password creation and reset; existing passwords will not be invalidated. Default: false.
        type: bool
        required: false
    password_requires_lower_alpha:
        description:
            - If true, administrator passwords will be required to contain a lower case alphabetic character. If false, administrator passwords will not be required to contain a lower case alphabetic character. This is only enforced on password creation and reset; existing passwords will not be invalidated. Default: false.
        type: bool
        required: false
    password_requires_numeric:
        description:
            - If true, administrator passwords will be required to contain a numeric character. If false, administrator passwords will not be required to contain a numeric character. This is only enforced on password creation and reset; existing passwords will not be invalidated. Default: false.
        type: bool
        required: false
    password_requires_special:
        description:
            - If true, administrator passwords will be required to contain a special (non-alphanumeric) character. If false, administrator passwords will not be required to contain a special (non-alphanumeric) character. This is only enforced on password creation and reset; existing passwords will not be invalidated. Default: false.
        type: bool
        required: false

author:
    - Mark Ciecior (@markciecior)
'''

EXAMPLES = '''
# Update the timezone of a Duo account
- name: Update timezone
  duo_admin_settings:
    ikey: ABCDEFGH
    skey: ABCDEFGH12345678
    host: api-123XYZ.duosecurity.com
    state: present
    timezone: "US/Eastern"

# Update the timezone and sms_batch value of a child account
- name: Update timezone
  duo_admin_settings:
    ikey: ABCDEFGH
    skey: ABCDEFGH12345678
    host: api-123XYZ.duosecurity.com
    name: Awesome Test Account
    state: present
    timezone: "US/Central"
    sms_batch: 9

# Retrieve the settings of a child account
- name: Update timezone
  duo_admin_settings:
    ikey: ABCDEFGH
    skey: ABCDEFGH12345678
    host: api-123XYZ.duosecurity.com
    name: Awesome Test Account
    state: query
'''

RETURN = '''
settings:
    description: dict of account settings
    type: dict
    returned: always
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
        lockout_threshold=dict(type='int', required=False),
        lockout_expire_duration=dict(type='int', required=False),
        inactive_user_expiration=dict(type='int', required=False),
        sms_batch=dict(type='int', required=False),
        sms_expiration=dict(type='int', required=False),
        sms_refresh=dict(type='bool', required=False),
        sms_message=dict(type='str', required=False),
        fraud_email=dict(type='str', required=False),
        fraud_email_enabled=dict(type='bool', required=False),
        keypress_confirm=dict(type='str', required=False),
        keypress_fraud=dict(type='str', required=False),
        timezone=dict(type='str', required=False),
        telephony_warning_min=dict(type='int', required=False),
        caller_id=dict(type='str', required=False),
        push_enabled=dict(type='bool', required=False),
        sms_enabled=dict(type='bool', required=False),
        voice_enabled=dict(type='bool', required=False),
        mobile_otp_enabled=dict(type='bool', required=False),
        u2f_enabled=dict(type='bool', required=False),
        user_telephony_cost_max=dict(type='int', required=False),
        minimum_password_length=dict(type='int', required=False, no_log=False),
        password_requires_upper_alpha=dict(type='bool', required=False, no_log=False),
        password_requires_lower_alpha=dict(type='bool', required=False, no_log=False),
        password_requires_numeric=dict(type='bool', required=False, no_log=False),
        password_requires_special=dict(type='bool', required=False, no_log=False)
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
    lockout_threshold = module.params.get('lockout_threshold')
    lockout_expire_duration = module.params.get('lockout_expire_duration')
    inactive_user_expiration = module.params.get('inactive_user_expiration')
    sms_batch = module.params.get('sms_batch')
    sms_expiration = module.params.get('sms_expiration')
    sms_refresh = module.params.get('sms_refresh')
    sms_message = module.params.get('sms_message')
    fraud_email = module.params.get('fraud_email')
    fraud_email_enabled = module.params.get('fraud_email_enabled')
    keypress_confirm = module.params.get('keypress_confirm')
    keypress_fraud = module.params.get('keypress_fraud')
    timezone = module.params.get('timezone')
    telephony_warning_min = module.params.get('telephony_warning_min')
    caller_id = module.params.get('caller_id')
    push_enabled = module.params.get('push_enabled')
    sms_enabled = module.params.get('sms_enabled')
    voice_enabled = module.params.get('voice_enabled')
    mobile_otp_enabled = module.params.get('mobile_otp_enabled')
    u2f_enabled = module.params.get('u2f_enabled')
    user_telephony_cost_max = module.params.get('user_telephony_cost_max')
    minimum_password_length = module.params.get('minimum_password_length')
    password_requires_upper_alpha = module.params.get('password_requires_upper_alpha')
    password_requires_lower_alpha = module.params.get('password_requires_lower_alpha')
    password_requires_numeric = module.params.get('password_requires_numeric')
    password_requires_special = module.params.get('password_requires_special')
    newSettings = dict(
        lockout_threshold=lockout_threshold,
        lockout_expire_duration=lockout_expire_duration,
        inactive_user_expiration=inactive_user_expiration,
        sms_batch=sms_batch,
        sms_expiration=sms_expiration,
        sms_refresh=sms_refresh,
        sms_message=sms_message,
        fraud_email=fraud_email,
        fraud_email_enabled=fraud_email_enabled,
        keypress_confirm=keypress_confirm,
        keypress_fraud=keypress_fraud,
        timezone=timezone,
        telephony_warning_min=telephony_warning_min,
        caller_id=caller_id,
        push_enabled=push_enabled,
        sms_enabled=sms_enabled,
        voice_enabled=voice_enabled,
        mobile_otp_enabled=mobile_otp_enabled,
        u2f_enabled=u2f_enabled,
        user_telephony_cost_max=user_telephony_cost_max,
        minimum_password_length=minimum_password_length,
        password_requires_upper_alpha=password_requires_upper_alpha,
        password_requires_lower_alpha=password_requires_lower_alpha,
        password_requires_numeric=password_requires_numeric,
        password_requires_special=password_requires_special,
        )
    admin_api = duo_client.Admin(
        ikey=ikey,
        skey=skey,
        host=host,
        )
    
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
    
    currentSettings = {}
    try:
        currentSettings = admin_api.get_settings()
    except Exception as e:
        module.fail_json(msg='Could not retrieve current account settings', **result)
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
        if result['changed'] == False:
            module.exit_json(**result)
        else:
            for k, v in newSettings.items():
                result['settings'][k] = v
            if not module.check_mode:
                try:
                    admin_api.update_settings(**newSettings)
                except Exception as e:
                    result['changed'] = False
                    module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
