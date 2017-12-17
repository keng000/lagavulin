
# To Run Test
## Insert dummy data
```
mysql -u root -p -e "CREATE DATABASE test"
mysql -u root -p test < tests/dummy.sql
```

## Run Test
```
python -m unittest discover tests
```