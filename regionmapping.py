import re
import subprocess
import time
import threading
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openai
import os
import sys


with open('token.txt', 'r') as file:
    openai.api_key = file.read()
# Define the Chrome user data directory for session persistence
chrome_user_data_dir = "C:\\projects\\projectcodeidentifyingwhatsappmessageandretrieve"  # Change to any directory path you prefer

# Setup Chrome WebDriver with user data directory
options = uc.ChromeOptions()
options.add_argument(f"--user-data-dir={chrome_user_data_dir}")  # Use user data directory
options.add_argument("--profile-directory=Default")  # Use the default profile

# Initialize undetected_chromedriver
driver = uc.Chrome(options=options)

# Open WhatsApp Web
driver.get("https://web.whatsapp.com")
print("If this is your first run, please scan the QR code to log in.")
time.sleep(10)  # Wait for QR code scan if needed

# Navigate to the desired group
group_name = "Test_data_collect"  # Replace with your group name
try:
    print(f"Searching for group: {group_name}")
    group = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, f"//span[@title='{group_name}']"))
    )
    group.click()
    print(f"Entered group: {group_name}")
except Exception as e:
    print(f"Error locating group: {e}")
    driver.quit()
    exit()

def send_sucessful_message(driver, group_name, successful_message):
    try:
        # Search for the group
        group = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, f"//span[@title='{group_name}']"))
        )
        group.click()

        # Locate the message input box
        chat_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='10']"))
        )
        chat_box.click()
        parts = successful_message.split('\n')

        for i, part in enumerate(parts):
            chat_box.send_keys(part)
            if i < len(parts) - 1:
                # Insert a newline without sending the message
                chat_box.send_keys(Keys.SHIFT, Keys.ENTER)
                # Alternatively:
                # chat_box.send_keys(Keys.SHIFT + Keys.ENTER)
                time.sleep(0.1)
        # chat_box.send_keys(successful_message)


        # Locate and click the send button
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]'))
        )
        send_button.click()
        print(f"Successful message sent to group: {group_name}")
    except Exception as e:
        print(f"Error sending message: {e}")



def send_error_message(driver, group_name, error_message):
    try:
        # Search for the group
        group = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, f"//span[@title='{group_name}']"))
        )
        group.click()

        # Locate the message input box
        chat_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='10']"))
        )
        chat_box.click()
        chat_box.send_keys(error_message)

        # Locate and click the send button
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]'))
        )
        send_button.click()
        print(f"Error message sent to group: {group_name}")
    except Exception as e:
        print(f"Error sending message: {e}")


# Function to monitor messages and save to group_chat_log.txt
def monitor_messages():
    print("Monitoring messages. Press Ctrl+C to stop.")
    try:
        while True:
            # Find all messages in the group

            messages = driver.find_elements(By.CSS_SELECTOR, "div.message-in")
            # messages = messages.find_element(By.CSS_SELECTOR, "")
            with open("group_chat_log.txt", "a", encoding="utf-8") as log_file:
                for message in messages:
                    try:
                        # message = message[0:-1]
                        # Extract timestamp
                        # timestamp = message.find_element(By.CSS_SELECTOR, "span.copyable-text").get_attribute("data-pre-plain-text")

                        # Extract sender name and message text
                        text_parts = message.text.split("\n")
                        if len(text_parts) >= 2:
                            text_content = " ".join(text_parts[0:-1])
                            # Format and save message
                            formatted_message = f"{text_content}"
                            log_file.write(formatted_message + "\n")
                            # print(formatted_message)
                    except Exception as e:
                        print(f"Error processing message: {e}")

            # Sleep for a while before checking again
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping monitoring...")
    finally:
        driver.quit()


# Function to continuously update filtered_group_chat_log.txt without duplication
def filter_chat_log():
    print("Starting filtering process...")
    processed_messages = set()

    try:
        while True:
            with open("group_chat_log.txt", "r", encoding="utf-8") as input_file:
                lines = input_file.readlines()

            new_lines = [line for line in lines if line not in processed_messages]
            processed_messages.update(new_lines)

            with open("filtered_group_chat_log.txt", "a", encoding="utf-8") as output_file:
                output_file.writelines(new_lines)

            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping filtering process...")


# Function to process region mapping and combine messages
def process_region_recognize():
    print("Starting Region Recognize process...")
    digit_pattern = re.compile(r"\d+-\d+")  # Detect digit and bet size
    combined_messages = []  # Store combined messages to avoid duplicates
    invalid_input = []
    region_pattern = re.compile(r"^[MPTSBWKHE]{1,9}$", re.IGNORECASE)

    def is_valid_input(input_str):
        has_any_of_MPTWKHE = bool(re.search(r"[MPTWKHE]", input_str, re.IGNORECASE))
        has_uppercase_S = ("S" in input_str)  # simple substring check

        has_valid_letter = has_any_of_MPTWKHE or has_uppercase_S
        if not has_valid_letter:
            return False
        has_digit = bool(re.search(r"\d", input_str))
        if not has_digit:
            return False
        if re.search(r"\d[MPTWKHES]", input_str):
            return False

        return True

    def processAI(input_ai):
        file_path = "basic rules.txt"
        # file_path_1 = "training_chat.txt"
        with open(file_path, "r") as file:
            file_content = file.read()
        # with open(file_path_1, "r") as file:
        #     file_content_1 = file.read()
        Q = "mpt 8579=2 9058=3 st 7676.3 8787.4 3621.8.6.3"
        # Z = "E\n7765  .3 .3 .3 iBox\nH E\n3453 .3\n1143 .3"
        response = openai.ChatCompletion.create(
            model="ft:gpt-4o-2024-08-06:abunene::AkNqx79Y",
            messages=[
                {"role": "system", "content": "Your job is to convert the user input based on knowledge uploaded"},
                {"role": "user", "content": f"Here is the rules \n\n{file_content}\n\n that you "
                                            f"need to understand, Please"
                                            f"look out the region make sure the region is compatible with the number. Now"
                                            f"answer this: {Q}"},
                {"role": "assistant", "content": "D\n#123\n8579#2\n9058#3\n#43\n7676#3\n8787#4\n3621#8#6#3"},
                {"role": "user", "content": f"answer this: {input_ai}"}
            ],
            temperature=0.3,
        )
        return response["choices"][0]["message"]["content"]
    while True:
        with open("filtered_group_chat_log.txt", "r", encoding="utf-8") as input_file:
            lines = input_file.readlines()

        for i, line in enumerate(lines):
            if is_valid_input(line):  # If line contains region mapping
                complete_message = line.strip()
                if complete_message not in combined_messages:
                    combined_messages.append(complete_message)
                    ai_message = processAI(complete_message)
                    print(ai_message)
                    if ai_message != "False":

                        # Write the complete message to RegionRecognize.txt
                        try:
                            print("Start Writing to website....")
                            python_executable = r"C:\Users\weilun\PycharmProjects\toto_project\.venv\Scripts\python"
                            result = subprocess.run(
                                [python_executable, "main.py", ai_message],  # Pass the command and arguments as a list
                                stdout=subprocess.PIPE,  # Capture standard output
                                stderr=subprocess.PIPE,  # Capture standard error
                                text=True,  # Decode output as text (str)
                                check=True  # Raise CalledProcessError on non-zero exit try again
                            )
                            finish_write = result.stdout.strip()
                            print(finish_write)

                            with open("RegionRecognize.txt", "a", encoding="utf-8") as output_file:
                                output_file.write(f"{finish_write}\n")

                            # Format the full receipt message for WhatsApp
                            full_message = finish_write.replace("\n", "\n")
                            print(f"the result going to print :{full_message}")
                            send_sucessful_message(driver, group_name, full_message)


                        except subprocess.CalledProcessError as e:
                            print("An error occurred:")
                            print(e.stderr)

                    else:

                        send_error_message(driver, group_name, f"{ai_message} (Order Receipt)")
                        pass
                        #need to reply to group
                    # subprocess.run('pytest', '')
            else:
                error_input = line.strip()
                if error_input not in invalid_input:
                    invalid_input.append(error_input)
                    print("Not valid input detected:", error_input)
                    send_error_message(driver, group_name, f"{error_input} is not valid, please send it again.")

        time.sleep(1)  # Wait before re-checking the log


# Function to clear the contents of RegionRecognize.txt once after all functions run once
def clear_region_recognize_file_once():
    try:
        with open("RegionRecognize.txt", "w", encoding="utf-8") as file:
            file.write("")
        with open("filtered_group_chat_log.txt", "w", encoding="utf-8") as file:
            file.write("")
        with open("group_chat_log.txt", "w", encoding="utf-8") as file:
            file.write("")
        print("All text file has been cleared once.")
    except Exception as e:
        print(f"Error clearing RegionRecognize.txt: {e}")


# Wrapper function to ensure all other functions run once before clearing RegionRecognize.txt
def initialize_functions_with_clear():
    # Clear RegionRecognize.txt once
    threads = []

    # Start monitor_messages, filter_chat_log, and process_region_recognize as threads
    threads.append(threading.Thread(target=monitor_messages, daemon=True))
    threads.append(threading.Thread(target=filter_chat_log, daemon=True))
    threads.append(threading.Thread(target=process_region_recognize, daemon=True))

    for thread in threads:
        thread.start()

    # Wait for all threads to run once
    time.sleep(10)  # Adjust this delay as needed to ensure all threads initialize and run their first iteration



    # Keep threads running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Main process stopped.")


# Run the initialization process
if __name__ == "__main__":
    clear_region_recognize_file_once()
    initialize_functions_with_clear()
