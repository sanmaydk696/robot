import speech_recognition as speech
from gtts import gTTS
import pygame
import time
import pyttsx3

engine = pyttsx3.init()

pygame.init()
fps = pygame.time.Clock()
width = 600
height = 600
surface = pygame.display.set_mode((width, height))
pygame.display.set_caption("Draic Bot")
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blink_time = 0
is_blinking = False
current_expression = 'neutral'
def eyes():
    pygame.draw.circle(surface, black, (width // 2 - 30, 180), 10)  # Left eye
    pygame.draw.circle(surface, black, (width // 2 + 30, 180), 10)  # Right eye

def neutral(is_blinking):
    if is_blinking:
        pygame.draw.line(surface, black, (width // 2 - 40, 180), (width // 2 - 20, 180), 3)  # Left eye closed
        pygame.draw.line(surface, black, (width // 2 + 20, 180), (width // 2 + 40, 180), 3)  # Right eye closed
    else:
        eyes()  
    pygame.draw.line(surface, black, (width // 2 - 30, 240), (width // 2 + 30, 240), 3)  # Neutral mouth


def moods(mood):
    eyes()  
    if mood == 'happy':
        pygame.draw.arc(surface, black, (width // 2 - 30, 230, 60, 40), 3.14, 6.28, 3)  # Happy mouth
    elif mood == 'sad':
        pygame.draw.arc(surface, black, (width // 2 - 30, 250, 60, 40), 0, 3.14, 3)  # Sad mouth
    elif mood == 'angry':
        pygame.draw.arc(surface, black, (width // 2 - 30, 250, 60, 40), 0, 3.14, 3)  # Angry mouth
        pygame.draw.line(surface, black, (width // 2 - 40, 160), (width // 2 - 20, 170), 3)  # Left eyebrow
        pygame.draw.line(surface, black, (width // 2 + 20, 170), (width // 2 + 40, 160), 3)  # Right eyebrow



engine.setProperty('rate', 100)
engine.say("say something")
engine.runAndWait()

s = speech.Recognizer()
with speech.Microphone() as source:
    s.adjust_for_ambient_noise(source)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        surface.fill(white)
        current_time = time.time() 
        if current_time - blink_time > 1:
            is_blinking = not is_blinking
            blink_time = current_time  
        if current_expression == 'neutral':
            neutral(is_blinking)
        else:
            moods(current_expression)             
        try:
            
            audio = s.listen(source, timeout = 3, phrase_time_limit = 3)
            print("listening...")
            recognized_text = s.recognize_google(audio)
            print("you said: "+ recognized_text)

            if "hello" in recognized_text.lower():

                engine.say("hey sanmay, whats up?")
                engine.runAndWait()
            if "be happy" in recognized_text.lower():
                current_expression = 'happy'
                engine.say("I am always happy")
                engine.runAndWait()
            if "be sad" in recognized_text.lower():
                current_expression = 'sad'
                engine.say("why you want me sad?")
                engine.runAndWait()
            if "be angry" in recognized_text.lower():
                current_expression = 'angry'
                engine.say("now, you are making me angry")
                engine.runAndWait() 
            if "go to sleep"in recognized_text.lower():
                current_expression = 'neutral'
                engine.say("bye bye")
                engine.runAndWait()
                pygame.quit()   
                break           
        except speech.UnknownValueError:
                print("Google could not understand the audio")
        except speech.RequestError as e:
                print(f"Google API error; {e}")
        except Exception as e:
                print(f"An unexpected error occurred: {e}")                 
        pygame.display.flip()
        fps.tick(60)