#!/bin/bash

npages=$(djvused -e 'n' $1)

for i in $(seq 1 $npages); do
  djvused -e "select $i;output-txt" $1 >page${i}.djvutxt
done
