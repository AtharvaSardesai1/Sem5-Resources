N = 4

def constraints(Q1_pos, Q2_pos):
    row1, col1 = Q1_pos
    row2, col2 = Q2_pos

    if row1 == row2:  # Same row
        return False
    if col1 == col2:  # Same column
        return False
    if abs(row1 - row2) == abs(col1 - col2):  # Same diagonal
        return False

    return True

def DFS(graph, variable, domain, assignment, constraints, solutions):

    if len(assignment) == N:
        solutions.append([assignment[i] for i in range(N)])
        print(f"Solution found: {[assignment[i] for i in range(N)]}")
        return

    current_var = variable[len(assignment)]  
    
    for value in domain:
        valid = True

        for prev_var in assignment:
            if not constraints((assignment[prev_var], prev_var), (value, current_var)):
                valid = False
                break
        
        if valid:
            assignment[current_var] = value  
            print(f"Placing Queen {current_var + 1} at row {value}")

            DFS(graph, variable, domain, assignment, constraints, solutions)
            
            print(f"Backtracking Queen {current_var + 1} from row {value}")
            del assignment[current_var]

def solveNQ():
    variable = list(range(N))  
    domain = list(range(1, N + 1))  
    graph = {} 
    assignment = {}  
    solutions = []  

    DFS(graph, variable, domain, assignment, constraints, solutions)
    
    return solutions if solutions else "Solution does not exist"

if __name__ == '__main__':
    solutions = solveNQ()
    for solution in solutions:
        print(solution)
