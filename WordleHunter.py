def start():
    global choice
    global wordList
    global valueDictionary
    global letters
    global lettersFrequency

    # Użytkownik wybiera język, a następnie program otwiera odpowiednie pliki
    while True:
        lang = input("Wybierz język:\nPolski - pl\nAngielski - en\nNiemiecki - de\n").lower()
        match lang:
            case "pl":
                f1 = open("wordle_dictionary_pl.txt", encoding="windows-1250")
                f2 = open("letters_pl.txt", encoding="windows-1250")
                print("Wybrano język polski")
                break
            case "en":
                f1 = open("wordle_dictionary_en.txt", encoding="utf-8")
                f2 = open("letters_en.txt", encoding="utf-8")
                print("Wybrano język angielski")
                break
            case "de":
                f1 = open("wordle_dictionary_de.txt", encoding="utf-8")
                f2 = open("letters_de.txt", encoding="utf-8")
                print("Wybrano język niemiecki")
                break
            case _:
                print("Podaj prawidłowy język")

                # Operacje na pliku ze słownikiem słów
    dictionary = f1.read()
    f1.close()
    dictionary = dictionary.split()

    # Operacje na pliku z częstotliwością liter
    letters = f2.read()
    f2.close()
    letters = letters.split()

    # Tworzy słownik częstotliwości liter
    lettersFrequency = {}
    for i in range(0, len(letters), 2):
        lettersFrequency[letters[i]] = float(letters[i + 1])

    # Pyta o liczbę liter, dopóki użytkownik nie poda prawidłowej liczby
    choice = ""
    while isInt(choice) == False:
        choice = input("Podaj liczbę liter w wyrazach: ")
        if isInt(choice) == False:
            print("Podaj wartość liczbową")

    wordList = []
    valueDictionary = {}

    # Tworzy słownik słów o pożądanej liczbie liter
    for word in dictionary:
        if len(word) == int(choice):
            wordList.append(word.lower())


# Funkcja licząca moc słowa
def wordValue(word):
    value = 0.0
    for i in range(0, len(letters), 2):
        if letters[i] in word and letters[i] not in usedLetters:
            value += lettersFrequency[letters[i]]
    return round(value, 2)


# Funkcja generująca wyrazy o możliwie wysokiej mocy
def generate():
    global usedLetters
    usedLetters = ""
    user_usedLetters = input("Podaj ciągiem już użyte litery: ")
    usedLetters += user_usedLetters

    # Tworzy słownik mocy wszystkich słów, o wybranej wcześniej długości
    for word in wordList:
        valueDictionary[word] = wordValue(word)

    word_value_pairs = [(word, value) for word, value in valueDictionary.items()]
    top_100 = sorted(word_value_pairs, key=lambda x: x[1], reverse=True)[:100]

    # Pyta użytkownika, czy wpisał słowo (ponieważ może zrezygnować lub Wordle mogą nie zawierać danego słowa w słowniku)
    accepted = False
    for i, (word, value) in enumerate(top_100):
        print(f"{i + 1}. {word}: {value}")
        while True:
            accept = input("Czy wpisałeś słowo i je zaakceptowano (tak/nie)?\n")
            if accept == "tak":
                usedLetters += word
                accepted = True
                break
            elif accept == "nie":
                break
        if accepted:
            break


# Funkcja pytająca o poszczególne litery i podająca rozwiązania
def answer():
    for i in range(0, int(choice)):
        while True:
            greenLetter = input("Zielona litera na " + str(i + 1) + ". miejscu to: ").lower()
            globals()['greenLetter{}'.format(i + 1)] = greenLetter
            if len(greenLetter) >= 2:
                print("Podaj maksymalnie jedną literę")
            else:
                break

    # Zmienne greenLettersCombined i yellowLettersCombined zapobiegają sytuacji,
    # w której dana litera wyświetla się we wpisanym wyrazie raz na zielono/zółto, a raz na szaro,
    # przez co prawidłowa odpowiedź jest wykluczana ze względu na występowanie w niej szarej litery

    greenLettersCombined = ""
    for i in range(0, int(choice)):
        greenLettersCombined = greenLettersCombined + globals()['greenLetter{}'.format(i + 1)]

    print("Jeśli na jednym miejscu występuje wiele liter, podaj je ciągiem")
    for i in range(0, int(choice)):
        globals()['yellowLetters{}'.format(i + 1)] = input("Żółte litery na " + str(i + 1) + ". miejscu to: ").lower()

    yellowLettersCombined = ""
    for i in range(0, int(choice)):
        yellowLettersCombined = yellowLettersCombined + globals()['yellowLetters{}'.format(i + 1)]

    greyLetters = input("Szare litery to (podaj ciągiem): ").lower()

    possibleWordsDictionary = {}

    # Początkowo wszystkie słowa uznawane są za pasujące
    for word in wordList:
        possibleWordsDictionary[word] = True

        # Jeśli litera szara występuje w słowie, to słowo jest wykluczane
        for letter in greyLetters:
            if letter in word and letter not in greenLettersCombined and letter not in yellowLettersCombined:
                possibleWordsDictionary[word] = False

        # Jeśli żółta litera nie występuje w słowie, to słowo jest wykluczane
        for i in range(0, int(choice)):
            for letter in globals()['yellowLetters{}'.format(i + 1)]:
                if letter not in word:
                    possibleWordsDictionary[word] = False

        # Jeśli miejsce zielonej litery, nie zgadza się z literą na danym miejscu słowo, to słowo jest wykluczane
        for i in range(0, int(choice)):
            if globals()['greenLetter{}'.format(i + 1)] != word[i] and globals()['greenLetter{}'.format(i + 1)] != "":
                possibleWordsDictionary[word] = False

        # Jeśli żółta litera, występuje na miejscu, w którym nie powinno jej być, to słowo jest wykluczane
        for i in range(0, int(choice)):
            for letter in globals()['yellowLetters{}'.format(i + 1)]:
                if word[i] == letter:
                    possibleWordsDictionary[word] = False

    # Na podstawie słownika pasujących słów (z wartościami True/False), tworzy listę
    possibleWordsList = []
    for key, value in possibleWordsDictionary.items():
        if value:
            possibleWordsList.append(key)

    # wyświetla możliwe odpowiedzi
    numberOfAnswers = 0
    if not possibleWordsList:
        print("Nie znaleziono pasujących rozwiązań\nUpewnij się, że wszystkie litery zostały podane prawidłowo")
    else:
        print("Pasujące rozwiązania to:")
        for word in possibleWordsList:
            numberOfAnswers += 1
            print(str(numberOfAnswers) + ". " + word)


# Funkcja, która sprawdza, czy podana przez użytkownika liczba liter jest rzeczywiście liczbą
def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


start()
while True:
    ask = input(
        "Aby wygenerować słowo o możliwie wysokiej wartości - gen\nAby znaleźć odpowiedź - odp\nAby zakończyć - kon\n").lower()
    if ask == "gen":
        generate()
    elif ask == "odp":
        answer()
    elif ask == "kon":
        break
    else:
        print("Podaj prawidłowe zapytanie")
