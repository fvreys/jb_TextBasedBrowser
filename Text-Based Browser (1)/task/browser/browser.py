import os
import requests
from sys import argv
from collections import deque
from bs4 import BeautifulSoup
from colorama import Fore, Style


WHITELIST_TAGS = ["p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "ul", "ol", "li"]
PROTOCOL_IDENTIFIER = "https://"
# Possible change: use os.path.join


def make_dir(directory_name: str):
    if not os.path.exists(directory_name):
        os.mkdir(f".\\{directory_name}")


def show_page(directory_name: str, page_name: str):
    with open(f".\\{directory_name}\\{page_name}", 'r', encoding='utf-8') as fh:
        print(fh.read())


def save_page(directory_name: str, page_name: str, page: str):
    with open(f".\\{directory_name}\\{page_name}", 'w', encoding='utf-8') as fh:
        fh.write(page)


def extract_convert_output(directory: str, content: str):
    soup = BeautifulSoup(content, 'html.parser')
    lines = soup.find_all(WHITELIST_TAGS)
    with open(f".\\{directory}\\webpage", 'w', encoding='utf-8') as output_fh:
        for line in lines:
            if line.name == 'a':
                print(Fore.BLUE + line.text)
                output_fh.write(Fore.BLUE + line.text + '\n')
            else:
                print(Style.RESET_ALL + line.text)
                output_fh.write(Style.RESET_ALL + line.text + '\n')
    with open(f".\\{directory}\\webpage", 'r', encoding='utf-8') as fh:
        page_to_show = fh.read()

    return page_to_show


# Read arguments of script
args = argv
if len(args) != 2:
    print(f"The function should be called with one argument for the output directory")
    dir_webpages = ""
    exit()
else:
    dir_webpages = args[1]
    make_dir(dir_webpages)

# Process instructions and URLs
instruction = input()
pages_stack = deque()
page_to_save = ""
while instruction != "exit":
    if instruction == "back":
        if len(pages_stack) > 0:
            previous_page = pages_stack.pop()
            print(previous_page)
    elif instruction in os.listdir(f".\\{dir_webpages}"):
        show_page(dir_webpages, instruction)
    elif "." not in instruction:
        print("Error: Invalid url - without dot. Please provide another url.")
    else:
        if page_to_save != "":
            # Place previous page in stack
            pages_stack.append(page_to_save)
        if instruction.find(PROTOCOL_IDENTIFIER) == -1:
            instruction = "https://" + instruction
        elif instruction.find(PROTOCOL_IDENTIFIER) > 1:
            print(f"Invalid url - https:// on wrong position {instruction}")

        r = requests.get(instruction)
        page_to_save = extract_convert_output(dir_webpages, r.content)
        filename = instruction[len(PROTOCOL_IDENTIFIER):instruction.rfind('.')]
        save_page(dir_webpages, filename, page_to_save)

    instruction = input()
