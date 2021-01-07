#!/bin/bash
# cron job //
cd ~/Desktop/code/corona-emailer/src
conda activate corona
python email_sender.py --country UK
