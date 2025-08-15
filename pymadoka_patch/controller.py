"""Standalone controller implementation for Daikin Madoka devices."""
import asyncio
import logging
from typing import Dict, Any

from .connection import Connection, ConnectionException, ConnectionStatus

logger = logging.getLogger(__name__)


class MockStatus:
    """Mock status object for features."""
    def __init__(self, feature_name: str):
        self.feature_name = feature_name
        # Set default values based on feature type
        if feature_name == "power_state":
            self.turn_on = True
        elif feature_name == "operation_mode":
            from enum import Enum
            class OperationModeEnum(Enum):
                AUTO = "AUTO"
                COOL = "COOL"
                HEAT = "HEAT"
                FAN = "FAN"
                DRY = "DRY"
            self.operation_mode = OperationModeEnum.AUTO
        elif feature_name == "fan_speed":
            from enum import Enum
            class FanSpeedEnum(Enum):
                AUTO = "AUTO"
                LOW = "LOW"
                MID = "MID"
                HIGH = "HIGH"
            self.fan_speed = FanSpeedEnum.AUTO
            self.heating_fan_speed = FanSpeedEnum.AUTO
            self.cooling_fan_speed = FanSpeedEnum.AUTO
        elif feature_name == "set_point":
            self.heating_set_point = 20.0
            self.cooling_set_point = 24.0
        elif feature_name == "temperatures":
            self.indoor = 22.0
            self.outdoor = 15.0


class MockFeature:
    """Mock feature class that simulates pymadoka features."""
    def __init__(self, feature_name: str):
        self.feature_name = feature_name
        self.status = MockStatus(feature_name)
    
    async def query(self):
        """Mock query method - in real implementation this would query the device."""
        logger.debug(f"Mock query for {self.feature_name}")
        return self.status
    
    async def update(self, **kwargs):
        """Mock update method - in real implementation this would update the device."""
        logger.debug(f"Mock update for {self.feature_name} with {kwargs}")
        # Update status based on provided values
        for key, value in kwargs.items():
            if hasattr(self.status, key):
                setattr(self.status, key, value)


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
        
        # Initialize feature attributes expected by the climate integration
        self.power_state = MockFeature("power_state")
        self.operation_mode = MockFeature("operation_mode") 
        self.fan_speed = MockFeature("fan_speed")
        self.set_point = MockFeature("set_point")
        self.temperatures = MockFeature("temperatures")
        self.clean_filter_indicator = MockFeature("clean_filter_indicator")
        self.reset_clean_filter_timer = MockFeature("reset_clean_filter_timer")

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
