# Changelog

## v1.0.28 (2019-05-15)
**dataset.count method**

```python
dataset = api.get_dataset('us30')
data_count = ds.count(
    start_date='2018-01-05 18:00:00',
    end_date='2018-01-05 18:01:00',
)
# {'count': 11, 'stories': 10, 'entities': 6}

``` 
