"""
Most efficient route between pair of G points, while getting the highest amount of S points en route

Use T Tiles to draw the path on the sys grid represented by a W x H map.
T tiles can be of different types. ( 11 )
Each tile has a usage cost, which is subtracted from the total points earned

primary goals:
find the path with the lowest cost

if u enter tile coordinates yield multiple routes with identical costs, only the route with the fewest scored points will be considered

if the path leads u to revisit the same tile a second time, both the cost of the tile and the s points will be doubled


final score is calculated by adding together the earned scores of all minimum paths and then subtracting the total costs of the tiles used
"""
import heapq


class Tile:
    def __init__(self, id, cost, num_available):
        self.id = id
        self.cost = cost
        self.num_available = num_available


class Point:
    def __init__(self, x, y, score=0):
        self.x = x
        self.y = y
        self.score = score


def parse_input(input_file):
    with open( input_file, 'r' ) as f:
        # Read the first line containing grid dimensions and other parameters
        W, H, GN, SM, TL = map( int, f.readline().split() )

        # Parse golden points
        golden_points = []
        for _ in range( GN ):
            x, y = map( int, f.readline().split() )
            golden_points.append( Point( x, y ) )

        # Parse silver points
        silver_points = []
        for _ in range( SM ):
            x, y, score = map( int, f.readline().split() )
            silver_points.append( Point( x, y, score ) )

        # Parse tile types
        tiles = {}
        for _ in range( TL ):
            tile_id, cost, num_available = f.readline().split()
            tiles[tile_id] = Tile( tile_id, int( cost ), int( num_available ) )

    return W, H, GN, SM, TL, golden_points, silver_points, tiles


W, H, GN, SM, TL, golden_points, silver_points, tiles = parse_input( "input.txt" )


def distance(g1, g2):
    distance_x = abs( g1.x - g2.x )
    distance_y = abs( g1.y - g2.y )
    return distance_x + distance_y


path = [golden_points[0]]


def my_way(start, path, visited=set(), gold_pass=1):
    visited.add( start )
    closest_distance = float( 'inf' )
    closest = None

    for p in golden_points + silver_points:
        if p not in visited:
            d = distance( start, p )
            if d < closest_distance:
                closest = p
                closest_distance = d

    if closest:
        if closest.score == 0:
            gold_pass += 1
        path.append( closest )
        if gold_pass != GN:
            my_way( closest, path, visited, gold_pass )

    return path


def move(start, end):
    tile_y = start.y
    tile_x = start.x

    while tile_x != end.x or tile_y != end.y:
        if tile_x > end.x:
            if tile_y > end.y:
                tile_x -= 1
                tile_y -= 1
                print( "using type 6" )
                tiles['6'].num_available -= 1;
            elif tile_y < end.y:
                tile_x -= 1
                tile_y += 1
                print( "using type 5" )
                tiles['5'].num_available -= 1;
            else:
                tile_x -= 1
                print( "using type 3" )
                tiles['3'].num_available -= 1;
            # print(tile_x, tile_y)

        elif tile_x < end.x:
            if tile_y > end.y:
                tile_x += 1
                tile_y -= 1
                print( "using type A" )
                tiles['A'].num_available -= 1;
            elif tile_y < end.y:
                tile_x += 1
                tile_y += 1
                print( "using type 6" )
                tiles['6'].num_available -= 1;
            else:
                tile_x += 1
                print( "using type 3" )
                tiles['3'].num_available -= 1;
            # print(tile_x, tile_y)

        else:
            if tile_y > end.y:
                tile_y -= 1
                print( "using type C" )
                tiles["C"].num_available -= 1;
            elif tile_y < end.y:
                tile_y += 1
                print( "using type C" )
                tiles["C"].num_available -=1;
                # print(tile_x, tile_y)


def move_all(lis):
    for i in range( len( lis ) ):
        print( "going to the closest Point" )
        print( lis[i].x, lis[i].y )
        move( lis[i], lis[i + 1] )
        print( lis[i + 1].x, lis[i + 1].y )


# print("findi path")

path = my_way( golden_points[0], path )
# print("look for number")
move_all( path )