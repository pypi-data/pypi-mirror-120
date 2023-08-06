# Pogema environment

## Installation 

Just install from PyPI:

```pip install pogema```

## Using Example

```python
import gym
from pogema.grid_config import GridConfig

env = gym.make('Pogema-v0', config=GridConfig(num_agents=2, size=8))
obs = env.reset()

done = [False, ...]
while not all(done):
    obs, reward, done, info = env.step([env.action_space.sample() for _ in range(env.config.num_agents)])
    env.render()
env.reset()
```