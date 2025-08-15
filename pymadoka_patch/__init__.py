"""Patched version of pymadoka to fix bleak compatibility issues."""

# Re-export everything from the original pymadoka, but with our patched connection module
from pymadoka.controller import Controller
from pymadoka.consts import *
from pymadoka.feature import *
from pymadoka.transport import *

# Import our patched connection module instead of the original
from .connection import discover_devices, force_device_disconnect, Connection

__all__ = [
    'Controller',
    'discover_devices', 
    'force_device_disconnect',
    'Connection'
]
