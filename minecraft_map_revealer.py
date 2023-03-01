import keyboard
import time
import os

chunck_size = 16
render_dist = 5
delay_between_tps = 1
number_of_teleportations = 100000
last_position_filename = "lastpos.dat"

#square spiral generator taken from https://stackoverflow.com/a/56574805/1346690
def create_spiral_coordinates_generator(num):

    def find_next(x, y):
        """find the coordinates of the next number"""

        def up(x, y):
            return x, y+1


        def down(x, y):
            return x, y-1


        def left(x, y):
            return x-1, y


        def right(x, y):
            return x+1, y

        if x == 0 and y == 0:
            return 1, 0

        if abs(x) == abs(y):
            if x > 0 and y > 0:
                x, y = left(x, y)
            elif x < 0 and y > 0:
                x, y = down(x, y)
            elif x < 0 and y < 0:
                x, y = right(x, y)
            elif x > 0 and y < 0:
                x, y = x+1, y
        else:
            if x > y and abs(x) > abs(y):
                x, y = up(x, y)
            elif x < y and abs(x) < abs(y):
                x, y = left(x, y)
            elif x < y and abs(x) > abs(y):
                x, y = down(x, y)
            elif x > y and abs(x) < abs(y):
                x, y = right(x, y)

        return x, y

    x = y = 0
    for _ in range(num-1):
        x, y = find_next(x, y)
        yield (x*chunck_size*render_dist, y*chunck_size*render_dist)

def send_command(str_command):
    keyboard.press_and_release('t')
    time.sleep(0.5)
    keyboard.write(str_command)
    print(str_command)
    time.sleep(0.2)
    keyboard.press_and_release('enter')
    time.sleep(0.5)

def write_last_position(filename, last_pos):
    with open(filename, 'w') as f:
        f.write(str(last_pos))

def get_last_position(filename):
    start_pos = 0
    if os.path.isfile(filename) and os.access(filename, os.R_OK):
        with open(filename, 'r') as f:
            start_pos = int(f.read())
    print("starting back from position : " + str(start_pos))
    return start_pos

last_position = get_last_position(last_position_filename)

print("be sure that you are in creative and flying ('/gamemode creative', then press the space bar 2 times)")
print("waiting 7 sec for you to switch ack to the game")

spiral_coordinates_generator = create_spiral_coordinates_generator(number_of_teleportations)
for current_position_number, coordinates in enumerate(spiral_coordinates_generator):
    if current_position_number < last_position:
        continue
    x, z = coordinates
    print("current position number : {}".format(current_position_number))
    write_last_position(last_position_filename, current_position_number)
    send_command("/teleport {} 180 {}".format(x, z))
    time.sleep(delay_between_tps)
