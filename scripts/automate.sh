#!/bin/bash

echo -e "\nEntering Virtual Environment...\n"
source ~/Documents/Projects/venv/bin/activate

clean() {
	echo -e "\nLeaving Virtual Environment...\n"
	deactivate
	echo -e "\nComplete!"
}

trap clean EXIT

python3 myNAS.py

