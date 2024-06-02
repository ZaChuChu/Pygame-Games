## ColorGroup
### Properties
1. color - represents the color of all cells in the set
2. cells - all sets that belong to the color group
3. adjacent_groups - dictionary{ Color - Set{ ColorGroup } } * each color groups set for it's own color will be empty

### Methods
1. size() - number of cells
2. addReference(other) - Add references between two color groups
2. changeReferences(oldRef, newRef) - Remove oldRef, add newRef
2. merge(other)
    ```
    combine cells
    iterate over all adjacent groups in other
        for each set
            change all references from other to self
            add set to self reference
    ```
3. union(other)
    ```
    if groups are same color
        merge
        return other
    else
        add references between groups
        return self
    ```
4. claimColor()
    ```
    change color of all cells
    change references to all adjacent groups so that reference is accurate
    merge with all adjacent groups of the same color
    clear set of color
    ```