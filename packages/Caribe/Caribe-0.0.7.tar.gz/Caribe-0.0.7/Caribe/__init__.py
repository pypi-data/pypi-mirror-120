from gingerit.gingerit import GingerIt
import re



caribedict = {
  "Know how long meen see you" : "I have not seen you in a long time",
  "Oo monsta" : "What's up",
  "Eyyy, look who" : "long time no see friend" ,
  "My g":"my friend",
  "Wais d word dawg":"what's up bro",
  "wam dawg": "how are you?",
  "everyting cool" : "how is everything",
  "wais d order": "What's up",  
  "ah wah": "I want",
  "waz de scene": "How are you",
  "waiz d scn": "How are you",
  "waiz de scene": "How are you",
  "waiz d scene": "How are you",
  "come nah boi": "I am being serious",
  "Father lawd": "Jesus help me", 
  "Skinnin yuh teet":"grinning",
  "Skinnin yuh teeth":"grinning",
  "Tabanca": "still holding feelings",
  "allyuh":"Everybody",
  "chupid": "stupid",
  "dotish": "stupid",
  "chupidee": "stupid",
  "fone":"phone",
  "tick":"thick",
  "crapo": "Frog",
  "trinbago": "Trinidad and Tobago",
  "dias":"that is",
  "lix" : "beating",
  "ent": "Is that not so?",
  "fed up": "tired",
  "preshah": "pressure",
  "ahse": "ass",
  "wajang":"roudy",
  "tief":"thief",
  "hush": "quiet",
  "oi": "Hello",
   "d" : "the",
  "whey":"where",
  "whey yuh say": "can you repeat?",
  "you an all":  "You too?",
  "you so": "people like you",
  "yuh makin joke":  "you can't be serious",
  "yuh look fuh dat": "it is your fault",
  "boldface": "ignorant",
  "bolface": "ignorant",
  "bacchanal":"confusion", 
  "liming": "hanging out",
  "hambug":"pester",
  "ting":"thing",
  "tanty":"aunty",
  "tantie":"aunty",
  "gyul": "girl",
  "gyal": "girl",
  "horn":"cheat",
  "wifey":"wife",
  "Yo": "Hi",
  "Yoo": "Hi",
  "Yooo": "Hi",
  "dis":"this",
  "wah": "want",
  "meh": "me",
   "waiz" : "what",
   "moda":"mother",
   "modda" : "mother",
  "fadda" : "father",
  "fada" : "father",
  "faddah": "father",
  "brodda": "brother",
  "broda": "brother",
  "dougla": "mixed race person",
  "backchat":"talks",
  "boi" : "boy",
  "yuh": "you",
  "tho":"though",
  "tru":"true",
  "dey" : "there",
  "Ah" : "I",
  "doh": "do not",
  "eh" : "not",
  "cah": "cannot",
  "fuh":"for",
  "dat": "that",
  "waz": "what is",
  "dah": "that",
  "nah": "no",
  "de": "the",
  "scene":"weather",
  "rel": "very",
  #"me":"my",
  "mi": "my",
  "ah": "I",
  "yh":"yes",
  "dias":"that is",
  "waiz":"what",
  "mi": "my",
  "ah": "I",
  "Eyyy":"Hey",
  "Eyy":"Hey",
  "Ey": "Hey",
  "Yo":"Hi",
  "Yoo": "Hi",
  "Oooo": "Hi",
  "cud":"could",
  "wais":"what is",
  "g":"friend",
  "dat": "that",
  "dawg":"friend"
 
}
splitdict = {
  "dawg": "friend",
  "topdawg": "friend",
  "d":"the",
  "y":"why",
  "Tabanca": "still holding feelings",
  "allyuh":"Everybody",
  "chupid": "stupid",
  "dotish": "stupid",
  "chupidee": "stupid",
  "fone":"phone",
  "tick":"thick",
  "crapo": "Frog",
  "trinbago": "Trinidad and Tobago",
  "dias":"that is",
  "lix" : "beating",
  "ent": "Is that not so?",
  "fed up": "tired",
  "preshah": "pressure",
  "ahse": "ass",
  "wajang":"roudy",
  "tief":"thief",
  "oi": "Hello",
   "d" : "the",
  "hush": "quiet",
  "whey":"where",
  "boldface": "ignorant",
  "bolface": "ignorant",
  "bacchanal":"confusion", 
  "liming": "hanging out",
  "hambug":"pester",
  "ting":"thing",
  "tanty":"aunty",
  "tantie":"aunty",
  "gyul": "girl",
  "gyal": "girl",
  "horn":"cheat",
  "Yo": "Hi",
  "Yoo": "Hi",
  "Yooo": "Hi",
  "dis":"this",
  "wah": "want",
  "meh": "me",
   "waiz" : "what",
   "modda" : "mother",
  "fadda" : "father",
  "fada" : "father",
  "faddah": "father",
  "brodda": "brother",
  "broda": "brother",
  "dougla": "mixed race person",
  "backchat":"talks",
  "boi" : "boy",
  "yuh": "you",
  "tho":"though",
  "tru":"true",
  "dey" : "there",
  "Ah" : "I",
  "doh": "do not",
  "eh" : "not",
  "cah": "cannot",
  "fuh":"for",
  "dat": "that",
  "waz": "what is",
  "dah": "that",
  "nah": "no",
  "de": "the",
  "scene":"weather",
  "rel": "very",
  "waz":"what is",
  "waiz":"what",
  "mi": "my",
  "ah": "I",
  "Eyyy":"Hey",
  "Eyy":"Hey",
  "Ey": "Hey",
  "Yo":"Hi",
  "Yoo": "Hi",
  "g":"friend",
  "Oooo": "Hi",
  "cud":"could",
  "wais":"what is",
  "dat": "that"
}


phrasedict = {
  "whey yuh say": "can you repeat?",
  "you an all":  "You too?",
  "you so": "people like you",
  "yuh makin joke":  "you can't be serious",
  "yuh look fuh dat": "it is your fault",
  "ah wah": "I want",
  "waz de scene": "How are you",
  "come nah boi": "I am being serious",
  "Father lawd": "Jesus help me", 
  "Skinnin yuh teet":"grinning",
  "Skinnin yuh teeth":"grinning",
  "Tabanca": "still holding feelings",
  "Wah foolishness is this" : "that was foolish",
  "Know how long meen see you" : "I have not seen you in a long time",
  "Oo monsta" : "What's up",
  "Eyyy, look who" : "long time no see friend" ,
  "My g":"my friend",
  "Wais d word dawg":"what's up bro",
  "wam dawg": "how are you?",
  "everyting cool" : "how is everything",
  "wais d order": "What's up"

}

def trinidad_decode(sentence):
    sentence=sentence.lower()
    sentence = " " + sentence 

    for x in caribedict:
        if sentence.find(x):
            #sentence=sentence.replace(x, caribedict[x])
            sentence = re.sub(r'\b%s\b' %x, caribedict[x], sentence)
    return sentence.strip()


def phrase_decode(sentence):
    sentence=sentence.lower()
    sentence = " " + sentence
    for x in phrasedict:
        if sentence.find(x):
            sentence=sentence.replace(x, phrasedict[x])
    return sentence.strip()


def trinidad_decode_split(sentence):
    sentence= sentence.lower()

    for subs in sentence.split():
        if subs in splitdict: 	
            sentence = sentence.replace(subs, str(splitdict[subs.lower()]))
    return sentence

def caribe_corrector(sentence):
    parser = GingerIt()
    sentence = parser.parse(sentence)
    sentence = sentence['result']
    return str (sentence)


