---
title: Space War RL #0: Series Introduction
published: false
description:
tags: reinforcementlearning,ai, pygame, spacewar
series: Space War RL Dev Blog
# cover_image: https://direct_url_to_image.jpg
# Use a ratio of 100:42 for best results.
# published_at: 2023-10-29 14:02 +0000
---

Machine learning is a field I always wanted to get into. I always thought I would need a masters or a PHD to get started; _Something I thought was out of my reach...until_ **recently**.  
This year I had the opportunity to get my hands dirty; I got involved with a group that specializes in machine learning. I worked on some Reinforcement Learning (RL) projects at work, but only scratched the surface due to limited funding. Regardless, this was the spark that I was missing! Since there is limited opportunity at work, _I must carve a path for myself on my own_.

This project will allow me to _express my creativity_, _dive deeper_, _discover new things_, and _most importantly have fun!_

## Inspiration

This project combines nostalgia with some of my interests: gaming, coding, and machine learning!

I remembered my dad showed me the 1985 Bill Seiler's version of [space War](http://www.1morecastle.com/2012/10/spacewar-dos/) on his IBM PC/AT as a child.

{% embed https://www.youtube.com/watch?v=cgG1rCx1DeA %}_You can play the emulator from your browser on [internet archive](https://archive.org/details/SPACEWAR_1020)_

I remembered the controls are hard for the human player, so I'm curious if Reinforcement Learning agents can play the game better.

First I will start building out the simulation/game until I have a minimal viable product (MVP) to start training the agents.

I will also recreate the original "AI" to measure baseline performance. I assume they are rules-based and have access to internal state. The left player was defensive and mostly used phasers. The right player was offensive and mostly used photon torpedoes.

My metrics of performance will be the game win rate. Once I get this going I will continue to make the simulation more complex and add more agents for Multi Agent Reinforcement Learning (MARL).

## Roadmap

_Crawl. Walk. Run_. Let's start simple and slowly work things up! My initial plan is to iterate on the simulation, iterate the agents, and rinse and repeat.

You can see what I'm working on with my [github project](https://github.com/users/e-dong/projects/3)

### Simulation v0

Some features will be omitted for simplicity in order to start working with RL sooner.

These features will be implemented in this first iteration:

- Basic movement with zero gravity physics
- Screen wrap-around
- Weapons (Photon torpedoes and Phasers)
- Energy management (balance shield and energy)

#### Baseline Agents

I will implement the defensive and offensive rule-based agents, denoted by `baseline_d` and `baseline_o` respectively. This will allow me to fix any bugs with the simulation prior to training the RL agents.

#### RL Agents

I will start with the classic Deep Q Network (DQN)[^1]</sup> using a continuous state space and discrete action space. I will be trying to implement this from scratch with the paper rather than copying code from a tutorial.

I will train the DQN agent against 3 agents to start:

- baseline defensive, denoted `DQN_d`
- baseline offensive, denoted `DQN_o`
- itself using [competitive self-play](https://openai.com/research/competitive-self-play), denoted `DQN_s`. The article mentioned the agents were initally trained with dense rewards to aid in exploration and then gradually replaced with sparse rewards when winning/losing the game. I will try using constant sparse rewards to see what happens first.

This will allow me to run my first experiment. I will compare the win rate between these pairs:

- `baseline_o` vs. `baseline_d`
- `DQN_d` vs. `baseline_d`
- `DQN_o` vs. `baseline_d`
- `DQN_s` vs. `baseline_d`
- `DQN_d` vs. `baseline_o`
- `DQN_o` vs. `baseline_o`
- `DQN_s` vs. `baseline_o`
- `DQN_o` vs. `DQN_d`
- `DQN_s` vs. `DQN_d`
- `DQN_s` vs. `DQN_o`

My initial hypothesis is the agents will overfit to the agent they were training against.
The agent they trained against will perform well during evaluation, but probably perform poorly when faced with different opponents. If I am right, I will need to train the DQN agents with a variety opponents in order for them to discover a generic strategy.

### Simulation v1

Implement the other features in Space war 1985.

- Gravity
- Planet
- Give Agent ability to warp via hyper space
- Give Agent ability to cloak

#### RL Agents

Rerun experiments and see how it impacts training and evaluation. I will also look into other algorithms like PPO and DDPG.

### Simulation v2

Once I have a good understanding of how the agents behave in a 1v1 setting, I will see what happens in team battles. I found this [OpenAI article](https://openai.com/research/emergent-tool-use) and paper[^2] fascinating because agents can learn to cooperative with each other in order to "outsmart" the other team. The other team can then learn a counter strategy. Both teams alternate in giving the other harder tasks. This feedback loop results in an evolutionary arms race where each team creates an implicit learning curriculum for each other. This training method allows agents to reach superhuman performance like with Dota 2[^3], Starcraft II[^4]. To learn more about OpenAI's Dota 2 research see this [article](https://openai.com/research/more-on-dota-2).

### Simulation v3

The final step is to see how to make the simulation more realistic and push the boundaries of RL to the limit!

Based on this roadmap, my initial posts in this series will be a software engineering effort to build the simulation and then RL research and tuning. More updates to come soon!

[^1]: Mnih, V., Kavukcuoglu, K., Silver, D., Graves, A., Antonoglou, I., Wierstra, D., & Riedmiller, M. "Playing Atari with Deep Reinforcement Learning" arXiv, 2013. Available: https://doi.org/10.48550/arXiv.1312.5602
[^2]: Baker, B., Kanitscheider, I., Markov, T., Wu, Y., Powell, G., McGrew, B., & Mordatch, I. "Emergent Tool Use From Multi-Agent Autocurricula" arXiv, 2020. Available: https://doi.org/10.48550/arXiv.1909.07528
[^3]: OpenAI, "Dota 2 with large scale deep reinforcement learning" arXiv, 2019, Available: https://doi.org/10.48550/arXiv.1912.06680
[^4]: Vinyals, O., Babuschkin, I., Chung, J., Mathieu, M., Jaderberg, M., et al. AlphaStar: Mastering the real-time strategy game StarCraft II. https://deepmind.com/blog/alphastar-mastering-real-time-strategy-game-starcraft-ii/, 2019.
