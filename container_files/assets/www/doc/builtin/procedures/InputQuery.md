# Input Query Specifications

When a procedure accepts data as input, the data can be specified in one of two ways:

* by a string representing an [SQL query](../sql/Sql.md).  For example,

```
SELECT column1, column2 FROM dataset1 WHERE column1 > column2 ORDER BY column1
```

where `column1` and `column2` refer to columns in a pre-existing dataset with id `dataset1`.

* by a json object representing a [Dataset Configuration](../datasets/DatasetConfig.md) and an [SQL query](../sql/Sql.md).  For example the json object

```
{
  "select" : "column1, column2",
  "from" : {
    "id" : "dataset1"
  },
  "where" : "column1 > column2",
  "orderBy" : "column1"
}
```

is equivalent to the query above on the pre-existing dataset with id `dataset1`.  In addition, this representation
offers the ability to first create a dataset.  In this example,

```
{
  "select" : "column1, column2",
  "from" : {
    "id" : "dataset1",
    "type" : "text.csv.tabular",
    "params" : {
        "dataFileUrl" : "http://example.com/myfile.csv"
      }
  },
  "where" : "column1 > column2",
  "orderBy" : "column1"
}
```

the dataset `dataset1` is first created by loading a csv file.

<div id=contrained-data-spec>
## Limitations

For performance reason, some procedures do not accept a full SQL query as their data input.  For details on what
is supported for a given procedure, read its documentation.

