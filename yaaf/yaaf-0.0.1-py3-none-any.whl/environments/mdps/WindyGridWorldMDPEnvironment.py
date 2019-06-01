import numpy as np

from yaaf.environments.mdps.MarkovDecisionProcessEnvironment import MarkovDecisionProcessEnvironment


class WindyGridWorldMDPEnvironment(MarkovDecisionProcessEnvironment):

    def __init__(self, render=False):

        num_actions = 4

        self._wind = (0, 0, 0, 1, 1, 1, 2, 2, 1, 0)
        self._rows = 7
        self._columns = 10

        assert len(self._wind) == self._columns

        self._start_state = np.array([3, 0])
        self._goal_state = np.array([3, 7])

        super(WindyGridWorldMDPEnvironment, self).__init__("Windy Grid World ", num_actions, render)

    def _initial_state(self):
        return self._start_state

    def _transition(self, action):
        s1 = self.state_index(self.state)
        probabilities = self._P[action, s1, :]
        s2 = np.where(probabilities == 1)[0][0]
        next_state = self.states[s2]
        is_terminal = not np.any(self._C[s2])
        return next_state, is_terminal, None

    def _generate_states(self):
        return [np.array([x, y]) for x in range(self._rows) for y in range(self._columns)]

    def _generate_transition_probabilities_matrix(self):

        P = np.zeros((self.num_actions, self.num_states, self.num_states))

        for s1 in range(self.num_states):

            state = self.states[s1]

            s1_transitions = dict()

            s1_transitions[0] = np.array([state[0] - self._wind[state[1]] - 1, state[1]])
            s1_transitions[1] = np.array([state[0] - self._wind[state[1]] + 1, state[1]])
            s1_transitions[2] = np.array([state[0] - self._wind[state[1]], state[1] - 1])
            s1_transitions[3] = np.array([state[0] - self._wind[state[1]], state[1] + 1])

            for action in range(self.num_actions):
                s1_transitions[action][0] = max(min(s1_transitions[action][0], self._rows - 1), 0)
                s1_transitions[action][1] = max(min(s1_transitions[action][1], self._columns - 1), 0)

                next_state = s1_transitions[action]
                s2 = self.state_index(next_state)
                P[action][s1, s2] = 1.0
        return P

    def _generate_cost_matrix(self):
        C = np.ones((self.num_states, self.num_actions))
        s = self.state_index(self._goal_state)
        C[s, :] = 0.0
        return C

    def _render(self):
        pass

    def describe_action(self, a):
        actions = [
            "Move Up",
            "Move Down",
            "Move Left",
            "Move Right"
        ]
        return actions[a]

    def close(self):
        pass
