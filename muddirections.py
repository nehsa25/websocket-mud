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
    directions = [
        up[0].lower(), 
        up[1].lower(), 
        down[0].lower(), 
        down[1].lower(), 
        north[0].lower(), 
        north[1].lower(), 
        south[0].lower(), 
        south[1].lower(), 
        east[0].lower(), 
        east[1].lower(), 
        west[0].lower(), 
        west[1].lower(), 
        northwest[0].lower(), 
        northwest[1].lower(), 
        northeast[0].lower(), 
        northeast[1].lower(), 
        southeast[0].lower(), 
        southeast[1].lower(), 
        southwest[0].lower(), 
        southwest[1].lower()
    ]
    pretty_directions = [up, down, north, south, east, west, northwest, northeast, southeast, southwest]

    opp_directions = [
        (up, down), 
        (east, west),
        (north, south),
        (northeast, southwest),
        (northwest, southeast)
    ]