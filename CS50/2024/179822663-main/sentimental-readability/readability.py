from cs50 import get_string

text = get_string("Text: ")

letters = 0

for characters in text:
    if characters.isalpha():
        letters += 1

words = len(text.split())

sentences = text.count(".") + text.count("?") + text.count("!")

L = letters / words * 100
S = sentences / words * 100

grade = 0.0588 * L - 0.296 * S - 15.8

if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Before Grade 16+")
else:
    print(f"Grade {round(grade)}")
