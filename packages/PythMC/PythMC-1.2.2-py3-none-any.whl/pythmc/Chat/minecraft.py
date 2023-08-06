# coding: utf-8

# Created at 30/03/2021
__license__ = "GNU General Public License v3.0"
__author__ = "Alexandre Silva // MrKelpy"
__copyright__ = "© Alexandre Silva 2021"

# Builtin imports
import time
import os
import math

# Third Party Imports
import keyboard

# Local Application Imports
from pythmc.Chat.chat_parser import parse_chat_messages
from pythmc.assets.exceptions import *
from pythmc.assets.essentials.interactor import Interactor

class ChatLink(Interactor):

    """
    Used to interact with the Minecraft Chat.
    """

    def __init__(self):

        super().__init__()
        self.default_logs_path = os.path.join(os.getenv("APPDATA"), ".minecraft", "logs", "latest.log")
        self._ensure_log_existance()


    def _ensure_log_existance(self):

        if not os.path.isfile(self.default_logs_path):
            raise LogsNotFoundError(f"Could not find any file at \"{self.default_logs_path}\"")

        return True


    def get_history(self, limit: int = math.factorial(16)):
        """
        :param limit: Limitation on how back the chat history goes
        :return: List or None
        """

        with open(self.default_logs_path, "r") as logs_file:
            log_history = logs_file.readlines()

        message_list = parse_chat_messages(log_history, limit)
        return message_list


    def send(self, message: str):
        """
        Sends a message in chat.
        :param message:
        :return:
        """

        self.activate_mc()

        # Handles message sending in chat.
        self._perform(self.CHAT)
        time.sleep(0.1)
        keyboard.write(message)
        self._perform("RETURN")

