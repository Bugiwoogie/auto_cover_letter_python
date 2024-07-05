import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
import tkinter as tk

load_dotenv()

# configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config
)


def check_and_read_file(): # This functions checks, if there is already some personal information present
  try:
    with open("personal_information.txt", "r") as f:  # Open in read mode ("r")
      content = f.read()
      print("Programm took the existing information out of the file")
      return content
  except FileNotFoundError:
    print(f"File '{"personal_information.txt"}' not found.")
    return ""

def save_personal_data(content):
    try:
      with open("personal_information.txt", "x") as f:  # Try to open in exclusive creation mode ("x")
        f.write(content)
        print(f"File '{"personal_information.txt"}' created and content written successfully.")
    except FileExistsError:  # If the file already exists
        while True:
            overwrite_confirmation = input(f"File '{"personal_information.txt"}' already exists. Overwrite data? (Y/N)")
            if overwrite_confirmation.upper() == "Y":
                with open("personal_information.txt", "w") as f:  # Open in write mode to clear contents
                    f.write(content)
                print(f"File '{"personal_information.txt"}' overwritten with new content.")
                break
            elif overwrite_confirmation.upper() == "N":
                print("Overwrite cancelled. No changes made.")
                break
            else:
                print(f"File '{"personal_information.txt"}' already exists. Overwrite data? (Y/N)")

def get_personal_data():
    while True:
        personal_information = input("Please tell me some personal information i should include in the cover letter: ")
        save_confirmation = input("Do you want your personal data to be saved in a file press (Y/N).")

        if save_confirmation.upper() == "Y":
            save_personal_data(personal_information)
            print("Your information has been saved")
            break
        elif save_confirmation.upper() == "N":
            print("Your information has not been saved")
            break
        else:
            print("Invalid choice. Please try again. Press (Y/N) to save your personal information.")
    
    return personal_information

def ask_for_taking_existing_personal_information(personal_information_from_file):
    take_existing_data_confirmation = input(f'There is already some personal information stored.\n\nContent:\n{personal_information_from_file}\n\nDo you want to take the existing information or type some new content? (Y/N)')
        
    while True:
        if take_existing_data_confirmation.upper() == "Y":
            personal_information = personal_information_from_file
            print("Personal data were taken from file")
            personal_information_took_from_file = True
            break
        elif take_existing_data_confirmation.upper() == "N":
            personal_information_took_from_file = False
            break
        else:
            take_existing_data_confirmation = input(f'Invalid input...\n\nThere is already some personal information stored.\n\nContent:\n{personal_information_from_file}\n\nDo you want to take the existing information or type some new content? (Y/N)')
    
    return personal_information_took_from_file

def get_personal_information():
    personal_information_from_file = check_and_read_file()

    if personal_information_from_file != "":
        personal_information_took_from_file = ask_for_taking_existing_personal_information(personal_information_from_file)
        print("in if personal_information_from_file != "":", personal_information_took_from_file)
    else:
        personal_information = input("Please tell me some personal information i should include in the cover letter: ")
        personal_information_took_from_file = False

    if not personal_information_took_from_file:
        personal_information = get_personal_data()

def generate_prompt(job_describtion, about_the_company, personal_information):
    prompt = f'Generate a cover letter for a job application in german.\njob description:\n{job_describtion}\n\nabout the company:\n{about_the_company}\n\ngive a personal touch to the cover letter with this information:\n{personal_information}\n\nThe first praragraph has to catch the attention of the reader, has to tell about my unique selling points and let the reader want to read further through this cover letter. My unique selling points are, that i love developing and use my skills as my hobby as well as professional and iam top motivated to learn new programming languages.\ndo only output the cover letter'

def get_job_describtion():
    print("yolo")

def main():
    job_describtion = get_job_describtion()
    about_the_company = input("Please give me some information about the company: ")
    personal_information = get_personal_information()

    # Make AI request
    chat_session = model.start_chat(history=[])
    # response = chat_session.send_message(generate_prompt(job_description, about_the_company, personal_information))

    print(response.text)

if __name__ == "__main__":
  main()