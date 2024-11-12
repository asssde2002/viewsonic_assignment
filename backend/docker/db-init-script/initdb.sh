#!/bin/bash

DB_NAME=viewsonic
TEST_DB_NAME=${DB_NAME}_test

echo "###";
echo "# Create Db";
echo "###";
createdb -U postgres ${DB_NAME}
createdb -U postgres ${TEST_DB_NAME}
