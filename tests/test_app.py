"""Imported modules/packages"""
import pytest

from src.app import App


def test_app():
    app: App = App()
    assert True == app.run()
