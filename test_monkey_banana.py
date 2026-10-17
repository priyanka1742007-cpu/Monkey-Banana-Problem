import unittest
from Monkey_Banana import MonkeyBananaProblem, SimplePlanner


class TestMonkeyBananaProblem(unittest.TestCase):
    def setUp(self):
        self.problem = MonkeyBananaProblem()

    def test_initial_state(self):
        self.assertEqual(self.problem.initial_state, ('door', 'corner', False, False))
        self.assertFalse(self.problem.is_goal(self.problem.initial_state))

    def test_goal_state(self):
        goal_state = ('under_banana', 'under_banana', True, True)
        self.assertTrue(self.problem.is_goal(goal_state))

    def test_bfs_optimal_length(self):
        path = self.problem.solve_bfs()
        self.assertIsNotNone(path)
        # Optimal action count is 4, which means path has 5 states
        self.assertEqual(len(path) - 1, 4)
        self.assertTrue(self.problem.is_goal(path[-1]))

    def test_astar_optimal_length(self):
        path = self.problem.solve_astar()
        self.assertIsNotNone(path)
        self.assertEqual(len(path) - 1, 4)
        self.assertTrue(self.problem.is_goal(path[-1]))

    def test_dfs_finds_valid_solution(self):
        path = self.problem.solve_dfs()
        self.assertIsNotNone(path)
        self.assertTrue(self.problem.is_goal(path[-1]))
        # DFS may find a sub-optimal solution
        self.assertGreaterEqual(len(path) - 1, 4)

    def test_heuristic_admissibility(self):
        # Heuristic must never overestimate the cost to reach goal (h <= h*)
        self.assertEqual(self.problem.heuristic(('under_banana', 'under_banana', True, True)), 0)
        self.assertEqual(self.problem.heuristic(('under_banana', 'under_banana', True, False)), 1)
        self.assertEqual(self.problem.heuristic(('under_banana', 'under_banana', False, False)), 2)
        self.assertEqual(self.problem.heuristic(('corner', 'corner', False, False)), 3)
        self.assertEqual(self.problem.heuristic(('door', 'corner', False, False)), 4)

    def test_simple_planner(self):
        planner = SimplePlanner()
        plan = planner.plan()
        expected = ["go_to_corner", "push_box_to_under_banana", "climb_box", "grab_banana"]
        self.assertEqual(plan, expected)


if __name__ == '__main__':
    unittest.main()

