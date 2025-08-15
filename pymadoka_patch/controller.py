"""Standalone controller implementation for Daikin Madoka devices."""
import asyncio
import logging
from typing import Dict, Any

from .connection import Connection, ConnectionException, ConnectionStatus

logger = logging.getLogger(__name__)


class Controller:
    """Simplified controller for Daikin Madoka devices.
    
    This is a minimal implementation that provides basic connectivity
    without the full feature set of the original pymadoka library.
    """
    
    def __init__(self, address: str, adapter: str = "hci0", reconnect: bool = True):
        """Initialize the controller with the device address.

        Args:
            address (str): MAC address of the device  
            adapter (str): Bluetooth adapter for the connection
            reconnect (bool): Whether to automatically reconnect on disconnect
        """
        if adapter is None:
            adapter = "hci0"

        self.address = address
        self.adapter = adapter
        self.status = {}
        self.info = {}
        self.connection = Connection(address, adapter=adapter, reconnect=reconnect)

    async def start(self):
        """Start the connection to the device."""        
        await self.connection.start()

    async def stop(self):
        """Stop the connection.""" 
        await self.connection.cleanup()

    async def update(self):
        """Update device status.
        
        This is a simplified implementation that just ensures the connection is active.
        In the full pymadoka library, this would query all device features.
        """
        if self.connection.connection_status != ConnectionStatus.CONNECTED:
            logger.warning(f"Device {self.address} is not connected")
            return
        
        # Basic status update - in a full implementation this would query device features
        self.status = {
            "connected": True,
            "address": self.address,
            "adapter": self.adapter
        }

    def refresh_status(self) -> Dict[str, Any]:
        """Get the current status dictionary.

        Returns:
            dict: Dictionary with the current device status
        """
        return self.status

    async def read_info(self) -> Dict[str, str]:
        """Read device information from Bluetooth services.
        
        Returns:
            Dict[str,str]: Dictionary with device info
        """
        if self.connection.connection_status == ConnectionStatus.CONNECTED:
            self.info = await self.connection.read_info()
        return self.info

    @property
    def is_connected(self) -> bool:
        """Check if the device is connected."""
        return self.connection.connection_status == ConnectionStatus.CONNECTED

    @property
    def name(self) -> str:
        """Get the device name."""
        return getattr(self.connection, 'name', self.address)
