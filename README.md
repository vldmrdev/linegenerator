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
 