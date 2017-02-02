import math

assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
row_col_units = row_units + column_units
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

"""
Fix for diagonal sudoku check, this is just addition of 2 more units in list of units.
This is to make sure they also get considered for: elimination, only_choice and naked_twins
This will make the solution meet the diagonal uniqueness criterion for digits.
"""
d1 = [r+c for r in rows for c in cols if rows.index(r)==cols.index(c)] # First diagonal, top-left to bottom right
d2 = [r+c for r in rows for c in cols if rows.index(r)== ( (len(cols)-1) - cols.index(c))] # Second diagonal,
diags = [d1,d2]
unitlist = row_units + column_units + square_units + diags
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist: # Scan each unit
        listOfUnitValues = [values[b] for b in unit]
        setOfUnitValues = set(listOfUnitValues)

        twins = set([])  # Using set as there might be possible more than 1 pair of twins, e.g 23 twice and 49 twice

        # Find all twins in this unit
        if len(setOfUnitValues) != len(listOfUnitValues):  # If there are duplicates set will have less elements
            for v in [uv for uv in setOfUnitValues if len(uv)==2 and listOfUnitValues.count(uv) == 2]:
                twins.add(v)  # Add each value of length 2 and is seen twice in unit.

        #Scan the unit and get rid of each twin's characters in unit's non-twin locations.
        for box in unit:
            for twin in twins: # For every twin value.
                if twin != values[box] and twin[0] in values[box]: # If this is not twin location itself and this box has first char in twin
                    assign_value(values, box, values[box].replace(twin[0], ''))  #replace first digit
                if twin != values[box] and twin[1] in values[box]:
                    assign_value(values, box, values[box].replace(twin[1], '')) # Same for second digit

    return values

def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """

    # Dictionary to be populated
    gridDictionary = {}

    for k in boxes: # For each key in boxes list
        if(grid[boxes.index(k)]=='.'):  # Because index of any box'key, eg. A5 in boxes list is same as index of digit in grid-string, I use that as check for encoding.
            gridDictionary[k]= '123456789'  #Assign 123456789 to . values if this box has '.' in grid string
        else:
            gridDictionary[k] = grid[boxes.index(k)] # Else for this box, assign the value from grid-string

    #Finally, return the fully populated grid
    return gridDictionary

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    # Provided in utils, just copied from there.
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    # naked_twins() as part of one more elimination stratagy, which might give more single digit solved boxes, which will increase eliminate()'s effectiveness.
    values = naked_twins(values)

    # This is capture all the already confirmed locations with single digit
    keysForSingleDigitValues = []
    for r in rows:
        for c in cols:
            if len(values[r + c]) == 1:
                keysForSingleDigitValues.append(r + c)

    for r in rows: # A, B, C ..... I
        for c in cols: # 1, 2, 3, ..... 9
            if (r + c) in keysForSingleDigitValues: # Run the loop for each solved box'key, which is already solved
                # do elimination
                # traverse through all the peers
                # Update each peer after eliminating the dict[r+c]

                # This is the logic, which is used to find respective box identifiers
                peerRowKeys = cross(r, cols.replace(c, ''))
                peerColKeys = cross(rows.replace(r, ''), c)

                # Logic to find peer square for any r row and c column box
                # Here we get the index of this square in square_units list.
                peerSquareIndex = math.floor((rows.index(r)) / 3) * 3 + math.floor((cols.index(c)) / 3)

                allPeerKeys = peerRowKeys + peerColKeys + square_units[peerSquareIndex]

                for k in allPeerKeys: # Loop for each peer of (r+c) box
                    if ((values[r + c] in values[k]) and len(values[k]) > 1): # if peer box has solved digit, replace it
                        values[k] = values[k].replace(values[r + c], '')
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    new_values = values.copy()  # Create a working copy

    digits = '123456789'
    for unit in unitlist: # Loop for each unit including row, column, square and diagonal
        unitStr = ''
        for b in unit: # Create string of all the values in unit
            unitStr += values[b]

        only_choices = [] # List is used to store only choice digits

        for d in digits: # Loop for each digit
            if unitStr.count(d) == 1: # If in unit's string has just 1 occurrence of this digit
                only_choices.append(d) # save this in only choice list

        for b in unit: # loop for each box in unit
            for oc in only_choices: # For each only choice digit in this unit
                if oc in new_values[b]: # if this box has only choice digit
                    #new_values[b] = oc # replace whole box' value with only choice for that box
                    assign_value(new_values, b, oc)

    return new_values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values) # Eliminate all already solved single values, apply naked_twins() at start of eliminate()
        values = only_choice(values) # Check for only possible choices in unit
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after # check if number of solved values do not increase with eliminate() and only_choice()
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False # this is the case, where reduction leads to invalid scenarios like empty values ''
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    # Check if this reduction has resulted in "invalid" sudoku state/comdination in unit
    if values == False:
        return False

    # Check if Solved, then return values, else proceed deeper in call tree
    if all(len(values[s]) == 1 for s in boxes):
        return values

    # Choose one of the unsolved box with the fewest possibilities
    v, optimumBoxKey = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # So, now values[optimumBoxKey] has value with digits,
    # which we can try out in our search, one char at a time.

    # Now use recursion to solve each one of the resulting sudokus, and if one returns
    # a value (not False), return that answer!
    for d in values[optimumBoxKey]:  # Iterate over all the choices for this box.
        new_values = values.copy() # Create a working copy
        assign_value(new_values, optimumBoxKey, d) # try out possible digit as box of this value
        new_reduced = search(new_values)  # With this new digit in place, try searching again, which tries reduction and check again
        if new_reduced: # If this digit placement, does yield a viable solution, No False is returned
            return new_reduced # Return the dictionary as solution

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid) # Convert Grid string to dictionary representation of sudoku problem, replace each '.' with 123456789

    try:
        values = search(values) # try to solve the puzzle, this will return solved puzzle or False, So, this can be returned as it is.
    except:
        return False # If call is broken, return False as indication of not solved.

    return values


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
