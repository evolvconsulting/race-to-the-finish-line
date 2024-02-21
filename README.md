
# Introduction
It may be challenging to present larger volumes of history in a succinct way that easily makes a point for the user.  Example: continually processing tasks or other automated processes that you would like to review.  In a situation when you have hundreds or more iterations of these items, to keep the user’s attention the output must be quick, short, and to the point.  Rather than having one scroll through line over line over line to understand historical trends, it makes more sense to provide a quick window into the previous iterations.  Presenting the information summarized to high may also create challenges trying to understand idiosyncrasies or inter relations within the continuous executions.   

This simple POC provide the ability to 
1. Setup a quick database with some sample data
2. Show what the base Streamlit data_editor widget can present the data
3. Show how using emojis instead can improve the user experience

# Setup
1. Login to your snowflake account and run the 2 files in the setup/data folder
   - item_hisotry.sql
   - emoji_content.sql
2. Create a settings.env file in the setup folder to store local env settings for your env
   - If you don't already have environment variables setup, add the following variables to this file and they will be established at runtime
     - emoji_env=local
     - emoji_snowflake_authenticator="externalbrowser if using SSO or None"
     - emoji_snowflake_user="your snowflake user name"
     - emoji_snowflake_pwd="your snowflake password or None if using SSO"
     - emoji_snowflake_account="your snowflake account"
     - emoji_snowflake_role="your snowflake role"
     - emoji_snowflake_warehouse="your snowflake warehouse"
     - emoji_snowflake_database=item_poc
     - emoji_snowflake_schema=history
   - Alternatively, you can set these env variables up manually in your local env for testing
3. run the following in the terminal window:
   - streamlit run setup/streamlit/ItemHistory.py - to show data with Streamlit data_editor widget options
   - streamlit run setup/streamlit/ItemHistoryEmoji.py - to show data with data-driven emoji options
  
# About the Author - Chris Schneider
Chris specializes in helping organizations derive insights from their data ecosystems. Having spent spent many years honing his craft in Data Architecture, focusing on Microsoft and Snowflake products, Chris has transformed businesses with scalable data architectures, approachable processes, and a keen eye on data quality. Using expertise in Data Management and industry experience in Finance, Lending, and Healthcare, he has built metadata-driven frameworks and data warehouses, and ensured that users leverage the appropriate tools to drive success.
