/*Create sample database for POC data*/
create database if not exists item_poc;

/*Create sample schema for POC data*/
create schema if not exists history;

/*Create sample table for POC data*/
create or replace table item_poc.history.item_type_history copy grants (
item_type_history_id integer autoincrement(1,1) 
,item_name varchar
,item_type varchar
,execution_timestamp timestamp_ltz
,execution_status varchar
);

/*Grant access to objects for POC data*/
grant usage on database item_poc to role native_app_demo;
grant usage on schema item_poc.history to role native_app_demo;
-- grant insert,select on table item_poc.history.item_type_history to role native_app_demo;
