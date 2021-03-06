#
# MLDB-869-select-expression.py
# datacratic, 2015
# this file is part of mldb. copyright 2015 datacratic. all rights reserved.
#

if False:
    mldb_wrapper = None
mldb = mldb_wrapper.wrap(mldb) # noqa

ds1 = mldb.create_dataset({
    'type': 'sparse.mutable',
    'id': 'dataset1'})

for i in xrange(10):
    ds1.record_row('row_' + str(i),
                   [['x', i, 0]])
ds1.commit()

try:
    mldb.get('/v1/query',
             q='SELECT 5 golden rings, 3 french hens FROM dataset1')
except mldb_wrapper.ResponseException as exc:
    mldb.log(exc.response)
else:
    assert False, 'should not be here'

#MLDB-835

result = mldb.get('/v1/query', q='SELECT x.* FROM dataset1 as x limit 3')

expected = [
    {
        "rowName": "row_8",
        "rowHash": "671b4a4dfa1563b5",
        "columns": [
            [
                "x",
                8,
                "1970-01-01T00:00:00Z"
            ]
        ]
    },
    {
        "rowName": "row_9",
        "rowHash": "0e832fd840141af8",
        "columns": [
            [
                "x",
                9,
                "1970-01-01T00:00:00Z"
            ]
        ]
    },
    {
        "rowName": "row_7",
        "rowHash": "54569df01a700c8b",
        "columns": [
            [
                "x",
                7,
                "1970-01-01T00:00:00Z"
            ]
        ]
    }
]

mldb.log(result.json())

assert result.json() == expected

#MLDB-958 rowhash printing when rowhash bigger than 7FFFFFFFFFFFFFFF
result = mldb.get('/v1/query',
                  q='SELECT rowHash() FROM dataset1 as x where x = 1')
mldb.log(result)
assert result.json()[0]['columns'][0][1] == 17390182720330652622

mldb.script.set_return('success')
