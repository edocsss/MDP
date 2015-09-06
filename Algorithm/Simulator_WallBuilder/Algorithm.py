from ArenaMap import *

class Algorithm:
    def __init__(self):
        pass

    @staticmethod
    def heuristicFunction(state):
        value = 0
        for i in range(ArenaMap.MAP_HEIGHT):
            for j in range(ArenaMap.MAP_WIDTH):
                if state.robot.mapKnowledge[i][j] == GridState.UNEXPLORED or state.robot.mapKnowledge[i][j] == GridState.END_ZONE:
                    value = 288 - 16 * (j + 1)
        return value      
    
    @staticmethod
    def A_star(start_state):
        # min heap
        pq = Queue.PriorityQueue()

        # (f(state), state)
        pq.push((0, start_state))

        # state -> (g(state), prev_state, prev_action)
        visited = { start_state: (0, None, None) }

        goal_state = None
        while not pq.empty():
            f, current_state = pq.get()
            current_cost = visited[current_state][0]

            if(current_state.isTerminal()):
                goal_state = current_state
                break
            
            for next_action, child_state in current_state.getChildren():
                if child_state not in visited:
                    visited[child_state] = (current_cost + transition_cost, current_state, next_action)
                    pq.put((current_cost + transition_cost + Algorithm.heuristicFunction(child_state), child_state))

        result = []
        v = goal_state
        while v != start_state:
            f, u, prev_action = visited[v]
            result.append(prev_action)
            v = u

        return result[::-1]
