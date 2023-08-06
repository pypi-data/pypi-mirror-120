# Pycom OTA server
Host Pycom firmware files and serve to client devices.

## Directory structure
All firmware versions must be located inside the `firmware` directory. Any version format is allowed, but the Python LooseVersion is recommended. Firmware files must be named `appimg.bin` and be located inside the version directory.
```
.
|
- main.py
- firmware.py
- firmware
  |
  - 0.0.1
  | |
  | - appimg.bin
  |
  - 0.0.2
  | |
  | - appimg.bin
  |
  - 0.0.2.dev-f673ba1
	|
	- appimg.bin
```
