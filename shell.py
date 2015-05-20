#!/usr/bin/env python3

import os, sys

def execute(args=list):
  output_file = ''

  if len(args) > 1 and args[-2] == '>':
    output_file = args[-1]
    args = args[:-2]
    file_descriptor = open(output_file, "w+")
    os.dup2(file_descriptor.fileno(), sys.stdout.fileno())

  os.execvp(args[0], args)

def pipe_exec(out_command, in_command, readfd, writefd):
  pid = os.fork()

  if pid == 0:
    pid2 = os.fork()

    if pid2 == 0:
      os.dup2(writefd, sys.stdout.fileno())
      execute(out_command)
      os.close(readfd)

    else:
      os.wait()
      os.dup2(readfd, sys.stdin.fileno())
      execute(in_command)

  else:
    os.wait()

def main():
  while True:
    line = input('dtshell$ ')
    args = line.split(' ')

    if line == '':
      continue

    elif args[0] == 'exit':
      sys.exit()

    elif args[0] == 'cd':
      os.chdir(args[1])

    elif '|' in args:
      read, write = os.pipe()
      pipe_location = args.index('|')
      pipe_exec(args[:pipe_location], args[pipe_location+1:], read, write)

    else:
      pid = os.fork()

      if pid == 0:
        execute(args)

      else:
        os.wait()

if __name__ == "__main__":
  main()

"""
<geirha> and once the pipe is created, you fork, and inside the child, connect stdout to the writing end of the pipe with dup2(), then execve the command.  In the parent you fork again, and in the child connect stdin to the reading end of the pipe and execve
<geirha> oh yeah, and in the first child, you close the reading end of the pipe. and in the second child, close the writing end of the pipe
<dtscode> Oh wait I need to pipe before I fork?
<greycat> that's how both children have access to the same pipeline
"""
