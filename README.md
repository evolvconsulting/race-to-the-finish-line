
# Introduction
Imagine that each time a user came up with a new measurement to report on, they had to wait days or even weeks for an SDLC to run the requirement through its paces before being able to see the metric in their dashboard.  This project introduces a simple but effective solution improving speed to market with your application by introducing a data-driven approach and framework to adding metrics to your dashboard.  

This simple POC provides the ability to 
1. Setup a quick database with some sample data
2. Show how to quickly add new metrics without having to redeploy the app

# Setup
1. Login to your snowflake account and run the the sql files from the setup/data/shcema folder to create the sample data tables. 
   - 1_item_type_history.sql - setup table to store historical run of items by various types
   - 3_metric.sql - setup table to store metrics and configurations used in the app by Streamlit
   - 5_query.sql - setup table to store queries to be referenced by metrics providing a simple output contract of: 
      - Value (int)
      - Historical_Days (int)
   - 7_metric_query.sql - setup table to store associations of metrics and their related queries
   - 9_metric_all.sql - create a view to bring all of this data together for the Streamlit app

1. Then run the sql files from the setup/data/seed folder to load the sample application data.
   
   - setup/data/schema/
      - 2_load_item_type_data.sql - load sample items and execution history
      - 4_load_metric_data.sql - load sample metrics
      - 6_load_query_data.sql - load sample queries
      - 8_load_metric_query_data.sql = load sample metric-query relationships

1. Create a settings.env file in the setup folder to store local env settings for your env so the app can log into your Snowflake account.
   - If you don't already have environment variables setup, add the following variables to this file and they will be established at runtime
     - snowflake_env=local
     - snowflake_authenticator="externalbrowser if using SSO or None"
     - snowflake_user="your snowflake user name"
     - snowflake_pwd="your snowflake password or None if using SSO"
     - snowflake_account="your snowflake account"
     - snowflake_role="your snowflake role"
     - snowflake_warehouse="your snowflake warehouse"
     - snowflake_database=item_poc
     - snowflake_schema=history
   - Alternatively, you can set these env variables up manually in your local env for testing
1. run the following in the terminal window:
   - streamlit run setup/streamlit/Home.py - Click on Data Driven Metrics to show metric loading metrics from data objects stored in the database
  
# About the Author - Chris Schneider
Chris specializes in helping organizations derive insights from their data ecosystems. Having spent spent many years honing his craft in Data Architecture, focusing on Microsoft and Snowflake products, Chris has transformed businesses with scalable data architectures, approachable processes, and a keen eye on data quality. Using expertise in Data Management and industry experience in Finance, Lending, and Healthcare, he has built metadata-driven frameworks and data warehouses, and ensured that users leverage the appropriate tools to drive success.

