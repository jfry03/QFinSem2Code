#!/bin/bash

# Step 1: Run the aggregator
python TradingGames/aggregator.py

# Step 2: Stage README and results folder
git add README.md TradingGames/

# Step 3: Commit (or skip if nothing changed)
git commit -m "Auto-update: README and TradingGameResults" || echo "Nothing to commit."

# Step 4: Push
git push