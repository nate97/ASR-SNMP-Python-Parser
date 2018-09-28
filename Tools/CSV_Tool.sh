#!/bin/bash
echo 'CSV Tool wrapper'
currentDir = $(pwd)
activeETool = 'ActiveE_CSV_Tool.py'
gponTool = 'GPON_CSV_Tool.py'
python3 *$currentDir$activeETool*
echo "$currentDir"
echo 'Combining CSV files...'