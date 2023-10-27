#!/bin/bash

sort "test.txt" | uniq -c | while read count key
        do
            if [ "$count" -gt 1 ]; then
                echo "$key is duplicated $count times"
            fi
            if [ "$count" -eq 1 ]; then
                echo "$key is not duplicated"
            fi