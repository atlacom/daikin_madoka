"""Constants for Daikin Madoka communication."""

# Bluetooth GATT characteristic UUIDs
NOTIFY_CHAR_UUID = "2141e110-213a-11e6-b67b-9e71128cae77"
WRITE_CHAR_UUID = "2141e111-213a-11e6-b67b-9e71128cae77"

# Communication settings
SEND_MAX_TRIES = 3
CHUNK_SIZE = 20

# Device discovery settings
DEFAULT_DISCOVERY_TIMEOUT = 5
DEFAULT_ADAPTER = "hci0"
