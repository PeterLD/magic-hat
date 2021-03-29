#!/usr/bin/env python

import os
import shutil
import random
import time
import click
from default_questions import question_list

HOME_DIR = os.path.expanduser('~')
CONFIG_DIR = os.path.join(HOME_DIR, '.magic-hat')
QUESTIONS_FILEPATH = os.path.join(CONFIG_DIR, 'questions.txt')
UNUSED_FILEPATH = os.path.join(CONFIG_DIR, 'unused.txt')

@click.command()
@click.option('--timer', type=int, help='Ask questions every n seconds. ctrl-c to exit.')
def pull(timer):
    """Simple program to generate ice-breaker questions."""
    if timer:
      while True:
        print(get_question())
        time.sleep(timer)
    else:
      print(get_question())

def get_question():
  refresh()

  with open(UNUSED_FILEPATH, "r") as unused_file:
    questions = unused_file.read().split('\n')

  with open(UNUSED_FILEPATH, "w") as unused_file:
    unused_file.write('\n'.join(questions[1:]))
  
  return questions[0]

# Idempotent method to create, populate, and rehydrate question files
def refresh():
  if not os.path.isdir(CONFIG_DIR):
    os.mkdir(CONFIG_DIR)

  # Initialize question file with defaults
  if not os.path.isfile(QUESTIONS_FILEPATH):
    with open(QUESTIONS_FILEPATH, "w") as questions_file:
      questions_file.write('\n'.join(question_list))

  # Initialize or rehydrate unused questions from questions file
  if not os.path.isfile(UNUSED_FILEPATH) or os.path.getsize(UNUSED_FILEPATH) <= 0:
    with open(QUESTIONS_FILEPATH, "r") as questions_file:
      questions = questions_file.read().split('\n')
      random.shuffle(questions)

      with open(UNUSED_FILEPATH, "w") as unused_file:
        unused_file.write('\n'.join(questions))

if __name__ == '__main__':
    pull()