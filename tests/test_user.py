"""
test_user.py - test suite for `Modules.User`

Copyright (c) 2018 The Fuel Rats Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md
"""
import pytest

from Modules.User import User


@pytest.mark.parametrize("expected_host", [
    "recruit.fuelrats.com",
    "rat.fuelrats.com",
    "dispatch.fuelrats.com",
    "overseer.fuelrats.com",
    "op.fuelrats.com",
    "techrat.fuelrats.com",
    "netadmin.fuelrats.com",
    "admin.fuelrats.com",
])
@pytest.mark.parametrize("prefix", ["potato.", "Orbital.", ""])
def test_process_vhost(prefix: str, expected_host: str):
    """
    Asserts vhost processing functions as expected
    """
    mixed_host = f"{prefix}{expected_host}"
    assert User.process_vhost(mixed_host) == expected_host


def test_process_vhost_orange():
    """
    Asserts vhost processing works for Orange, as he has a special vhost
    (that can't be tested in the parametrize)
    """
    assert User.process_vhost("i.see.all") == "i.see.all"


@pytest.mark.parametrize("data", (
        {'oper': False,
         'idle': 0,
         'away': False,
         'away_message': None,
         'username': 'White',
         'hostname': 'recruit.fuelrats.com',
         'realname': 'WhiteStrips',
         'identified': False,
         'server': 'irc.fuelrats.com',
         'server_info': 'Fuel Rats IRC Server',
         'secure': True,
         'account': 'WhiteStrips'},
        {'oper': True,
         'idle': 0,
         'away': False,
         'away_message': None,
         'username': 'AwesomeAdmin',
         'hostname': 'admin.fuelrats.com',
         'realname': 'you know',
         'identified': True,
         'server': 'irc.fuelrats.com',
         'server_info': 'Fuel Rats IRC Server',
         'secure': True,
         'account': 'AwesomeAdmin'}
))
def test_user_constructor(data: dict):
    """
    Tests the User constructor
    """
    my_user = User(oper=data['oper'],
                   idle=data['idle'],
                   away=data['away'],
                   away_message=data['away_message'],
                   identified=data['identified'],
                   secure=data['secure'],
                   account=data['account'],
                   nickname="unit_test",
                   username=data['username'],
                   hostname=data['hostname'],
                   realname=data['realname'],
                   server=data['server'],
                   server_info=data['server_info'],
                   )

    assert data['oper'] == my_user.oper
    assert data['idle'] == my_user.idle
    assert data['away'] == my_user.away
    assert data['away_message'] == my_user.away_message
    assert data['identified'] == my_user.identified
    assert data['secure'] == my_user.secure
    assert data['account'] == my_user.account
    assert "unit_test" == my_user.nickname
    assert data['hostname'] == my_user.hostname
    assert data['realname'] == my_user.realname
    assert data['server'] == my_user.server
    assert data['server_info'] == my_user.server_info
