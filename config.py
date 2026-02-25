"""
AATS Configuration Management
Centralized configuration with validation and environment variable support
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

@dataclass
class ExchangeConfig:
    """Exchange API configuration with validation"""
    name: str = "binance"
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    testnet: bool = True
    
    def __post_init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY', self.api_key)
        self.api_secret = os.getenv('BINANCE_API_SECRET', self.api_secret)
        
        if not self.api_key or not self.api_secret:
            logging.warning("Exchange API credentials not fully configured")
            # In production, this would trigger a human intervention request

@dataclass
class TradingConfig:
    """Trading strategy parameters"""
    initial_capital: float = 10000.0
    max_position_size: float = 0.1  # 10% of portfolio
    stop_loss_percent: float = 0.02  # 2%
    take_profit_percent: float = 0.05  # 5%
    default_symbol: str = "BTC/USDT"
    timeframe: str = "1h"  # 1 hour candles
    
    def validate(self):
        """Validate trading parameters"""
        if self.max_position_size > 0.5:
            raise ValueError("Max position size exceeds safety limit (50%)")
        if self.stop_loss_percent > 0.1:
            raise ValueError("Stop loss too large (max 10%)")
        return True

@dataclass
class FirebaseConfig:
    """Firebase configuration (CRITICAL for state management)"""
    project_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    
    def __post_init__(self):
        self.project_id = os.getenv('FIREBASE_PROJECT_ID')
        self.private_key = os.getenv('FIREBASE_PRIVATE_KEY')
        self.client_email = os.getenv('FIREBASE_CLIENT_EMAIL')
        
        # Validate Firebase configuration
        if not all([self.project_id, self.private_key, self.client_email]):
            logging.error("Firebase configuration incomplete. State management will fail.")
            # This is a critical failure - system cannot operate without Firebase

class AATSConfig:
    """Main configuration orchestrator"""
    def __init__(self):
        self.exchange = ExchangeConfig()
        self.trading = TradingConfig()
        self.firebase = FirebaseConfig()
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        # Initialize logging
        self.setup_logging()
    
    def setup_logging(self):
        """Configure system-wide logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('aats_system.log')
            ]
        )
    
    def validate(self):
        """Validate entire configuration"""
        try:
            self.trading.validate()
            
            if not self.firebase.project_id:
                raise ValueError("Firebase configuration required for state management")
                
            return True
        except Exception as e:
            logging.error(f"Configuration validation failed: {e}")
            return False

# Global configuration instance
config = AATSConfig()