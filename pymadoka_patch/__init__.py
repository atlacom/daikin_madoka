"""Standalone implementation of pymadoka essentials to fix bleak compatibility issues."""

# Import our standalone implementations
from .connection import discover_devices, force_device_disconnect, Connection
from .controller import Controller

__all__ = [
    'Controller',
    'discover_devices', 
    'force_device_disconnect',
    'Connection'
]
