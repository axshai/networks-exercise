def main():
    num = input("Please enter a 5 digit number\n")
    print("You entered the number: {}".format(num))
    sum = 0
    print("The digits of this number are: ", end="")
    for i in num[:-1]:
        sum += int(i)
        print(i + ",", end="")
    print(num[-1])
    print("The sum of the digits is: {}".format(sum + int(num[-1])), end="")

if __name__ == "__main__":
    main()