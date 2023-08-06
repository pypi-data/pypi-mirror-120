import os
from packaging import version
from typing import List

class Firmware:
    def __init__(self, path: str):
        self._path = path
        self._version = version.parse(self.versionForPath(self._path))
        self._checksum = None

    def __repr__(self):
        return '{}@{}'.format(self.path, self.versionNumber)

    def dict(self):
        return { "path": self.path, "version": self.versionNumber, "checksum": self.checksum }

    @property
    def path(self) -> str:
        return self._path

    @property
    def filename(self) -> str:
        return os.path.basename(self.path)

    @property
    def version(self):
        return self._version

    @property
    def versionNumber(self) -> str:
        return self._version.public

    @property
    def checksum(self) -> str:
        return self._checksum

    # Get version for firmware path
    #
    # :param path: firmware path
    # :return: firmware version
    @classmethod
    def versionForPath(cls, path: str) -> str:
        return path.split(os.sep)[-2:-1][0]

class FirmwareManager:
    def __init__(self, fw_path: str, fw_name: str):
        self._fw_path = fw_path
        self._fw_name = fw_name
        self._firmwares = None

    # Get all firmwares
    #
    # :param cached: if True the cache will be used
    # :return: complete firmware list
    def firmwares(self, cached: bool = True) -> List[Firmware]:
        if not cached or self._firmwares is None:
            self._firmwares = []
            for dirname, _, filenames in os.walk(self._fw_path):
                for filename in filenames:
                    if filename == self._fw_name:
                        self._firmwares.append(Firmware(os.path.join(dirname, filename)))
        return self._firmwares

    # Get firmware for a given version
    #
    # :param version: target version
    # :return: firmware object or None if no matching version was found
    def firmwareForVersion(self, version: str) -> Firmware:
        for fw in self.firmwares():
            if fw.versionNumber == version:
                return fw
        return None

    # Get a list with all version
    #
    # :return: list with all versions
    def versions(self) -> List[str]:
        return [fw.versionNumber for fw in self.firmwares()]

    # Get latest firwmare
    #
    # :return: latest firmware
    def latestFirmware(self) -> Firmware:
        latest = None
        for fw in self.firmwares():
            if latest is None or fw.version > latest.version:
                latest = fw
        return latest
