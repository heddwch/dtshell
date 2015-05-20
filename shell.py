#!/usr/bin/env python3

import os
import string

while True:
  line = input('dtshell$ ')
  args = line.split(' ')
  pid = os.fork()

  if pid == 0:
    output_file = ''

    if len(args) > 1 and args[-2] == '>':
      output_file = args[-1]
      args = args[:-2]
      file_descriptor = open(output_file, "w")
      os.dup2(file_descriptor.fileno(), sys.stdout.fileno())

    os.execvp(args[0], args)

  else:
    os.wait()
