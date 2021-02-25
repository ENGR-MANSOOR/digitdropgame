########################################BUTTONS WITH LOGIN/SIGNUP###########################################
import pygame
import time
import random
import pyrebase

#######################################LOGIN SIGNUP################################################################

firebaseConfig = {'apiKey': "AIzaSyDaUD3vmVuwPf8B4f1zwnbtPeqTISSLMMA",
                  'authDomain': "digitdroppygame.firebaseapp.com",
                  'projectId': "digitdroppygame",
                  'databaseURL': 'https://digitdroppygame-default-rtdb.firebaseio.com/',
                  'storageBucket': "digitdroppygame.appspot.com",
                  'messagingSenderId': "694567252591",
                  'appId': "1:694567252591:web:6d2486e83741bbe928139a",
                  'measurementId': "G-75RJHY13F7"
                  }

# init. DB
firebase = pyrebase.initialize_app(firebaseConfig)

# db = firebase.database()
auth = firebase.auth()


# storage = firebase.storage()


# login
def login():
    email = input('Enter your email: ')
    password = input('Enter your password: ')

    try:
        auth.sign_in_with_email_and_password(email, password)
        print('Successfully signed in!')
        game_loop()

    except:
        print('Invalid Username/Password!\n\tTry again')
        login()


# create an account
def signup():
    email = input('Enter your email: ')
    password = input('Enter your password: ')
    Confirmpassword = input('Confirm your password: ')
    if password == Confirmpassword:  # do the passwords match?
        try:
            login = auth.create_user_with_email_and_password(email, password)
            auth.send_email_verification(login['idToken'])
            print('Account created successfully')
            game_loop()
        except:
            print('Email is already in use!\nTry again')  # if email has already been used in DB
            signup()


# start up

def ignition():
    print('Welcome to Digit Drop\nPlease choose the relevant option:')
    print('1. Login with an existing account')
    print('2. Signup')
    print('3. Exit Program')
    x = int(input('Input the appropriate number: '))
    try:
        if x == 1:
            login()
        elif x == 2:
            signup()
        elif x == 3:
            exit()
    except:
        print('Incorrect entry')


#######################################LOGIN SIGNUP ########################*END*################################

pygame.init()
# We define window size:
WIN_WIDTH = 800
WIN_HEIGHT = 600

# Text fonts we will use during the game:
titleFont = pygame.font.SysFont('Calibri', 120)
font = pygame.font.SysFont('Calibri', 55)
miniFont = pygame.font.SysFont('Calibri', 65)
textFont = pygame.font.SysFont('Calibri', 35)


# Class of the board:
class board(object):
    def __init__(self, size):  # this will be called when we create a board
        self.size = size
        self.cells = []
        number = 1
        # Creates all the cells:
        for i in range(self.size):
            for k in range(self.size):
                self.cells.append(cell(i, k, number))
            number += 1

    # Draw board:
    def draw(self, win):
        for cell in self.cells:  # draw each cell
            cell.draw(win)


class cell(object):
    def __init__(self, x, y, num):  # this will be called when we create a cell
        self.x = x
        self.y = y
        self.num = num
        self.size = 64
        self.disabled = False
        self.hover = False
        self.selected = False
        self.rect = pygame.Rect(self.x * self.size + 100, self.y * self.size + 100, self.size, self.size)

    def draw(self, win):
        # Draw cells depending if its clicked, selected or disabled:
        self.rect = pygame.Rect(self.x * self.size + 100, self.y * self.size + 100, self.size, self.size)
        if self.selected:
            pygame.draw.rect(win, (0, 255, 0), self.rect)
        elif self.disabled:
            pygame.draw.rect(win, (150, 150, 150), self.rect)
        elif self.hover:
            pygame.draw.rect(win, (200, 200, 200), self.rect)
        else:
            pygame.draw.rect(win, (255, 255, 255), self.rect)
        # Draw number:
        message = miniFont.render(str(self.num), 1, (0, 0, 0))  # render text
        win.blit(message, (self.x * self.size + 115, self.y * self.size + 100))  # show text

        pygame.draw.rect(win, (0, 0, 0), self.rect, 3)  # border rect


def sendMail(hs):
    import smtplib, ssl

    port = 465

    sender, password = "digitdropmanager@gmail.com", "ilovepygame123"

    recieve = sender  # here you can put the receiver email (now it send to the same mail)

    message = """\
    Subject: NEW HIGHSCORE

    Your new highscore is %s
    """ % (hs)

    context = ssl.create_default_context()

    print("Starting to send")
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, recieve, message)

    print("sent email!")


def gameOver(win, score):
    f = open('file.txt', 'r')  # we open file of higscore.
    for i in f:
        hs = i  # get file text
    if float(hs) < score:  # if we have a highscore
        f = open('file.txt', 'w')  # we open file of higscore.
        f.write(str(round(score, 2)))  # write new score.
        sendMail(score)

    pygame.draw.rect(win, (255, 0, 0), (0, 0, WIN_WIDTH, WIN_HEIGHT))  # backoground rect
    pygame.draw.rect(win, (0, 0, 0), (0, 0, WIN_WIDTH, WIN_HEIGHT), 20)  # border rect

    message = titleFont.render("GAME OVER", 1, (0, 0, 0))  # render title text
    win.blit(message,
             (WIN_WIDTH / 2 - message.get_width() // 2, WIN_HEIGHT / 2 - message.get_height() // 2))  # show text

    pygame.display.update()
    pygame.time.delay(2500)


def game_loop():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # display window

    pygame.display.set_caption("Game")
    clock = pygame.time.Clock()  # set clock

    f = open('file.txt', 'r')  # we open file of higscore.
    for i in f:
        hs = i  # get file text
    run = True
    level = 0

    # MainLoop:
    while run:
        clock.tick(50)
        click = False
        # Get events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                click = True

        mouse_position = pygame.mouse.get_pos()  # gets position of the mouse.
        keys = pygame.key.get_pressed()  # gets key pressed.

        # Menu:
        if level == 0:
            pygame.draw.rect(win, (253, 120, 107), (0, 0, WIN_WIDTH, WIN_HEIGHT))  # backoground rect
            pygame.draw.rect(win, (255, 0, 0), (0, 0, WIN_WIDTH, WIN_HEIGHT), 20)  # border rect

            message = titleFont.render("Numbers", 1, (0, 0, 0))  # render title text
            win.blit(message, (220, 150))  # show text

            buttonRect = pygame.Rect(WIN_WIDTH / 2 - 63, 280, 125, 55)  # rect of the play button

            # Changes button colour if the mouse is over it:
            if buttonRect.collidepoint(mouse_position):
                buttonColor = (253, 120, 107)
            else:
                buttonColor = (255, 0, 0)

            pygame.draw.rect(win, buttonColor, buttonRect)  # button
            pygame.draw.rect(win, (0, 0, 0), buttonRect, 3)  # button border
            message = miniFont.render('PLAY', 1, (0, 0, 0))  # render text
            win.blit(message, (WIN_WIDTH / 2 - 63, 280))  # show text
            message = font.render('HIGHSCORE:' + hs, 1, (0, 0, 0))  # render text
            win.blit(message, (225, 380))  # show text

            quitButtonRect = pygame.Rect(WIN_WIDTH / 2 - 63, 480, 135, 55)  # rect of the play button

            # Changes button colour if the mouse is over it:
            if quitButtonRect.collidepoint(mouse_position):
                quitButtonColor = (253, 120, 107)
            else:
                quitButtonColor = (255, 0, 0)

            pygame.draw.rect(win, quitButtonColor, quitButtonRect)  # button
            pygame.draw.rect(win, (0, 0, 0), quitButtonRect, 3)  # button border
            message = miniFont.render('QUIT', 1, (0, 0, 0))  # render text
            win.blit(message, (WIN_WIDTH / 2 - 63, 480))  # show text

            if click:  # if we click something:
                if buttonRect.collidepoint(mouse_position):  # if we click the play button
                    level += 1
                    b = board(6)
                    num_1 = 0
                    num_2 = 0
                    x = random.randint(1, 9)
                    score = 0
                    loose = False

                elif quitButtonRect.collidepoint(mouse_position):  # if we click the quit button
                    run = False

        else:
            win.fill((0, 150, 160))  # fill window with color
            b.draw(win)  # draw board
            # Write score and others:
            message = font.render('SCORE:' + str(score), 1, (0, 0, 0))  # render text
            win.blit(message, (WIN_WIDTH - 280, 80))  # show text
            add = num_1 + num_2
            message = textFont.render(str(num_1) + ' + ' + str(num_2) + ' = ' + str(add), 1, (0, 0, 0))  # render text
            win.blit(message, (WIN_WIDTH - 230, 150))  # show text
            message = textFont.render('Divisor:' + str(x), 1, (0, 0, 0))  # render text
            win.blit(message, (WIN_WIDTH - 230, 200))  # show text

            if num_1 > 0 and num_2 > 0:  # if 2 numbers were selected:
                if (add % x != 0):  # if they arent divisor with x:
                    color = (0, 255, 0)
                    score += round(add / x, 2)  # we add the result to the score
                    num_1, num_2 = 0, 0
                    for c in b.cells:
                        if c.selected:
                            for cel in b.cells:
                                if cel.num == c.num and cel.y < c.y:
                                    cel.y += 1

                            b.cells.pop(b.cells.index(c))

                else:
                    color = (255, 0, 0)
                    loose = True
                # Draw division (red rectangle if its whole number, green if its fractional):
                rect = pygame.Rect(WIN_WIDTH - 232, 248, 150, 37)
                pygame.draw.rect(win, color, rect)
                pygame.draw.rect(win, (0, 0, 0), rect, 2)
                message = textFont.render(str(add) + '/' + str(x) + ' = ' + str(round(add / x, 2)), 1,
                                          (0, 0, 0))  # render text
                win.blit(message, (WIN_WIDTH - 230, 250))  # show text

                pygame.display.update()  # update changes in screen.
                pygame.time.delay(1000)  # delay for a second

            if loose:
                gameOver(win, score)
                f = open('file.txt', 'r')  # we open file of higscore.
                for i in f:
                    hs = i
                level = 0

            loose = True
            # game ends if every cell is disabled
            for c in b.cells:
                if not c.disabled:
                    loose = False
                    break

            # change color when a cell has the mouse on it or is clicked.
            for c in b.cells:
                if c.rect.collidepoint(mouse_position):
                    if click:
                        if num_1 == 0:
                            num_1 = c.num
                            c.selected = True
                            c.disabled = True
                        elif num_2 == 0 and num_1 != c.num:
                            num_2 = c.num
                            c.selected = True
                            c.disabled = True
                    else:
                        c.hover = True
                else:
                    c.hover = False

        pygame.display.update()  # update changes in screen.


ignition()  # menu of the game
pygame.quit()  # quit pygame.
quit()