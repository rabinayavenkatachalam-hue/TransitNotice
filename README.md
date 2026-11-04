# TransitNotice – Tamil Nadu Public Transport Service Update Tracker

[![Python 3.14](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![Flask 3.1](https://img.shields.io/badge/Flask-3.1-black.svg)](https://palletsprojects.com/p/flask/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)](https://www.sqlalchemy.org/)
[![Coverage](https://img.shields.io/badge/Districts-All%2038%20TN-brightgreen.svg)]()
[![Tests](https://img.shields.io/badge/Tests-13%20Passed-success.svg)]()

> A centralized, source-verified web application that collects publicly available transport service announcements, route diversions, road closures, and traffic advisories from permitted official Tamil Nadu government portals and displays them in a modern, responsive dashboard.

---

## 1. Project Introduction

Public transport commuters across Tamil Nadu frequently face unannounced route diversions, road closures (due to metro construction, flyover load tests, stormwater drainage works), and seasonal festival terminal relocations. Official announcements are traditionally scattered across regional transport corporation portals, traffic police updates, and district collector releases.

**TransitNotice** serves as an integrated state-wide platform covering **all 38 districts of Tamil Nadu**. It monitors official portals, extracts and cleans notices without inventing missing dates, tracks revisions with SHA-256 cryptographic content hashing, and visualizes service updates on a modern dashboard.

---

## 2. Key Features

- **Full Coverage of All 38 Tamil Nadu Districts:**
  Ariyalur, Chengalpattu, Chennai, Coimbatore, Cuddalore, Dharmapuri, Dindigul, Erode, Kallakurichi, Kancheepuram, Kanniyakumari, Karur, Krishnagiri, Madurai, Mayiladuthurai, Nagapattinam, Namakkal, Nilgiris, Perambalur, Pudukkottai, Ramanathapuram, Ranipet, Salem, Sivaganga, Tenkasi, Thanjavur, Theni, Thoothukudi, Tiruchirappalli, Tirunelveli, Tirupathur, Tiruppur, Tiruvallur, Tiruvannamalai, Tiruvarur, Vellore, Viluppuram, Virudhunagar.
- **Official Transport Authorities Supported:**
  - Metropolitan Transport Corporation (MTC) Chennai
  - Tamil Nadu State Transport Corporation (TNSTC) divisions (Villupuram, Coimbatore, Kumbakonam, Madurai, Salem, Tirunelveli)
  - State Express Transport Corporation (SETC Tamil Nadu)
  - Greater Chennai Traffic Police (GCTP)
  - Tamil Nadu State Transport Authority (TNSTA)
  - Tamil Nadu Police & District Administration Portals (NIC S3WaaS)
- **Categorization into 9 Official Notice Types:**
  1. Route Diversion
  2. Bus Service Interruption
  3. Road Closure
  4. Temporary Route Change
  5. Service Delay
  6. Traffic Diversion
  7. Planned Maintenance
  8. Special Transport Announcement
  9. Other
- **Automatic Status Calculation in Asia/Kolkata Timezone:**
  - `Active`: Currently in effect
  - `Upcoming`: Scheduled for future date
  - `Expired`: Concluded validity (an expired notice is **never** shown as active)
  - `Revised`: Content or validity modified by authority
  - `Withdrawn`: Officially cancelled/retracted
  - `Unknown / Pending Verification`: Inconclusive dates
- **Cryptographic Change Detection & Revision History:**
  - SHA-256 content hashing of normalized notice fields
  - Incremental `revision_id` tracking
  - Preserves full audit history of previous versions
  - Generates automatic change summaries (e.g., validity date extensions)
- **Multi-District & Multi-Route Association:**
  Notices can link to multiple affected districts and corridors (e.g., SETC express services from Kilambakkam KCBT affecting multiple southern districts).
- **Dedicated Data Sources Management:**
  Monitors health, permissions, last checked timestamps, last successful refresh, and detailed scraper execution logs. Features manual "Verify" buttons for individual sources and "Refresh All Sources".
- **In-Application Passenger Alerts:**
  Automated alert notifications with duplicate suppression whenever new or revised notices are detected.
- **Strict Separation of Demo / Test Data:**
  All demo and fixture notices are prominently labeled:
  `DEMO DATA – NOT AN OFFICIAL TRANSPORT ANNOUNCEMENT`.

---

## 3. Technology Stack

- **Backend:** Python 3.14, Flask 3.1
- **Database:** MySQL 8.x / MariaDB via SQLAlchemy (with seamless SQLite fallback for zero-configuration local runs)
- **Web Scraping:** Requests, BeautifulSoup4 (`html.parser`), `urllib.robotparser`
- **Timezone Management:** Standard library `zoneinfo` (`Asia/Kolkata`)
- **Job Scheduling:** APScheduler 3.11 (Background thread-safe interval worker)
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5.3, Chart.js 4.4, Bootstrap Icons
- **Testing:** PyTest 9.1

---

## 4. Database Design (10 Required System Tables)

The database strictly implements the 10 required relational tables:

1. `districts`: All 38 Tamil Nadu districts with codes, headquarters, and portal links.
2. `transport_authorities`: Operating corporations (MTC, TNSTC, SETC, Police).
3. `notices`: Core notices table storing normalized notices, validity, SHA-256 hash, and status.
4. `routes`: Transit corridors and bus lines with origin/destination.
5. `notice_routes`: Many-to-many junction linking notices to multiple routes.
6. `notice_districts`: Many-to-many junction linking notices to multiple districts.
7. `notice_history`: Historical snapshots of modified notices with diffs and timestamps.
8. `data_sources`: Registry of official sources with status, URLs, and health metrics.
9. `scraper_logs`: Execution audit records (records found, inserted, updated, skipped, duration).
10. `alert_logs`: In-app passenger notification logs generated from new/revised advisories.
- *(Auxiliary tables: `admin_users`, `subscribers`)*

Full SQL schema definitions are available in:
- `TransitNotice/migrations/schema_mysql.sql`
- `TransitNotice/database/schema.sql`

---

## 5. Installation & Setup

### Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Pip
- MySQL 8.x (optional; defaults to SQLite if MySQL is not configured)

### Step 1: Navigate to Project Directory
```powershell
cd TransitNotice
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Environment Configuration
Copy `.env.example` to `.env`:
```powershell
cp .env.example .env
```

Configuration variables in `.env`:
```ini
FLASK_ENV=development
PORT=5000
SECRET_KEY=transitnotice-tamilnadu-transport-secret-key-2026

# SQLite (Default out-of-the-box):
DATABASE_URL=sqlite:///transitnotice.db

# Or MySQL (Production / Local MySQL):
# DATABASE_URL=mysql+pymysql://root:password@localhost:3306/transitnotice_db

DEFAULT_DISTRICT=All Tamil Nadu
DEFAULT_STATE=Tamil Nadu
APP_TIMEZONE=Asia/Kolkata
SCHEDULER_ENABLED=True
SCHEDULER_INTERVAL_MINUTES=30
```

---

## 6. How to Run the Application

### Option A: From Workspace Root
```powershell
python run_transitnotice.py
```

### Option B: From `TransitNotice` Folder
```powershell
cd TransitNotice
python app.py
```

Open your web browser at:
👉 **http://127.0.0.1:5000**

---

## 7. How to Seed Initial Database Records

To populate the database with all 38 Tamil Nadu districts, operating transport authorities, known corridors, registered official sources, and demo notices:

```powershell
python TransitNotice/scripts/seed_data.py
```

Default Admin Credentials:
- **Username:** `admin`
- **Password:** `AdminTransit@2026`

---

## 8. How to Trigger Web Scraping

### Manual Scraping from Command Line
```powershell
python TransitNotice/scripts/run_scrapers.py
```

### Manual Scraping from Web UI
Navigate to **Data Sources** (`/sources`), where you can:
- Click **"Verify"** next to any individual source adapter.
- Click **"Refresh All Sources"** to run a complete verification cycle.

### Automated Background Refresh
The application starts APScheduler automatically on startup (configurable via `SCHEDULER_INTERVAL_MINUTES=30` in `.env`). The worker runs safely with concurrency locking to prevent overlapping jobs.

---

## 9. Running the Automated Test Suite

Run all 13 automated tests using PyTest:

```powershell
python -m pytest -c TransitNotice/pytest.ini TransitNotice/tests -v
```

### Test Coverage Highlights:
- `test_expired_notices_must_not_be_marked_active` (Criterion 1)
- `test_district_filters` (Criterion 2)
- `test_route_filters_and_multiple_routes` (Criteria 3 & 4)
- `test_extended_advisories_update_notice_history` (Criterion 5)
- `test_duplicate_notices_prevention` (Criterion 6)
- `test_missing_end_dates_handled_correctly` (Criterion 7)
- `test_timezone_calculations_reproducible` (Criterion 8)
- `test_failed_scraping_must_not_delete_old_data` (Criterion 9)
- `test_data_cleaner_normalizes_9_types` (Criterion 10)
- `test_one_failed_source_does_not_stop_others` (Criterion 11)
- `test_dashboard_statistics_match_db` (Criterion 12)

---

## 10. Official Source Inspection & Known Limitations

During live inspection of official Tamil Nadu government portals, the following source characteristics and limitations were verified:

1. **TNSTC / SETC Portal (`https://www.tnstc.in/OTRSOnline/`)**
   - *Status:* `No Supported Advisory Page Found`
   - *Findings:* This is primarily an online seat reservation portal. It does not publish structured disruption advisories. Booking details are intentionally excluded to prevent misleading passengers.
2. **Metropolitan Transport Corporation (MTC) Chennai (`https://mtcbus.tn.gov.in/`)**
   - *Status:* `Temporarily Unavailable`
   - *Findings:* Gateway connection timeouts occur periodically during external network requests. Handled gracefully via timeout limits and exponential backoff without crashing the application.
3. **Greater Chennai Traffic Police (`https://gctp.in/`)**
   - *Status:* `Success` / SPA Architecture
   - *Findings:* React-based SPA. The adapter inspects press announcements and road diversion notifications.
4. **Tamil Nadu State Transport Authority (`https://tnsta.gov.in/transport/`)**
   - *Status:* `Success`
   - *Findings:* Citizen transport services portal verified; provides RTO and regulatory updates.
5. **Tamil Nadu Government District Directory (`https://tn.nic.in/publication/list-of-websites/`)**
   - *Status:* `Success`
   - *Findings:* Central directory verified linking to S3WaaS NIC portals across all 38 districts (`{district}.nic.in`).
6. **Unified Multi-District Transport Test Adapter (DEMO)**
   - *Status:* `Success`
   - *Findings:* Provides structured test fixtures across all 38 districts with explicit `DEMO DATA` labeling to allow complete verification of charts, filters, and history tracking.
