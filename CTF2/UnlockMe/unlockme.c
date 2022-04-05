#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

char * read_file(char *);
void give_flag();
void give_error();
void timeout();

int i, input_char;

int main(int argc, char * argv[]) {
  setvbuf(stdin,  NULL, _IONBF, 0);   // Switch off I/O buffering
  setvbuf(stdout, NULL, _IONBF, 0);   // Switch off I/O buffering
  setvbuf(stderr, NULL, _IONBF, 0);   // Switch off I/O buffering

  signal(SIGALRM, timeout);           // Set program to exit on timeout
  alarm(10);                          // Exit program after 10s

  void (*call_function)() = &give_error;  // function pointer to invoke function later on
  char input[128];

  // Check program usage
  if (argc < 2) {
    printf("Secret value needs to be supplied as an argument to this program!\n");
    printf("Example: ./unlockme secret\n");
    return 1;
  }
  else if (strlen(argv[1]) != 128) {
    printf("Secret value must be exactly 128 characters long!\n");
    return 1;
  }

  printf("Enter the secret value to unlock the flag => ");
  for (i = 0; i <= 128; i++) {
    input_char = getchar();
    // Exit loop if end of user input is reached
    if (feof(stdin) || ferror(stdin) || input_char == '\n' || input_char == '\x00') {
      input[i] = '\x00';
      break;
    }
    else {
      input[i] = input_char;
    }
  }

  // Check if user input equals to secret value
  if (strcmp(input, argv[1]) == 0) {
    call_function = &give_flag;  // give user flag!
  }

  // If user input is incorrect, print error
  if (call_function != &give_flag) {
    call_function = &give_error;
  }

  call_function();

  return 0;
}

// Read contents of file and return a string containing the contents
char * read_file(char * filename) {
  char * file_contents = malloc(4096 * sizeof(char));

  FILE * file;
  file = fopen(filename, "r");

  if (file == NULL) {
    printf("\nUnable to open file!\n");
    _exit(1);
  }

  fread(file_contents, 4096, sizeof(char), file);
  fclose(file);

  return file_contents;
}

// Print flag
void give_flag() {
  printf("\nOkay here you go: %s", read_file("flag.txt"));
  _exit(0);
}

// Print error message
void give_error() {
  printf("\nNah the secret value you've provided is incorrect!\n");
  _exit(1);
}

// Exit program after 10s
void timeout() {
  printf("\nToo slow!\n");
  _exit(1);
}
