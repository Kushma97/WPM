import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 900, 500

screen = pygame.display.set_mode((WIDTH,HEIGHT))
# surface = pygame.surface((WIDTH,HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("!!!WPM!!!")
timer = pygame.time.Clock()
fps = 60

#Game variables
characters = list("abcdefghijklmnopqrstuvwxyz,?.\"\':@!#() ")
paused = False
def getText():
    with open("wpm_text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()
sentence = getText()
typedText = ''
start_time = None
elapsed_time = 0
paused_time = 0
pause_start = None
wpm = 0

header_font = pygame.font.Font("RobotoSlab-VariableFont_wght.ttf", 32)
textfont = pygame.font.SysFont("calibri", 28, bold=True)

class Button:
  def __init__(self, xPos, yPos, surf, text, clicked):
    self.xPos = xPos
    self.yPos = yPos
    self.surf = surf  
    self.text = text
    self.clicked = clicked
  def drawCircles(self):
    cir = pygame.draw.circle(self.surf, (45, 89, 135), (self.xPos, self.yPos), 24) 
    if cir.collidepoint(pygame.mouse.get_pos()):
      butns =  pygame.mouse.get_pressed()
      if butns[0]: #If button is clicked not just hovered by mouse, changing the color
          pygame.draw.circle(self.surf, (190, 23, 44), (self.xPos, self.yPos), 24) 
          self.clicked = True
      else: #changing color when just hovered
        pygame.draw.circle(self.surf, (190, 89, 135), (self.xPos, self.yPos), 24) 

    pygame.draw.circle(self.surf, 'white', (self.xPos, self.yPos), 24, 3) 
    self.surf.blit(header_font.render(self.text, True, 'white'), (self.xPos-12, self.yPos - 22)) 

    text_surface = header_font.render(self.text, True, 'white')
    text_width, text_height = header_font.size(self.text)
    self.surf.blit(text_surface, (self.xPos - text_width // 2, self.yPos - text_height // 2))

def mesuring_wpm(words, elapsed_time):
  sentence_list = sentence.split()
  typed_list = typedText.split()
  extratime = 0
  for word1, word2 in zip(sentence_list, typed_list):  # Loops through words
    # print(word1, word2)
    min_length = min(len(word1), len(word2)) 
    for i in range(min_length):
      if word1[i] != word2[i]:
        extratime += 1
  totaltime = elapsed_time + extratime
  wpm = round((words / totaltime) * 60)
  return wpm
      
def drawPause():
  surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
  pygame.draw.rect(surface, (211,211,211,50), [130, 150, 510, 170], 0, 5) # 0 border-thickness, 5 is edge
  pygame.draw.rect(surface, (0,0,0,200), [130, 150, 510, 170], 5, 5)
  # Creating pause buttons menu from Button class
  restart_btn = Button(200, 245, surface, '>', False)
  restart_btn.drawCircles()
  quit_btn = Button(460, 245, surface, 'X', False)
  quit_btn.drawCircles()
  # defining options for pause menu
  surface.blit(header_font.render(f'WPM:{wpm}', True, 'Red'), (300, 170))
  surface.blit(header_font.render('PLAY!', True, 'red'), (230, 220))
  surface.blit(header_font.render('QUIT', True, 'red'), (490, 220))

  screen.blit(surface, (0,0))
  return restart_btn.clicked, quit_btn.clicked

def reset_game():
  #Resetting all the game variables to replay.
  global sentence, typedText, start_time, elapsed_time, wpm, paused
  sentence = getText()  # Get a new sentence
  typedText = ''  # Clear typed text
  start_time = None  # Reset timer
  elapsed_time = 0  # Reset elapsed time
  wpm = 0  # Reset WPM counter
  paused = False  # Unpause the game
  print("Game resetted")

# Function to wrap text
def wrap_text(text, font, max_width):
  words = text.split(' ')
  lines = []
  current_line = ''

  for word in words:
    # Check the width of the current line plus the new word
    test_line = current_line + ' ' + word if current_line else word
    text_width, _ = font.size(test_line)
    if text_width <= max_width:
      current_line = test_line
    else:
      lines.append(current_line)
      current_line = word

  if current_line:
    lines.append(current_line)
    
  return lines

def displayText():
  # Displaying the text
  surface = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
  pygame.draw.rect(surface, (30,103,0, 100), [40, 80, WIDTH-60, HEIGHT-300], 0, 4)
  lines = wrap_text(sentence, textfont, WIDTH - 70)
  y_offset = 120 #Initial vertical position
  for line in lines:
    text = textfont.render(line, True, 'white')
    surface.blit(text, (65, y_offset))
    y_offset += textfont.get_height()  # Move down for next line 

  screen.blit(surface,(0,0))

def displayTypedTxt():
  lines = wrap_text(typedText, textfont, WIDTH - 70)
  y_offset = HEIGHT-150   
 # Typed text at the bottom
  for line in lines:
    text = textfont.render(line, True, "white")
    screen.blit(text, (80, y_offset))
    y_offset += textfont.get_height()

def draw_screen():
  pygame.draw.rect(screen, 'white', [0, 0, WIDTH, HEIGHT], 5)
  pygame.draw.rect(screen, (65, 90, 245), [5, HEIGHT-180, WIDTH-10, 180], 0)
  pygame.draw.line(screen, 'white',(5, HEIGHT-180), (WIDTH-6, HEIGHT-180), 3)
  pygame.draw.rect(screen, 'white', (0, 0, WIDTH, HEIGHT), 2)

  screen.blit(header_font.render(f"Time: {int(elapsed_time)}", True, 'white'), (20, 20))
  screen.blit(header_font.render(f"WPM: {wpm}", True, 'white'), (280, 20))

  pauseBtn = Button(WIDTH-37, 33, screen, '| |',False )
  pauseBtn.drawCircles()

  displayText()
  displayTypedTxt()

  return pauseBtn.clicked

#Main Game Loop
run = True
while run:
  screen.fill("black")
  timer.tick(fps)
  pauseBtn = draw_screen()
  if pauseBtn:
    paused = True
  if paused:
    restart_btn, quitBtn = drawPause()
    if restart_btn:
      reset_game()
      paused = False
      # if start_time is not None and pause_start is not None: #Adjusting the start_time so the timer resumes correctly.
      #   paused_time += time.time() - pause_start
      #   pause_start = None
    if quitBtn:
      run = False
  if start_time is not None and not paused:
    elapsed_time = time.time() - start_time 
  # elif start_time is not None and paused:
  #   pause_start = time.time()  # Getting the time at which the game was paused
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if event.type == pygame.KEYDOWN:
      if not paused:
        if start_time is None:
          start_time = time.time()  # Start timer on first keypress
        if event.unicode.lower() in characters:
          typedText += event.unicode
        if event.key == pygame.K_BACKSPACE and len(typedText)>0:
            typedText = typedText[:-1]

        if event.key == pygame.K_ESCAPE:
          if paused:
            paused = False
          else:
            paused = True

        if event.key == pygame.K_RETURN:
          end_time = time.time()
          elapsed_time = end_time - start_time
          words = len(typedText.split())  #Counting the words in the sentence
          wpm = mesuring_wpm(words, elapsed_time)
          drawPause()
          paused = True
          start_time = None

  pygame.display.flip()

pygame.quit()

