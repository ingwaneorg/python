import pandas as pd
import numpy as np
import json
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# SCENARIO: You're integrating customer data from 3 systems
# System A: CRM (CSV) - customer details
# System B: Orders (JSON) - transaction history  
# System C: Support (API simulation) - service interactions

# ===============================
# EXTRACT: Messy, realistic data
# ===============================

# System A: CRM data (CSV format) - has quality issues
crm_data = {
    'customer_id': [1001, 1002, '', 1004, 1005, 1006, 1007],
    'first_name': ['John', 'jane', 'MIKE', '', 'Sarah', 'Bob', 'alice'],
    'last_name': ['Smith', 'DOE', 'Johnson', 'Wilson', '', 'Brown', 'Cooper'],
    'email': ['john@email.com', 'JANE@EMAIL.COM', 'mike@invalid', 
              'sarah@email.com', 'bob@email.com', '', 'alice@email.com'],
    'phone': ['01234567890', '0987654321', 'invalid', '', '01111111111', 
              '02222222222', '03333333333'],
    'registration_date': ['2023-01-15', '2023/02/20', '15-03-2023', 
                         '', '2023-05-01', '2023-06-15', 'invalid'],
    'status': ['active', 'ACTIVE', 'inactive', 'Active', 'suspended', 'active', '']
}

# System B: Orders data (JSON format) - inconsistent structure
orders_json = '''
[
    {"order_id": 2001, "customer_id": 1001, "amount": 150.50, "date": "2023-03-01"},
    {"order_id": 2002, "cust_id": 1002, "total": 75.25, "order_date": "2023-03-15"},
    {"order_id": 2003, "customer_id": 1003, "amount": -50.00, "date": "2023-04-01"},
    {"order_id": 2004, "customer_id": 1001, "amount": 200.00, "date": ""},
    {"order_id": 2005, "customer_id": 1005, "amount": "invalid", "date": "2023-05-01"}
]
'''

# System C: Support tickets (API simulation)
support_data = {
    'ticket_id': [3001, 3002, 3003, 3004],
    'customer_ref': [1001, 1002, 1004, 1006],
    'issue_type': ['billing', 'technical', 'billing', 'general'],
    'priority': ['high', 'medium', 'low', 'medium'],
    'created_date': ['2023-04-01', '2023-04-15', '2023-05-01', '2023-05-15']
}

# ===============================
# TRANSFORM: Your challenge starts here!
# ===============================

def clean_crm_data(data):
    """
    Clean and standardise CRM data
    TODO: Implement data cleaning logic
    - Handle missing customer IDs
    - Standardise name formatting
    - Validate email addresses
    - Clean phone numbers
    - Parse various date formats
    - Standardise status values
    """
    df = pd.DataFrame(data)
    logger.info(f"CRM data loaded: {len(df)} records")
    
    # YOUR CODE HERE
    # Hint: You'll need to handle each column's specific issues
    
    return df

def process_orders_data(json_string):
    """
    Process orders from JSON with inconsistent schema
    TODO: Implement order processing logic
    - Handle different column names (customer_id vs cust_id)
    - Handle different amount fields (amount vs total)
    - Validate amounts (no negatives)
    - Handle missing dates
    - Standardise date formats
    """
    orders = json.loads(json_string)
    logger.info(f"Orders data loaded: {len(orders)} records")
    
    # YOUR CODE HERE
    # Hint: You'll need to normalise the schema first
    
    return pd.DataFrame(orders)

def enrich_with_support_data(customer_df, support_dict):
    """
    Enrich customer data with support ticket counts
    TODO: Implement enrichment logic
    - Count tickets per customer
    - Identify high-priority customers
    - Calculate days since last support contact
    """
    support_df = pd.DataFrame(support_dict)
    logger.info(f"Support data loaded: {len(support_df)} records")
    
    # YOUR CODE HERE
    # Hint: Use groupby and merge operations
    
    return customer_df

def create_customer_360_view(crm_df, orders_df, support_df):
    """
    Create a unified customer view
    TODO: Implement integration logic
    - Join all datasets
    - Calculate customer metrics (total spent, order frequency)
    - Create customer segments
    - Handle customers that exist in some systems but not others
    """
    logger.info("Creating unified customer view...")
    
    # YOUR CODE HERE
    # This is where real ETL thinking happens!
    
    return unified_df

def validate_final_data(df):
    """
    Perform data quality checks on final dataset
    TODO: Implement validation logic
    - Check for duplicates
    - Validate required fields
    - Check data consistency
    - Generate quality report
    """
    logger.info("Validating final dataset...")
    
    # YOUR CODE HERE
    # What business rules should we enforce?
    
    return True

# ===============================
# MAIN ETL PIPELINE
# ===============================

def run_etl_pipeline():
    """Main ETL orchestration function"""
    try:
        logger.info("Starting ETL pipeline...")
        
        # Extract
        logger.info("=== EXTRACT PHASE ===")
        crm_df = clean_crm_data(crm_data)
        orders_df = process_orders_data(orders_json)
        support_df = pd.DataFrame(support_data)
        
        # Transform
        logger.info("=== TRANSFORM PHASE ===")
        enriched_crm = enrich_with_support_data(crm_df, support_data)
        final_df = create_customer_360_view(enriched_crm, orders_df, support_df)
        
        # Validate
        logger.info("=== VALIDATION PHASE ===")
        if validate_final_data(final_df):
            logger.info("Data validation passed!")
        
        # Load
        logger.info("=== LOAD PHASE ===")
        output_file = f"customer_360_view_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        final_df.to_csv(output_file, index=False)
        logger.info(f"Pipeline completed! Output saved to {output_file}")
        
        return final_df
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise

# ===============================
# DISCUSSION QUESTIONS
# ===============================
"""
After completing the ETL pipeline, discuss:

1. Data Quality Issues:
   - What types of data quality problems did you encounter?
   - How did you decide what to do with missing/invalid data?
   - What business rules did you implement?

2. Integration Challenges:
   - How did you handle schema differences between systems?
   - What assumptions did you make about data relationships?
   - How would you handle new data sources being added?

3. Scalability Considerations:
   - What would happen if each dataset had millions of records?
   - How would you monitor this pipeline in production?
   - What would you do if the API was temporarily unavailable?

4. Business Impact:
   - What insights can stakeholders gain from the unified view?
   - How would you present data quality issues to management?
   - What metrics would you track for pipeline success?
"""

if __name__ == "__main__":
    # Uncomment to run the pipeline
    # result = run_etl_pipeline()
    # print(result.head())
    
    # For now, just show the messy data
    print("=== SAMPLE MESSY DATA ===")
    print("CRM Data Issues:")
    print(pd.DataFrame(crm_data))
    print("\nOrders JSON Issues:")
    print(orders_json)
    print("\nYour mission: Clean this up and create a unified customer view!")
