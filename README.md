# Floutteur de scripts

## Qu'est ce que c'est

Remplace les noms de fonctions/variables pour rendre le code difficile à lire  
Quasiment impossible de faire la maintenance  

## A quoi ça sert ?

A rien...  
(bien pour s'exercer avec les expressions régulières)  

## TODO
 - mettre des alias aux modules importés  
    `import math`&nbsp;&nbsp;&nbsp;&nbsp;=>&nbsp;&nbsp;&nbsp;&nbsp;`import math as X`  
    `from os import chdir`&nbsp;&nbsp;&nbsp;=>&nbsp;&nbsp;&nbsp;`from os import chdir as Y`  

 - Compréhension de liste sur plusieurs lignes  
 - Changer noms de classes

### Mise à jour
 - 3 Mai 2024 :
   * Ajout de la fonction `join_similar_line`, les lignes d'indentation identique sont concaténés avec les points-virgule ';'.
   * Suspension de la fonction `replace_global_var`, elle peut générer des erreurs ! Si on remplace toutes les variables globales puis qu'on en réassigne plus loin de manière dynamique dans le code on ne peux plus revenir en arrière.
