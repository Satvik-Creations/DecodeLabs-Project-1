/*
=====================================================
 DecodeLabs Project 1
 SQL Commands Used
 Author : Satvik Singhal
 Database : TDL (: To_Do_List)
=====================================================
*/

-----------------------------------------------------
-- Create Database
-----------------------------------------------------

CREATE DATABASE IF NOT EXISTS TDL;

-----------------------------------------------------
-- Select Database
-----------------------------------------------------

USE TDL;

-----------------------------------------------------
-- Create Table
-----------------------------------------------------

CREATE TABLE IF NOT EXISTS to_do_list (
    ID INT UNIQUE KEY,
    TASK VARCHAR(255)
);

-----------------------------------------------------
-- Create Stored Procedure
-----------------------------------------------------

DROP PROCEDURE IF EXISTS RenumberID;

CREATE PROCEDURE RenumberID()
BEGIN
    SET @count = 0;

    UPDATE TO_DO_LIST
    SET ID = (@count := @count + 1)
    ORDER BY ID;
END;

-----------------------------------------------------
-- Insert Task
-----------------------------------------------------

INSERT INTO to_do_list
VALUES (ID, TASK);

-----------------------------------------------------
-- Retrieve All Tasks
-----------------------------------------------------

SELECT *
FROM to_do_list;

-----------------------------------------------------
-- Get Highest Existing ID
-----------------------------------------------------

SELECT MAX(ID)
FROM to_do_list;

-----------------------------------------------------
-- Delete a Task
-----------------------------------------------------

DELETE FROM to_do_list
WHERE TASK = ?
ORDER BY ID
LIMIT 1;

-----------------------------------------------------
-- Execute Stored Procedure
-----------------------------------------------------

CALL RenumberID();

-----------------------------------------------------
-- Clear Entire Table
-----------------------------------------------------

TRUNCATE TABLE to_do_list;

-----------------------------------------------------
-- Helpful MySQL Commands (Used for Testing)
-----------------------------------------------------

SHOW DATABASES;

SHOW TABLES;

DESC to_do_list;

SELECT * FROM to_do_list;