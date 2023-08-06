from simple_ddl_parser import DDLParser

ddl = r'''
CREATE EXTERNAL TABLE test (
job_id STRING COMMENT 'test\'s'
)
STORED AS PARQUET LOCATION 'hdfs://test'
'''
result = DDLParser(ddl).run(group_by_type=True, output_mode='hql')
import pprint

pprint.pprint(result)
