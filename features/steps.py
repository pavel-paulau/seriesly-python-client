#
# Copyright 2012, Couchbase, Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import time
from ConfigParser import ConfigParser
from tempfile import mkdtemp
from subprocess import Popen

from lettuce import step, world, before, after
from nose.tools import assert_raises

from seriesly import Seriesly
from seriesly.exceptions import ExistingDatabase, NotExistingDatabase


@before.all
def read_config():
    world.config = ConfigParser()
    world.config.readfp(open('test.cfg'))


@before.all
def init_client():
    world.client = Seriesly(host=world.config.get('database', 'host'),
                            port=world.config.get('database', 'port'))


@before.each_scenario
def reset_exceptions(scenario):
    world.exceptions = list()


@before.each_scenario
def start_seriesly(scenario):
    temp_dir = mkdtemp()
    world.seriesly = Popen(['seriesly', '--root={0}'.format(temp_dir),
                            '--flushDelay=0.1s'])
    time.sleep(1)


@after.each_scenario
def stop_seriesly(feature):
    world.seriesly.kill()


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


@step(u'I see "(.*)" in that list')
def db_exist(step, dbname):
    assert dbname in world.dbs


@step(u'I do not see "(.*)" in that list')
def db_not_exist(step, dbname):
    assert dbname not in world.dbs


@step(u'I get "(.*)" exception')
def raise_exception(step, exception):
    assert isinstance(world.exceptions[-1], eval(exception))
