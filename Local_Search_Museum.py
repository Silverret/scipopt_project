import math
import random
from itertools import combinations

import matplotlib.pyplot as plot


class Museum:
    def __init__(self):
        with open("./museum_problem/input_9.txt", "r") as file:
            self.small_radius, self.big_radius = tuple(map(int, file.readline().split(",")))
            self.small_price, self.big_price = tuple(map(int, file.readline().split(",")))
            self.locations = [tuple(map(int, row.split(","))) for row in file.read().split("\n")]
            self.width = max(x[0] for x in self.locations)
            self.height = max(x[1] for x in self.locations)

    def first_cam_positions_split(self):
        """We divide the problem in 8x8 squares of size 100.
        We compute cameras' positions in each square,
        and we collect them"""
        square_size = 100
        nb_row = self.height // square_size + 1
        nb_col = self.width // square_size + 1

        cam_positions = list()
        for j in range(nb_row):
            for i in range(nb_col):
                sub_loc = list(filter(lambda x: (i * square_size <= x[0] < (i + 1) * square_size) and (
                    j * square_size <= x[1] < (j + 1) * square_size), self.locations))
                sub_problem = SubMuseum(sub_loc)
                cam_positions += sub_problem.new_cam_positions()
        return cam_positions

    def new_cam_positions(self):
        """From a given collections of arts objects location,
        we compute a sub-optimal list of cameras' positions."""
        new_positions = list()
        big_radius_remaining = True
        small_radius_remaining = True
        no_more_big_radius = False
        no_more_small_radius = False
        while not self.all_covered(new_positions):
            if not no_more_big_radius:
                big_radius_remaining = False
                combi = list(combinations(self.art_not_covered(new_positions), 2))
                len_combi = len(combi)
                for (loc1_i, loc1_j), (loc2_i, loc2_j) in random.sample(combi, len_combi):
                    if (loc1_i, loc1_j) == (loc2_i, loc2_j):
                        continue
                    sd = (loc1_i - loc2_i) ** 2 + (loc1_j - loc2_j) ** 2  # square distance between loc1 and loc2
                    if sd < self.big_radius ** 2:
                        xa, ya, xb, yb = self.get_circle_centers(loc1_i, loc1_j, loc2_i, loc2_j, self.big_radius)
                        selected_loc = self.art_not_covered(new_positions)
                        nb_covered_by_a = self.nb_arts_covered_with_a_cam(xa, ya, self.big_radius,
                                                                          selected_locations=selected_loc)
                        nb_covered_by_b = self.nb_arts_covered_with_a_cam(xb, yb, self.big_radius,
                                                                          selected_locations=selected_loc)
                        if nb_covered_by_a >= nb_covered_by_b:
                            new_positions.append((2, xa, ya))
                        else:
                            new_positions.append((2, xb, yb))
                        big_radius_remaining = True
                        break

            if not big_radius_remaining:
                no_more_big_radius = True

            if no_more_big_radius and not no_more_small_radius:
                small_radius_remaining = False
                combi = list(combinations(self.art_not_covered(new_positions), 2))
                len_combi = len(combi)
                for (loc1_i, loc1_j), (loc2_i, loc2_j) in random.sample(combi, len_combi):
                    sd = (loc1_i - loc2_i) ** 2 + (loc1_j - loc2_j) ** 2  # square distance between loc1 and loc2
                    if (loc1_i, loc1_j) == (loc2_i, loc2_j):
                        continue
                    if sd < self.small_radius ** 2:
                        xa, ya, xb, yb = self.get_circle_centers(loc1_i, loc1_j, loc2_i, loc2_j, self.small_radius)
                        selected_loc = self.art_not_covered(new_positions)
                        nb_covered_by_a = self.nb_arts_covered_with_a_cam(xa, ya, self.small_radius,
                                                                          selected_locations=selected_loc)
                        nb_covered_by_b = self.nb_arts_covered_with_a_cam(xb, yb, self.small_radius,
                                                                          selected_locations=selected_loc)
                        if nb_covered_by_a >= nb_covered_by_b:
                            new_positions.append((1, xa, ya))
                        else:
                            new_positions.append((1, xb, yb))
                        small_radius_remaining = True
                        break

            if not small_radius_remaining:
                no_more_small_radius = True

            if no_more_small_radius and no_more_big_radius:
                for i, j in self.art_not_covered(new_positions):
                    new_positions.append((1, i, j))

        return new_positions

    def nb_arts_covered_with_a_cam(self, x_circle, y_circle, radius, selected_locations=None):

        """
        Given a circle center coordonnate, and its radius, we retreive the number of cameras in its range

        :param x_circle: float
        :param y_circle: float
        :param radius: int
        :param selected_locations: list of couples (i,j) of cameras
        :return: int
        """
        res = 0
        sq_radius = radius ** 2
        if selected_locations is None:
            selected_locations = self.locations
        for i, j in selected_locations:
            if (x_circle - i) ** 2 + (y_circle - j) ** 2 < sq_radius:
                res += 1
        return res

    def nb_arts_covered(self, cam_positions):
        """
        Retrieve the number of art objects (located in locations) covered by cameras (located in positions)
        """
        nb_covered = 0
        for i, j in self.locations:
            for cam_type, x, y in cam_positions:
                if (x - i) ** 2 + (y - j) ** 2 <= (self.small_radius ** 2 if cam_type == 1 else self.big_radius ** 2):
                    nb_covered += 1
                    break
        return nb_covered

    @staticmethod
    def get_circle_centers(x1, y1, x2, y2, r):
        """
        Determine (xa, ya) and (xb, yb) :
        the centers of the two circles of radius l,
        passing by the points (x1, y1) and (x2, y2)

        Notation:
            - r: circle radius
            - sd: square distance between (x1, y1) and (x2, y2)
            - l: distance between (xa, ya) (resp. (xb, yb)) and the middle of (x1, y1) and (x2, y2)
        """
        r = r - 0.0125
        sd = (x2 - x1) ** 2 + (y2 - y1) ** 2
        l = math.sqrt(r ** 2 - sd / 4)
        d = math.sqrt(sd)
        xa = x1 + (1 / 2) * (x2 - x1) + (l / d) * (y1 - y2)
        ya = y1 + (1 / 2) * (y2 - y1) + (l / d) * (x2 - x1)

        xb = x1 + (1 / 2) * (x2 - x1) - (l / d) * (y1 - y2)
        yb = y1 + (1 / 2) * (y2 - y1) - (l / d) * (x2 - x1)

        """
        try:
            assert math.isclose((xa-x1)**2 + (ya-y1)**2, r**2, rel_tol=1e-03)
            assert math.isclose((xa-x2)**2 + (ya-y2)**2, r**2, rel_tol=1e-03)
            assert math.isclose((xb-x1)**2 + (yb-y1)**2, r**2, rel_tol=1e-03)
            assert math.isclose((xb-x2)**2 + (yb-y2)**2, r**2, rel_tol=1e-03)
        except:
            import pdb; pdb.set_trace()
        """

        return xa, ya, xb, yb

    def all_covered(self, selected_positions):
        sq_small_radius = self.small_radius ** 2
        sq_big_radius = self.big_radius ** 2
        for x_art, y_art in self.locations:
            if any((x_art - x_cam) ** 2 + (y_art - y_cam) ** 2 <= (sq_small_radius if cam_type == 1 else sq_big_radius)
                   for
                   cam_type, x_cam, y_cam in selected_positions):
                continue
            else:
                return False
        return True

    def selection_cost(self, selected_positions):
        """Retrieve the cost of a given collections of cameras' positions"""
        res = 0
        for cam_type, x_cam, y_cam in selected_positions:
            res += self.small_price if cam_type == 1 else self.big_price
        return res

    def art_not_covered(self, selected_positions):
        """Return the list of uncovered art objects"""
        sq_small_radius = self.small_radius ** 2
        sq_big_radius = self.big_radius ** 2
        res = []
        for x_art, y_art in self.locations:
            if any((x_art - x_cam) ** 2 + (y_art - y_cam) ** 2 <= (sq_small_radius if cam_type == 1 else sq_big_radius)
                   for
                   cam_type, x_cam, y_cam in selected_positions):
                continue
            else:
                res.append((x_art, y_art))
        return res

    def plot_solution(self, cam_positions):
        """Print/Plot the result"""

        loc_circles = []
        for loc in self.locations:
            loc_circles.append(plot.Circle(loc, 0.3, color='r'))

        cam_circles = []
        for cam_type, x, y in cam_positions:

            if cam_type == 1:
                cam_circles.append(plot.Circle((x, y), 0.1, color='b'))
                cam_circles.append(plot.Circle((x, y), self.small_radius, color='b', fill=False))
            if cam_type == 2:
                cam_circles.append(plot.Circle((x, y), 0.1, color='g'))
                cam_circles.append(plot.Circle((x, y), self.big_radius, color='g', fill=False))

        fig, ax = plot.subplots()
        ax.set_xlim(0, max(self.width, self.height))
        ax.set_ylim(0, max(self.width, self.height))
        for loc_circle in loc_circles:
            ax.add_artist(loc_circle)

        for cam_circle in cam_circles:
            ax.add_artist(cam_circle)

        plot.grid(True)
        fig.savefig('./museum_problem/plot_sol_1.png')
        print("Optimal value: %f" % self.selection_cost(cam_positions))
        plot.show()

    ###########################################################################################
    ################################ To be refactored #########################################
    ###########################################################################################




    def cover_uncovered_art(self, selected_positions):
        new_selected_positions = set(selected_positions)
        locations_to_cover = self.art_not_covered(selected_positions)
        new_positions = self.cam_positions(locations_to_cover)  # TODO pas optimal
        for pos in new_positions:
            new_selected_positions.add(pos)
        return new_selected_positions

    def improve(self, selected_positions):
        """ Deux améliorations possibles, couvrirent les objets d'arts non couverts
        et mutualiser les caméras des objets d'arts couverts plusieurs fois"""

        new_selected_positions = set(selected_positions)

        # Ensure that all object arts are covered
        if not self.all_covered(new_selected_positions):
            new_selected_positions = self.cover_uncovered_art(new_selected_positions)

        # Improvements

        # Remove small cam in big cam radius
        for small_type, x_small, y_small in filter(lambda x: x[0] == 1, new_selected_positions):
            for big_type, x_big, y_big in filter(lambda x: x[0] == 2, new_selected_positions):
                if math.sqrt((x_small - x_big) ** 2 + (y_small - y_big) ** 2) + self.small_radius <= self.big_radius:
                    new_selected_positions.remove((small_type, x_small, y_small))

        # Prefer a small radius to a big one if less than 4 art objects are covered
        for big_type, x_big, y_big in new_selected_positions:
            if big_type == 2:
                nb_art_covered = 0
                for x_art, y_art in self.locations:
                    if (x_art - x_big) ** 2 + (y_art - y_big) ** 2 <= self.big_radius ** 2:
                        nb_art_covered += 1
                if nb_art_covered < 4:
                    new_selected_positions.remove((big_type, x_big, y_big))
                    if not self.all_covered(new_selected_positions):
                        new_selected_positions = self.cover_uncovered_art(new_selected_positions)

        return new_selected_positions

    def localmin(self, selected_positions):
        new_selected_positions = self.improve(selected_positions)
        while selected_positions != new_selected_positions:
            if self.selection_cost(selected_positions) > self.selection_cost(new_selected_positions):
                selected_positions = new_selected_positions
            new_selected_positions = self.improve(selected_positions)
            print('new_selected_positions')
        return selected_positions

    def solve(self):
        result_pool = []
        i = 0
        while i <= 5:
            random_positions = {pos for pos in POSITIONS if random.randint(0, 1)}
            selected_positions = self.localmin(random_positions)
            result_pool.append((selected_positions, self.selection_cost(selected_positions)))
            i += 1
        best_solution = min(result_pool, key=lambda x: x[1])
        self.plot_solution(best_solution[0])


class SubMuseum(Museum):
    def __init__(self, subloc):
        super().__init__()
        self.locations = subloc


if __name__ == '__main__':
    problem = Museum()
    positions = problem.first_cam_positions_split()
    problem.plot_solution(positions)
