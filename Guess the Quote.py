# Pandas will be used to store and access the sql database, 
# pyodbc will be used to gain access to the sql database, 
# and random will be used to make the quiz questions randomized.
import pandas as pd
import pyodbc
import random
from random import randrange

# Open a connection bewteen this file and the Tinkering database
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Database=Tinkering;'
                      'Trusted_Connection=yes;')

# Query will be used to access all information in the Quotee table
query = ('SELECT * FROM Tinkering.dbo.Quotee')
count = ('SELECT COUNT(*) FROM Tinkering.dbo.Quotee')

# Variables that don't need to be reset at the beginning of every loop
df = pd.read_sql(query, conn)
cnt = pd.read_sql(count, conn)
cnt = int(cnt.iloc[0])
options = ['1) ', '2) ', '3) ', '4) '] # An array for labeling each answer choice
play = True

while(play):
    # Variables that need to be reset at the beginning of each loop
    choices = random.sample(range(cnt), 4)  
    answer_index = randrange(len(choices))
    answer = choices[answer_index]
    wrong = True
    replay = True
    opt = 0
    
    print('Who said this quote?' + '\n')
    print('"' + df.loc[answer, 'Quote'] + '"' + '\n')
    print('Your choices are: ')

    for i in choices:
        print(options[opt] + df.loc[i, 'FullName'])
        print('\n')
        df.drop(i, inplace = True)
        cnt -= 1
        opt += 1

    df.reset_index(drop = True, inplace = True)

    while(wrong):
        user_answer = input()
        if int(user_answer) == (answer_index + 1):
            print('Correct! Good job!')
            wrong = False
        else:
            print('Incorrect! Try again!')    

    while(replay):
        play_again = input('Would you like to play again? (yes/no) \n')
        if play_again == 'no':
            play = False
            replay = False
        elif play_again == 'yes':
            replay = False
        else:
            print('Please respond with either yes or no.')

    if cnt == 0:
        play = False
        print('You\'ve answered all our questions! \n')

print('Thanks for playing!')