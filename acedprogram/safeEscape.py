__author__ = 'rdasxy'

from universalImports import *

escapedCharacters = [34,39,40,41, 91, 92, 93, 123, 124, 125]

################################################################################################################################################################
#Escapes an input string with HTML escape characters.
def escapeString(word):
    for n in word:
        if ord(n) in escapedCharacters:
            word = word.replace(n,"&#"+str(ord(n)))
    return word
################################################################################################################################################################
#Removes all HTML escapes and returns a string.
def unescapeString(word):
    for n in escapedCharacters:
        if re.findall("&#"+str(n), word):
            word = word.replace("&#"+str(n), chr(int(n)))
    return word
################################################################################################################################################################




                    
