/*Create sample database for POC data*/
create database if not exists item_poc;

/*Create sample schema for POC data*/
create schema if not exists history;

/*Create sample table for POC data*/
create or replace table item_poc.history.query copy grants (
query_id integer autoincrement(1,1)
,subject varchar 
,name varchar
,data_function varchar
);

/*Grant access to objects for POC data*/
grant usage on database item_poc to role native_app_demo;
grant usage on schema item_poc.history to role native_app_demo;
grant select on table item_poc.history.query to role native_app_demo;