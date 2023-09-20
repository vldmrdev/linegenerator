### Log generator:

This is a simple sample-webserver-logs-generator for testing your scripts and algorithms.

### Hot to use examples:

#### Get help:

`python3 log-generator.py --help`

```
Usage: log-generator.py [OPTIONS]

Options:
  --lines INTEGER        Lines count
  --output TEXT          Output file
  --templates_path TEXT  Templates directory path
  --template TEXT        Template file
  --help                 Show this message and exit.

```

#### Use example:

`python3 log-generator.py --output test.txt --template web-server-template.txt --lines 10`
 

#### Template variables:

`{{ date }} - date and time, example [2022-07-11 21:55:00]`

`{{ uri }} - web site URL, example www.gooogle.com`

`{{ port }} - random choice from ports list`

`{{ ip_v4 }} - ipv4 generated from Faker`

`{{ method }} - HTTP methods generated from Faker`

`{{ http_code }}  - random choice from HTTP response codes list`
