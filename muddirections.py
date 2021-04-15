class MudDirections:# directions
    up = ('u', 'Up')
    down = ('d', 'Down')
    north = ('n', 'North')
    south = ('s', 'South')
    east = ('e', 'East')
    west = ('w', 'West')
    northwest = ('nw', 'Northwest')
    northeast = ('ne', 'Northeast')
    southeast = ('se', 'Southeast')
    southwest = ('sw', 'Southwest')
    directions = [up[0], up[1], down[0], down[1], north[0], north[1].lower(), south[0], south[1].lower(), east[0], east[1].lower(), west[0], west[1].lower(), northwest[0], northwest[1].lower(), northeast[0], northeast[1].lower(), southeast[0], southeast[1].lower(), southwest[0], southwest[1].lower()]
    pretty_directions = [up, down, north, south, east, west, northwest, northeast, southeast, southwest]