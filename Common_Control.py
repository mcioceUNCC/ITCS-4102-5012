#Roa Locklear/Norman Ananda
#Group Members: Addison Curtis, Michael Cicoe, Tripp Satterfield
#Program to demonstrate control structures in Python
#This code runs on Python 3!



#Sequential, this is the default interpetration of code execution.

print("This is")
print("the default")
print("order")
print("of execution.\n")



#Selection  Python supports the standard conditionals

def numberGame():
    
    play_more = 'y'

#while loop conditional demonstration    
    while(play_more == 'y'):

        question=(input("Please enter a positive integer: "))
        question=int(question)

#Notice how else if is can be handle with the key word "elif"
#Also Python relies on correct indentation to group commands together, there are no brackets
#in terms of control structures, functions, etc.
        if question<10:
            print("Why so small?")
        elif question>10 and question<500:
            print("Okay that is better.")
        elif question<500:
            print("It's okay to think big")
        elif question<0:
            print("No, it was supposed to be positive...")
        else:
            print("Okay, things may have gotten out of control...")
    
        play_more = input("Wanna guess again? (enter y/n): ")
        
        

#Demonstrate for loops
#iterating through letters in a string
def forLoopsDemo(word):
    n=1
    for i in word:
        print("Letter "+str(n)+": "+i)
        n+=1
        


#Start of program
print("Let's play a little game")
numberGame()

print("Let's see how for loops work to iterate through strings...")
w=input("Enter a word to iterate over: ")
forLoopsDemo(w)



#There is also "Short Circuit Evaluation"



#Python does not have Switch, Switch-Case, or Case control structures
#Instead one can make use of either a custom Dictionary or "Compound Statements"
