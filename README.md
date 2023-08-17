Y2_2023_03165
# Money Management

## Introduction

Money management is a program which helps users to control their money flows. The
program includes the UI part (visual diagram) where users' expenses are separated into different categories.
All the communication between the user and the program happens through the UI part. The expenses
are read from a CSV file and can be added manually by the user. One important thing
to mention is the program automatically displays and saves only expenses but not incoming
money to the account. For example, a family wants to see spendings of all their family
members in one diagram. Features introduced: grouping of categories manually chosen by the user, separating back
(removing the group), ability to show the chart without rent and with, adding savings which
will be subtracted from the least important spendings, concating multiple CSV files for a combined result,
importance is configured by AI of the program (the more separate transactions in the category you have, 
the more important category becomes) but also the user can change the importance manually, savings can
never be deducted from rent, loan and electricity bill (configured within the program).

## File and directory structure

  - the project directory is very simplistic
  - all the code is stored in the `main.py` file
  - there is one class which was created specifically for purposes of the project and it's saved in a separate file `transaction.py`
  - directory also contains 2 csv files which are used for testing

## Installation instructions

  - the program requires libraries like PyQt5 and PyQt5.QtChart to be installed (sometimes QtChart is not included in the main package so it might require separate installation)
  - installation instructions: `pip install pyqt5` and `pip install pqtchart`

## User instructions

  - to use the program, user needs to run `main.py` file
  - after that a window will pop and the whole programm will be executed via that window, no command line usage
  - to start using money managemnet system, the user should upload a csv file downloaded from a finnish bank or use one as an example from the directory, for that push the button `Read new csv-file`
  - after the file has been uploaded, pie chart for the expenses will be shown
  - you can upload more files through the same button, transactions will be summed up
  - other buttons:
      - check box without rent will show a pie chart excluding rent expenses
      - text input field is used for combining categories into groups, for that type the name of the group you want to create, push the button `Add group`, a pop window will show up, there type all the categories you want to combine, separated with `,`
    example: `Fazer Cafe,Cafetoria Aalto,Kanniston Leipomo`
      - after you click `ok` pie chart will be updated 
      - you can add as many groups as you want 
      - to remove a group, type its name into the same input field and click button `Remove`
functionality of adding savings is also available:
      - click the button `Add savings`, in the pop up window you can select or type in the amount you wish to save 
      - after clicking `ok` chart will be updted and the amount you want to save will be substracted from the least important expenses (AI decision)
      - you can also the the importance of your spendings just use the button `Change importance` and enter categories in the prder from the most important to the least, format is the same, just separated by `,`
      - all the functionality can be used as many times as you wish and after uploading more files or even grouping the categories 
      - BUT! Be careful with trying to save more than you spend, the code will throw an error
