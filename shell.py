#!/usr/bin/env python3

import os
import string

while True:
  line = input('> ')
  args = str.split(line, ' ')
  pid = os.fork()

  if pid == 0:
    os.execvp(args[0], args)

  else:
    os.wait()
