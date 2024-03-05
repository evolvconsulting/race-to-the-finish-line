
/*Load sample Metrics and their base configurations*/
merge into item_poc.history.metric t
using (
    select subject,name,metric_type,label,help_text,trend_normal,output_format,is_active
    from (
        values
        ('model','modelCount','sum','Total Model Count','The number of models processed in the time selected.','True','Decimal 0',True)
        ,('entity','entityCount','sum','Total Entity Count','The number of entities processed in the time selected.','True','Decimal 0',True)
        ,('attribute','attributeCount','sum','Total Attribute Count','The number of attributes processed in the time selected.','True','Decimal 0',True)
        ,('relationship','relationshipCount','sum','Total Relationship Count','The number of relationships processed in the time selected.','True','Decimal 0',True)
        ,('rule','ruleCount','sum','Total Rule Count','The number of rules processed in the time selected.','True','Decimal 0',True)
        
        ,('model','modelSuccessCount','sum','Total Successful Model Count','The number of models successfully processed in the time selected.','True','Decimal 0',True)
        ,('entity','entitySuccessCount','sum','Total Successful Entity Count','The number of entities successfully processed in the time selected.','True','Decimal 0',True)
        ,('attribute','attributeSuccessCount','sum','Total Successful Attribute Count','The number of attributes successfully processed in the time selected.','True','Decimal 0',True)
        ,('relationship','relationshipSuccessCount','sum','Total Successful Relationship Count','The number of relationships successfully processed in the time selected.','True','Decimal 0',True)
        ,('rule','ruleSuccessCount','sum','Total Successful Rule Count','The number of rules successfully processed in the time selected.','True','Decimal 0',True)

        ,('model','modelFailCount','sum','Total Failed Model Count','The number of models unsuccessfully processed in the time selected.','False','Decimal 0',True)
        ,('entity','entityFailCount','sum','Total Failed Entity Count','The number of entities unsuccessfully processed in the time selected.','False','Decimal 0',True)
        ,('attribute','attributeFailCount','sum','Total Failed Attribute Count','The number of attributes unsuccessfully processed in the time selected.','False','Decimal 0',True)
        ,('relationship','relationshipFailCount','sum','Total Failed Relationship Count','The number of relationships unsuccessfully processed in the time selected.','False','Decimal 0',True)
        ,('rule','ruleFailCount','sum','Total Failed Rule Count','The number of rules unsuccessfully processed in the time selected.','False','Decimal 0',True)

        ,('model','modelIncompleteCount','sum','Total Incomplete Model Count','The number of models neither successfully nor unsuccessfully processed in the time selected.','True','Decimal 0',True)
        ,('entity','entityIncompleteCount','sum','Total Incomplete Entity Count','The number of entities neither successfully nor unsuccessfully processed in the time selected.','True','Decimal 0',True)
        ,('attribute','attributeIncompleteCount','sum','Total Incomplete Attribute Count','The number of attributes neither successfully nor unsuccessfully processed in the time selected.','True','Decimal 0',True)
        ,('relationship','relationshipIncompleteCount','sum','Total Incomplete Relationship Count','The number of relationships neither successfully nor unsuccessfully processed in the time selected.','True','Decimal 0',True)
        ,('rule','ruleIncompleteCount','sum','Total Incomplete Rule Count','The number of rules neither successfully nor unsuccessfully processed in the time selected.','True','Decimal 0',True)

        ,('model','modelSuccessRate','rate','Model Successful Rate','The rate of successful models processed to all models processed in the time selected.','True','Percentage 2',True)
        ,('entity','entitySuccessRate','rate','Entity Successful Rate','The rate of successful entities processed to all entities processed in the time selected.','True','Percentage 2',True)
        ,('attribute','attributeSuccessRate','rate','Attribute Successful Rate','The rate of successful atttributes processed to all atttributes processed in the time selected.','True','Percentage 2',True)
        ,('relationship','relationshipSuccessRate','rate','Relationship Successful Rate','The rate of successful relationships processed to all relationships processed in the time selected.','True','Percentage 2',True)
        ,('rule','ruleSuccessRate','rate','Rule Successful Rate','The rate of successful rules processed to all rules processed in the time selected.','True','Percentage 2',True)

        ,('model','modelFailRate','rate','Model Failed Rate','The rate of Failed models processed to all models processed in the time selected.','False','Percentage 2',True)
        ,('entity','entityFailRate','rate','Entity Failed Rate','The rate of Failed entities processed to all entities processed in the time selected.','False','Percentage 2',True)
        ,('attribute','attributeFailRate','rate','Attribute Failed Rate','The rate of Failed atttributes processed to all atttributes processed in the time selected.','False','Percentage 2',True)
        ,('relationship','relationshipFailRate','rate','Relationship Failed Rate','The rate of Failed relationships processed to all relationships processed in the time selected.','False','Percentage 2',True)
        ,('rule','ruleFailRate','rate','Rule Failed Rate','The rate of Failed rules processed to all rules processed in the time selected.','False','Percentage 2',True)

        ,('model','modelIncompleteRate','rate','Model Incomplete Rate','The rate of incomplete models processed to all models processed in the time selected.','False','Percentage 2',True)
        ,('entity','entityIncompleteRate','rate','Entity Incomplete Rate','The rate of incomplete entities processed to all entities processed in the time selected.','False','Percentage 2',True)
        ,('attribute','attributeIncompleteRate','rate','Attribute Incomplete Rate','The rate of incomplete atttributes processed to all atttributes processed in the time selected.','False','Percentage 2',True)
        ,('relationship','relationshipIncompleteRate','rate','Relationship Incomplete Rate','The rate of incomplete relationships processed to all relationships processed in the time selected.','False','Percentage 2',True)
        ,('rule','ruleIncompleteRate','rate','Rule Incomplete Rate','The rate of incomplete rules processed to all rules processed in the time selected.','False','Percentage 2',True)

    ) x (subject,name,metric_type,label,help_text,trend_normal,output_format,is_active)
) s 
on s.subject = t.subject and s.name = t.name
when matched then update set t.metric_type = s.metric_type,t.label = s.label,t.help_text = s.help_text,t.trend_normal = s.trend_normal,t.output_format = s.output_format,t.is_active = s.is_active
when not matched then insert (subject,name,metric_type,label,help_text,trend_normal,output_format,is_active) values (s.subject,s.name,s.metric_type,s.label,s.help_text,s.trend_normal,s.output_format,s.is_active)
;