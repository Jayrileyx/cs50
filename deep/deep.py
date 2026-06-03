answer = input("What is the answer to the Great Question of Life, the Universe and Everything? ")

string_answer = str(answer)
string_answer = answer.lower().replace("-", " ").strip()
string_answer = " ".join(string_answer.split())
if string_answer == "42":
    print("Yes")
elif string_answer == "forty-two":
    print("Yes")
elif string_answer == "forty two":
    print("Yes")
else:
    print("No")
