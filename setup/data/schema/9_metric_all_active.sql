
/*Create a view to pull all of the configurations together with the appropriate meta data*/
create or replace view item_poc.history.metric_all_active as 
with base as (
    select
    mcq.metric_id
    ,mc.subject
    ,mc.name 
    ,mc.metric_type
    ,mc.label
    ,mc.help_text
    ,mc.trend_normal
    ,mc.output_format
    ,mq.data_function as data_function1
    from item_poc.history.metric_query mcq
    join item_poc.history.metric mc on mcq.metric_id = mc.metric_id and mc.is_active = True
    join item_poc.history.query mq on mcq.query_id = mq.query_id 
    where mcq.ordinal = 1
)
, secondary as (
    select 
    mcq.metric_id
    ,mq.data_function as data_function2
    from item_poc.history.metric_query mcq
    join item_poc.history.query mq on mcq.query_id = mq.query_id 
    where mcq.ordinal = 2
)
select
b.metric_id
,b.subject
,b.name 
,b.metric_type
,b.label
,b.help_text
,b.trend_normal
,b.output_format
,b.data_function1
,s.data_function2
from base b
left join secondary s on b.metric_id = s.metric_id
;

grant select on view item_poc.history.metric_all_active to role native_app_demo;