import string

words = []

with open("words.txt", "r") as file:
    for line in file.readlines():
        words.append(line.strip())

frequencies = {}

# Get frequency of letters
for word in words:
    for letter in word:
        if letter not in frequencies:
            frequencies[letter] = 1
        else:
            frequencies[letter] = frequencies[letter] + 1

word_scores = {}

for word in words:
    score = 0
    letters = []
    for letter in word:
        if letter in letters:
            continue
        score += frequencies[letter]
        letters.append(letter)
    word_scores[word] = score

knowns = [None, None, None, None, None]
inclusions = []
bads = []
bad_inclusions = [[], [], [], [], []]

print("Enter each word to Wordle and then input the resulting colours")
print("If the word does not exist, enter an empty line")
print("b is for black, y is for yellow and g is for green\n")

while True:
    # Filter based on inclusions
    for inclusion in inclusions:
        deletions = []
        for word in word_scores:
            if inclusion not in word:
                deletions.append(word)
        for deletion in deletions:
            del word_scores[deletion]

    # Filter based on knowns
    for j in range(5):
        if knowns[j] is not None:
            deletions = []
            for word in word_scores:
                if word[j] != knowns[j]:
                    deletions.append(word)
            for deletion in deletions:
                del word_scores[deletion]

    # Filter based on bads
    for bad in bads:
        deletions = []
        for word in word_scores:
            if bad in word:
                deletions.append(word)   
        for deletion in deletions:
            del word_scores[deletion]

    # Filter based on bad inclusions
    for j in range(5):
        for bad in bad_inclusions[j]:
            deletions = []
            for word in word_scores:
                if word[j] == bad:
                    deletions.append(word)
            for deletion in deletions:
                del word_scores[deletion]

    # Print the word with the highest score
    best_word = ""
    best_score = 0

    for word in word_scores:
        if word_scores[word] > best_score:
            best_score = word_scores[word]
            best_word = word
    
    print(best_word)

    check = False 
    first = True

    while first or check:
        check = False

        if not first:
            print("Invalid colours and/or length. Use b (black), y (yellow) and g (green)")

        response = input("Enter the colours: ")

        if len(response) == 0:
            del word_scores[best_word]
            break

        if len(response) != 5:
            check = True

        for index, colour in enumerate(response):
            if colour == "b":
                bads.append(best_word[index])
            elif colour == "y":
                inclusions.append(best_word[index])
                bad_inclusions[index].append(best_word[index])
            elif colour == "g":
                knowns[index] = best_word[index]
            else: 
                check = True

        first = False

    if "b" not in response and "y" not in response and len(response) > 0:
        break
    