"""
Real-time Market Data Collector
Handles data ingestion from multiple exchanges with fault tolerance
"""
import ccxt
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta
import time
from config import config

class MarketDataCollector:
    """Robust market data collector with retry logic and error handling"""
    
    def __init__(self, exchange_name: str = None):
        self.exchange_name = exchange_name or config.exchange.name
        self.exchange = self._initialize_exchange()
        self.connected = False
        self.last_successful_fetch = None
        self.failure_count = 0