#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <string.h>

#define EXIT_SUCCESS 0
#define EXIT_FAILURE 1
#define CODE_LENGTH 4
#define ATTEMPTS_DEFAULT 10

// main project
// generate Secret Code
// Pieces will be '0' '1' '2' '3' '4' '5' '6' '7' '8'.
// print secret code

// If the player finds the code, he wins, and the game stops.
// A misplaced piece is a piece that is present in the secret code butthat is
// not in a good position.
// You must read the player's input from the standard input.

// EXIT_SUCCESS & EXIT-FAILURE
// 10 GUESSES
// features
// attempts / custom code

// qwasar hints
//- Proper usage of `read()` for input.

//- Efficient handling of multiple file compilation without including them.

// - Adhering to macro restrictions and avoiding forbidden functions.

// **Tips for the Project:**

// - Use `man` pages for `read()` and `rand()`.

// - Pay attention to case sensitivity in the Makefile.
//  -----------------------------------------
// ./a.out = run code
// gcc mastermind = compile
// work on Pseudo coding
// main focus
// more comments!!!!!!
// test my code as i go!!!!!!!!!!!
// better time management
// test more often
// my_mastermind.c

// Function to read a line from standard input

void generateSecretCode(char *code) { //The purpose of this function is to generate a secret code.
    srand(time(NULL)); //Initializes the random number generator 
    for (int i = 0; i < CODE_LENGTH; ++i) {
        code[i] = '0' + rand() % 9;
    }
    code[CODE_LENGTH] = '\0'; // ensures that the generated code is null-terminated
}

void printPrompt() { 
    printf("Will you find the secret code?\nPlease enter a valid guess\n");
}

int isValidInput(const char *input) { //  check player's input for a valid guess
    if (strlen(input) != CODE_LENGTH) { //  checks the length of input vs code_length
        return 0;
    }
//      for loop
//  return an integer - 0 false/invalid, 1 true/valid
    for (int i = 0; i < CODE_LENGTH; ++i) { //Declares a function that takes a pointer to character as a parameter and return integer.
    //  checking the length
        if (input[i] < '0' || input[i] > '8') {
             //  invalid/false
            return 0;
        }
    }
//  valid/true
    return 1;
}
//pin point why 4321 misplaeced pieces are double.
//this line declares my evaluteGuess function.
void evaluateGuess(const char *secretCode, const char *guess, int *wellPlaced, int *misplaced) {
    *wellPlaced = 0; //don't need pointers for wellPlaced & misplaced.
    *misplaced = 0;
//dont use an int arry 
//  warren 
//      secret count - does nothing in this function
//      guess count     10 int   intarray = {0,1,2,3,4}
//      
//  logic for project -> remaining guesses 10 -> user guess -> check guess
//                                                              either wrong or right
//                                                              if wrong -> guess count - 1 = 9
//                                                              if right -> guess count doesn't change -> user wins/end game
    int guessCount[10] = {0};

    for (int i = 0; i < CODE_LENGTH; ++i) {
        if (guess[i] == secretCode[i]) {
            (*wellPlaced)++;
        } else {
            guessCount[secretCode[i] - '0']++;
        }
    }

    // Count misplaced
    for (int i = 0; i < CODE_LENGTH; ++i) {
        if (secretCode[i] != guess[i] && guessCount[guess[i] - '0'] > 0) {
            (*misplaced)++;
            guessCount[guess[i] - '0']--; // Reduce the count as it is used
        }
    }
}

// warren notes - don't use ternaries, your misplaced will never be negative. rewrite it lines 99 - 108, figure out the logic again
//  line 99 - why hardcode 10? user can use -t flag to make as many guesses as they want
//  review data types - what they do, how they're used and why. i.e. int vs *int vs &int vs int[] vs int[10]
//  also review i++ vs ++i
//  don't guess on your code ever, always know exactly how xyz works and why

// main project
int main(int argc, char *argv[]) { //The standard entry point of a C program.
     //  default attempts
    int attempts = ATTEMPTS_DEFAULT;//Declares and initializes a variable number of attempts the player has to guess the secret code.
    char secretCode[CODE_LENGTH + 1];
 // Initialization of Command-line
    if (argc > 1) {//Checks for command-line arguments other than the program name.
        for (int i = 1; i < argc; ++i) {//Initiates a loop to iterate through the command-line arguments
            if (argv[i][0] == '-' && argv[i][1] == 'c') { //specify the secret code.
                if (i + 1 < argc) {//Checks if there is an argument following -c.
                    strncpy(secretCode, argv[i + 1], CODE_LENGTH);//Copies CODE_LENGTH characters from the argument to the secretCode
                    secretCode[CODE_LENGTH] = '\0';//Adds a null terminator to secretCode to make it a valid string.
                } else {
                    fprintf(stderr, "Error: Missing secret code argument.\n");
                    return EXIT_FAILURE;
                }//Checks if the current argument is an option -t to specify the number of attempts.
            } else if (argv[i][0] == '-' && argv[i][1] == 't') {
                if (i + 1 < argc) { //Checks if there is an argument following -t.
                    attempts = atoi(argv[i + 1]);//Converts the argument to an integer and assigns it to the attempts variable.
                } else {
                    fprintf(stderr, "Error: Missing attempts argument.\n");
                    return EXIT_FAILURE;
                }
            }
        }
    }
 // generate Secret Code
           // Pieces will be '0' '1' '2' '3' '4' '5' '6' '7' '8'.
           // print the Secret Code
    if (secretCode[0] == '\0') {//This condition checks if the secretCode is an empty string
        generateSecretCode(secretCode); //If the condition is true it generate a new secret code
    }
    //secret = 1234
    char guess[CODE_LENGTH + 1];//this array is intended to store the player's guess for the secret code
    int wellPlaced, misplaced;//variables used to store the counts of well-placed and misplaced pieces in the player's guess.

    printPrompt();

    for (int round = 0; round < attempts; ++round) { //This loop represents the rounds of the game.
        int bytesRead = read(0, guess, CODE_LENGTH + 1); //The number of bytes actually read is stored in the bytesRead variable.
        if (bytesRead == 0) {//Checks if the number of bytes read is 0. 
            printf("\n");//Prints a newline
            return EXIT_SUCCESS;
        }

        guess[bytesRead - 1] = '\0'; // Remove newline

        if (!isValidInput(guess)) {//Checks if the result of the function is false
            fprintf(stderr, "Wrong input!\n");//Prints an error message.
            continue;//If the input is not valid the statement is used to skip the loop.
        }
                        //1234    1111      1           3
                        //1234    1211      2           2
        evaluateGuess(secretCode, guess, &wellPlaced, &misplaced);

        printf("---\nRound %d\n>%s\nWell placed pieces: %d\nMisplaced pieces: %d\n", round, guess, wellPlaced, misplaced);

        if (wellPlaced == CODE_LENGTH) {
            printf("Congratz! You did it!\n");
            return EXIT_SUCCESS;
        }
    }

    printf("Sorry, you couldn't find the secret code. It was %s\n", secretCode);
    return EXIT_SUCCESS;
}


    

    // If the player finds the code, he wins, and the game stops.
    // A misplaced piece is a piece that is present in the secret code butthat
    // is not in a good position.
    // You must read the player's input from the standard input.

    // EXIT_SUCCESS & EXIT-FAILURE
    // 10 GUESSES
    //check out EOF which is equal to 0 to end program
