# Alchemy

Given a target element, this will produce a sequence of recipes (either crafting/decrafting) to produce it.

e.g. for this recipe tree
```
     AB
    /  \
   CD  EF
  / \   \
 GH IJ  KL
```

Passing in 'AB' will produce:
```
GH + IJ = CD
KL -> EF
CD + EF = AB
```