class MonkeyBananaProblem:
    def __init__(self):
        # Initial state: (monkey_position, box_position, monkey_on_box, has_banana)
        # Positions: 0 = door, 1 = corner, 2 = under_banana
        self.initial_state = ('door', 'corner', False, False)
        self.goal_state = (None, None, None, True)  # Only care about has_banana = True
        
    def is_goal(self, state):
        """Check if the goal state is reached"""
        return state[3] == True  # has_banana is True
    
    def get_actions(self, state):
        """Return list of possible actions from current state"""
        monkey_pos, box_pos, on_box, has_banana = state
        actions = []
        
        if has_banana:
            return ['success']
        
        # Action 1: Go to different locations
        locations = ['door', 'corner', 'under_banana']
        for loc in locations:
            if loc != monkey_pos and not on_box:
                actions.append(f'go_to_{loc}')
        
        # Action 2: Push box (only if monkey at same position as box)
        if monkey_pos == box_pos and not on_box:
            for loc in locations:
                if loc != box_pos:
                    actions.append(f'push_box_to_{loc}')
        
        # Action 3: Climb box (only if monkey at box and box under bananas)
        if monkey_pos == box_pos and box_pos == 'under_banana' and not on_box:
            actions.append('climb_box')
        
        # Action 4: Grab banana (only if on box under bananas)
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
    
    def solve(self, current_state, path=None):
        """DFS search to find solution path"""
        if path is None:
            path = [current_state]
        
        if self.is_goal(current_state):
            return path
        
        for action in self.get_actions(current_state):
            if action == 'success':
                continue
                
            new_state = self.apply_action(current_state, action)
            
            # Avoid cycles (don't revisit same state)
            if new_state not in path:
                result = self.solve(new_state, path + [new_state])
                if result:
                    return result
        
        return None
    
    def print_solution(self, solution_path):
        """Print the solution in a readable format"""
        if not solution_path:
            print("No solution found!")
            return
        
        print("=" * 50)
        print("MONKEY AND BANANA PROBLEM - SOLUTION")
        print("=" * 50)
        print("\nInitial State:")
        self.print_state(solution_path[0])
        
        print("\nSolution Steps:")
        for i in range(len(solution_path) - 1):
            current = solution_path[i]
            next_state = solution_path[i + 1]
            
            # Determine what action was taken
            if current[3] == False and next_state[3] == True:
                action = "Grabbed the banana!"
            elif current[2] == False and next_state[2] == True:
                action = "Climbed onto the box"
            elif current[0] != next_state[0] and current[1] == next_state[1]:
                action = f"Went from {current[0]} to {next_state[0]}"
            elif current[1] != next_state[1]:
                action = f"Pushed box from {current[1]} to {next_state[1]}"
            else:
                action = "Unknown action"
            
            print(f"\nStep {i+1}: {action}")
            self.print_state(next_state)
        
        print("\n" + "=" * 50)
        print("GOAL ACHIEVED! The monkey got the banana! 🐒🍌")
        print("=" * 50)
    
    def print_state(self, state):
        """Print current state in readable format"""
        monkey_pos, box_pos, on_box, has_banana = state
        
        status = []
        status.append(f"Monkey is at: {monkey_pos}")
        status.append(f"Box is at: {box_pos}")
        status.append(f"Monkey on box: {'Yes' if on_box else 'No'}")
        status.append(f"Has banana: {'Yes' if has_banana else 'No'}")
        
        print("  " + "\n  ".join(status))

# Alternative implementation using a simple planner approach
class SimplePlanner:
    def __init__(self):
        self.actions_taken = []
    
    def plan(self):
        """Simple hardcoded plan for demonstration"""
        print("\n" + "=" * 50)
        print("SIMPLE PLANNER APPROACH")
        print("=" * 50)
        
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

# Run both implementations
if __name__ == "__main__":
    print("MONKEY AND BANANA PROBLEM")
    print("=" * 50)
    
    # Method 1: State-space search
    print("\nMETHOD 1: State-Space Search (DFS)")
    print("-" * 30)
    
    problem = MonkeyBananaProblem()
    solution = problem.solve(problem.initial_state)
    
    if solution:
        problem.print_solution(solution)
    else:
        print("No solution found using DFS!")
    
    # Method 2: Simple planner
    print("\n" + "=" * 50)
    planner = SimplePlanner()
    plan = planner.plan()
    
    print(f"\nPlan steps: {' -> '.join(plan)}")
    
    # Method 3: Interactive demonstration
    print("\n" + "=" * 50)
    print("INTERACTIVE DEMONSTRATION")
    print("=" * 50)
    
    print("\nLet's trace through the solution:")
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