# Python metric producer / consumer

This is a small demonstraiton on how to measure system metrics and publish it via a Kafka topic for a consumer to read and persist to a database.

Creating metrics is a configuration option and adding more guage type metrics is reasonably straight forward. In `producer_config.py` you define a metric name and supply a function to provide the value for the metric.

```python
create_metric_functions(
    [
        ("cpu.percent", psutil.cpu_percent),
        ("disk.usage.percent", lambda: psutil.disk_usage("/").percent),
    ]
)
```

## Setup

Pipenv is used as the environment and dependency manager. To get started ensure you have `pipenv` and `python 3.7.5` installed. Clone this repository and run `pipenv install`

## Configuration

This project relies on code as configuration and there are 3 files to edit for config

- kafka_config.py
- consumer_config.py
- producer_config.py

Ensure that these are configured with the proper values for your Kafka and Postgres, MySql or Sqllite database

## Running

To execute run `pipenv run produce` or `pipenv run consume`

## Libraries and tools

For the most part I tried to use as much native Python as possible

- *black* Great code formatter to ensure code consistency
- *mypy* Static type checking for python
- *coverage* Code test coverage generator
- *pre-commit* Pre commit hooks library
- *psutil* Cool little library for measuring system utilization I found out about on StackOverflow many years ago: https://stackoverflow.com/questions/26573681/python-getting-upload-download-speeds My answer got the bounty though :D
- *kafka-python* Pure python Kafka client
- *peewee* Very simple ORM
- *psycopg2-binary* Libraries to connect to Postgres

## Guides

I needed a bit of guidence on this project to setup pre-commit hooks (on of my personal favorite feature of git). Why fail in CI when you can fail even earlier. THe following guide proved to be quite useful

https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/

Connecting to Kafka using certifciates and kafka python initially gave some problems, but the documentation was good and thee is a great guide on how to connect using SSL

https://github.com/dpkp/kafka-python

http://maximilianchrist.com/python/databases/2016/08/13/connect-to-apache-kafka-from-python-using-ssl.html

## If time was unlimited

- MyPy should be part of the pre-commit hooks
- Better ORM with database migrations. SqlAlchemy with Alembic is pretty good, but also takes a bit more time to configure.
- Better database schema. For now the consumer assumes everything is a gauge
- Better host identification, host name is potentially not unique enough.
- Integration testing. It would be interesting to do some BDD style tests around a system like this.
- More metrics. My focus was getting a basic system done for gauges
- More types of metrics. The system only supports gauges. Added support for timers and counters would be cool.
- Perhaps redoing everything in Go could be fun.

