"""goldhunt_inefficient

This module contains code for the 'Gold Hunt' scenario as described
in the chapter on performance improvement using Python. The code here
represents the inefficient code! the book will show you how to optimize
this code further.

This module is compatible with Python 3.5.x. It contains
supporting code for the book, Learning Python Application Development,
Packt Publishing.


:copyright: 2016, Ninad Sathaye

:license: The MIT License (MIT) . See LICENSE file for further details.
"""
from __future__ import print_function
import sys
import time
import random
import math

if sys.version_info < (3, 0):
    print("This code requires Python 3.x, It is tested only with 3.5")
    print("Looks like you are trying to run this using "
          "Python version: %d.%d " % (sys.version_info[0], sys.version_info[1]))
    print("Exiting...")
    sys.exit(1)

try:
    import matplotlib.pyplot as plt
except ImportError:
    msg = "You won't be able to visualize the random point distribution."
    print("ImportError: matplotlib.pyplot ",msg)


def plot_points(ref_radius, x_coords, y_coords):
    """Utility function to show the 'Gold Field!"""
    # Define axis limits
    a1 = ref_radius + 1
    a2 = a1*(-1.0)
    plt.plot(x_coords, y_coords, ".", color='#A67C00', ms=4)
    plt.axis([a2, a1, a2, a1])
    plt.show()


# Enable the @profile decorator only when you are running line_profiler
# or memory_profiler. Otherwise it will throw an error.
#@profile
def generate_random_points(ref_radius, total_points):
    """Return x, y coordinate lists representing random points inside a circle.

    Generates random points inside a circle with center at (0,0). For any point
    it randomly picks a radius between 0 and ref_radius.

    :param ref_radius: The random point lies between 0 and this radius.
    :param total_points: total number of random points to be created
    :return: x and y coordinates as lists

    .. note:: This function shows an inefficient way of generating random
            points. In the next few chapters, the book will show a better
            way of writing this code.
    .. todo:: Refactor! Move the function to a module like gameutilities.py
    """
    x = []
    y = []
    show_plot = False

    for i in range(total_points):
        theta = random.uniform(0.0, 2*math.pi)
        r = ref_radius*math.sqrt(random.uniform(0.0, 1.0))
        x.append(r*math.cos(theta))
        y.append(r*math.sin(theta))

    if show_plot:
        plot_points(ref_radius, x, y)

    return x, y


class GoldHunt:
    """Class to play a game scenario 'Great Gold Hunt' in 'Attack of The Orcs'.

    This class is created to illustrate a scenario discussed in the book:
    'Learning Python Application Development (Packt Publishing).

    This class illustrates various bottlenecks that impact
    the performance of the application. The bottlenecks will be visible if
    appropriately change the input arguments to __init__. For example,
    setting field_coins to a large number and/or making the search radius very
    small. A word of caution: if you do such changes, it will likely
    consume a lot of memory and you may notice performance lag on your computer.
    So do it at your own risk!

    :ivar int field_coins: Gold coins scattered over a circular field
    :ivar float field_radius: Radius of the circular field with gold coins
    :ivar float search radius: Radius of a circle. The gold search will be
            constrained within this circle.
    :ivar float x_ref: X-coordinate of the game unit searching for gold.
    :ivar float y_ref: Y-coordinate of the game unit searching for gold.
    :ivar float move_distance: Distance by which the game unit advances for the
           next search.
    """
    def __init__(self, field_coins=5000, field_radius=10.0, search_radius=1.0):
        self.field_coins = field_coins
        self.field_radius = field_radius
        self.search_radius = search_radius

        # Sir Foo's initial coordinates e.g. (-9.0, 0)
        self.x_ref = - (self.field_radius - self.search_radius)
        self.y_ref = 0.0
        # Distance by which Sir Foo (or any unit) advances for the
        # next search
        self.move_distance = 2*self.search_radius

    def reset_params(self):
        """Resets some dependent params to their default computed value."""
        self.x_ref = - (self.field_radius - self.search_radius)
        self.move_distance = 2*self.search_radius

    # Enable the @profile decorator only when you are running line_profiler
    # or memory_profiler. Otherwise it will throw an error.
    #@profile
    def find_coins(self, x_list, y_list):
        """Return list of coins that lie within a given distance.

        :param x_list: List of x coordinates of all the coins (points)
        :param y_list: List of y coordinates of all the coins (points)
        :return: A list containing (x,y) coordinates of all the eligible coins
        """
        collected_coins = []

        for x, y in zip(x_list, y_list):
            delta_x = self.x_ref - x
            delta_y = self.y_ref - y
            dist = math.sqrt(delta_x*delta_x + delta_y*delta_y)

            if dist <= self.search_radius:
                collected_coins.append((x, y))

        return collected_coins

    def play(self):
        total_collected_coins = []
        x_list, y_list = generate_random_points(self.field_radius,
                                                self.field_coins)
        count = 0
        while self.x_ref <= 9.0:
            count += 1
            # Find all the coins that lie within the circle of radius 1 unit
            coins = self.find_coins(x_list, y_list)
            print("Circle# {num}, center:({x}, {y}), coins: {gold}".format(
                num=count, x=self.x_ref, y=self.y_ref, gold=len(coins)))

            # Update the main list that keeps record of all collected coins.
            total_collected_coins.extend(coins)

            # Move to the next position along positive X axis
            self.x_ref += self.move_distance

        print("Total_collected_coins =", len(total_collected_coins))

if __name__ == '__main__':
    start = time.perf_counter()
    game = GoldHunt()

    # Optionally you can specify the problem size using input args
    # to GoldHunt.The line of code that does this is shown below (disabled)
    # IMPORTANT: The choice of input suggested below can consume a lot of
    # computational resources on your machine. See what your computer can
    # handle first by choosing a smaller size for field_coins and a LARGER
    # search_radius!

    ##game = GoldHunt(field_coins=2000000, search_radius=0.1)

    game.play()
    end = time.perf_counter()
    print("Total time delta (time interval):", end - start)
