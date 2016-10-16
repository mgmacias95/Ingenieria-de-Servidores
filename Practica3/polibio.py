tabla_polibio = [['a','b','c','d','e'],['f','g','h','i','k'],['l','m','n','o','p'],
['q','r','s','t','u'],['v','w','x','y','z']]

def cifra_polibio (frase):
    cifrado = []
    for caracter in frase:
        for lista in tabla_polibio:
            for letra in lista:
                if letra == caracter:
                    cifrado.append((tabla_polibio.index(lista)+1)*10+(lista.index(letra)+1))

    return cifrado

def descrifrado_polibio (cifrado):
    frase = ""

    for numero in cifrado:
        frase += tabla_polibio[int(numero/10)-1][int(numero%10)-1]

    return frase

if __name__ == '__main__':
    frase_original = input("Introduce una frase: ")
    frase = frase_original.replace("j", "i");

    cifrado = cifra_polibio(frase)

    print("Texto cifrado: "+' '.join(str(n) for n in cifrado))

    descrifrado = descrifrado_polibio(cifrado)

    print("Texto descrifrado: "+descrifrado)
