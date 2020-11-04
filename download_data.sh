#! /bin/bash

if [ ! -d "datasets" ]; then
    mkdir datasets
fi

declare -a final_data=(
    "asd"
    "asdasdasd"
    "asdadadsdasdsa"
)

for i in "${final_data[@]}"
do
    echo $i
done
