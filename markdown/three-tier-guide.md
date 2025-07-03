# Three-Tier Implementation Guide for Day 1

## Implementation Strategy

**Tier Selection Approach:**
- **L1 (Beginners)**: "I'm new to Python - give me guided steps"
- **L2 (Intermediate)**: "I can code but need some direction"  
- **L3 (Advanced)**: "I want to build it properly from scratch"

## Morning Lab: Customer Data Cleaning

### **L1 Version: Guided Jupyter Notebook**
```python
# STEP 1: Load the messy data (code provided)
import pandas as pd
df = pd.DataFrame(messy_customer_data)

# STEP 2: Clean customer IDs (example provided)
df_clean = df[df['customer_id'] != ''].copy()

# TODO: Clean the names using .str.title()
# HINT: df['first_name'] = df['first_name'].str.title()
df['first_name'] = _______________

# TODO: Validate email addresses
# HINT: Use the provided is_valid_email function
df['email_valid'] = df['email'].apply(_______________)

# Continue with guided TODOs for each step...
```

**Characteristics:**
- Pre-written functions provided
- Step-by-step guidance with hints
- Focus on understanding concepts
- Can complete successfully with minimal Python experience

### **L2 Version: Semi-Independent Jupyter**
```python
# TASK 1: Data Quality Investigation
# TODO: Load the customer data and identify quality issues
# TODO: Create a summary of what needs fixing

# TASK 2: Data Cleaning Pipeline
# TODO: Implement cleaning functions for:
# - Customer ID validation
# - Name standardisation  
# - Email validation
# - Phone number cleaning
# - Status normalisation

def clean_customer_data(df):
    """
    Implement comprehensive data cleaning
    Requirements:
    - Handle missing values appropriately
    - Standardise formats consistently
    - Validate business rules
    - Return quality metrics
    """
    # Your implementation here
    pass

# TASK 3: Quality Reporting
# TODO: Create a business-ready quality report
```

**Characteristics:**
- Broader requirements, less specific guidance
- Must implement logic themselves
- Need to make design decisions
- Error handling challenges included

### **L3 Version: VS Code + Production Patterns**
```python
# customer_etl.py
"""
Production Customer Data ETL Pipeline
Author: [Student Name]
Date: [Current Date]

Requirements:
- Modular, testable code structure
- Comprehensive error handling
- Logging and monitoring
- Configuration management
- Data validation framework
"""

import logging
import configparser
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class DataQualityMetrics:
    """Track data quality throughout pipeline"""
    total_records: int
    valid_records: int
    quality_score: float
    issues_found: List[str]

class CustomerDataCleaner:
    """Production-ready customer data cleaning pipeline"""
    
    def __init__(self, config_file: str):
        self.config = self._load_config(config_file)
        self.logger = self._setup_logging()
        
    def process_pipeline(self, input_file: str) -> DataQualityMetrics:
        """Execute complete ETL pipeline with monitoring"""
        # Students build complete production pipeline
        pass
        
    def _load_config(self, config_file: str) -> configparser.ConfigParser:
        """Load pipeline configuration"""
        pass
        
    def _setup_logging(self) -> logging.Logger:
        """Configure structured logging"""
        pass
```

**L3 Requirements:**
- Object-oriented design
- Configuration files (config.ini)
- Comprehensive logging
- Unit tests (test_customer_etl.py)
- Error handling with custom exceptions
- Performance monitoring
- Documentation strings

---

## Afternoon Lab: API Enrichment

### **L1 Version: Step-by-Step API Integration**
```python
# STEP 1: Test single API call (code provided)
def test_postcode_api():
    response = requests.get("https://api.postcodes.io/postcodes/SW1A1AA")
    print(response.json())

# STEP 2: Complete the enrichment function
def enrich_postcode(postcode):
    """
    TODO: Complete this function
    HINT: Clean the postcode, call the API, return the data
    """
    clean_postcode = postcode.replace(' ', '')
    # TODO: Make the API call
    url = f"https://api.postcodes.io/postcodes/{clean_postcode}"
    response = requests.get(____________)
    
    # TODO: Handle the response
    if response.status_code == 200:
        data = response.json()
        return {
            'region': data['result']['region'],
            # TODO: Add more fields
        }

# STEP 3: Apply to all customers (loop provided)
for index, row in df.iterrows():
    # TODO: Call your enrichment function
    result = enrich_postcode(row['postcode'])
```

### **L2 Version: Multi-Source Integration Challenge**
```python
# CHALLENGE: Build multi-source enrichment pipeline
# 
# Requirements:
# 1. Postcode enrichment (UK Postcodes API)
# 2. Company enrichment (simulate business data lookup)
# 3. Risk calculation (combine geographic + business factors)
# 4. Error handling for API failures
# 5. Performance considerations (rate limiting)

class DataEnrichmentPipeline:
    def __init__(self):
        self.success_count = 0
        self.failure_count = 0
        
    def enrich_customer_data(self, df_customers):
        """
        TODO: Implement comprehensive enrichment
        - Handle multiple APIs
        - Graceful failure handling
        - Progress tracking
        - Quality metrics
        """
        pass
        
    def calculate_risk_score(self, customer_data):
        """
        TODO: Implement business logic
        - Geographic risk factors
        - Company size considerations
        - Account status impact
        - Data completeness scoring
        """
        pass
```

### **L3 Version: Enterprise ETL Architecture**
```python
# etl_pipeline.py
"""
Enterprise Customer Enrichment Pipeline
- Async API calls for performance
- Circuit breaker pattern for resilience
- Comprehensive monitoring and alerting
- Database connection pooling
- Configuration-driven business rules
"""

import asyncio
import aiohttp
from typing import AsyncIterator
from dataclasses import dataclass
from enum import Enum

class EnrichmentStatus(Enum):
    SUCCESS = "success"
    PARTIAL = "partial" 
    FAILED = "failed"

@dataclass
class EnrichmentResult:
    customer_id: int
    status: EnrichmentStatus
    data: Dict
    errors: List[str]
    processing_time: float

class AsyncCustomerEnricher:
    """Production async enrichment pipeline"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.session = None
        self.circuit_breaker = CircuitBreaker()
        
    async def process_batch(self, customers: List[Dict]) -> List[EnrichmentResult]:
        """Process customer batch with async API calls"""
        pass
        
    async def enrich_single_customer(self, customer: Dict) -> EnrichmentResult:
        """Enrich individual customer with error handling"""
        pass
```

---

## Database Loading Component

### **L1 Version: Simple Database Insert**
```python
# STEP 1: Connect to database (connection string provided)
import pyodbc

connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=customer_db;Trusted_Connection=yes;'
db = pyodbc.connect(connection_string)

# STEP 2: Create table (SQL provided)
cursor = db.cursor()
cursor.execute("""
CREATE TABLE enriched_customers (
    customer_id INT PRIMARY KEY,
    first_name NVARCHAR(50),
    last_name NVARCHAR(50),
    email NVARCHAR(100),
    region NVARCHAR(50),
    risk_score NVARCHAR(20)
)
""")

# STEP 3: Insert data (loop provided)
for index, row in df_final.iterrows():
    # TODO: Complete the INSERT statement
    insert_sql = "INSERT INTO enriched_customers VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(insert_sql, (
        row['customer_id'],
        # TODO: Add the remaining fields
    ))
```

### **L2 Version: Robust Database Operations**
```python
# CHALLENGE: Implement production database loading
# 
# Requirements:
# 1. Upsert logic (INSERT or UPDATE if exists)
# 2. Batch processing for performance
# 3. Transaction management
# 4. Error handling and rollback
# 5. Data validation before insert

class DatabaseLoader:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        
    def load_enriched_customers(self, df_customers):
        """
        TODO: Implement robust database loading
        - Check for existing records
        - Batch insert for performance
        - Handle constraint violations
        - Provide loading metrics
        """
        pass
        
    def validate_data_before_load(self, df):
        """
        TODO: Pre-load validation
        - Required field checks
        - Data type validation
        - Business rule compliance
        """
        pass
```

### **L3 Version: Enterprise Data Loading**
```python
# database_operations.py
"""
Enterprise database operations with:
- Connection pooling
- Retry logic with exponential backoff
- Dead letter queues for failed records
- Audit logging
- Performance monitoring
"""

from contextlib import contextmanager
import time
from typing import Generator

class EnterpriseDBLoader:
    """Production database loading with enterprise patterns"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.connection_pool = self._create_pool()
        self.audit_logger = AuditLogger()
        self.metrics_collector = MetricsCollector()
        
    @contextmanager
    def get_connection(self) -> Generator[pyodbc.Connection, None, None]:
        """Connection pool management with automatic cleanup"""
        pass
        
    def bulk_upsert_with_retry(self, records: List[Dict]) -> LoadResult:
        """Enterprise bulk loading with comprehensive error handling"""
        pass
```

---

## Instructor Guidance

### **Tier Selection Process**
1. **Start of day**: Brief explanation of three tiers
2. **Self-selection**: Let learners choose their comfort level
3. **Flexibility**: Allow switching between tiers during the day
4. **Support strategy**: 
   - L1: Direct guidance and pair programming
   - L2: Conceptual help and design review
   - L3: Architecture discussion and code review

### **Assessment Approach**
- **All tiers achieve same learning objectives**
- **Different evidence of competence**:
  - L1: Successful completion with understanding
  - L2: Independent problem-solving and design decisions
  - L3: Production-ready code and architectural thinking

### **Time Management**
- **L1 learners**: May finish activities faster (more guidance)
- **L3 learners**: May need more time (building from scratch)
- **Flexible pairing**: L3 learners can mentor L1/L2 if they finish early

This three-tier approach ensures everyone succeeds while allowing natural stretch and challenge based on experience level.
