"""
Using MILP to solve the YES Puzzle: Given three piecesthat look like a Y, an E, and an S, find a way to create a "symmetric" figure.
Idea: We use Gurobi to find feasible solutions (if any) of an appropriate integer linear program. Three pieces Y, E, S are placed in a grid satisfying certain conditions 
"""
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import itertools
Y0 = np.array([[1, 0, 1], [1, 1, 1], [0, 1, 0], [0, 1, 0], [0, 1, 0]], dtype= int)
Y1 = np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0], [1, 1, 1], [1, 0, 1]], dtype= int)
Y2 = np.array([[1, 1, 0, 0, 0], [0, 1, 1, 1, 1], [1, 1, 0, 0, 0]], dtype= int)
Y3 = np.array([[0, 0, 0, 1, 1], [1, 1, 1, 1, 0], [0, 0, 0, 1, 1]], dtype= int)
# Y0, Y1, Y2, Y3 are possible ways to place the piece "Y". Similarly for E0, ..., E3, S0, ..., S3. 
# E.g., Y0 = [[1, 0, 1],
#             [1, 1, 1],
            # [0, 1, 0],
            # [0, 1, 0],
            # [0, 1, 0]]
charY0 = [(a, b) for a in range(Y0.shape[0]) for b in range(Y0.shape[1]) if Y0[a, b] == 1]
charY1 = [(a, b) for a in range(Y1.shape[0]) for b in range(Y1.shape[1]) if Y1[a, b] == 1]
charY2 = [(a, b) for a in range(Y2.shape[0]) for b in range(Y2.shape[1]) if Y2[a, b] == 1]
charY3 = [(a, b) for a in range(Y3.shape[0]) for b in range(Y3.shape[1]) if Y3[a, b] == 1]
# charY0 is a list of coordinates of unit squares in the piece Y0. We shall use these coordinate later to actually "place" the pieces in a lattice.
E0 = np.array([[1, 1], [1, 0], [1, 1], [1, 0], [1, 1]], dtype= int)
E1 = np.array([[1, 1], [0, 1], [1, 1], [0, 1], [1, 1]], dtype= int)
E2 = np.transpose(E1)
E3 = np.transpose(E0)
charE0 = [(a, b) for a in range(E0.shape[0]) for b in range(E0.shape[1]) if E0[a, b] == 1]
charE1 = [(a, b) for a in range(E1.shape[0]) for b in range(E1.shape[1]) if E1[a, b] == 1]
charE2 = [(a, b) for a in range(E2.shape[0]) for b in range(E2.shape[1]) if E2[a, b] == 1]
charE3 = [(a, b) for a in range(E3.shape[0]) for b in range(E3.shape[1]) if E3[a, b] == 1]
S0 = np.array([[1, 1], [1, 0], [1, 1], [0, 1], [1, 1]], dtype= int)
S1 = np.array([[1, 1], [0, 1], [1, 1], [1, 0], [1, 1]], dtype= int)
S2 = np.transpose(S1)
S3 = np.transpose(S0)
# There are four ways to place the piece "S".
charS0 = [(a, b) for a in range(S0.shape[0]) for b in range(S0.shape[1]) if S0[a, b] == 1]
charS1 = [(a, b) for a in range(S1.shape[0]) for b in range(S1.shape[1]) if S1[a, b] == 1]
charS2 = [(a, b) for a in range(S2.shape[0]) for b in range(S2.shape[1]) if S2[a, b] == 1]
charS3 = [(a, b) for a in range(S3.shape[0]) for b in range(S3.shape[1]) if S3[a, b] == 1]

# gurobi model.
model = gp.Model("YESPuzzle")
model.Params.MIPFocus = 1
# MIPFocus = 1: focus more on finding feasible solutions.

varY0 = model.addMVar(shape = (15, 15), vtype = GRB.BINARY)
varY1 = model.addMVar(shape = (15, 15), vtype = GRB.BINARY)
varY2 = model.addMVar(shape = (15, 15), vtype = GRB.BINARY)
varY3 = model.addMVar(shape = (15, 15), vtype = GRB.BINARY)
# varY0 corresponds to the piece "Y" placed in the lattice with the position similar to Y0. Similarly for other variables.
varE0 = model.addMVar(shape = (15, 15), vtype = GRB.BINARY)
varE1 = model.addMVar(shape = (15, 15), vtype = GRB.BINARY)
varE2 = model.addMVar(shape = (15, 15), vtype = GRB.BINARY)
varE3 = model.addMVar(shape = (15, 15), vtype = GRB.BINARY)

varS0 = model.addMVar(shape = (15, 15), vtype = GRB.BINARY)
varS1 = model.addMVar(shape = (15, 15), vtype = GRB.BINARY)
varS2 = model.addMVar(shape = (15, 15), vtype = GRB.BINARY)
varS3 = model.addMVar(shape = (15, 15), vtype = GRB.BINARY)

positions = tuple(itertools.product(range(15), repeat = 2))
# We use a table of size 15 x 15. positions = all unit squares of the table.
forbidden_set_Y0 = [c for c in positions if any([(c[0] + x[0], c[1] + x[1]) not in positions for x in charY0])]
# forbidden_set_Y0 = all unit squares that the piece Y0 cannot be placed in. Similarly for other variables. 
forbidden_set_Y1 = [c for c in positions if any([(c[0] + x[0], c[1] + x[1]) not in positions for x in charY1])]
forbidden_set_Y2 = [c for c in positions if any([(c[0] + x[0], c[1] + x[1]) not in positions for x in charY2])]
forbidden_set_Y3 = [c for c in positions if any([(c[0] + x[0], c[1] + x[1]) not in positions for x in charY3])]

forbidden_set_E0 = [c for c in positions if any([(c[0] + x[0], c[1] + x[1]) not in positions for x in charE0])]
forbidden_set_E1 = [c for c in positions if any([(c[0] + x[0], c[1] + x[1]) not in positions for x in charE1])]
forbidden_set_E2 = [c for c in positions if any([(c[0] + x[0], c[1] + x[1]) not in positions for x in charE2])]
forbidden_set_E3 = [c for c in positions if any([(c[0] + x[0], c[1] + x[1]) not in positions for x in charE3])]

forbidden_set_S0 = [c for c in positions if any([(c[0] + x[0], c[1] + x[1]) not in positions for x in charS0])]
forbidden_set_S1 = [c for c in positions if any([(c[0] + x[0], c[1] + x[1]) not in positions for x in charS1])]
forbidden_set_S2 = [c for c in positions if any([(c[0] + x[0], c[1] + x[1]) not in positions for x in charS2])]
forbidden_set_S3 = [c for c in positions if any([(c[0] + x[0], c[1] + x[1]) not in positions for x in charS3])]

varY0pos = model.addMVar(shape = (15, 15, 4), vtype = GRB.BINARY)
# varY0pos = how to place the piece "Y". Why do we need the third axis being 4? Because there are four possible ways to place the piece "Y", namely Y0, Y1, Y2 and Y3.
varE0pos = model.addMVar(shape = (15, 15, 4), vtype = GRB.BINARY)
varS0pos = model.addMVar(shape = (15, 15, 4), vtype = GRB.BINARY)


model.addConstr(sum([varY0pos[i, j, k] for i in range(15) for j in range(15) for k in range(4)]) == 1)
# This constraint means that we must use exactly one piece "Y". Similarly for "E" and "S".
model.addConstr(sum([varE0pos[i, j, k] for i in range(15) for j in range(15) for k in range(4)]) == 1)
model.addConstr(sum([varS0pos[i, j, k] for i in range(15) for j in range(15) for k in range(4)]) == 1)

table = model.addMVar(shape = (15, 15), vtype = GRB.BINARY)
# Our table, divided into unit squares. We want to place the puzzle pieces here.
model.addConstr(table == varY0 + varY1 + varY2 + varY3 + varE0 + varE1 + varE2 + varE3 + varS0 + varS1 + varS2 + varS3)
# This counts the number of squares occupied by the puzzle pieces. It is easy to see that the puzzle pieces occupy exactly 24 squares, as we do not allow them to overlap. 
model.addConstr(sum([sum(table[i, :]) for i in range(15)]) == 24)

# Now we add conditions to ensure that the resulting configuration has nontrivial symmetries. There are several possible types of symmetries: (1) the figure has a symmetric axis: "Diagonal symmetric" (the axis of symmetry is a diagonal of the table), "Odd symmetric" (the axis of symmetry is parallel to one of the table's edges, and it passes through the center of some unit square), "Even symmetric" (the axis of symmetry is parallel to one of the table's edges, and it contains an edge of some unit square), (2) the figure has an antipodal point (Point Central Symmetric) (there are some possible types of this: the antipodal point must have coordinate (a/2, b/2) for some integer a, b.). We found a solution for this challenge, however this might not be the only solution.
for coordinate in itertools.product(range(15), repeat= 2):
    i, j = coordinate[0], coordinate[1] 
    # Diagonal symmetric: Model is infeasible. Checked.
    # model.addConstr(table[i, j] == table[j, i])
    # Square Central symmetric: Infeasible. Checked
    # model.addConstr(table[i, j] == table[14 - i, 14 - j])
    # Symmetric Type1: Odd Symmetric: Solved below! So this is solvable.
    model.addConstr(table[i, j] == table[14 - i, j])
    # Symmetric Type2: Even Symmetric: Infeasible.
    # if i <= 13:
    #     model.addConstr(table[i, j] == table[13 - i, j])
    # Point Central Symmetric: Infeasible.
    # if i <= 13 and j <= 13:
    #     model.addConstr(table[i, j] == table[13 - i, 13 - j])
    positions_of_Y0 = [(i - x[0], j - x[1]) for x in charY0 if (i - x[0], j - x[1]) not in forbidden_set_Y0]
    model.addConstr(varY0[i, j] == sum([varY0pos[c[0], c[1], 0] for c in positions_of_Y0]))
    positions_of_Y1 = [(i - x[0], j - x[1]) for x in charY1 if (i - x[0], j - x[1]) not in forbidden_set_Y1]
    model.addConstr(varY1[i, j] == sum([varY0pos[c[0], c[1], 1] for c in positions_of_Y1]))
    positions_of_Y2 = [(i - x[0], j - x[1]) for x in charY2 if (i - x[0], j - x[1]) not in forbidden_set_Y2]
    model.addConstr(varY2[i, j] == sum([varY0pos[c[0], c[1], 2] for c in positions_of_Y2]))
    positions_of_Y3 = [(i - x[0], j - x[1]) for x in charY3 if (i - x[0], j - x[1]) not in forbidden_set_Y3]
    model.addConstr(varY3[i, j] == sum([varY0pos[c[0], c[1], 3] for c in positions_of_Y3]))
    
    position_of_E0 = [(i - x[0], j - x[1]) for x in charE0 if (i - x[0], j - x[1]) not in forbidden_set_E0]
    model.addConstr(varE0[i, j] == sum([varE0pos[c[0], c[1], 0] for c in position_of_E0]))
    position_of_E1 = [(i - x[0], j - x[1]) for x in charE1 if (i - x[0], j - x[1]) not in forbidden_set_E1]
    model.addConstr(varE1[i, j] == sum([varE0pos[c[0], c[1], 1] for c in position_of_E1]))
    position_of_E2 = [(i - x[0], j - x[1]) for x in charE2 if (i - x[0], j - x[1]) not in forbidden_set_E2]
    model.addConstr(varE2[i, j] == sum([varE0pos[c[0], c[1], 2] for c in position_of_E2]))
    position_of_E3 = [(i - x[0], j - x[1]) for x in charE3 if (i - x[0], j - x[1]) not in forbidden_set_E3]
    model.addConstr(varE3[i, j] == sum([varE0pos[c[0], c[1], 3] for c in position_of_E3]))

    position_of_S0 = [(i - x[0], j - x[1]) for x in charS0 if (i - x[0], j - x[1]) not in forbidden_set_S0]
    model.addConstr(varS0[i, j] == sum([varS0pos[c[0], c[1], 0] for c in position_of_S0]))
    position_of_S1 = [(i - x[0], j - x[1]) for x in charS1 if (i - x[0], j - x[1]) not in forbidden_set_S1]
    model.addConstr(varS1[i, j] == sum([varS0pos[c[0], c[1], 1] for c in position_of_S1]))
    position_of_S2 = [(i - x[0], j - x[1]) for x in charS2 if (i - x[0], j - x[1]) not in forbidden_set_S2]
    model.addConstr(varS2[i, j] == sum([varS0pos[c[0], c[1], 2] for c in position_of_S2]))
    position_of_S3 = [(i - x[0], j - x[1]) for x in charS3 if (i - x[0], j - x[1]) not in forbidden_set_S3]
    model.addConstr(varS3[i, j] == sum([varS0pos[c[0], c[1], 3] for c in position_of_S3]))
    

model.setObjective(0, sense = GRB.MAXIMIZE)
model.optimize()


# A way to visualize the solution:
for i in range(4):
    exec(f'Y_pos = varY{i}.x.astype(int)')
    if Y_pos.any():
        print(f'Y is placed in the grid like this:\n{Y_pos}')
    exec(f'E_pos = varE{i}.x.astype(int)')
    if E_pos.any():
        print(f'E is placed in the grid like this:\n{E_pos}')
    exec(f'S_pos = varS{i}.x.astype(int)')
    if S_pos.any():
        print(f'S is placed in the grid like this:\n{S_pos}')

print(table.x.astype(int))
# Our final table-turning result :D.

"""
E is placed in the grid like this:
[[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 1 1 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 1 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 1 1 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 1 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 1 1 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]]
Y is placed in the grid like this:
[[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 1 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 1 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 1 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 1 1 1 0 0 0 0 0 0 0]
 [0 0 0 0 0 1 0 1 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]]
S is placed in the grid like this:
[[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 1 1 1 0 1 0 0 0 0 0 0 0]
 [0 0 0 1 0 1 1 1 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]]
 
OddSymmetric:
[[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 E E Y 0 Y 0 0 0 0 0 0 0]
 [0 0 0 E 0 Y Y Y 0 0 0 0 0 0 0]
 [0 0 0 E E 0 Y 0 0 0 0 0 0 0 0]
 [0 0 0 E 0 0 Y 0 0 0 0 0 0 0 0]
 [0 0 0 E E 0 Y 0 0 0 0 0 0 0 0]
 [0 0 0 S 0 S S S 0 0 0 0 0 0 0]
 [0 0 0 S S S 0 S 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]]

"""

