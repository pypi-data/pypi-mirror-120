import numpy as np
import gym
from gym.error import ResetNeeded

from pogema.animation import AnimationMonitor
from pogema.grid import Grid
from pogema.grid_config import GridConfig


class PogemaBase(gym.Env):

    def __init__(self, config: GridConfig = GridConfig()):
        # noinspection PyTypeChecker
        self.grid: Grid = None
        self.config = config

        full_size = self.config.obs_radius * 2 + 1
        self.observation_space = gym.spaces.Box(0.0, 1.0, shape=(3, full_size, full_size))
        self.action_space = gym.spaces.Discrete(len(self.config.MOVES))

    def _get_agents_obs(self, agent_id=0):
        return np.concatenate([
            self.grid.get_obstacles(agent_id)[None],
            self.grid.get_positions(agent_id)[None],
            self.grid.get_square_target(agent_id)[None]
        ])

    def check_reset(self):
        if self.grid is None:
            raise ResetNeeded("Please reset environment first!")

    def render(self, mode='human'):
        self.check_reset()
        return self.grid.render(mode=mode)


# class StochasticPogesa(PogesaBase):
#     def __init__(self, config: GridConfig = GridConfig(num_agents=1), morph_tau=1):
#         super().__init__(config)
#         self.morph_tau = morph_tau
#         self.rnd = np.random.default_rng(self.config.seed)
#         self._steps = 0
#
#     def morph_obstacles(self):
#         r = self.config.obs_radius
#         self.grid.obstacles[r:-r, r:-r] = generate_obstacles(self.config, self.rnd)
#         for position in self.grid.positions_xy:
#             self.grid.obstacles[position] = self.config.FREE
#
#     def step(self, action):
#         self.check_reset()
#
#         if self._steps % self.morph_tau == 0:
#             self.morph_obstacles()
#
#         finish = self.grid.move(0, action)
#         info = dict()
#         reward = 1.0 if finish else 0.0
#
#         self._steps += 1
#         return self._get_obs(), reward, finish, info
#
#     def reset(self):
#         self._steps = 0
#         self.grid: Grid = Grid.random_grid_generator(config=self.config)
#         return self._get_obs()


class Pogema(PogemaBase):
    def __init__(self, config=GridConfig(num_agents=2)):
        super().__init__(config)
        self.num_agents = self.config.num_agents
        self.is_multiagent = True
        self.active = None

    def _obs(self):
        return [self._get_agents_obs(index) for index in range(self.num_agents)]

    def step(self, action: list):
        assert len(action) == self.config.num_agents
        rewards = []

        infos = [dict() for _ in range(self.num_agents)]

        dones = []
        for agent_idx in range(self.config.num_agents):
            agent_done = self.grid.move(agent_idx, action[agent_idx])
            infos[agent_idx]['is_active'] = self.active[agent_idx]

            if agent_done and self.active[agent_idx]:
                rewards.append(1.0)

            else:
                rewards.append(0.0)

            dones.append(agent_done)
            if agent_done:
                self.active[agent_idx] = False

        # if all(rewards):
        #     # multi-agent environments should auto-reset!
        #     obs = self.reset()
        # else:
        #     obs = self._obs()
        obs = self._obs()
        return obs, rewards, dones, infos

    def reset(self):
        self.grid: Grid = Grid.random_grid_generator(config=self.config)
        self.active = {agent_idx: True for agent_idx in range(self.config.num_agents)}
        return self._obs()


def main():
    env = gym.make('Pogema-v0', config=GridConfig(num_agents=2, size=8))
    env = AnimationMonitor(env=env)
    env.reset()

    done = [False, ...]
    while not all(done):
        obs, reward, done, info = env.step([env.action_space.sample() for _ in range(env.config.num_agents)])
        print(reward, done, info)
        # env.render()


if __name__ == '__main__':
    main()
