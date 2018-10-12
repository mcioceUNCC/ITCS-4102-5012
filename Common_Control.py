#Roa Locklear
#Group Members: Addison Curtis, Norman Ananda, Michael Cicoe, Tripp Satterfield
#Program to Demonstrate control structures in Python



#Sequential, this is the default interpetration of code execution.

print("This is")
print("the default")
print("Order")
print("of execution.")



#Selection  Python supports the standard conditionals

def numberGame():

    question =int(input("Please enter a positive integer: "))
    type(question)
#Notice how else if is can be handle  with the key word "elif"
#Also Python relies on correct indentation to group commands together, there are no brackets
#in terms of control structures, functions, etc.

    if question <10:
        print("Why so small?")
    elif question>10:
        print("Okay that is better.")
    elif question<500:
        print("It's okay to think big")
    elif question<0:
        print("No, it was supposed to be positive...")
    else:
        print("Okay, things may have gotten out of control...")

#There are ways to handle repetition
    return;

numberGame()

play_more = input("Wanna do that again? (y/n) ")

while (play_more != 'Y' or play_more != 'y' or play_more !='Yes' or play_more != 'yes'):
    numberGame()


#There is also "Short Circuit Evaluation"



#Python does not have Switch, Switch-Case, or Case control structures
#Instead one can make use of either a custom Dictionary or "Compound Statements"