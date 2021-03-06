# Wordle Solver
import re


def solve():
    correctLetters = []
    displacedLetters = []
    nullLetters = []
    totalLetters = 0
    
    dictionary = set()
    file = open("words_alpha.txt", "r")
    for word in file:
        dictionary.add(word.strip().lower())
    
    solving = True
    while(solving):
        guessed = ""
        response = ""
        
        gettingInput = True
        while(gettingInput):
            print("Enter your guessed word. 'ctrl-c' to exit")
            guessed=input(":").strip()
            
            # Error handling
            if len(correctLetters) != 0 and len(guessed) != len(correctLetters):
                print("\nYour guessed word is a different length than previous guesses. Try again.\n")
                continue
            elif guessed not in dictionary:
                print("\nYour guessed word wasn't found in our dictionary. There might have been a typo. Try again.\n")
                continue
            
            print("Enter Wordle's response: 'g' for green; 'o' for orange; '.' for blank. eg o.oo..og")
            response=input(":").strip()
            
            # Error handling
            if len(guessed) != len(response):
                print("\nYour guessed word and the response are different lengths. Try again.\n")
                continue
            
            guessed = list(guessed)
            response = list(response)
            totalLetters = len(guessed)
            gettingInput = False
        
        if len(correctLetters) == 0:      
            correctLetters = ( list("." * totalLetters) )
        for i in range(0, len(response)):
            if response[i] == 'g':
                correctLetters[i] = guessed[i]
            elif correctLetters[i] != '.':
                continue
            else:
                correctLetters[i] = '.'
        
        for i in range(0, len(response)):
            if response[i] == 'o' and ( guessed[i] + str(i) ) not in displacedLetters:
                displacedLetters.append( guessed[i] + str(i) )
            elif response[i] == '.' and guessed[i] not in nullLetters:
                notADuplicate = True
                for j in range(0, len(displacedLetters)):
                    if displacedLetters[j][0] == guessed[i]:
                        notADuplicate = False
                if notADuplicate:
                    nullLetters.append(guessed[i])
                
        regex = "^"
        for i in range(0, totalLetters):
            if correctLetters[i] != ".":
                regex += correctLetters[i]        
            elif nullLetters:
                regex += "[^"
                for letter in nullLetters:
                    regex += letter
                if displacedLetters:
                    for letter in displacedLetters:
                        if int(letter[1:]) == i:
                            regex += letter[0]
                regex += "]"
                            
            else:
                regex += "."
        regex += "$"
        # print("Regex", regex)
            
        words = []
        for word in dictionary:
            if re.search(regex, word): # Has correct letters in correct spaces, contains no null letters
                if displacedLetters:
                    correct = 0
                    for i in range(0, len(displacedLetters)):
                        if displacedLetters[i][0] in word: # Contains displaced letters
                            correct += 1
                        else:
                            break
                    if correct == len(displacedLetters) and word not in words:
                        words.append(word)
                else:
                    words.append(word)
        
        words = sorted(words, key=len)
        for word in words:
            print(word)
        print("Words Found:", len(words))
    
solve()