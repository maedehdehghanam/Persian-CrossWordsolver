from crossword import Crossword
import sys

class CrosswordCreator:
    def __init__(self, crossword):
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == variable.DOWN else 0)
                j = variable.j + (k if direction == variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                   print(sys.stdout.buffer.write((letters[i][j]).encode("UTF-8")) or " ", end="")
                   #   print(letters[i][j] or " ", end="")
                else:
                    print("#", end="")
            print()

    def save(self, assignment):
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        draw = ImageDraw.Draw(img)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j])
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                        )
        img.save("table.png")

    def solve(self):
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        for var in self.domains:
            for word in self.domains[var].copy():
                if var.length != len(word):
                    self.domains[var].remove(word)
        return

    def revise(self, x, y):
        # get the index of the overlap between word var x and word var y
        i, j = self.crossword.overlaps[x, y]
        is_revised = False
        # loop on all word options for var x and var y
        for word1 in self.domains[x].copy():
            found_match = False
            for word2 in self.domains[y]:
                # check if 2 words have same letter at the overlaping index
                if word1[i] == word2[j] and word1 != word2:
                    found_match = True
                    break
            # remove word1 from optional choices for var x
            if found_match is False:
                self.domains[x].remove(word1)
                is_revised = True
        return is_revised

    def ac3(self, arcs=None):
        if arcs is None:
            arcs = self.get_initial_arcs_list()

        for v1, v2 in arcs:
            is_v1_revised = self.revise(v1, v2)
            if is_v1_revised is True and len(self.domains[v1]) == 0:
                return False
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete return False otherwise.
        """
        if len(assignment) == len(self.crossword.variables):
            return True
        return False

    def consistent(self, assignment):
        """
        Return True if words fit in crossword puzzle
        without conflicting characters); return False otherwise.
        """
        # 1. check all assigned words are distinct
        if len(assignment) != len(set(assignment.values())):
            return False
        # 2. check every value is the correct length
        for var in assignment:
            if var.length != len(assignment[var]):
                return False
        # 3. check there are no conflicts between neighboring variables.
        for var in assignment:
            word1 = assignment[var]
            neighbors = self.crossword.neighbors(var)
            for var2 in neighbors:
                if var2 in assignment:
                    word2 = assignment[var2]
                    i, j = self.crossword.overlaps[var, var2]
                    # check if 2 words have same letter at the overlaping index
                    if word1[i] != word2[j] or word1 == word2:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        res_dict = {}
        for word1 in self.domains[var]:
            eliminates = 0
            for var2 in self.crossword.variables:
                if var2 != var:
                    index = self.crossword.overlaps[var, var2]
                    if var2 not in assignment and index != None:
                        for word2 in self.domains[var2]:
                            if word1[index[0]] != word2[index[1]]:
                                eliminates += 1
            res_dict[word1] = eliminates
        return sorted(res_dict, key=res_dict.get)

    def select_unassigned_variable(self, assignment):
        # optional_vars = self.domains.copy()
        best_options_set1 = set()
        # find variable(s) with the fewest number of remaining values in its domain
        lowest_remaining_options = len(self.crossword.words)
        for var in self.crossword.variables:
            if var not in assignment:
                if len(self.domains[var]) < lowest_remaining_options:
                    # found new lower option, reset result
                    best_options_set1 = {var}
                    lowest_remaining_options = len(self.domains[var])
                elif len(self.domains[var]) == lowest_remaining_options:
                    # found var with same num of options as the lowest already found
                    best_options_set1.add(var)

        # found one best option
        if len(best_options_set1) == 1:
            return best_options_set1.pop()

        most_neighbors = 0
        best_options_set2 = set()
        for var in best_options_set1:
            neighbors = len(self.crossword.neighbors(var))
            if neighbors > most_neighbors:
                best_options_set2 = {var}
                most_neighbors = neighbors
            elif neighbors == most_neighbors:
                best_options_set2.add(var)

        # return 1 option out of the best options found so far
        return best_options_set2.pop()

    def backtrack(self, assignment):
        # if found completed solution. return it
        if self.assignment_complete(assignment):
            return assignment

        # select a variable that wasnt assigned yet
        var = self.select_unassigned_variable(assignment)
        # get possible word options for the selected var
        domain = self.order_domain_values(var, assignment)
        outcome = None
        for word in domain:
            assignment[var] = word
            if self.consistent(assignment):
                outcome = self.backtrack(assignment)

            if outcome is not None:
                break  # outcome is finished assignment

        return outcome

    def get_initial_arcs_list(self):
        arcs = []
        for v1, v2 in self.crossword.overlaps:
            if self.crossword.overlaps[v1, v2] is not None:
                arcs.append((v1, v2))
        return arcs


words = [
    "الففا",
    "بیت",
    "کرعشته",
    "لوسس",
    "ستارت",
    "تروع",
]

'''
words = ["alpha", "arc", "bit", "create", "loss", "start", "true", "fine"]
words =words+['one',
'two',
'three',
'four',
'five',
'سین',
'seven',
'eight',
'nine',
'ten']

words =words+['adversarial',
'alpha',
'ار',
'artificial',
'bayes',
'beta',
'bit',
'breadth',
'byte',
'classification',
'classify',
'condition',
'constraint',
'create',
'depth',
'distribution',
'end',
'false',
'graph',
'heuristic'
'infer',
'inference',
'initial',
'intelligence',
'knowledge',
'language',
'learning',
'line',
'logic',
'loss',
'markov',
'minimax',
'network',
'neural',
'node',
'optimization',
'probability',
'proposition',
'prune',
'reason',
'recurrent',
'regression',
'resolution',
'resolve',
'satisfaction',
'search',
'سان',
'start',
'true',
'truth',
'uncertainty'
]'''

def structure(file_name):
    with open(file_name, encoding="UTF-8") as f:
        line1, line2 = next(f), next(f)
    line1 = line1.split(" ")
    row = ""
    rows = []
    for j in range(1, len(line2)):
        row = row + line2[j - 1]
        if (j) % int(line1[1]) == 0:
            rows.append(row)
            row = ""
    f = open("myfile.txt", "w")
    for elem in rows:
        f.write(elem + "\n")
    f = open("myfile.txt", "r")


structure("crossword_404_recons.txt")
crossword = Crossword("myfile.txt", words)
creator = CrosswordCreator(crossword)
assignment = creator.solve()
if assignment is None:
        print("No solution.")
else:
        creator.print(assignment)
# creator.save(assignment)
