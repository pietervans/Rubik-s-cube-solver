from state_and_action import State, Action, ALL_ACTIONS, Color
from move import move
from typing import List

def bfs(state: State, max_depth=5) -> List[Action]:
    """Return an optimal sequence of actions to solve the given state
        state: the initial state
        max_depth: the maximum number of actions that will be performed on the initial state"""
    if state.isSolved():
        return []
    states = [state]
    action_seqs = [[]]
    depth = 1
    while depth <= max_depth:
        depth += 1
        # Expand all states
        l = len(states)
        for _ in range(l):
            s = states.pop(0)
            action_seq = action_seqs.pop(0)
            # Try all actions
            for action in ALL_ACTIONS:
                new_s = move(s, action)
                new_seq = list(action_seq)
                new_seq.append(action)
                if new_s.isSolved():
                    return new_seq
                states.append(new_s)
                action_seqs.append(new_seq)
    raise Exception("No solution found! Try increasing max_depth")
    