import os
import sys
import time
import random
import pyautogui
from PIL import Image, ImageGrab
import google.generativeai as genai

def print_same_line(text):
    # Clear the line and move the cursor to the beginning
    sys.stdout.write("\033[2K\r")
    # Print the new text
    sys.stdout.write(text)
    sys.stdout.flush()


def capture_left_screen():
    #Capture and save a screenshot of the left half of the screen.
    full_screenshot = ImageGrab.grab()
    screen_width, screen_height = full_screenshot.size
    left_side_region = (0, 0, screen_width // 2, screen_height)
    left_screenshot = ImageGrab.grab(bbox=left_side_region)
    left_screenshot.save("screenshot.png")

def generate_code_from_image(api_key):
    #Generate code from the screenshot using the Gemini API.
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = "give me the c code for the attached question remove all the extra text just the code as if I am typing on terminal"
    img = Image.open("screenshot.png")
    response = model.generate_content([prompt, img])
    return response.text[5:-3]  # Remove leading and trailing characters

def save_code_to_file(code):
    #Save the generated code to a file.
    with open("code.txt", "w") as code_file:
        code_file.write(code)
def human_typing_simulation():
    time.sleep(random.uniform(0.2, 0.3))    
    if random.random() < 0.05:  # 10% chance of adding a random pause
        time.sleep(random.uniform(1, 3))
    
    if random.random() < 0.1:  # 10% chance of simulating a typo
        typo = chr(random.randint(33, 44))
        pyautogui.typewrite(typo)
        time.sleep(random.uniform(0.1, 0.3))
        pyautogui.press("backspace")

def typing(code):
    #Simulate typing the code with realistic delays and errors.
    lines = code.split('\n')
    for line in lines:
        line=line.strip()
        # if line.strip().startswith('#'):
        #     continue
        for char in line:
            if char == ' ':
                pyautogui.press("space")
            else:
                pyautogui.press(char)
            human_typing_simulation()
        pyautogui.press("enter")

def main():
    print("-- Developed By Harshit Singh ---")
    # Capture screenshot
    capture_left_screen()
    
    # Generate code
    print("-- Waiting for Response --")
    api_key = os.environ["API_KEY"]
    generated_code = generate_code_from_image(api_key)
    # Save and display code
    save_code_to_file(generated_code)
    
    # Simulate typing
    print_same_line("-- Entering Code --")
    typing(generated_code)
    
    # Clean up
    os.remove("screenshot.png")
    os.remove("code.txt")

if __name__ == "__main__":
    main()