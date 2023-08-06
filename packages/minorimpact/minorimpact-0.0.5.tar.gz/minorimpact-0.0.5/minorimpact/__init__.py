#!/usr/bin/env python3

import hashlib
import os.path
import psutil
import random
import sys

# Reads a process id from *pidfile* and checks for it  in the current list of running processes.
#   Returns True if it finds it, False otherwise.
def checkforduplicates(pidfile = None):
    if (pidfile is None):
        return False

    oldpid = None
    if (os.path.exists(pidfile)):
        with open(pidfile, "r") as p:
            oldpid = p.read().rstrip()

    if (oldpid is not None):
        for proc in psutil.process_iter():
            try:
                if int(oldpid) == proc.pid:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    pid = os.getpid()

    with open(pidfile, "w") as p:
        p.write(str(pid))
    return False

# Prints to stderr.
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Identical to print(), but it flushes the cache everytime.  Useful to capture stdout from a long
#   running cron.
def fprint(*args, **kwargs):
    print(*args, flush=True, **kwargs)

# Gets a single character from stdin.
# Optional parameters:
#   *default*: what to return if the user simply presses 'return'.
#   *echo*: display the pressed character.
#   *end*: what to follow the character with, if *echo* is True.
#   *prompt*: A string to print before pausing for input.
def getChar(default = None, end = '\n', prompt = None, echo = False):
    # figure out which function to use once, and store it in _func
    if "_func" not in getChar.__dict__:
        try:
            # for Windows-based systems
            import msvcrt # If successful, we are on Windows
            getChar._func=msvcrt.getch

        except ImportError:
            # for POSIX-based systems (with termios & tty support)
            import tty, sys, termios # raises ImportError if unsupported

            def _ttyRead():
                fd = sys.stdin.fileno()
                oldSettings = termios.tcgetattr(fd)

                try:
                    tty.setcbreak(fd)
                    answer = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)

                return answer

            getChar._func=_ttyRead

    if (prompt is not None):
        print(prompt, end = '', flush = True)
    c = getChar._func()
    if (default is not None and c == '\n'): c = default
    if (echo):
        if (c == '\n'): print("", end = end, flush = True)
        else: print(c, end = end, flush = True)
    return c

# If *filename* is a directory, recursively traverse it and combine the md5 sums of every file
#   into a single sum.  Used to verify that a directory's contents have not changed.
def md5dir(filename):
    m = hashlib.md5()
    if (os.path.isdir(filename)):
        for f in sorted(os.listdir(filename)):
            md5 = md5dir(filename + "/" + f)
            m.update(md5.encode('utf-8'))
    else:
        with open(filename, 'rb') as f:
            data = f.read(1048576)
            while(data):
                md5 = hashlib.md5(data).hexdigest()
                m.update(md5.encode('utf-8'))
                data = f.read(1048576)
    return m.hexdigest()

# Returns a random odd value in the range of *min* to *max*-1, inclusive.  I have no idea why.
def randintodd(min, max):
    int = random.randint(min,max)
    if (int % 2) == 0:
        if (int < max): int = int + 1
        else: int = int - 1
    return int

# Split a string into a list of strings no more than <maxlength> long.
def splitstringlen(string, maxlength, expandtabs=True):
    newstrings = []
    if (expandtabs):
        string = string.replace("\t", "    ")

    for i in range(0, len(string), maxlength):
        newstrings.append(string[i:i+maxlength])
    return newstrings

# Recursively traverse a directory and collect the total size of every file it contains.  Used to indicate
#   whether the contents of a directory have changed without incurring the high cost of md5dir().
def dirsize(filename):
    size = 0
    if (os.path.isdir(filename)):
        for f in os.listdir(filename):
            size += dirsize(filename + "/" + f)
    else:
        size = os.path.getsize(filename)
    return size


