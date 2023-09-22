import copy
import random

class MarkovDP:
    def __init__(self, x, y, walls, terminals, reward, trans_probs, epsilon, discount_factor):
        self.x_max = x
        self.y_max = y
        self.state = [[0] * self.x_max for _ in range(self.y_max)]
        self.grid = [[reward] * self.x_max for _ in range(self.y_max)]
        self.wall_locs = []
        self.terminals = []
        for wall in walls:
            wall_x, wall_y = wall[0] - 1, self.y_max - wall[1]
            self.state[wall_y][wall_x] = None
            self.grid[wall_y][wall_x] = None
            self.wall_locs.append([wall_y, wall_x])

        for terminal in terminals:
            term_x, term_y, term_val = terminal[0] - 1, self.y_max - terminal[1], terminal[2]
            self.grid[term_y][term_x] = term_val
            self.terminals.append([term_y, term_x])

        self.reward = reward
        self.transition_probs = trans_probs
        self.epsilon = epsilon
        self.discount = discount_factor

    def valid_action(self, x, y, a):
        if a == "N" and x - 1 >= 0 and [x - 1, y] not in self.wall_locs:
            return [x - 1, y]
        elif a == "S" and x + 1 < self.y_max and [x + 1, y] not in self.wall_locs:
            return [x + 1, y]
        elif a == "E" and y + 1 < self.x_max and [x, y + 1] not in self.wall_locs:
            return [x, y + 1]
        elif a == "W" and y - 1 >= 0 and [x, y - 1] not in self.wall_locs:
            return [x, y - 1]
        else:
            return [x, y]

    def action_space(self):
        return ["E", "N", "W", "S"]

    def is_terminal(self, x, y):
        return [x, y] in self.terminals or [x, y] in self.wall_locs

    def transition(self, x, y, a):
        directions = ["E", "N", "W", "S"]
        turns = FORWARD, LEFT, RIGHT, BACK = (0, +1, -1, +2)

        def change_heading(heading, inc, headings=directions):
            return headings[(headings.index(heading) + inc) % len(headings)]

        result = []
        for i in turns:
            result.append(self.valid_action(x, y, change_heading(a, i)))

        return result

    

def value_iter(mdp):
    iteration = 0
    V = mdp.state
    print("Iteration :", iteration)
    display_grid(V, mdp)
    while True:
        iteration += 1
        new_V = copy.deepcopy(V)
        for x, row in enumerate(V):
            for y, item in enumerate(row):
                if not mdp.is_terminal(x, y):
                    new_V[x][y] = max(q_value(mdp, x, y, action, V) for action in mdp.action_space())

        max_diff = max(abs(V[x][y] - new_V[x][y]) for x, row in enumerate(V) for y, item in enumerate(row) if not mdp.is_terminal(x, y))
        if max_diff <= (mdp.epsilon * (1 - mdp.discount) / mdp.discount):
            break
        print("Iteration :", iteration)
        display_grid(new_V, mdp)
        V = new_V

    optimal_policy = copy.deepcopy(V)
    for x, row in enumerate(V):
        for y, item in enumerate(row):
            if not mdp.is_terminal(x, y):
                optimal_policy[x][y] = max((q_value(mdp, x, y, action, V), action) for action in mdp.action_space())[1]

    print("Final Value after Convergence")
    display_grid(new_V, mdp)
    return optimal_policy

def policy_eval(policy, U, mdp):
    new_U = copy.deepcopy(U)
    for x, row in enumerate(new_U):
        for y, item in enumerate(row):
            if not mdp.is_terminal(x, y):
                new_U[x][y] = q_value(mdp, x, y, policy[x][y], U)
    return new_U

def q_value(mdp, x, y, action, V):
    transition_states = mdp.transition(x, y, action)
    probs = mdp.transition_probs
    total = sum(probs[i] * (mdp.grid[item[0]][item[1]] if mdp.is_terminal(item[0], item[1]) else (mdp.grid[x][y] + mdp.discount * V[item[0]][item[1]])) for i, item in enumerate(transition_states))
    return total


def policy_iter(mdp):
    policy = copy.deepcopy(mdp.state)
    U = copy.deepcopy(mdp.state)
    for x, row in enumerate(policy):
        for y, item in enumerate(row):
            if not mdp.is_terminal(x, y):
                policy[x][y] = random.choice(mdp.action_space())
                

    while True:
        U = policy_eval(policy, U, mdp)
        unchanged = True
        for x, row in enumerate(U):
            for y, item in enumerate(row):
                if not mdp.is_terminal(x, y):
                    best_action = max((q_value(mdp, x, y, action, U), action) for action in mdp.action_space())[1]
                    if q_value(mdp, x, y, best_action, U) > q_value(mdp, x, y, policy[x][y], U):
                        unchanged = False
                        policy[x][y] = best_action
        if unchanged:
            return policy
                    
def parse_input(lines):
    params = {}
    for line in lines:
        if line[0] != '#' and line[0] != '\r' and line[0] != '\n' and line.strip() != '':
            key, value = line.split(':')
            key = key.strip()
            value = value.strip()
            if key == 'size':
                params['gridx'], params['gridy'] = map(int, value.split())
            elif key == 'walls':
                params['wallLocations'] = [list(map(int, loc.split())) for loc in value.split(',')]
            elif key == 'terminal_states':
                params['terminalStates'] = [list(map(int, state.split())) for state in value.split(',')]
            elif key == "reward":
                params['reward'] = float(value)
            elif key == "transition_probabilities":
                params['transitionProbabilities'] = list(map(float, value.split()))
            elif key == "discount_rate":
                params['discount'] = float(value)
            elif key == "epsilon":
                params['epsilon'] = float(value)
    return params

def display_grid(grid, mdp):
    for row_idx, row in enumerate(grid):
        line = ''
        for col_idx, item in enumerate(row):
            if [row_idx, col_idx] in mdp.wall_locs:
                line += '--------------'
            elif isinstance(item, (int, float)):
                line += '%.12f' % item
            else:
                line += '%s' % item
            line += '  '
        print(line)
    print()


def display_policy(policy, mdp):
    for row_idx, row in enumerate(policy):
        line = ''
        for col_idx, item in enumerate(row):
            if [row_idx, col_idx] in mdp.terminals:
                line += 'T'
            elif [row_idx, col_idx] in mdp.wall_locs:
                line += '-'
            else:
                line += item
            line += '  '
        print(line)
    print()

def main():
    with open("mdp_input.txt") as fp:
        lines = fp.readlines()
        params = parse_input(lines)

    mdp = MarkovDP(params['gridx'], params['gridy'], params['wallLocations'], params['terminalStates'],
                params['reward'], params['transitionProbabilities'], params['epsilon'], params['discount'])

    print("({0}, {1}, {2}, {3}, {4}, '{5}', {6}, {7})\n".format(
        mdp.y_max, mdp.x_max, mdp.wall_locs, {tuple(loc): mdp.grid[loc[0]][loc[1]] for loc in mdp.terminals},
        mdp.reward, " ".join(str(prob) for prob in mdp.transition_probs), mdp.discount, mdp.epsilon))
        
    print("################ VALUE ITERATION ###########################\n")
    optimal_PI = value_iter(mdp)
    print("Final Policy\n")
    display_policy(optimal_PI, mdp)


    print("################ POLICY ITERATION ###########################\n")
    PI = policy_iter(mdp)
    display_policy(PI, mdp)

if __name__=="__main__":main()
