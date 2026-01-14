#!/bin/bash

echo "Executing detector.py"

# prompt-types
prompt[0]="base"
prompt[1]="dtype"
prompt[2]="directive"
prompt[3]="full"

array_length=${#prompt[@]}
index=$(($RANDOM % $array_length))

echo "Running detector with " ${prompt[$index]} " prompt."
