# python-unit-tester
A program that runs unit tests for python files

*Checker.py* is designed to run unit tests on the functions in another .py file by using
unit test data that is stored in .txt files. Checker is designed for computer science
teachers to grade student work.

**Unit Testing Files format**:
The unit test text files must have a specific format. A series of punctuation is used for delimiting input and output data:

* | separates multiple input values for a function
* , the delimiter for elements within a list
* $ the delimiter for rows within a 2D list


Example:

>1,2,3$4,5,6$7,8,9|0,1,0$0,1,0$0,1,0
>
>EXPECTED 1,1,3$4,1,6$7,1,9

The above data specifies that a function is accepting two 2D lists of integers. In this case, each 2D list has three rows and three elements per row.
The expected output for this function is a single 2D list of integers that has three rows and columns

>0|0|2|1
>
>EXPECTED right
>
>0|0|0|0
>
>EXPECTED equal
>
>0|0|2|-3
>
>EXPECTED down

Here, there are three unit tests. A function expects four integers as inputs, and has an expected output of a string

The unit test files are named following the format of:

unit_tests_#assignmentname_#function.txt

Eg. unit_tests_homework3_0.txt

--> the unit tests for homework 3's first function to be tested

--> The next function's unit tests would have the text file name of
    unit_tests_homework3_1.txt
