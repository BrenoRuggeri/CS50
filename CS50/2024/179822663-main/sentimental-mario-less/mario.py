from cs50 import get_int

while True:
    N = get_int("Height: ")
    if (N > 0 and N < 9):
        break

for i in range(N):
    print(" " * (N-i-1), end="")
    print("#" * (i+1))
