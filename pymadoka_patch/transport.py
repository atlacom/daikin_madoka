"""Transport layer for Daikin Madoka communication protocol."""
import logging
from typing import List

logger = logging.getLogger(__name__)


class TransportDelegate:
    """Base class for transport delegates."""
    
    def response_rebuilt(self, data: bytearray):
        """Called when a response is successfully rebuilt."""
        pass
    
    def response_failed(self, data: bytearray):
        """Called when a response fails to be rebuilt."""
        pass


class Transport:
    """Transport layer for handling chunked communication."""
    
    def __init__(self, delegate: TransportDelegate):
        """Initialize transport with a delegate.
        
        Args:
            delegate: Object that implements TransportDelegate interface
        """
        self.delegate = delegate
        self.chunks = []
        self.expected_length = 0
        
    def split_in_chunks(self, data: bytearray, chunk_size: int = 20) -> List[bytearray]:
        """Split data into chunks for transmission.
        
        Args:
            data: Data to split
            chunk_size: Maximum size of each chunk
            
        Returns:
            List of chunks
        """
        chunks = []
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            chunks.append(chunk)
        return chunks
    
    def rebuild_chunk(self, chunk: bytearray):
        """Rebuild a message from received chunks.
        
        Args:
            chunk: Received chunk of data
        """
        try:
            if not self.chunks:
                # First chunk should contain the expected length
                if len(chunk) > 0:
                    self.expected_length = chunk[0]
                    self.chunks = [chunk]
                else:
                    logger.warning("Received empty first chunk")
                    return
            else:
                # Subsequent chunks
                self.chunks.append(chunk)
            
            # Check if we have all chunks
            total_received = sum(len(c) for c in self.chunks)
            if total_received >= self.expected_length:
                # Rebuild complete message
                complete_data = bytearray()
                for chunk in self.chunks:
                    complete_data.extend(chunk)
                
                # Reset for next message
                self.chunks = []
                self.expected_length = 0
                
                # Notify delegate
                self.delegate.response_rebuilt(complete_data)
        except Exception as e:
            logger.error(f"Error rebuilding chunk: {e}")
            self.chunks = []
            self.expected_length = 0
            if hasattr(self.delegate, 'response_failed'):
                self.delegate.response_failed(bytearray())
