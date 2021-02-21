import numpy as np

initial_state = []      #Blank array to input initial state
goal_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]     #Goal state array
states = {}     #Blank dictionary of states

instructions = """
                To enter the initial state of the puzzle, type the numbers of the puzzle
                row by row, starting with the top left corner and reading from left-to-right, 
                top-to-bottom. Put a space after each number. After entering the first row 
                of numbers, hit enter, and begin entering the next row. For the blank tile,
                enter 0.
                """
                
print(instructions)     #Pritns instructions for user inputting initial state

for i in range(4):      #This "for" loop allows the user to input the initial state row-by-row
   row = list(map(int, input("Enter row: ").split()))
   initial_state.append(row)

initial_state = np.array(initial_state)     #Converts the intial state to a numpy array to allow numpy operations
goal_state = np.array(goal_state)       #Converts the goal state to a numpy array to allow numpy operations

states["I"] = initial_state         #Stores the first initial state in the states dictionary

i,j = np.where(initial_state == 0)      #Finds the locations of blank tile in initial state

x = 0       #Sets "x=o", this changes to x=1 when a solution is found, which breaks the "while" loop below

def ReadAround(state):      #This functions reads the current values around the blank tile
    i,j = np.where(state == 0)      #Finds the blank tile
    right_val = 16      #If the blank tile is along an edge, the value outside the puzzle is "16"
    left_val = 16
    up_val = 16
    down_val = 16
    if i == 0:      #The following "if", "elif", and "else" statements find the values around the blank tile
        if j == 0:
            right_val = state[0][1]
            down_val = state[1][0]
            return right_val, left_val, up_val, down_val
        elif j == 3:
            left_val = state[0][2]
            down_val = state[1][3]
            return right_val, left_val, up_val, down_val
        else:
            right_val = state[0][j+1]
            left_val = state[0][j-1]
            down_val = state[1][j]
            return right_val, left_val, up_val, down_val
    elif i == 1:
        if j == 0:
            right_val = state[1][1]
            up_val = state[0][0]
            down_val = state[2][0]
            return right_val, left_val, up_val, down_val
        if j == 3:
            left_val = state[1][2]
            up_val = state[0][3]
            down_val = state[2][3]
            return right_val, left_val, up_val, down_val
        else:
            right_val = state[1][j+1]
            left_val = state[1][j-1]
            up_val = state[0][j]
            down_val = state[2][j]
            return right_val, left_val, up_val, down_val
    elif i == 2:
        if j == 0:
            right_val = state[2][1]
            up_val = state[1][0]
            down_val = state[3][0]
            return right_val, left_val, up_val, down_val
        if j == 3:
            left_val = state[2][2]
            up_val = state[1][3]
            down_val = state[3][3]
            return right_val, left_val, up_val, down_val
        else:
            right_val = state[2][j+1]
            left_val = state[2][j-1]
            up_val = state[1][j]
            down_val = state[3][j]
            return right_val, left_val, up_val, down_val
    elif i == 3:
        if j == 0:
            right_val = state[3][1]
            up_val = state[2][0]
            return right_val, left_val, up_val, down_val
        elif j == 3:
            left_val = state[3][2]
            up_val = state[2][3]
            return right_val, left_val, up_val, down_val
        else:
            right_val = state[3][j+1]
            left_val = state[3][j-1]
            up_val = state[2][j]
            return right_val, left_val, up_val, down_val

def MoveUp(state):      #This function finds the state of the puzzle if the blank tile moves up
    i,j = np.where(state == 0)      #Finds the blank tile
    child_up = state.copy()         #Copies the state to make a child state
    right_val, left_val, up_val, down_val = ReadAround(state)       #Reads the values around the blank tile
    key_list = list(states.keys())      #Lists the keys in dictionary
    new_key = key_list[x]       #Finds the key for parent state
    if up_val != 16:        #If the value above the blank is a valid number...
        i_new = int(i)
        j_new = int(j)
        child_up[i_new][j_new] = up_val   #Switch the blank tile with the value above it
        child_up[i_new-1][j_new] = 0
        if any(np.array_equal(child_up, x) for x in list(states.values())):     #If the new state is in dicitonary, ignore the new child state
            return child_up
        else:
            states[new_key + "U"] = child_up   #If the child state is not in diciontary, store it with the previous key + the direction the blank tile moved (in this case, "U" for up)
            return child_up
        return child_up
    else:
        return child_up
        
def MoveDown(state):        #Same as MoveUp, but for when blank tile moves down
    i,j = np.where(state == 0)
    child_down = state.copy()
    right_val, left_val, up_val, down_val = ReadAround(state)
    key_list = list(states.keys())
    new_key = key_list[x]
    if down_val != 16:
        i_new = int(i)
        j_new = int(j)
        child_down[i_new][j_new] = down_val
        child_down[i_new+1][j_new] = 0
        if any(np.array_equal(child_down, x) for x in list(states.values())):
            return child_down
        else:
            states[new_key + "D"] = child_down
            return child_down
    else:
        return child_down

def MoveRight(state):       #Same as MoveUp, but for when blank tile moves right
    i,j = np.where(state == 0)
    child_right = state.copy()
    right_val, left_val, up_val, down_val = ReadAround(state)
    key_list = list(states.keys())
    new_key = key_list[x]
    if right_val != 16:
        i_new = int(i)
        j_new = int(j)
        child_right[i_new][j_new] = right_val
        child_right[i_new][j_new+1] = 0
        if any(np.array_equal(child_right, x) for x in list(states.values())):
            return child_right
        else:
            states[new_key + "R"] = child_right
            return child_right
    else:
        return child_right
    
def MoveLeft(state):        #Same as MoveUp, but for when blank tile moves left
    i,j = np.where(state == 0)
    child_left = state.copy()
    right_val, left_val, up_val, down_val = ReadAround(state)
    key_list = list(states.keys())
    new_key = key_list[x]
    if left_val != 16:
        i_new = int(i)
        j_new = int(j)
        child_left[i_new][j_new] = left_val
        child_left[i_new][j_new-1] = 0
        if any(np.array_equal(child_left, x) for x in list(states.values())):
            return child_left
        else:
            states[new_key + "L"] = child_left
            return child_left
    else:
        return child_left

def Update(state):      #Updates the parent state to find the four child states
    state_up = MoveUp(state)
    state_down = MoveDown(state)
    state_right = MoveRight(state)
    state_left = MoveLeft(state)
    return state_up, state_down, state_right, state_left

solution = 0
x = 0
while solution == 0:        #While the solution hasn't yet been found...
    parent = list(states.values())[x]       #Set current state as parent state
    if np.array_equal(parent, goal_state) == True:          #If goal state is found, break this "while" loop
        solution = 1
        break
    else:
        Update(parent)      #Find child states for the current parent state
        x = x + 1
        print("Iteration #" , x)
        print("--------------------------")
        
answer = """
         'I' is the intial state. Follow the order provided below, where U = move the
         blank tile up, D = move the blank tile down, R = move the blank tile right,
         and L = move the blank tile left.
         """

print()
print("Solution found!")
print()
print(answer)    #Print instructions for reading output
print()
print(list(states.keys())[x])       #Print key for solution