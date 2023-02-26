from random import random, randint

EPSILON = 0.1
BANDITS = 3
EPISODES = 10000


class Bandit:
    def __init__(self, probability):
        self.q = 0
        self.k = 0
        self.probability = probability

    def get_reward(self):
        if random() < self.probability:
            return 1
        else:
            return 0


class NArmedBandit:
    def __init__(self):
        self.bandits = []
        self.bandits.append(Bandit(0.5))
        self.bandits.append(Bandit(0.6))
        self.bandits.append(Bandit(0.4))

    def run(self):
        for i in range(EPISODES):
            bandit = self.bandits[self.select_bandit()]
            reward = bandit.get_reward()
            self.update(bandit, reward)
            print(f'Iteration {i} bandit {bandit.probability} with Q value {bandit.q}')

    def select_bandit(self):
        # epsilon -greedy strategy.
        # with epsilon probability we explore and with 1- eps probaility we exploit
        if random() < EPSILON:
            # exploration
            bandit_index = randint(0, BANDITS - 1)
        else:
            # exploitation
            bandit_index = self.get_bandit_max_q()
        return bandit_index

    def update(self, bandit, reward):
        bandit.k += 1
        bandit.q = bandit.q + (1 / (1 + bandit.k)) * (reward - bandit.q)

    def get_bandit_max_q(self):
        max_q_bandit_index = 0
        max_q = self.bandits[max_q_bandit_index].q

        for i in range(1, BANDITS):
            if self.bandits[i].q > max_q:
                max_q = self.bandits[i].q
                max_q_bandit_index = i

        return max_q_bandit_index

    def show_statistics(self):
        for i in range(BANDITS):
            print('Bandit %s with k: %s' % (i, self.bandits[i].k))


if __name__ == '__main__':
    bandit_problem = NArmedBandit()
    bandit_problem.run()
    bandit_problem.show_statistics()
