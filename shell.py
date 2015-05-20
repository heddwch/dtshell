#!/usr/bin/env python3

import os, sys

while True:
  line = input('dtshell$ ')
  args = line.split(' ')

  if args[0] == 'exit':
    sys.exit()

  pid = os.fork()

  if pid == 0:
    if args[0] == 'cd':
      os.chdir(args[1])

    else:
      output_file = ''
      non_piped_command = True

      if len(args) > 1 and args[-2] == '>':
        output_file = args[-1]
        args = args[:-2]
        file_descriptor = open(output_file, "w+")
        os.dup2(file_descriptor.fileno(), sys.stdout.fileno())

      elif len(args) > 1 and '|' in args:
        pipe_location = args.index('|')
        out_command = args[:pipe_location]
        in_command = args[pipe_location+1:]
        read, write = os.pipe()
        os.dup2(read, sys.stdout.fileno())
        os.execvp(out_command[0], out_command)
        os.dup2(write, sys.stdin.fileno())
        os.execvp(in_command[0], in_command)
        non_piped_command = False

    if non_piped_command:
      os.execvp(args[0], args)

  else:
    os.wait()
