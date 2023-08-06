# How to use
pip install antlr4-mysql

# How to build
## What You Need

JDK 1.8 or later (generate python code)

Python3

## generated python code
java -jar antlr4-4.9.2-complete.jar -Dlanguage=Python3 *.g4 -visitor -o am/autogen
 
## Required dependency

antlr4-python3-runtime

## For test
mysql_base_test.py
