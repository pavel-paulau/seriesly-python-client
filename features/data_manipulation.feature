Feature: Data manipulation

    Scenario: Appending new data
        Given I create database named "testdb"
        When I append key "a" with value 2 to "testdb" database
        Then I get response ""

    Scenario: Querying data
        Given I create database named "testdb"
        When I append key "a" with value 2 to "testdb" database
        When I query that value "a" from "testdb" database using reducer "any"
        Then I get value 2 in query result
