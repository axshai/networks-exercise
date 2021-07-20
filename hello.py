
import os
import msvcrt
import sys


def main():
    ss=""
    x=""
    s=0
    print("ggf")
    while x!="\r":
        if msvcrt.kbhit():
            print("true")
            x=msvcrt.getch()
            print(x)

    print(ss)


main()
