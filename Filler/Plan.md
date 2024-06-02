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

when two cells are unioned if they are not the same color a reference is established between them
    create links

when two cells are merged all references to one set will be changed to reference the other set - One set is "Consumed, all references
    remove all references to the other group
    make sure all referenced group have links with main group

when a set changes colors it updates all references so that it is referenced under the correct color
    remove all references in old color
    add references to main set in new color

    it then merges with all groups of the same color


no group can ever reference itself