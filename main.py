#!/usr/bin/python3
# -*- coding: utf-8 -*-

# =============================================================================
#
#        FILE:  main.py
#      AUTHOR:  Tan Duc Mai <henryfromvietnam@gmail.com>
#     CREATED:  2021-08-20
# DESCRIPTION:  Retrieve the content of Merriam-Webster online dictionary.
#   I hereby declare that I completed this work without any improper help
#   from a third party and without using any aids other than those cited.
#
# =============================================================================


# ------------------------------- Module Imports ------------------------------
"""Description of all imported modules.

The time module - sleep() function - gives a short break (0.5 second) between
each major part of the program.

The urllib.request module - urlretrieve - retrieves the content of a URL
directly into a local location on disk.

The bs4 module - BeautifulSoup() function - downloads data of HTML files from
the website.

The pygame module - mixer() function - loads and plays sound or the mp3 file.
This is what I use to play the pronunciation file downloaded by using the
urlretrieve() function.

The requests module - get() function - allows for the exchange of HTTP
requests.

The functions module - a user-defined module - contains a set of three
functions which I separate from the main program to improve code legibility and
code reuse.
"""
# Standard library imports.
from time import sleep
from urllib.request import urlretrieve

# Related third party imports.
from bs4 import BeautifulSoup
from pygame import mixer
from requests import get

# Local application/library specific imports.
import functions as func


# ------------------------------- Main Function -------------------------------
if __name__ == '__main__':
    # Welcome message.
    func.draw_line_break()
    print('Welcome to the Dictionary of Merriam-Webster')
    func.draw_line_break()

    # Word of the Day.
    url = 'https://www.merriam-webster.com/dictionary'
    res = get(url)
    text = res.text
    soup = BeautifulSoup(res.content, 'html.parser')

    day = soup.find('a', attrs={'href': '/word-of-the-day'})
    for _ in range(2):
        day = day.find_next('a', attrs={'href': '/word-of-the-day'})
    print('Word of the Day:', day.get_text())

    # Look up a word.
    func.draw_line_break()
    word = None
    while word is None or word == '':
        word = input('Search for a Word: ')
        if word == '':
            print('Please Enter a non-empty word.', end='\n\n')

    # Connect to the dictionary.
    url = f'https://www.merriam-webster.com/dictionary/{word}'
    res = get(url)
    text = res.text
    soup = BeautifulSoup(res.content, 'html.parser')

    # Validate word that is not in the dictionary.
    false_message = "isn't in the dictionary"
    while false_message in text:
        print(f'The word you\'ve entered, "{word}", {false_message}.\n')
        word = None
        while word is None or word == '':
            word = input('Try again: ')
            if word == '':
                print('Please Enter a non-empty word.', end='\n\n')
        url = f'https://www.merriam-webster.com/dictionary/{word}'
        res = get(url)
        text = res.text
        soup = BeautifulSoup(res.content, 'html.parser')

    # Now we have a valid word.
    func.draw_line_break()

    # Get the definition.
    # Count the number of definitions of the word.
    count = text.count('dtText')

    print(f'-> Definition of {word.upper()}:', end='\n\n')

    if count == 1:                  # If the word has only 1 definition
        definition = soup.find('span', class_='dtText')
        print(definition.get_text())
    else:                           # If the word has more than 1 definitions
        try:
            definition = soup.find('span', class_='dtText')
            print('Entry 1', definition.get_text(), sep='')
            func.find_all_definitions(count, definition)
        except AttributeError:
            print(': LAST ENTRY FOUND!')

    sleep(0.5)

    # MP3: the pronunciation file.
    func.draw_line_break()

    try:
        # Call the function to return the list of the elements of the URL of
        # the mp3 file for pronouncing.
        url = func.mp3(text)

        # Convert the mp3_url from a list into a string.
        mp3_url = ''.join(url)

        # Ask the user whether they want to hear the pronunciation.
        acceptable_response = ('Y', 'y', 'N', 'n', '')
        pronounce = None
        while pronounce is None or pronounce not in acceptable_response:
            pronounce = input('Do you want to hear its pronunciation? [Y/n] ')
            if pronounce not in acceptable_response:
                print('Please Enter an appropriate command.', end='\n\n')

        # Download the mp3 file to the local directory.
        urlretrieve(mp3_url, 'word_to_pronounce.mp3')

        # Repeatedly pronounce the word if user responds 'y' or presses Enter.
        while pronounce.lower() == 'y' or pronounce == '':
            mixer.init()
            mixer.music.load('word_to_pronounce.mp3')
            mixer.music.play()
            # Ask the user again.
            pronounce = None
            while pronounce is None or pronounce not in acceptable_response:
                pronounce = input('One more time? [Y/n] ')
                if pronounce not in acceptable_response:
                    print('Please Enter an appropriate command.', end='\n\n')
    except ValueError:
        print(
            f'Sorry! There isn\'t a pre-recorded pronunciation for "{word}".'
        )

    sleep(0.5)

    # Close the program.
    func.draw_line_break()
    print('Thank you for using our translation service!')
    func.draw_line_break()
