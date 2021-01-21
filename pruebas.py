def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

texto = "Hola"

print (texto[:0])
print (texto[0:2])

exec ("pp = 8")
chau = "\\" + "hola"
chau = chau.replace("o","\\")
print (chau)