import time
from ConfigParser import ConfigParser
from tempfile import mkdtemp
from subprocess import Popen

from lettuce import step, world, before, after
from nose.tools import assert_raises, assert_equals

from seriesly import Seriesly
from seriesly.exceptions import ExistingDatabase, NotExistingDatabase,\
    BadRequest


@before.all
def read_config():
    world.config = ConfigParser()
    world.config.readfp(open('test.cfg'))


@before.all
def start_seriesly():
    temp_dir = mkdtemp()
    world.seriesly = Popen(['seriesly', '--root={0}'.format(temp_dir),
                            '--flushDelay=0.1s'])
    time.sleep(1)


@after.all
def stop_seriesly(total):
    world.seriesly.kill()


@before.all
def init_client():
    world.client = Seriesly(host=world.config.get('database', 'host'),
                            port=world.config.get('database', 'port'))


@before.each_scenario
def reset_exceptions(scenario):
    world.exceptions = list()


@after.each_scenario
def drop_all_dbs(scenario):
    for db in world.client.list_dbs():
        world.client.drop_db(db)


@step(u'I create database named "(.*)"')
def create_database(step, dbname):
    try:
        world.client.create_db(dbname)
    except Exception, error:
        world.exceptions.append(error)


@step(u'I remove database named "(.*)"')
def drop_database(step, dbname):
    try:
        world.client.drop_db(dbname)
    except Exception, error:
        world.exceptions.append(error)


@step(u'I list all existing databases')
def list_databases(step):
    world.dbs = world.client.list_dbs()


@step(u'I append key "(.*)" with value (.*) to "(.*)" database')
def append_data(step, key, value, dbname):
    doc = {key: int(value)}
    world.response = world.client[dbname].append(doc)


@step(u'I query that value "(.*)" from "(.*)" database using reducer "(.*)"')
def query_data(step, value, dbname, reducer):
    time.sleep(0.25)
    params = {'group': 3600, 'ptr': '/{0}'.format(value), 'reducer': reducer}
    try:
        world.response = world.client[dbname].query(params=params)
    except Exception, error:
        world.exceptions.append(error)


@step(u'I see "(.*)" in that list')
def db_exist(step, dbname):
    assert dbname in world.dbs


@step(u'I do not see "(.*)" in that list')
def db_not_exist(step, dbname):
    assert dbname not in world.dbs


@step(u'I get "(.*)" exception')
def raise_exception(step, exception):
    assert isinstance(world.exceptions[-1], eval(exception))


@step(u'I get response "(.*)"')
def get_response(step, response):
    assert_equals(world.response, response)


@step(u'I get value (.*) in query result')
def get_response(step, value):
    assert_equals(world.response.values()[-1][-1], value)
