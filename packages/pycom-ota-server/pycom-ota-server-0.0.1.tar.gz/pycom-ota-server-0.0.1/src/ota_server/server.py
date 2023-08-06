from flask import Flask, jsonify
from flask_classful import FlaskView, route
from .firmware import Firmware, FirmwareManager

_app = Flask('Firmware Server')

class FirmwareServer(FlaskView):
    def __init__(self, host: str = '0.0.0.0', port: int = 5000, fw_path: str = 'firmware', fw_name: str = 'appimg.bin'):
        self.host = host
        self.port = port
        self.fwm = FirmwareManager(fw_path, fw_name)

    @classmethod
    def download_file(self, path: str, name: str):
        with open(path, 'rb') as f:
            return send_file(io.BytesIO(f.read()), download_name=name, mimetype='application/octet-stream')

    @classmethod
    def download_firmware(self, firmware: Firmware):
        if firmware:
            return self.download_file(firmware.path, firmware.filename)
        resp = jsonify({ 'error': 'Firmware file is not available'})
        resp.status = 404
        return resp

    @classmethod
    def firmware_json(self, firmware: Firmware):
        if firmware:
            return jsonify(firmware.dict())
        resp = jsonify({ 'error': 'Firmware file is not available'})
        resp.status = 404
        return resp

    def start(self):
        _app.run(host=self.host, port=self.port)

    @route('/versions')
    def get_versions(self):
        return jsonify(self.fwm.versions())

    @route('/firmware')
    def get_firmwares(self):
        return jsonify([fw.dict() for fw in self.fwm.firmwares()])

    @route('/firmware/<version>')
    def get_version(self, version):
        return self.firmware_json(self.fwm.firmwareForVersion(version))

    @route('/firmware/latest')
    def get_latest_firmware(self):
        return self.firmware_json(self.fwm.latestFirmware())

    @route('/update/<device>')
    def update_device(self, device):
        # e.g. check DB for an update for a specific device
        return self.get_latest_firmware()

    @route('/download/<version>')
    def download_version(self, version):
        return self.download_firmware(self.fwm.firmwareForVersion(version))

FirmwareServer.register(_app, route_base='/')

if __name__ == "__main__":
    _app.run(debug=True)
