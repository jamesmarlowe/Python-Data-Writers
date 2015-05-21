Data-Writers
=======================

Write to multiple databases and formats easily from python.

This project is useful in any scenario where you need to write some data in a 
readable manner quickly and easily.

It can be used to write to:
* csv
* sqlite
* mysql
* redis

Example usage is as simple as:

```
DataWriter(writer='csv').save([{"column1":"row1-item1", "column2":"row1-item2"},
                               {"column1":"row2-item1", "column2":"row2-item2"},
                               {"column1":"row3-item1", "column2":"row3-item2"}])
```

source code available at: https://github.com/jamesmarlowe/Python-Data-Writers
