LEN = 5


def doinput():
    """
    this function receives the input from the user
    :return: the user input
    """
    num = input("Please enter a 5 digit number\n")
    while not validinput(num):
        num = input("Please enter a 5 digit number\n")
    return num


def validinput(user_input):
    """
    this function checks validation of the input
    :param user_input:the user input
    :return: true if the input is valid and otherwise false
    """
    if len(user_input) != LEN:
        return False
    for i in user_input:
        if not i.isdigit():
            return False
    return True


def printdigits(num):
    """
    This func prints the digits of a number
    :param num: the number to print his digits
    :return: string of the digits
    """
    res = ""
    for i in num[:-1]:
        res += i + ","
    res += num[-1]
    return res


def printsum(num):
    """
    This func prints the sum of a digits of a number
    :param num: the number to print his digits sum
    :return: the sum
    """
    sum = 0
    for i in num:
        sum += int(i)
    return sum


def main():
    """
    main func
    """
    runasserts()
    num = doinput()
    print("You entered the number: {}".format(num))
    print("The digits of this number are: ", end="")
    print(printdigits(num))
    print("The sum of the digits is: {}".format(printsum(num), end=""))


def runasserts():
    assert validinput("123456") is False
    assert validinput("12f23") is False
    assert printdigits("12345") == "1,2,3,4,5"
    assert printsum("12345") == 15


if __name__ == "__main__":
    main()
