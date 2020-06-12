from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

visited_rooms = dict()
path = [] # chronological list of where player has recently moved (used for backtracking)
reverse = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'} # reference for opposite direction

visited_rooms[player.current_room.id] = player.current_room.get_exits()

# we want the number of visited rooms to be the same as the number of rooms
while len(visited_rooms) < len(room_graph):
    # if the room hasn't been visited
    if player.current_room.id not in visited_rooms:
        # add this room to visited rooms
        visited_rooms[player.current_room.id] = player.current_room.get_exits()
        # set current move to where player went according to backtracker
        current_move = path[-1]
        # remove current move from the visited room so that we don't revisit it
        visited_rooms[player.current_room.id].remove(current_move)
    # if there are no exits (or all exits have been explored)
    if len(visited_rooms[player.current_room.id]) == 0:
        # set current move to where player went according to backtracker
        current_move = path[-1]
        # remove the last move from path
        path.pop()
        # add the current move to the final traversal path
        traversal_path.append(current_move)
        # player travels backwards to get out of room with no more unexplored exits
        player.travel(current_move)
    else:
        # pick an unexplored exit
        next_room = visited_rooms[player.current_room.id][-1]
        # remove the exit because it is now going to be explored
        visited_rooms[player.current_room.id].pop()
        # move player to the next room
        player.travel(next_room)
        # add the movement to the backtracker path
        path.append(reverse[next_room])
        # add the movement to the final path
        traversal_path.append(next_room)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######ls

player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
