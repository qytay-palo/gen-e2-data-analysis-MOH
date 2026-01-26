# Quick Start Guide - Automated Data Extraction

Get up and running with the MOH data extraction system in minutes.

## Prerequisites Check

```bash
# 1. Verify Python version (3.8+)
python --version

# 2. Verify pip
pip --version
```

## Setup (5 minutes)

### Step 1: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### Step 2: Configure Database Access

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

Minimal `.env` configuration:
```bash
DB_HOST=your-database-host
DB_PORT=5432
DB_NAME=polyclinic_db
DB_USER=your-username
DB_PASSWORD=your-password
```

### Step 3: Test Connection

```bash
# Quick connection test
python -c "from src.data_processing.db_connector import DatabaseConnector; \
  dc = DatabaseConnector(); \
  print('✓ Connected!' if dc.test_connection() else '✗ Connection failed')"
```

## First Extraction (2 minutes)

### Option A: Extract One Source (Fastest)

```bash
# Extract patient data from last 7 days
python scripts/run_extraction.py \
  --sources patients \
  --last-n-days 7
```

### Option B: Extract Multiple Sources

```bash
# Extract attendance and diagnosis data
python scripts/run_extraction.py \
  --sources attendances diagnoses \
  --last-n-days 7
```

### Option C: Extract All Sources

```bash
# Full incremental extraction
python scripts/run_extraction.py \
  --sources all \
  --incremental
```

## Check Results

```bash
# View extraction logs
tail -n 50 logs/extraction.log

# Check output files
ls -lh data/processed/

# View execution summary
cat results/metrics/etl_summary_*.json | python -m json.tool
```

## Common First-Run Commands

```bash
# Test with small dataset (yesterday only)
python scripts/run_extraction.py --sources patients --last-n-days 1

# Extract with validation details
python scripts/run_extraction.py --sources attendances --log-level DEBUG

# Extract specific date range
python scripts/run_extraction.py \
  --sources diagnoses \
  --start-date 2025-01-01 \
  --end-date 2025-01-31

# Stop if data quality issues found
python scripts/run_extraction.py \
  --sources all \
  --stop-on-validation-failure
```

## Setup Automation (Optional)

### Start Scheduler

```bash
# Run in foreground (Ctrl+C to stop)
python scripts/run_scheduler.py

# Run in background (Linux/macOS)
nohup python scripts/run_scheduler.py > scheduler.log 2>&1 &

# Check scheduler is running
ps aux | grep run_scheduler
```

### Schedule Configuration

Edit `config/database.yml`:

```yaml
schedule:
  daily:
    enabled: true
    time: "02:00"  # 2 AM daily
    extractions:
      - attendances
      - diagnoses
```

## Verify Everything Works

Run this verification script:

```bash
# Create verification script
cat > verify_setup.py << 'EOF'
from src.data_processing.db_connector import DatabaseConnector
from src.data_processing.data_extractor import DataExtractor
from src.utils.logging_config import setup_logging

setup_logging(log_level='INFO')

# Test 1: Database connection
print("1. Testing database connection...")
dc = DatabaseConnector()
assert dc.test_connection(), "❌ Connection failed"
print("   ✓ Database connected")

# Test 2: Configuration load
print("2. Testing configuration...")
extractor = DataExtractor()
print(f"   ✓ Loaded {len(extractor.data_sources)} data sources")

# Test 3: Checkpoint system
print("3. Testing checkpoint system...")
checkpoint = extractor.get_last_extraction_date('attendances')
print(f"   ✓ Checkpoint system working (last: {checkpoint or 'never'})")

print("\n✓ All systems operational!")
EOF

python verify_setup.py
```

## Next Steps

1. **Review Configuration**: Check `config/database.yml` and `config/queries.yml`
2. **Customize Queries**: Modify SQL templates in `config/queries.yml` to match your schema
3. **Run Full Extraction**: Extract all data sources
4. **Set Up Automation**: Enable scheduled jobs
5. **Monitor Logs**: Regularly check `logs/` directory

## Troubleshooting

### Connection Issues

```bash
# Check environment variables loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); \
  print(f'DB_HOST: {os.getenv(\"DB_HOST\")}')"

# Test direct connection
python -c "import psycopg2; \
  conn = psycopg2.connect(host='YOUR_HOST', port=5432, \
  database='YOUR_DB', user='YOUR_USER', password='YOUR_PASS'); \
  print('✓ Direct connection successful')"
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Verify installations
pip list | grep -E "pandas|pyarrow|pyyaml|psycopg2"
```

### Permission Errors

```bash
# Create required directories
mkdir -p data/{raw,processed,interim,external}
mkdir -p logs results/metrics

# Set permissions
chmod -R 755 data logs results
```

## Quick Reference

### Command Patterns

```bash
# Basic pattern
python scripts/run_extraction.py --sources <SOURCE> --last-n-days <N>

# With date range
python scripts/run_extraction.py --sources <SOURCE> \
  --start-date YYYY-MM-DD --end-date YYYY-MM-DD

# Full extraction (not incremental)
python scripts/run_extraction.py --sources <SOURCE> --full

# Debug mode
python scripts/run_extraction.py --sources <SOURCE> --log-level DEBUG
```

### Available Sources

Common sources (check `config/database.yml` for full list):
- `attendances` - Patient visits
- `patients` - Demographics
- `diagnoses` - Diagnosis records
- `procedures` - Procedures/treatments
- `medications` - Prescriptions
- `lab_results` - Lab test results
- `polyclinics` - Facility reference data
- `conditions` - Disease reference data

### Log Files

- `logs/extraction.log` - Main extraction activities
- `logs/errors.log` - Errors only
- `logs/audit.log` - Structured audit trail

### Output Locations

- `data/raw/` - Raw extracted data
- `data/processed/` - Cleaned, ready-to-analyze data
- `results/metrics/` - Execution summaries and metrics

## Getting Help

1. **Check logs**: `tail -f logs/extraction.log`
2. **Review documentation**: See `docs/DATA_EXTRACTION_GUIDE.md`
3. **Debug mode**: Add `--log-level DEBUG` to any command
4. **Verify configuration**: Ensure `config/*.yml` files are correct

---

**Time to First Extraction**: ~5 minutes  
**Recommended First Run**: `python scripts/run_extraction.py --sources patients --last-n-days 1`
