/*
 * Todo:
 *  Make shell hot-swappable via dlfcn.h
 *  Add in >, >>, and < (in that order)
 *  Add in readline support
 *  Put in piping
 *  Put in signal handling
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/types.h>

char *get_line(char prompt[]) {
  fputs(prompt, stdout);
  const int LINE_SIZE = 100;
  char *line = malloc(LINE_SIZE);
  line = fgets(line, LINE_SIZE, stdin);

  char *pos;
  if((pos = strrchr(line, '\n')) != NULL) {
    *pos = ' ';
  }

  return line;
}

char **split(char *line, int *arg_count) {
  char **words = NULL;
  char *word = strtok(line, " ");
  size_t counter = 0;

  while(word != NULL) {
    words = (char**)realloc(words, (counter+1)*sizeof(char*));
    words[counter] = (char*)malloc(strlen(word)+1);
    strcpy(words[counter], word);
    counter++;
    word = strtok(NULL, " ");
  }

  words = (char**)realloc(words, (counter+1)*sizeof(char*));
  words[counter] = NULL;
  *arg_count = counter;
  return words;
}

int main(int argc, char **argv, char **env) {
  while(true) {
    char *line = get_line("dtsh$ ");
    int arg_count;
    char **args = split(line, &arg_count);

    if(strcmp(args[0], "cd") == 0) {
      if((arg_count > 1 && strcmp(args[1], "~") == 0) || arg_count == 1) {
        chdir(getenv("HOME"));
      }

      else {
        chdir(args[1]);
      }
    }

    else if(strcmp(args[0], "exit") == 0) {
      exit(1);
    }

    else {
      pid_t pid = fork();

      if(pid == 0) {
        execvp(args[0], args);
      }

      else {
        int status;
        wait(&status);
      }
    }
  }
}
