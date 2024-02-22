/*Create sample database for POC data*/
create database if not exists item_poc;

/*Create sample schema for POC data*/
create schema if not exists history;

/*Create sample table for POC data*/
create or replace table item_poc.history.item_history copy grants (
item_history_id integer autoincrement(1,1) 
,item_name varchar
,execution_timestamp timestamp_ltz
,execution_status varchar
);

/*Grant access to objects for POC data*/
grant usage on database item_poc to role native_app_demo;
grant usage on schema item_poc.history to role native_app_demo;
grant insert,select on table item_poc.history.item_history to role native_app_demo;

/*Load sample data with output for all dates for the last year to establish timeline within sample POC data*/
insert into item_poc.history.item_history (item_name,execution_timestamp,execution_status)
with last_year as (
    select 
    dateadd(year,-1,current_timestamp()) as start_execution_timestamp
    ,current_timestamp() as end_execution_timestamp
)
, last as (
    select 
    max(end_execution_timestamp) as execution_timestamp
    from last_year
)
, each as (
    select 
    start_execution_timestamp as execution_timestamp
    from last_year
    union all
    select 
    dateadd(day,1,execution_timestamp) as execution_timestamp
    from each
    where execution_timestamp < (select execution_timestamp from last)
)
, each_row as (
    select 
    execution_timestamp
    ,row_number() over(order by execution_timestamp) as date_number
    from each
)
, items as (
    select item_name
    from (
        values
        ('Failed Item')
        ,('Successful Item')
        ,('Partially Successful Item')
        ,('Failed Last Run Item')
        ,('Failed First Run Item')
        ,('Successful Trend Item')
        ,('Failed Trend Item')
        ,('Incomplete Intermittent Item')
        ,('Failed Intermittent Item')
        ,('Successful Intermittent Item')
        ) x (item_name)
)
select 
i.item_name
,r.execution_timestamp
,case 
    when item_name = 'Failed Item' then 'Failed'
    when item_name = 'Successful Item' then 'Successful'  
    when item_name =  'Partially Successful Item' and r.date_number % 2 > 0 then 'Successful'
    when item_name =  'Partially Successful Item' and r.date_number % 2 = 0 then 'Failed'
    when item_name =  'Failed Last Run Item' and r.date_number = (select max(date_number) from each_row) then 'Failed'
    when item_name =  'Failed Last Run Item' and r.date_number < (select max(date_number) from each_row) then 'Successful'
    when item_name =  'Failed First Run Item' and r.date_number = 1 then 'Failed'
    when item_name =  'Failed First Run Item' and r.date_number > 1 then 'Successful'
    when item_name =  'Successful Trend Item' and r.date_number % 10 > 0 then 'Successful'
    when item_name =  'Successful Trend Item' and r.date_number % 10 = 0 then 'Failed'
    when item_name =  'Failed Trend Item' and r.date_number % 10 > 0 then 'Failed'
    when item_name =  'Failed Trend Item' and r.date_number % 10 = 0 then 'Successful'
    when item_name =  'SuccesFailedsful Trend Item' and r.date_number % 10 = 0 then 'Successful'
    when item_name =  'Incomplete Intermittent Item' and r.date_number % 4 = 0 then 'Incomplete'
    when item_name =  'Incomplete Intermittent Item' and r.date_number % 4 > 0 then 'Successful'
    when item_name =  'Failed Intermittent Item' and r.date_number % 4 = 0 then 'Failed'
    when item_name =  'Failed Intermittent Item' and r.date_number % 4 > 0 then 'Successful'
    when item_name =  'Successful Intermittent Item' and r.date_number % 4 = 0 then 'Successful'
    when item_name =  'Successful Intermittent Item' and r.date_number % 6 = 0 then 'Incomplete'
    when item_name =  'Successful Intermittent Item' and r.date_number % 1 = 0 then 'Failed'
    else 'Unknown'
end as execution_status
from items i
join each_row r
;