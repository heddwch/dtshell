#!/usr/bin/env python3

import os, sys
import signal

def hook_c(signal, frame):
  print('^c')

signal.signal(signal.SIGINT, hook_c)

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

      if len(args) > 1 and args[-2] == '>':
        output_file = args[-1]
        args = args[:-2]
        file_descriptor = open(output_file, "w+")
        os.dup2(file_descriptor.fileno(), 1)

      os.execvp(args[0], args)

  else:
    os.wait()
