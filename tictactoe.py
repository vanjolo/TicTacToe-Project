import mysql.connector
import sys
import os

def registration():
  mydb = mysql.connector.connect(
    host="remotemysql.com",
    port = 3306,
    user="3W3BHT4RDU",
    password="6TlVjzhCme",
    database="3W3BHT4RDU"
  )

  mycursor = mydb.cursor()

  mycursor.execute("SELECT * FROM users")

  myresult = mycursor.fetchall()
  while True:
    username = input('Enter username: ')
    password = input('Enter password: ')
    users = [i[0] for i in myresult]
    if username in users:
        print('The username is already taken try diffrent one.')
    else:
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        val = (username, password)
        mycursor.execute(sql, val)

        mydb.commit()
        print('Registration successful!')
        break
  return username
 

def login():

    mydb = mysql.connector.connect(
    host="remotemysql.com",
    port = 3306,
    user="3W3BHT4RDU",
    password="6TlVjzhCme",
    database="3W3BHT4RDU"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM users")

    myresult = mycursor.fetchall()

    while True:
        username = input('Enter username: ')
        password = input('Enter password: ')
        found = False

        for user, pwd in myresult:
            if user == username and pwd == password:
                print('Login successful!')
                found = True
                break
            
        if not found:
            print("Incorrect. Try again!")
            ext = input('Press L to login or R to register: ')
            if ext == 'L':

                for user, pwd in myresult:
                    if user == username and pwd == password:
                        print('Login successful!')
                        found = True
                        break
            elif ext == 'R':
                registration()
                
                break
            
        else:
            
            break
    return username


def display_board(board):
    for i in board:
        print('| ', end = '')
        print(*i,sep = ' | ', end = '')
        print(' |')

def check_row(board, player):
    for i in board:
        if i.count(player) == 3:
            return True
    return False

def check_columns(board, player):
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] == player:
            return True
    return False

def check_diagonals(board, player):
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    elif board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

def insert_winner(player_name):
    mydb = mysql.connector.connect( 
    host="remotemysql.com",
    port = 3306,
    user="3W3BHT4RDU",
    password="6TlVjzhCme",
    database="3W3BHT4RDU"
    )

    mycursor = mydb.cursor()
    sql = "INSERT INTO score (name, wins) VALUES (%s, %s)"
    val = (player_name, "1")
    mycursor.execute(sql, val)

    mydb.commit()
    print('The winner was inserted into the database')

def display_leaderboard():
    mydb = mysql.connector.connect(
    host="remotemysql.com",
    port = 3306,
    user="3W3BHT4RDU",
    password="6TlVjzhCme",
    database="3W3BHT4RDU"
    )

    mycursor = mydb.cursor()

    mycursor.execute("select name, count(*) as c FROM score GROUP BY name ORDER BY c DESC")

    myresult = mycursor.fetchall()
    print('Ranking | Player name | Score')
    i = 1
    for x in myresult:
        print('{0:^8d}|{1:^13s}| {2:<d}'.format(i,x[0],x[1]))
        i += 1
        

def main():
    while True:
        print('Menu Player 1:')
        print('1. Login')
        print('2. Register as new user')

        choice = input('Enter option 1 or 2: ')
        if choice == '1':
            username1 = login()
            break
        elif choice == '2':
            username1 = registration()
            break
        else:
            print("Invalid selection. Try again!")
        break
    while True:
        print('Menu Player 2:')
        print('1. Login')
        print('2. Register as new user')
        choice = input('Enter option 1 or 2: ')
        if choice == '1':
            username2 = login()
                    
            break
        elif choice == '2':
            username2 = registration()
            break
        else:
            print("Invalid selection. Try again!")
        break
        
    board = [[' ' for i in range(3)] for j in range(3)]
    players = ['X','O'] 
    name_x = username1
    print('Player X ' + username1)
    name_o = username2
    print('Player O ' + username2)
    player_names = [name_x, name_o]
    player = 0
    while True:
        print('Player',players[player],"'s turn")
        while True:
            try:
                row,column = input('Enter the row and column separated by the space: ').split()
                os.system('cls')
                row = int(row)
                column = int(column)
                if board[row - 1][column - 1] != " ":
                    print('Sorry that position is taken.Try again')
                else:

                    board[row - 1][column - 1] = players[player]
                    break
            except:
                print("Invalid input.Try again.")
        display_board(board)
        
        
        flat_board = [j for i in board for j in i ] 
    
        if check_row(board,players[player]) or check_columns(board,players[player]) or check_diagonals(board,players[player]):
            print('Player',players[player],'wins!' )
            insert_winner(player_names[player])
            display_leaderboard()
            input('Press Enter to quit')
            break
        elif ' ' not in flat_board:
            print('Game is draw')

            display_leaderboard()
            input('Press Enter to quit')
            break
        if player == 0:
            player = 1
        else:
            player = 0



if __name__ == '__main__':
    main()