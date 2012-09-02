Feature: seriesly database management

    Scenario: Adding new database
        Given I create database named "testdb"
        When I list all existing databases
        Then I see "testdb" in that list

    Scenario: Removing database
        Given I create database named "testdb"
        When I remove database named "testdb"
        And  I list all existing databases
        Then I do not see "testdb" in that list

    Scenario: Adding duplicate database
        Given I create database named "testdb"
        When I create database named "testdb"
        Then I get "ExistingDatabase" exception

    Scenario: Removing not existing database
        Given I create database named "testdb"
        When I remove database named "testdb2"
        Then I get "NotExistingDatabase" exception
