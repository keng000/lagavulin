
# To Run Test

## Create User and Database
```
(in mysql console)
CREATE DATABASE test;
CREATE USER test@localhost IDENTIFIED BY 'test';
GRANT ALL ON test.* TO test@localhost;
```

## Insert dummy data

```
mysql -u test -ptest < model/tests/dummy.sql

```

## Run Test
```
cd model/tests/
python -m unittest discover
```