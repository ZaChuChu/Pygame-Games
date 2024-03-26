Simple Checkers Game with pygame

Object relationships:
    Board has Cells
        A cell can have piece

Classes:
    main:
        board
        selected cells
        pygame stuff
        

    Board:
        Grid of Cells
        The num rows and cols
        The x,y origins for the board
        The alloted height and width for the board
        Draw each cell of the board

    Cells:
        The piece they contain
        Their color
        dimensions
        row and col
        x and y offset
        Draw self and then piece if any

    Pieces:
        Know:
            If they're queens
            Their color
            row and col ?? 
            direction of movement
            valid squares to move to

        Do:
            Get valid squares:
                If Queen all diagnol plus jumps
                Else Directional diagnols or jumps

            Move:
                Move piece to new cell
                If a jump happened 
                    kill other piece
                    Check for other jumps
                if the piece is now a queen
                Return true if another jump can happen
            

The game will start with alternating players. Active player will be indicated in a small window to indicate color. The number of remaining pieces for each team

When click on cell if it has a piece highlight viable spots, if cell clicked on is already clicked toggle click off.

Move piece: Target Cell
    Set target cell piece
    return path of all indicies of path [start, end)

Clicking in main passes click coordinates to responsible feature, ie click in board gives coords to board object.

Board takes click cell and handles the logic for itself.


