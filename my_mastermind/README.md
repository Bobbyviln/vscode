# Welcome to My Mastermind
***

## Task
The task is to create a Mastermind game in C. The challenge lies in generating a secret code, allowing the user to guess the code, providing feedback on each guess, and implementing the game logic wit[...]  

## Description
The project consists of a C program that simulates the Mastermind game. It generates a random secret code, allows the user to input guesses, and provides feedback on each guess, indicating the number [...]  

## Installation
To install and compile the project, follow these steps:

- Clone the repository to your local machine.
- Navigate to the project directory.
- Run the make command to compile the code.
- Execute the compiled program.

## Usage
To play the game, run the compiled program from the command line with optional arguments:

./my_mastermind -c [SECRET_CODE] -t [ATTEMPTS]

Replace [SECRET_CODE] with a 4-digit number to set a custom secret code.
Replace [ATTEMPTS] with the desired number of attempts. If not specified, the default is 10.

Example:

./my_mastermind -c 1234 -t 10

This command starts the game with a secret code of "1234" and 10 attempts.

Once the game starts, follow the prompts to input your guesses. After each guess, the program will provide feedback on the correctness of your guess.

### The Core Team

crockett_r

<span><i>Made at <a href='https://qwasar.io'>Qwasar SV -- Software Engineering School</a></i></span>
<span><img alt='Qwasar SV -- Software Engineering School's Logo' src='https://storage.googleapis.com/qwasar-public/qwasar-logo_50x50.png' width='20px' /></span>