# Py4Geo

Is still experimental...

## Description

This module implements a [DAL](https://github.com/web2py/pydal) database model
inspired to the OpenstreetMap database, optimized for storing informations, with
a very flexible json structure able to host and model any kind of data.

It supports OpenstreetMap and geojson as main data structures for import.

## System requirements

* [PostgreSQL](https://www.postgresql.org/)
* [PostGIS](https://postgis.net/)

### Optional requirements

* [H3](https://eng.uber.com/h3/)
    - [Pgh3](https://github.com/dlr-eoc/pgh3)
    - [Install notes](https://github.com/manuelep/py4geo/wiki/Doc)

## Install

```sh
pip install py4geo
```

## Use Py4geo in custom [py4web](http://py4web.com/) applications

Py4web applications are nothing more than native [python modules](https://docs.python.org/3/tutorial/modules.html),
Py4geo tools can be imported from them and for integration you just need to
overwrite few basic setting variables.

### Setup

1. Define in your application settings subsequent variables with values adapted to your needs:

    ```python
    # db settings
    # WARNING! Commented out variables are optional.
    # DB_FOLDER =
    DB_URI = "postgres://<PG user>:<password>@<host name>/<db name>"
    # DB_POOL_SIZE = 10
    # DB_MIGRATE = True # Actually True is the default if not specified.
    # MATERIALIZED_VIEWS = []
    ```

2. Create your own setup script (`setup.py`) in the `root` of your application:

    ```python
    from . import settings
    from py4geo import settings as py4geo_settings

    py4geo_settings.DB_URI = settings.DB_URI
    py4geo_settings.DB_FOLDER = settings.DB_FOLDER
    py4geo_settings.MATERIALIZED_VIEWS = settings.MATERIALIZED_VIEWS

    from py4geo.setup import initdb

    initdb()

    # WARNING! These imports must follow the call of the previous initdb function.
    from py4geo.setup.setup import modelsetup
    # Importing the model defined tables are automatically created
    from py4geo.models import db
    # This will create necessary geometry views.
    modelsetup()
    ```

3. Go to your `apps` folder and run:

    ```bash
    cd path/to/apps
    python -m <yourAppName>.setup
    ```

> **WARNING**
> the script will ask for necessary PostgreSQL power user credentials that you
> must know.

### Share your py4web/web2py application database with Py4geo

You have two options

* Overwrite the settings variable `DB_URI` with a [valid PostgreSQL connection string](https://py4web.com/_documentation/static/en/chapter-07.html#connection-strings-the-uri-parameter)
to a PostGIS dtabase.

* Overwrite the `db` variable in the `common` module with a DAL object connected
to a PostGIS database.

## Resources

* [Home](https://github.com/manuelep/py4geo)
* [Project](https://pypi.org/project/py4geo)
* [Wiki](https://github.com/manuelep/py4geo/wiki)

## Dev notes

* [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/#packaging-python-projects)
