#!/usr/bin/env python3

import os
import string

while True:
  line = input('dtshell$ ')
  args = line.split(' ')
  pid = os.fork()

  if pid == 0:
    redirect = False
    outputFile = ''
    for arg in args:
      if arg == '>':
        redirect = True
      if redirect:
        outputFile = arg

    os.execvp(args[0], args)

  else:
    os.wait()
