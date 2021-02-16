Role Name
=========

Duo Security Accounts API

Requirements
------------

duo_client python library

Role Variables
--------------

* duo_account_ikey: Duo Accounts API Integration Key
* duo_account_skey: Duo Accounts API Secret Key
* duo_account_host: Duo Accounts API Host
* duo_account_name: Name of child account to be created/removed

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: localhost
      roles:
        - {role: duo_account, duo_account_ikey: "ABCDEFGH", duo_account_skey: "ABCDEFGH123456", duo_account_host: "api-123xyz.duosecurity.com", duo_account_name: "Awesome Test Account"}

License
-------

GPL v3.0+

Author Information
------------------

Mark Ciecior <mciecior@carrieraccessit.com>
