import pycom

import urequests
from urequests import URL

class FirmwareManager:
    _FIRMWARE_RESOURCE = 'firmware'
    _VERSIONS_RESOURCE = 'versions'
    _DOWNLOAD_RESOURCE = 'download'
    _UPDATE_RESOURCE = 'update'

    def __init__(self, host: str, port: int, protocol: str = 'http'):
        self.host = host
        self.port = port
        self.protocol = protocol
        self._firmwares = None
        self._versions = None
        self._update = None

    # Create a URL with the specified resources
    #
    # :param resources: resources list
    # :return: target URL
    def url(self, *resources) -> URL:
        return URL(self.protocol, self.host, self.port, *resources)

    # Get data from host in JSON format
    #
    # :param args: URL resource list
    # :return: response data as JSON object
    def getJSON(self, *args):
        with urequests.get(self.url(*args)) as req:
            if req.status == 200:
                return req.json
        return None

    # Get all firmwares available
    #
    # :param cahced: if True cache will be used
    # :return: list of available firmwares
    def firmwares(self, cached: bool = True):
        if not cached or self._firmwares is None:
            self._firmwares = self.getJSON(self._FIRMWARE_RESOURCE)
        return self._firmwares

    # Get specific firmware version
    #
    # :param version: target firmware version
    # :return: firmware data as JSON object
    def firmware(self, version: str):
        return self.getJSON(self._FIRMWARE_RESOURCE, version)

    # Get latest firmware version available
    #
    # :return: latest firmware version data as JSON object
    def latest(self):
        return self.firmware('latest')

    # Get a list of available firmware versions
    #
    # :param cached: if True cache will be used
    # :return: available firmware version as JSON object
    def versions(self, cached: bool = True):
        if not cached or self._versions is None:
            self._versions = self.getJSON(self._VERSIONS_RESOURCE)
        return self._versions

    # Get best firmware update candidate for current firmware version
    #
    # :param current_version: current firmware version
    # :param cached: if True cache will be used
    # :return: firmware update candidate data as JSON object
    def update(self, current_version: str, cached: bool = True):
        if not cached or self._update is None:
            self._update = self.getJSON(self._UPDATE_RESOURCE, current_version)
        return self._update

    # Download firmware version
    #
    # :param version: firmware version to download
    # :return: socket stream with firmware data
    def download(self, version: str):
        try:
            resp = urequests.get(self.url(self._DOWNLOAD_RESOURCE, version))
            if resp.status != 200:
                raise
            return resp.file
        except:
            return None

_BLOCKSIZE = const(0x1000)

def flash(file, blocksize: int = _BLOCKSIZE, write_callback: callable = None):
    buffer = bytearray(blocksize)
    mv = memoryview(buffer)
    size = 0
    chunk = None
    pycom.ota_start()
    while chunk is None or chunk > 0:
        chunk = file.readinto(buffer)
        pycom.ota_write(mv[:chunk])
        size += chunk
        if write_callback:
            write_callback(size)
    pycom.ota_finish()
