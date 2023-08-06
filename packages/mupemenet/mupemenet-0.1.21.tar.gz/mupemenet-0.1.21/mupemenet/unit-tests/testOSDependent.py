import logging
import platform
import unittest
from abc import abstractmethod, ABC
from logging import info, debug, basicConfig, DEBUG

import coloredlogs

from mupemenet.osdependent.platforms import platform_dependent


class AbstractDummy(ABC):

    @abstractmethod
    def get_platform(self) -> str:
        pass

    def say(self):
        debug("Dummy " + self.get_platform() + "-dependent class")


class DummyWin(AbstractDummy):
    def get_platform(self) -> str:
        return "win"


class DummyRpi(AbstractDummy):
    def get_platform(self) -> str:
        return "rpi"


@platform_dependent(rpi=DummyRpi, win=DummyWin)
class Dummy:
    pass


class TestPlatformDependency(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        coloredlogs.install(level='DEBUG')
        logging.getLogger().setLevel(level=logging.DEBUG)
        debug("Test debug")

    def test_platform_dependent_dummy_class(self):
        dummy = Dummy()
        dummy.say()
        dummy_plt = dummy.get_platform()
        plt = platform.system().lower()[:3]
        self.assertTrue(dummy_plt == plt)
