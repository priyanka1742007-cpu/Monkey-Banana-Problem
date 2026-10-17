"""
Monkey and Banana Problem in Artificial Intelligence
Classic State-Space Search & Classical Planning Demonstration

Contains:
1. Depth-First Search (DFS)
2. Breadth-First Search (BFS) - Guaranteed Optimal
3. A* Search (A-Star with Admissible Heuristic) - Guaranteed Optimal & Efficient
4. Simple Rule-Based Planner
5. Step-by-Step Interactive Demonstration
"""

from collections import deque
import heapq


class MonkeyBananaProblem:
    def __init__(self):
        # Initial state: (monkey_position, box_position, monkey_on_box, has_banana)
        # Positions: 'door', 'corner', 'under_banana'
        self.initial_state = ('door', 'corner', False, False)
        self.goal_state = (None, None, None, True)  # Goal: has_banana = True
        
    def is_goal(self, state):
        """Check if the goal state is reached"""
        return state[3] is True  # has_banana is True
    
    def get_actions(self, state):
        """Return list of possible actions from current state"""
        monkey_pos, box_pos, on_box, has_banana = state
        actions = []
        
        if has_banana:
            return ['success']
        
        locations = ['door', 'corner', 'under_banana']

        # Action 1: Go to different locations (only if not standing on box)
        for loc in locations:
            if loc != monkey_pos and not on_box:
                actions.append(f'go_to_{loc}')
        
        # Action 2: Push box (only if monkey at same position as box and on the floor)
        if monkey_pos == box_pos and not on_box:
            for loc in locations:
                if loc != box_pos:
                    actions.append(f'push_box_to_{loc}')
        
        # Action 3: Climb box (only if monkey at box and box is under the banana)
        if monkey_pos == box_pos and box_pos == 'under_banana' and not on_box:
            actions.append('climb_box')
        
        # Action 4: Grab banana (only if standing on box under banana)
        if on_box and box_pos == 'under_banana' and not has_banana:
            actions.append('grab_banana')
        
        return actions
    
    def apply_action(self, state, action):
        """Apply action to state and return new state"""
        monkey_pos, box_pos, on_box, has_banana = state
        
        if action.startswith('go_to_'):
            new_pos = action.replace('go_to_', '')
            return (new_pos, box_pos, False, has_banana)
        
        elif action.startswith('push_box_to_'):
            new_pos = action.replace('push_box_to_', '')
            return (new_pos, new_pos, False, has_banana)
        
        elif action == 'climb_box':
            return (monkey_pos, box_pos, True, has_banana)
        
        elif action == 'grab_banana':
            return (monkey_pos, box_pos, on_box, True)
        
        return state

    def heuristic(self, state):
        """
        Admissible & consistent heuristic estimating remaining actions to goal:
        h(n) <= h*(n)
        - +1 to grab banana
        - +1 to climb box (if not already on box)
        - +1 to push box to under_banana (if box not already under banana)
        - +1 to go to box (if monkey is not at box)
        """
        monkey_pos, box_pos, on_box, has_banana = state
        if has_banana:
            return 0
        
        h = 1  # Action: grab_banana
        if not on_box:
            h += 1  # Action: climb_box
        if box_pos != 'under_banana':
            h += 1  # Action: push_box_to_under_banana
            if monkey_pos != box_pos:
                h += 1  # Action: go_to_<box_pos>
        elif monkey_pos != box_pos and not on_box:
            h += 1  # Action: go_to_under_banana
            
        return h

    # 1. Depth-First Search (DFS)
    def solve_dfs(self, current_state=None, path=None):
        """DFS search to find solution path (not guaranteed to be optimal)"""
        if current_state is None:
            current_state = self.initial_state
        if path is None:
            path = [current_state]
        
        if self.is_goal(current_state):
            return path
        
        for action in self.get_actions(current_state):
            if action == 'success':
                continue
                
            new_state = self.apply_action(current_state, action)
            
            # Avoid cycles (don't revisit same state in current branch)
            if new_state not in path:
                result = self.solve_dfs(new_state, path + [new_state])
                if result:
                    return result
        
        return None

    # Backward compatibility alias
    solve = solve_dfs

    # 2. Breadth-First Search (BFS)
    def solve_bfs(self, start_state=None):
        """BFS search to guarantee shortest/optimal solution path"""
        if start_state is None:
            start_state = self.initial_state
        
        queue = deque([(start_state, [start_state])])
        visited = {start_state}
        
        while queue:
            state, path = queue.popleft()
            
            if self.is_goal(state):
                return path
                
            for action in self.get_actions(state):
                if action == 'success':
                    continue
                new_state = self.apply_action(state, action)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, path + [new_state]))
                     
        return None

    # 3. A* Search (A-Star)
    def solve_astar(self, start_state=None):
        """A* search with admissible heuristic to find optimal solution efficiently"""
        if start_state is None:
            start_state = self.initial_state
            
        counter = 0  # Tie-breaker for heap
        # Priority queue stores: (f_score, g_score, counter, state, path)
        g_start = 0
        f_start = g_start + self.heuristic(start_state)
        open_set = [(f_start, g_start, counter, start_state, [start_state])]
        best_g = {start_state: 0}
        
        while open_set:
            f, g, _, current, path = heapq.heappop(open_set)
            
            if self.is_goal(current):
                return path
                
            if g > best_g.get(current, float('inf')):
                continue
                
            for action in self.get_actions(current):
                if action == 'success':
                    continue
                    
                neighbor = self.apply_action(current, action)
                tentative_g = g + 1  # Cost of each action is 1
                
                if tentative_g < best_g.get(neighbor, float('inf')):
                    best_g[neighbor] = tentative_g
                    counter += 1
                    f_score = tentative_g + self.heuristic(neighbor)
                    heapq.heappush(open_set, (f_score, tentative_g, counter, neighbor, path + [neighbor]))
                    
        return None

    def print_solution(self, solution_path, method_name="SOLUTION"):
        """Print the solution in a readable format"""
        if not solution_path:
            print(f"No solution found using {method_name}!")
            return
        
        print("=" * 55)
        print(f"MONKEY AND BANANA PROBLEM - {method_name.upper()}")
        print("=" * 55)
        print("\nInitial State:")
        self.print_state(solution_path[0])
        
        print(f"\nSolution Steps (Total Actions: {len(solution_path) - 1}):")
        for i in range(len(solution_path) - 1):
            current = solution_path[i]
            next_state = solution_path[i + 1]
            
            # Determine what action was taken
            if current[3] is False and next_state[3] is True:
                action = "Grabbed the banana!"
            elif current[2] is False and next_state[2] is True:
                action = "Climbed onto the box"
            elif current[0] != next_state[0] and current[1] == next_state[1]:
                action = f"Went from {current[0]} to {next_state[0]}"
            elif current[1] != next_state[1]:
                action = f"Pushed box from {current[1]} to {next_state[1]}"
            else:
                action = "Unknown action"
            
            print(f"\nStep {i+1}: {action}")
            self.print_state(next_state)
        
        print("\n" + "=" * 55)
        print("GOAL ACHIEVED! The monkey got the banana! 🐒🍌")
        print("=" * 55)
    
    def print_state(self, state):
        """Print current state in readable format"""
        monkey_pos, box_pos, on_box, has_banana = state
        
        status = [
            f"Monkey is at: {monkey_pos}",
            f"Box is at: {box_pos}",
            f"Monkey on box: {'Yes' if on_box else 'No'}",
            f"Has banana: {'Yes' if has_banana else 'No'}"
        ]
        print("  " + "\n  ".join(status))


# Alternative implementation using a simple planner approach
class SimplePlanner:
    def __init__(self):
        self.actions_taken = []
    
    def plan(self):
        """Simple hardcoded plan for demonstration"""
        print("\n" + "=" * 55)
        print("SIMPLE PLANNER APPROACH")
        print("=" * 55)
        
        # Step 1: Go to box
        print("\nStep 1: Monkey goes to the corner where the box is")
        self.actions_taken.append("go_to_corner")
        
        # Step 2: Push box under banana
        print("Step 2: Monkey pushes the box from corner to under the banana")
        self.actions_taken.append("push_box_to_under_banana")
        
        # Step 3: Climb the box
        print("Step 3: Monkey climbs onto the box")
        self.actions_taken.append("climb_box")
        
        # Step 4: Grab banana
        print("Step 4: Monkey grabs the banana!")
        self.actions_taken.append("grab_banana")
        
        print("\n🎉 Success! The monkey enjoyed the banana!")
        
        return self.actions_taken


# Run all implementations and compare
if __name__ == "__main__":
    print("MONKEY AND BANANA PROBLEM - AI SEARCH COMPARISON")
    print("=" * 55)
    
    problem = MonkeyBananaProblem()

    # Method 1: State-space search (DFS)
    print("\n[1] METHOD 1: State-Space Search (DFS)")
    print("-" * 40)
    solution_dfs = problem.solve_dfs()
    if solution_dfs:
        problem.print_solution(solution_dfs, "DFS (Depth-First Search)")
    else:
        print("No solution found using DFS!")

    # Method 2: Breadth-First Search (BFS)
    print("\n[2] METHOD 2: Optimal Search (BFS)")
    print("-" * 40)
    solution_bfs = problem.solve_bfs()
    if solution_bfs:
        problem.print_solution(solution_bfs, "BFS (Breadth-First Search - Optimal)")
    else:
        print("No solution found using BFS!")

    # Method 3: A* Search
    print("\n[3] METHOD 3: Informed Heuristic Search (A*)")
    print("-" * 40)
    solution_astar = problem.solve_astar()
    if solution_astar:
        problem.print_solution(solution_astar, "A* Search (Heuristic - Optimal)")
    else:
        print("No solution found using A*!")

    # Algorithm Comparison Table
    print("\n" + "=" * 55)
    print("SEARCH ALGORITHM COMPARISON")
    print("=" * 55)
    print(f"{'Algorithm':<20} | {'Action Steps':<15} | {'Optimality':<15}")
    print("-" * 55)
    dfs_steps = len(solution_dfs) - 1 if solution_dfs else "N/A"
    bfs_steps = len(solution_bfs) - 1 if solution_bfs else "N/A"
    astar_steps = len(solution_astar) - 1 if solution_astar else "N/A"
    print(f"{'DFS':<20} | {str(dfs_steps):<15} | {'Sub-optimal':<15}")
    print(f"{'BFS':<20} | {str(bfs_steps):<15} | {'Optimal (Shortest)':<15}")
    print(f"{'A*':<20} | {str(astar_steps):<15} | {'Optimal (Shortest)':<15}")
    print("=" * 55)

    # Method 4: Simple planner
    planner = SimplePlanner()
    plan = planner.plan()
    print(f"\nPlan steps: {' -> '.join(plan)}")
    
    # Method 5: Interactive demonstration
    print("\n" + "=" * 55)
    print("INTERACTIVE STEP-BY-STEP TRACE")
    print("=" * 55)
    
    print("\nLet's trace through the optimal solution:")
    current_state = ('door', 'corner', False, False)
    
    print(f"\nStart: Monkey at door, Box in corner")
    print("↓ Go to corner")
    current_state = ('corner', 'corner', False, False)
    print(f"Now: Monkey at corner with box")
    
    print("↓ Push box under banana")
    current_state = ('under_banana', 'under_banana', False, False)
    print(f"Now: Box under banana, monkey with box")
    
    print("↓ Climb box")
    current_state = ('under_banana', 'under_banana', True, False)
    print(f"Now: Monkey on box under banana")
    
    print("↓ Grab banana")
    current_state = ('under_banana', 'under_banana', True, True)
    print(f"Finally: 🎉 Monkey has banana!")
