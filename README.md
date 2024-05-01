# Floutteur de scripts

## Qu'est ce que c'est

Remplace les noms de fonctions/variables pour rendre le code difficile à lire  
Quasiment impossible de faire la maintenance  

## A quoi ça sert ?

A rien...  
(bien pour s'exercer avec les expressions régulières)  

## TODO
 - mettre les appels de fonctions et assignations de variables sur une ligne si possible  
    
    ```
    variableA = 1  
    variableB = 2  
    function()  
         ||
         \/
    variableA = 1; variableB = 2; function()
    ```
 - mettre des alias aux modules importés  
   
    ```
    import math
    from random import randint
    math.sqrt(randint(5, 20))
        ||
        \/
    import math as X
    from random import randint as Y
    X.sqrt(Y(5, 20))
    ```
