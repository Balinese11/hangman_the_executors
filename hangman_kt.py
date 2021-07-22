import sys
import os

valid_characters = "abcdefghijklmnopqrstuvwxyz"


#-----------MAIN
def main():
    words = {}
    is_hard = False
    is_first_running = True
    current_word = ""

    clear_terminal()

    while True:
        is_hard = show_start()

        if is_first_running:
            words = load_words()

        current_word = get_game_word(words, is_hard) 

        play(current_word, is_hard)
        is_first_running = False

        next_try = input("Want to try again? (Y, N)")
        if next_try.upper() != "Y":
            sys.exit()

def play(word, ishard):
    wrong_guesses = []
    right_guesses = []
    current_guess = ""

    while True:
        update_ui(ishard, word, wrong_guesses, right_guesses)
        show_info()

        current_guess = get_next_guess()

        if current_guess.upper() == "QUIT":
            show_message("quit")
            sys.exit()
        
        if is_valid_char(current_guess, valid_characters):
            if contain(current_guess, word):
                if not contain(current_guess, right_guesses):
                    right_guesses.append(current_guess)
                    if check_right_ending(right_guesses, word):
                        update_ui(ishard, word, wrong_guesses, right_guesses)
                        show_win()
                        return
            else:
                if not contain(current_guess, wrong_guesses):
                    wrong_guesses.append(current_guess)
                    if check_wrong_ending(ishard, wrong_guesses):
                        update_ui(ishard, word, wrong_guesses, right_guesses)
                        show_game_over(word)
                        return

def update_ui(ishard, word, wrongs, rights):
    clear_terminal()
    level = get_wrong_step(ishard, wrongs)
    show_tree(level)
    word_display = get_display_string(word, rights)
    show_current_word(word_display)
    show_wrong_guesses(wrongs)

def load_words():
    return {"H:London", "E:Budapest", "H:Copenhagen", "E:Amsterdam", "H:Stockholm", "E:Bukarest"}

def get_game_word(gamewords, hard):
    for item in gamewords:
        if (item[0] == "H" and hard == True) or (item[0] == "E" and hard == False):
            return item[2:]

def get_wrong_step(ishard, wrongs):
    if ishard:
        return len(wrongs) * 2
    else:
        return len(wrongs)

# params:
 # str: current_word értéke
 # rights: right_guesses értéke
 # return:
 # az aktuális feladvány megjelenítendő karakterek listájával  
def get_display_string(str, rights):
    result = []
    for c in str:
        if contain(c, rights):
            result.append(c)
        else:
            result.append("_")

    return result

def check_wrong_ending(ishard, wrongs):
    if (ishard == True) and (len(wrongs) < 4):
        return False
    elif (ishard == False) and (len(wrongs) < 8):
        return False
    return True

 #eltalálta e az összes betűt
 #True: megtalálta az összes betűt - kitalálta a szót - vége a játéknak
 #False: van legalább egy betű, amit még nem talált ki

def check_right_ending(rights, c_word):
    for item in c_word:
        if not contain(item, rights):
            return False
    
    return True
    
#-----------HELP
# params:
 # char: current_guess értéke
 # charlist: right_guesses/wrong-guesses/rights értéke
 # return:
 # c benne van-e vagy nincs a listában  
def contain(char, charlist):
    for c in charlist:
        if c.upper() == char.upper(): # nem akarjuk, hogy case sensitive legyen
            return True
        
    return False

# params:
 # character: current_guess értéke
 # string: valid-char / current_word értéke
 # return:
 # c benne van-e vagy nincs a stringben
def is_valid_char(character, string):
    return contain(character, string)


#-----------UI
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_start():
    print("Welcome!")

    while True:
        x = input("Choose difficulty: Type 'e' for easy or 'h' for hard!")
        if x == 'e':
            return False
        elif x == 'h':
            return True
        elif x == 'quit':
            print("Good-bye!")
            sys.exit()

def show_tree(level):
    line = ""
    line = "------------"
    print(line)

    line = " | "
    if level > 0:
        line += "   | "
    print(line)

    line = " | "
    if level > 1:
        line += "   0"
    print(line)  

    line = " | "
    if level == 3:
        line += "   |"
    if level == 4:
        line += "  \\|" 
    if level > 4:
        line += "  \\|/" 
    print(line)  

    line = " | "
    if level > 5:
        line += "   |"
    print(line) 

    line = " | "
    if level == 7:
        line += "  /"
    if level == 8:
        line += "  / \\"
    print(line) 

    line = " | "
    print(line) 

    line = "___________"
    print(line) 

def show_current_word(charlist):
    temp = ""
    for c in charlist:
        temp = temp + c + " "
        
    print("                    " + temp)

def show_wrong_guesses(wrongs):
    temp = ""
    lenght = len(wrongs)-1
    for index in range(len(wrongs)):
        temp = temp + wrongs[index]
        if index < lenght:
            temp = temp + ", "
    print("Wrong guesses: " + temp.upper())

def show_info():
    print("Type 'quit' to Quit.")

def get_next_guess():
    next = input("Next guess: ")
    return next

def show_message(status, word = ""):
    if status == "quit":
        print("The word was: " + word + ". Thanks for playing! Good-bye!")
    elif status == "win":
        print("You are awesome! You won!")
    elif status == "loose":
        print("The word was: " + word + ". You lost this one, you will win the next!")

def show_win():
    show_message("win")

def show_game_over(word):
    show_message("loose", word)

main()
