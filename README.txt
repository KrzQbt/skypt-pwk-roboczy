Skrypt znajdujący niektóre błędy na rysunkach. Skrypt jest dopiero testowany, więc proszę zgłaszać błędne działanie

WYMAGANIA:
    żeby uruchomić skrypt należy umieścić takie pliki w folderze z którego pracuje skrypt (odpowienio dozwolone produkcje generyczne, postaci, przedmioty i miejsca, najlepiej w aktualnej wersji):

    produkcje_generyczne.json
    allowedCharacters.json
    allowedItems.json
    allowedLocations.json


URUCHOMIENIE (należy podstawić nazwę swojego pliku z rysunkiem w miejsce example.drawio.xml):

        python3 validator.py example.drawio.xml

    dla wygody polecam uruchomić od razu z wypisaniem do pliku, żeby nie czytać z terminala:

        python3 validator.py example.drawio.xml > test.txt


    A żeby włączyć na przykładzie z folderu można użyć:

        python3 validator.py q00_DragonStory_diagram\ projektowy.drawio.xml > test.txt


    uwaga - rysunek musi być pobrany jako nieskompresowany xml


JAK ROZUMIEĆ WYNIKI:

    Wyniki różnych walidacji są zapisywane w formacie:
        WARNING/ERROR
            Element przy którym znaleziono problem
            opis problemu
    
    WARNING - ostrzeżenie, które należy samodzielnie sprawdzić, najczęściej w elementach, które ciężko zweryfikować skryptem. Jeśli ostrzeżenie jest niesłuszne to można je spokojnie zignorować

    ERROR - błąd, który należy skorygować

    Jeśli jakieś sprawdzenie zostało pominięte, to zazwyczaj z powodu złego typu wierchołka grafu (np. zły kształt - rhombus)

TYPOWE BŁĘDY

    1. Produkcja / miejsce / przedmiot wyglądają poprawnie, ale są wskazywane jako nieobecne na liście.
        Powód: zły apostrof, niedokładne przepisanie nazwy produkcji lub argumentów ( najlepiej je skopiować z listy, a nie wpisywać ręcznie),
        
        np. Wizard's_hut zamiast Wizards_hut w argumencie
    
    2. Niepotrzebny średnik na końcu produkcji szczegółowej ( zielonej )

    3. Kolor spoza głównej palety

    4. Typ produkcji nie został rozpoznany
        Powody mogą być różne:
            niedozwolony znak dla typu produkcji, zły format, nadmiar białych znaków

    5. Zły kształt produkcji (np. rhombus) lub opisy na krawędziach

    6. Krawędzie nie są dołączone do wierzchołków - nie  można czasem przez to dojść do końca



