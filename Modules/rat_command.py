# coding: utf8
"""
rat_command.py - Handles Command Events

Copyright (c) 2018 The Fuel Rats Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md

This module is built on top of the Pydle system.

"""

from functools import wraps
import logging
from Modules.constants import base_logger

# set the logger for handlers
log = logging.getLogger(f'{base_logger}.handlers')


class CommandException(Exception):
    """
    base Command Exception
    """
    pass


class InvalidCommandException(CommandException):
    """
    invoked command failed validation
    """
    pass


class CommandNotFoundException(CommandException):
    """
    Command not found.
    """
    pass


class NameCollisionException(CommandException):
    """
    Someone attempted to register a command already registered.
    """
    pass


class Commands:
    """
    Handles command registration and execution
    """

    ####
    # logger facility
    log = logging.getLogger(f"{base_logger}.commands")
    ####
    # commands registered with @command will populate this dict
    _registered_commands = {}

    ####
    # character/s that must prefix a message for it to be parsed as a command.
    prefix = '!'

    ####
    # Pydle bot instance. #FIXME set value during MechaClient init!
    bot = None

    @classmethod
    async def trigger(cls, message: str, sender: str, channel: str):
        """
        Invoke a command, passing args and kwargs to the called function
        :param message: triggers message to invoke
        :param sender: author of triggering message
        :param channel: channel of triggering message
        :return: bool command
        """
        log.debug("trigger called!")
        if cls._registered_commands is None:
            cls.log.critical(" registered commands dict somehow was set to None")
            raise CommandException("registered_commands is None!")
        if not cls.bot:
            # someone didn't set me.
            raise CommandException(f"cls.bot is not set. (value = {cls.bot}")

        cls.log.debug(f"triggered! message is {message}")

        if not message:
            raise InvalidCommandException(f"Command required, got {message}")
        elif not message.startswith(cls.prefix):
            log.debug(f"ignoring message{message} as it does not start with my prefix.")
            return None
        else:
            raw_command: str = message.strip(cls.prefix)  # remove command prefix
            words = raw_command.split(" ")  # split command into words via spaces
            command = words[0]
            c_args = words[1:]
            cls.log.debug(f"words={words}\ncommand={command}\nc_args={c_args}")
            if command not in cls._registered_commands:
                cls.log.error(f"unable to find command.{message}")
                raise CommandNotFoundException(f"Unable to find command {message}")
            else:
                cls.log.debug("found command, invoking...")
                cmd = cls.get_command(command)
                return await cmd(*c_args, bot=cls.bot, sender=sender, channel=channel)

    @classmethod
    def _register(cls, func, names: list or str) -> bool:
        """
        Register a new command
        :param func: function
        :param names: names to register
        :return: success
        """
        if isinstance(names, str):
            names = [names]  # idiot proofing

        if func is None or not callable(func):
            # command not callable
            return False

        else:
            for alias in names:
                if alias in cls._registered_commands:
                    # command already registered
                    raise NameCollisionException(f"attempted to re-register command(s) {alias}")
                else:
                    formed_dict = {alias: func}
                    cls._registered_commands.update(formed_dict)

            return True

    @classmethod
    def _flush(cls)->None:
        """
        Flushes registered commands
        Probably useless outside testing...
        :return: None
        """
        cls._registered_commands = {}

    @classmethod
    def command(cls, alias: list):
        # stuff that occurs here executes when the wrapped command is first computed
        # use this space for command registration

        def real_decorator(func):
            # this also only executes during intial wrap
            # methinks this is where command reg should occur?
            cls.log.debug("inside real_decorator")
            cls.log.debug(f"Congratulations.  You decorated a function that does something with {alias}")
            cls.log.debug(f"registering command with aliases: {alias}...")
            if not cls._register(func, alias):
                raise InvalidCommandException("unable to register commands.")
            cls.log.debug(f"Success! done registering commands {alias}!")

            @wraps(func)
            def wrapper(*args, **kwargs):
                cls.log.debug("inside wrapper")
                func(*args, **kwargs)

            return wrapper

        return real_decorator

    @classmethod
    def get_command(cls, name: str):
        # remove the prefix.
        name = name.strip(cls.prefix)
        # see if its a command
        if name in cls._registered_commands:
            cls.log.debug("command found!")
            return cls._registered_commands[name]
        else:
            return None
