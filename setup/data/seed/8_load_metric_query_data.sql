
/*Load sample Metrics and Query relationships*/
merge into item_poc.history.metric_query t
using (
    with map as (
        select subject, config_name, query_name, ordinal
        from (
            values
            ('model','modelFailCount','modelFailCountbyDay',1)
            ,('model','modelSuccessCount','modelSuccessCountbyDay',1)
            ,('model','modelIncompleteCount','modelIncompleteCountbyDay',1)
            ,('model','modelCount','modelCountbyDay',1)
            ,('model','modelSuccessRate','modelSuccessCountbyDay',1)
            ,('model','modelSuccessRate','modelCountbyDay',2)
            ,('model','modelFailRate','modelFailCountbyDay',1)
            ,('model','modelFailRate','modelCountbyDay',2)
            ,('model','modelIncompleteRate','modelIncompleteCountbyDay',1)
            ,('model','modelIncompleteRate','modelCountbyDay',2)
            ,('entity','entityFailCount','entityFailCountbyDay',1)
            ,('entity','entitySuccessCount','entitySuccessCountbyDay',1)
            ,('entity','entityIncompleteCount','entityIncompleteCountbyDay',1)
            ,('entity','entityCount','entityCountbyDay',1)
            ,('entity','entitySuccessRate','entitySuccessCountbyDay',1)
            ,('entity','entitySuccessRate','entityCountbyDay',2)
            ,('entity','entityFailRate','entityFailCountbyDay',1)
            ,('entity','entityFailRate','entityCountbyDay',2)
            ,('entity','entityIncompleteRate','entityIncompleteCountbyDay',1)
            ,('entity','entityIncompleteRate','entityCountbyDay',2)
            ,('attribute','attributeFailCount','attributeFailCountbyDay',1)
            ,('attribute','attributeSuccessCount','attributeSuccessCountbyDay',1)
            ,('attribute','attributeIncompleteCount','attributeIncompleteCountbyDay',1)
            ,('attribute','attributeCount','attributeCountbyDay',1)
            ,('attribute','attributeSuccessRate','attributeSuccessCountbyDay',1)
            ,('attribute','attributeSuccessRate','attributeCountbyDay',2)
            ,('attribute','attributeFailRate','attributeFailCountbyDay',1)
            ,('attribute','attributeFailRate','attributeCountbyDay',2)
            ,('attribute','attributeIncompleteRate','attributeIncompleteCountbyDay',1)
            ,('attribute','attributeIncompleteRate','attributeCountbyDay',2)            
            ,('relationship','relationshipFailCount','relationshipFailCountbyDay',1)
            ,('relationship','relationshipSuccessCount','relationshipSuccessCountbyDay',1)
            ,('relationship','relationshipIncompleteCount','relationshipIncompleteCountbyDay',1)
            ,('relationship','relationshipCount','relationshipCountbyDay',1)
            ,('relationship','relationshipSuccessRate','relationshipSuccessCountbyDay',1)
            ,('relationship','relationshipSuccessRate','relationshipCountbyDay',2)
            ,('relationship','relationshipFailRate','relationshipFailCountbyDay',1)
            ,('relationship','relationshipFailRate','relationshipCountbyDay',2)
            ,('relationship','relationshipIncompleteRate','relationshipIncompleteCountbyDay',1)
            ,('relationship','relationshipIncompleteRate','relationshipCountbyDay',2)
            ,('rule','ruleFailCount','ruleFailCountbyDay',1)
            ,('rule','ruleSuccessCount','ruleSuccessCountbyDay',1)
            ,('rule','ruleIncompleteCount','ruleIncompleteCountbyDay',1)
            ,('rule','ruleCount','ruleCountbyDay',1)  
            ,('rule','ruleSuccessRate','ruleSuccessCountbyDay',1)
            ,('rule','ruleSuccessRate','ruleCountbyDay',2)
            ,('rule','ruleFailRate','ruleFailCountbyDay',1)
            ,('rule','ruleFailRate','ruleCountbyDay',2)
            ,('rule','ruleIncompleteRate','ruleIncompleteCountbyDay',1)
            ,('rule','ruleIncompleteRate','ruleCountbyDay',2)
        ) x (subject, config_name, query_name, ordinal)
    )
    , config as (
        select metric_id,subject,name from item_poc.history.metric
    )
    , query as (
        select query_id,subject,name from item_poc.history.query  
    )
    select c.metric_id, q.query_id, m.ordinal
    from map m
    join config c on m.subject = c.subject and m.config_name = c.name
    join query q on m.subject = q.subject and m.query_name = q.name
) s 
on s.metric_id = t.metric_id and s.query_id = t.query_id
when matched then update set t.ordinal = s.ordinal
when not matched then insert (metric_id,query_id,ordinal) values (s.metric_id,s.query_id,s.ordinal)
;  