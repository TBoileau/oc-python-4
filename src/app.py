"""Imported modules/packages"""
import os

from dotenv import load_dotenv

from src.controller.app_controller import AppController
from src.templating.templating import Templating, TemplatingInterface


class App:
    """
    App class
    """

    def __init__(self):
        """
        Constructor
        """
        self.__templates_folder: str = os.path.join(os.getcwd(), "templates")

    def run(self):
        """
        Run app

        :return:
        """
        load_dotenv(".env")

        templating: TemplatingInterface = Templating(self.__templates_folder)

        while True:
            app_controller: AppController = AppController(templating)
            app_controller.home()
