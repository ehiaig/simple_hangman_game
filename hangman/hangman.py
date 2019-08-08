from random import choice
from sys import exit

class hangman_game(object):

  """
    dictionary_file (string): Full path to dictionary file for hangman game
    dictionary_file (bool): Enable to output test data (default is False)
        
  """

  def __init__(self, dictionary_file, debug=True):

    ## Debug Mode for testing system
    self.debug = debug
    
    self.visible = ""
    self.hidden = ""

    self.incorrect_guesses = [];

    #Process and load word list from passed dictionary file
    with open(dictionary_file, 'r') as sowpods_file:
      self.words = sowpods_file.readlines()
  
    self.get_word()

  def reset(self):
    self.incorrect_guesses = [];
    self.get_word()
    self.start()


  def start(self):
    self.draw_board()
    self.get_guess()

  def get_word(self):

    self.visible = ""
    self.hidden = choice(self.words).strip()
    
    for elem in self.hidden:
      self.visible += "_"

  """
    Displays the hangman, a list of previous incorrect guesses, and 
        a dashed out word w/ letters in places where correctly guessed    
  """
  def draw_board(self):

    vis_word = ' '.join(self.visible)
    num_wrong_guesses = len(self.incorrect_guesses)
    incorrect_letters = ', '.join(self.incorrect_guesses)

    if self.debug:
      print(self.hidden)
    
    for i in range(20):
      print("\n")
    
    print("  +=====+          " + vis_word)
    print("  |     '")
    if num_wrong_guesses >= 1:
      print("  |     O           Incorrect Guesses:")
    else:
      print("  |                 Incorrect Guesses:")


    if num_wrong_guesses >= 4:
      print("  |    / \\")
    elif num_wrong_guesses == 3:
      print("  |    /")
    else:
      print("  |")
    print("  |")
    print("==========")

    if num_wrong_guesses == 6:
      print("  |    /|\               " + incorrect_letters)
    elif num_wrong_guesses == 5:
      print("  |    /|                " + incorrect_letters)
    elif num_wrong_guesses >= 2:
      print("  |     |                " + incorrect_letters)
    else:
      print("  |                      " + incorrect_letters)

  """
      Prompt user for a guess. User can also start a new game or exit out of program.
  """
  def get_guess(self):

    letter = input("What letter would you like to guess? (Quit) | (Reset)  ")
    while ((not letter.isalpha()) or (letter.lower() not in ('quit', 'reset') and len(letter) != 1)):
      # invalid input detected
      letter = input("You may type quit to end game, reset to start a new game (get new"
                     + " word), or a letter if you would like to continue playing/guessing.  ")
        
    guess = letter.upper()

    if guess == 'QUIT':
      self.quit()
    elif guess == 'reset':
      self.reset()
    else:                
      # check if correct guess
      self.check_guess(guess)
        
      # check if win
      if self.visible == self.hidden:
        self.draw_board()
        print("Congratulations!")
            
        if self.play_again():
          self.reset()
        else:
          self.quit()
      else:
        self.draw_board()
        self.get_guess()

  """
      Check whether guess is in hidden_word or not  
  """
  def check_guess(self, guess):

    vis_word = list(self.visible)
    hid_word = list(self.hidden)
    
    if guess not in self.incorrect_guesses and guess not in vis_word:
      # has not been attempted/guessed before
      if guess in set(hid_word):
        for i, elem in enumerate(hid_word):
          if guess == elem:
            vis_word[i] = guess
      else:
          self.incorrect_guesses.append(guess)

    self.visible = ''.join(vis_word)
    

  """
      Prompt user if he/she would like to play another game.
      
      returns bool
  """
  def play_again(self):

    another_game = input("Would you like to play again? (y)es | (n)o")    
    while another_game.upper() not in ('y', 'n'):
      # invalid input detected
      another_game = input("Press y to play again, n to quit.")
        
    if another_game.lower() == 'y':
      return True
    else:
      return False

  def quit(self):
    print("Thank you for playing! Good bye!")
    exit()

        
