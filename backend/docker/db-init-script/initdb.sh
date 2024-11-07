#!/bin/bash

DB_NAME=viewsonic

echo "###";
echo "# Create Db";
echo "###";
createdb -U postgres ${DB_NAME}