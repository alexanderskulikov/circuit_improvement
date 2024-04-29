#!/bin/bash

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 token"
    exit 1
fi

if [ "$(basename "$PWD")" != "circuit_improvement" ]; then
    echo "Cloning repo..."
    if [ ! -d "circuit_improvement" ]; then
        git clone git@github.com:alexanderskulikov/circuit_improvement.git
    fi
    cd circuit_improvement
else
    echo "Already in the 'circuit_improvement' directory"
fi

echo "Preparing existing solutions"
if [ ! -d "circuit-synthesis" ]; then
    git clone git@github.com:SPbSAT/circuit-synthesis.git
else
    printf "Do you want to update existing solutions from git? (y/N) "
    read -r ans
    if [[ "$ans" == "y" || "$ans" == "Y" ]]; then
        rm -rf circuit-synthesis
        git clone git@github.com:SPbSAT/circuit-synthesis.git
    else
        echo "Continue with current benchmarks"
    fi
fi

circuits_dir="experiments/circuits"
echo "Cleaning $circuits_dir"
mkdir -p "$circuits_dir"
rm -f "$circuits_dir/xaig_"*
rm -f "$circuits_dir/aig_"*
echo "Copying solutions into $circuits_dir"
for i in {0..99}; do
    for basis in "aig" "xaig"; do
        pattern="ex$(printf "%02d" $i)*"
        dir1="circuit-synthesis/iwls2024/solutions/${basis}_bench/"
        dir2="circuit-synthesis/iwls2024/best_from_2023/${basis}_bench_cleaned"
        files1=$(find "$dir1" -maxdepth 1 -name "$pattern")
        files2=$(find "$dir2" -maxdepth 1 -name "$pattern")
        if [[ -n $files1 ]]; then
            for file in $files1; do
                cp "${file}" "$circuits_dir/${basis}_$(basename $file)"
            done
        elif [[ -n $files2 ]]; then
            for file in $files2; do
                cp "${file}" "$circuits_dir/${basis}_$(basename $file)"
            done
        else
            echo "Circuit $pattern not found in both: $dir1, $dir2"
            exit 1
        fi
    done
done
echo "All current solutions copied to $circuits_dir"

if [ -d "experiments/log" ]; then
    echo "Clearing old logs"
    rm -r experiments/log
fi



if [ ! -d "bot_venv" ]; then
    echo "Creating bot_venv..."
    python -m venv bot_venv
    echo "Activating bot_venv"
    source bot_venv/bin/activate
    echo "Installing requirements.txt"
    pip install -r requirements.txt
    echo "Installing python-telegram-bot"
    pip install "python-telegram-bot[job-queue]"
fi
source bot_venv/bin/activate

echo "Launching bot using $(which python)"
python experiments/tg_bot.py $1
