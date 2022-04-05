#include <ctype.h>
#include <signal.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define COMMAND_BUF_SIZE 50
#define GREP_STRING_SIZE 15           // Not a lot of space, eh? :)

// Exit program after 10s
void timeout() {
  printf("\nToo slow!\n");
  _exit(1);
}

int main(int argc, char *argv[]) {
  setvbuf(stdin,  NULL, _IONBF, 0);   // Switch off I/O buffering
  setvbuf(stdout, NULL, _IONBF, 0);   // Switch off I/O buffering
  setvbuf(stderr, NULL, _IONBF, 0);   // Switch off I/O buffering

  signal(SIGALRM, timeout);           // Set program to exit on timeout
  alarm(10);                          // Exit program after 10s

  setregid(getegid(), getegid());     // Set real and effective group IDs

  int i = 0;
  char c, grep_string[GREP_STRING_SIZE + 1];
  char *blacklist_filter = " `!$?:(){},*/\\<>-", *blacklist_keyword = "flag";
  bool invalid_input = false;

  char *banner = "  ________________               \n"
                 "< Flag - Sneakpeek >             \n"
                 "  ----------------               \n"
                 "         \\   ^__^               \n"
                 "          \\  (oo)\\_______      \n"
                 "             (__)\\       )\\/\\ \n"
                 "                 ||----w |       \n"
                 "                 ||     ||       \n";

  printf("%s", banner);
  printf("Enter a pattern to match lines in flag: ");
  fflush(stdout);

  // Read user input character by character
  while (i < GREP_STRING_SIZE && (c = getchar()) != EOF && c != '\n') {
    // Only append non-null, printable ASCII characters to parameter passed to grep command
    if (c != '\0' && c < '\x7f' && strchr(blacklist_filter, c) == NULL) {
      grep_string[i] = c;
      i++;
    }
    else {
      printf("died at %02x\n", c);
      invalid_input = true;
    }
  }

  // Blacklisted keyword is not permitted
  if (strstr(grep_string, blacklist_keyword) != NULL) {
    invalid_input = true;
  }

  // User input is empty
  if (i == 0) {
    printf("Awww I hope you don't regret missing this exclusive sneakpeek!\n");
    _exit(0);
  }
  // Invalid input detected => Exits program.
  else if (invalid_input) {
    printf("Hey hey hey! I told you to be nice!\n");
    printf("I don't want to see forbidden characters again.\n");
    fflush(stdout);
    _exit(1);
  }

  // C strings need to be NULL-terminated
  grep_string[i] = '\x00';

  // Insert grep pattern into the command
  // Reads first 10 characters of flag.txt and pass it to grep command.
  char command[COMMAND_BUF_SIZE + 1];
  
  snprintf(command, COMMAND_BUF_SIZE, "head -c 10 './flag.txt' | grep '%s'", grep_string);

  // Execute command
  printf("\nExecuting command: %s\n", command);
  printf("Here's your sneak peek:\n");
  fflush(stdout);

  system(command);
  fflush(stdout);

  return 0;
}
