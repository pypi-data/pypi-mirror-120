"""Settings for unit tests."""

DEBUG = True

DATABASE_CLASS = 'simplescheduler.corescheduler.datastore.providers.sqlite.DatastoreSqlite'
DATABASE_CONFIG_DICT = {
    # Use in-memory sqlite for unit tests
}
