import json
import unicodedata
import re

def morse_file(morsefile):

    # retrieve the morse code - simple

    morsefile = "morse.json"

    jsonFile = open(morsefile, "r")
    jsonContent = jsonFile.read()
    jsonFile.close()

    return json.loads(jsonContent)
     


def morse_codes(morse, direction):

    codes = {}

    if direction=="encode":
        for character in morse:
            codes[ character["unicode"] ] = character["morse"]
    else:
        for character in morse:
            codes[character["morse"]] = character["latin"]

    return codes


def morse_extend( morse, cu ):

    morseunknown = {
        "latin": " ",
        "morse": "-.-.-.-",
        "unicode": cu
    }

    morse.append( morseunknown )
    
    outFile = open("morse_extended.json", 'w') 
    outFile.write( json.dumps(morse, indent=4, sort_keys=True ) )
    outFile.close()

    return morse 


def morse_encode(message):

    morse = morse_file("morse.json")

    codes = morse_codes(morse, "encode")

    coded = ""
    words = re.split(' ', message )

    for i, word in enumerate(words):

        for j, character in enumerate(word) :
            
            #print(unicodedata.name(character))

            # character unicode
            cu = unicodedata.name(character)
            cus = re.split(' ', unicodedata.name(character) )

            if cus[0]=="LATIN" and cus[2] + " " + cus[3] in list(codes.keys()):
                #print(cu[0], cu[3],  codes[cu[3]])
                coded += codes[ cus[2] + " " + cus[3] ]

            elif unicodedata.name(character) in list(codes.keys()):
                 coded += codes[ cu ]

            else:

                # 'GREEK CAPITAL LETTER OMEGA' - unicodedata.name("Ω")
                # 'EXCLAMATION MARK'

                morse = morse_extend( morse, cu )
                codes = morse_codes(morse, "encode")
                coded += codes[ cu ]

            if j+1 < len(word):
                coded += " "
            elif i+1 < len(words):
                coded += "/"


    return coded


def morse_decode(message):

    morse = morse_file("morse.json")

    codes = morse_codes(morse, "decode")

    coded = ""
    words = re.split('/', message )

    for i, word in enumerate(words):

        for l in re.split(' ', word ):
            if l in list(codes.keys()):
                coded += codes[l]
            else:
                print("NOT IN MORSE?!", l )

        if i+1 < len(words):
            coded += " "

    return coded


def messageencodedecode(messagename):

    f = open( f"{messagename}.txt", "r")
    message = f.read()

    #message = "HULP NODIG 50 MAN ZIT VAST OP HET EILAND RED ONS"
    #message = "SOS Aan wie ons horen kan. We weten niet wat er is gebeurt, maar we zitten zonder telefoonlijnen en internet. Daarom vallen we terug op morsecode. We zitten met 50 man vast op het eiland. Met de kerstdagen nabij willen we weer terug naar onze families en dus willen we opgehaald worden. Daarnaast moet Zoë haar hondje weer te eten geven en is de vrouw van Rubìn morgen uitgerekend. Stuur snel hulp!"
    #message = "Yoo 012345 6Ω789 bla!" # ,:;.'()" + '"'

    print(f"\nmessage { messagename} input")
    print("-"*50)
    print(message)


    # 2 print encoded message in terminal
    morseencoded = morse_encode(message)
    print(f"\nmessage {messagename} encoded" )
    print("-"*50)
    print(morseencoded + "<EOF>" )

    f = open( f"{messagename}.txt.mc", "w")
    f.write(morseencoded)

    # 3 print decoded message in terminal
    morsedecoded = morse_decode( morseencoded )
    print(f"\nmessage {messagename} decoded")
    print("-"*50)
    print(morsedecoded + "<EOF>")

    f = open( f"{messagename}.txt.dc", "w")
    f.write(morsedecoded)

    f.close()

    return True

#messageoktxt = lambda m : "OK" if (m) else "NOT OK" 

# messageok = messageencodedecode("noodoproep")
# print("\nmessage is", (lambda m : "OK" if (m) else "NOT OK") (messageok) )
# print("")


# messageok = messageencodedecode("noodoproep-extended")
# print("\nmessage is", (lambda m : "OK" if (m) else "NOT OK") (messageok) )
# print("zie morse-extended.json voor morsecode van buitengewone letters en leestekens!")
# print("")





