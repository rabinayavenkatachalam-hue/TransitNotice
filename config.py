import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')


class Config:
    """Base configuration for TransitNotice – Tamil Nadu Public Transport Service Update Tracker."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'transitnotice-tamilnadu-transport-secret-key-2026')
    
    # Database configuration
    # Supports MySQL with SQLite fallback
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f"sqlite:///{BASE_DIR / 'transitnotice.db'}")
    if SQLALCHEMY_DATABASE_URI.startswith("sqlite:///transitnotice.db") and not os.path.isabs(SQLALCHEMY_DATABASE_URI.replace("sqlite:///", "")):
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'transitnotice.db'}"
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,
        'pool_pre_ping': True,
    } if 'mysql' in SQLALCHEMY_DATABASE_URI else {}

    # State and Timezone
    STATE_NAME = 'Tamil Nadu'
    DEFAULT_STATE = 'Tamil Nadu'
    DEFAULT_DISTRICT = os.getenv('DEFAULT_DISTRICT', 'All Tamil Nadu')
    APP_TIMEZONE = os.getenv('APP_TIMEZONE', 'Asia/Kolkata')

    # All 38 Districts of Tamil Nadu (Official Gazette)
    TAMIL_NADU_DISTRICTS = [
        'Ariyalur', 'Chengalpattu', 'Chennai', 'Coimbatore', 'Cuddalore',
        'Dharmapuri', 'Dindigul', 'Erode', 'Kallakurichi', 'Kancheepuram',
        'Kanniyakumari', 'Karur', 'Krishnagiri', 'Madurai', 'Mayiladuthurai',
        'Nagapattinam', 'Namakkal', 'Nilgiris', 'Perambalur', 'Pudukkottai',
        'Ramanathapuram', 'Ranipet', 'Salem', 'Sivaganga', 'Tenkasi',
        'Thanjavur', 'Theni', 'Thoothukudi', 'Tiruchirappalli', 'Tirunelveli',
        'Tirupathur', 'Tiruppur', 'Tiruvallur', 'Tiruvannamalai', 'Tiruvarur',
        'Vellore', 'Viluppuram', 'Virudhunagar'
    ]

    # Official Transport Authorities in Tamil Nadu
    TRANSPORT_AUTHORITIES = [
        {'code': 'MTC', 'name': 'Metropolitan Transport Corporation (MTC) Chennai', 'category': 'Urban Bus Corporation', 'hq': 'Chennai'},
        {'code': 'TNSTC-VPM', 'name': 'TNSTC - Villupuram Division', 'category': 'State Bus Corporation', 'hq': 'Villupuram'},
        {'code': 'TNSTC-CBE', 'name': 'TNSTC - Coimbatore Division', 'category': 'State Bus Corporation', 'hq': 'Coimbatore'},
        {'code': 'TNSTC-KUM', 'name': 'TNSTC - Kumbakonam Division', 'category': 'State Bus Corporation', 'hq': 'Kumbakonam'},
        {'code': 'TNSTC-MDU', 'name': 'TNSTC - Madurai Division', 'category': 'State Bus Corporation', 'hq': 'Madurai'},
        {'code': 'TNSTC-SLM', 'name': 'TNSTC - Salem Division', 'category': 'State Bus Corporation', 'hq': 'Salem'},
        {'code': 'TNSTC-TNV', 'name': 'TNSTC - Tirunelveli Division', 'category': 'State Bus Corporation', 'hq': 'Tirunelveli'},
        {'code': 'SETC', 'name': 'State Express Transport Corporation (SETC)', 'category': 'Interstate & Long Distance', 'hq': 'Chennai'},
        {'code': 'GCTP', 'name': 'Greater Chennai Traffic Police (GCTP)', 'category': 'Traffic Police & Road Safety', 'hq': 'Chennai'},
        {'code': 'TNSTA', 'name': 'Tamil Nadu State Transport Authority (TNSTA)', 'category': 'Transport Commissionerate & Regulatory', 'hq': 'Chennai'},
        {'code': 'TNPOLICE', 'name': 'Tamil Nadu Police - Traffic & Safety Cell', 'category': 'State Police Traffic Wing', 'hq': 'Chennai'}
    ]

    # Standard Advisory Types (Prompt Section 6)
    ADVISORY_TYPES = [
        'Route Diversion',
        'Bus Service Interruption',
        'Road Closure',
        'Temporary Route Change',
        'Service Delay',
        'Traffic Diversion',
        'Planned Maintenance',
        'Special Transport Announcement',
        'Other'
    ]

    # Standard Statuses (Prompt Section 7)
    STATUS_TYPES = [
        'Active',
        'Upcoming',
        'Expired',
        'Revised',
        'Withdrawn',
        'Unknown / Pending Verification'
    ]

    # Source Scraping Statuses (Prompt Section 13)
    SOURCE_STATUSES = [
        'Success',
        'Failed',
        'Pending',
        'No Supported Advisory Page Found',
        'Permission Required',
        'Temporarily Unavailable'
    ]

    # Scheduler settings
    SCHEDULER_ENABLED = os.getenv('SCHEDULER_ENABLED', 'True').lower() in ('true', '1', 't')
    SCHEDULER_INTERVAL_MINUTES = int(os.getenv('SCHEDULER_INTERVAL_MINUTES', 30))

    # Initial Admin Credentials
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'AdminTransit@2026')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@transitnotice.tn.gov.local')

    # Web Scraping Policy
    SCRAPER_USER_AGENT = os.getenv(
        'SCRAPER_USER_AGENT',
        'TransitNotice-Bot/1.0 (+http://localhost:5000/about; academic public transit monitor for Tamil Nadu)'
    )
    SCRAPER_REQUEST_TIMEOUT = int(os.getenv('SCRAPER_REQUEST_TIMEOUT', 15))


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SCHEDULER_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
