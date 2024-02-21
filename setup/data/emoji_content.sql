/*Create sample database for POC data*/
create database if not exists item_poc;

/*Create sample schema for POC data*/
create schema if not exists history;

/*Create sample table for POC emoji output by status*/
create or replace table item_poc.history.execution_status copy grants (
execution_status_id integer autoincrement(1,1) 
,emoji_group varchar
,execution_status varchar
,emoji_content varchar
);

/*Grant access to objects for POC data*/
grant usage on database item_poc to role native_app_demo;
grant usage on schema item_poc.history to role native_app_demo;
grant insert,select on table item_poc.history.execution_status to role native_app_demo;

/*Load Initial data for this table*/
insert into item_poc.history.execution_status (emoji_group,execution_status,emoji_content)
select 
emoji_group
,execution_status
,emoji_content
from (
    values
    ('Pattern Display','Failed',':x:')
    ,('Pattern Display','Successful',':heavy_check_mark:')
    ,('Pattern Display','Incomplete',':warning:')
    ,('Stoplight Display','Failed',':large_red_square:')
    ,('Stoplight Display','Successful',':large_green_square:')
    ,('Stoplight Display','Incomplete',':large_yellow_square:')

) x (emoji_group,execution_status,emoji_content)
;
