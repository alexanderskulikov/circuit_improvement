#!/bin/bash

set -e



if [ "$(basename "$PWD")" != "circuit_improvement" ]; then
    echo "Cloning repo..."
    if [ ! -d "circuit_improvement" ]; then
        git clone git@github.com:alexanderskulikov/circuit_improvement.git
    fi
    cd circuit_improvement
else
    echo "Already in the 'circuit_improvement' directory"
fi


echo "Configuring venv..."
if [ ! -d "venv" ]; then
    python -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
pip install python-telegram-bot

echo "Preparing benchmarks"
if [ ! -d "circuit-synthesis" ]; then
    echo "Downloading benchmarks"
    git clone git@github.com:SPbSAT/circuit-synthesis.git
fi
mkdir -p experiments/circuits
mkdir -p experiments/circuits/aig
mkdir -p experiments/circuits/xaig
cp -r circuit-synthesis/iwls2024/best_from_2023/aig_bench_cleaned/* experiments/circuits/aig
cp -r circuit-synthesis/iwls2024/best_from_2023/xaig_bench_cleaned/* experiments/circuits/xaig
for file in experiments/circuits/aig/*; do
    cp "$file" "experiments/circuits/aig_$(basename "$file")"
done
for file in experiments/circuits/xaig/*; do
    cp "$file" "experiments/circuits/xaig_$(basename "$file")"
done
cp experiments/circuits/aig/* experiments/circuits/
cp experiments/circuits/xaig/* experiments/circuits/
rm -r experiments/circuits/aig/
rm -r experiments/circuits/xaig/







