from pyfiglet import Figlet
from colorama import init, Fore, Style
import platform
import requests
import random
import time
import sys
import os

init(autoreset=True)
f = Figlet(font='slant')
print(f.renderText('ConsoleApp'))
# Driver program
if __name__ == '__main__':
    global login_status
    print(Fore.RED + 'Du muss eingeloggt sein um das Programm benutzen zu können!!!')
    login_status = False
    while not login_status:
        login_status = False
        ask = input(Fore.GREEN + 'Möchtest du A) dich regestrieren oder B) anmelden? \n')

        if ask == 'A' or ask == 'a':
            while True:
                BASE = 'http://127.0.0.1:5000/'
                email = input('Email: ')
                username = input('Username: ')
                password = input('Password: ')
                if username == '' or password == '' or email == '':
                    print(Fore.RED + 'Password,Username or Email must not be empty!!!')
                    continue
                else:
                    response = requests.post(BASE + 'register', {'username': str(username), 'password': str(password), 'email': str(email)})
                    print(response)
                    status_ = response.json()
                    print(status_)
                    print(response.status_code)
                    if response.status_code == 201:
                        print(Fore.BLUE + f'Register as {username}')
                        login_status = True
                        break
                    else:
                        print(Fore.RED + 'Username or email already taken ... Please try again')
                        continue

        elif ask == 'B' or ask == 'b':
            while True:
                print('If you have forgotten your password, just enter -reset pwd-')
                username = input('Username: ')
                if username == 'reset pwd':
                    while True:
                        email = input(Fore.CYAN +'<Password Reset> Please enter youre Email: ')
                        BASE = 'http://127.0.0.1:5000/'
                        response = requests.post(BASE + 'resetpwd', {'email': str(email)})
                        if response.status_code == 404:
                            print(Fore.RED + 'No account found with this email! Please restart the script')
                            exit(0)
                        else:
                            code = input(Fore.CYAN + '<Passwort Reset> Please enter your recovery code that you received by email: ')
                            BASE = 'http://127.0.0.1:5000/'
                            response = requests.post(BASE + 'doreset', {'code': int(code), 'email': email})
                            if response.status_code == 200:
                                new_password = input(Fore.CYAN + '<Passwort Reset> Please enter youre New Password: ')
                                BASE = 'http://127.0.0.1:5000/'
                                response = requests.put(BASE + 'doreset', {'code': int(code), 'password': new_password})
                                if response.status_code == 200:
                                    print(Fore.CYAN + '<Passwort Reset> ' + Fore.GREEN + 'Password changed successfully, please restart the Script!')
                                    exit(0)
                            else:
                                print(Fore.RED + 'An error has occurred!! Please restart the Script and try again')
                                exit(0)
                passwd = input('Password: ')
                if username == '' or passwd == '':
                    print(Fore.RED + 'the password or username must not be empty!!!')
                    continue
                else:
                    BASE = 'http://127.0.0.1:5000/'
                    response = requests.post(BASE + 'login', {'username': str(username), 'password': str(passwd)})

                    if response.status_code == 200:
                        print(Fore.BLUE + f'sucessfully logged in as {username}')
                        login_status = True
                        break
                    else:
                        print(Fore.RED + 'Wrong password or wrong username ... please try again ')
                        continue

        else:
            print(Fore.RED + 'Invalid information')

    # Restlicher Code hier:
    status = 1
    if status == 1:
        os.system('clear')
        time.sleep(1)
        durchlauf = -1
        while True:
            durchlauf += 1
            if durchlauf >= 1:
                f = Figlet(font='slant')
                print(f.renderText('ConsoleApp'))

            print(Fore.BLUE + """
        Bitte Wähle Aus:
        -1: Guessing game
        -2: Pinger
            """)
            while True:
                ask = int(input('Please choose a number from above: '))
                if ask > 2:
                    print(Fore.RED + 'Please enter a valid Number!')
                    continue
                else:
                    break

            if ask == 1:
                f = Figlet(font='slant')
                print(f.renderText('Guessing Game'))

                status = True
                runde = 1
                Zahl = random.randint(0, 30)
                while status < 7:
                    print('This is youre ' +
                          str(runde) +
                          ' Round')

                    Eingabe = float(input('What number do you think it is?'))

                    if Eingabe == Zahl:
                        print('You were right and you won!')
                        break

                    elif Eingabe > Zahl:
                        print('''       
                         Your number is greater!
                                ''')
                        runde = runde + 1

                    elif Eingabe < Zahl:
                        print('''
                         Your number is smaller!
                               ''')
                        runde = runde + 1

                print('End of Game')
                continue

            if ask == 2:
                f = Figlet(font='slant')
                print(f.renderText('Pinger'))

                current_os = platform.system().lower()

                how_much = int(input('How often should you ping ?: '))

                if current_os == 'windows':
                    parameter = '-n'

                else:
                    parameter = f'-c {how_much}'

                ip = input('Please enter the ip here: ')
                exit_code = os.system(f'ping {ip} {parameter}')
                continue
