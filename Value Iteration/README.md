# **MDL Assignment 2 Report**

## **Team 83: Arushi Mittal (2019101120), Meghna Mishra (2019111030)**

### Task 1

#### **Trace File Results:**
    Number of Iterations: 115
    Step Cost: -5

##### ***Code Explanation***

The program generates a list of all possible states in a dictionary `state_set` for the game and iterates over them one by one. For each state, depending on position in the map and the state of the monster, the next possible actions and next possible states are generated, along with the expected utilities of all the actions. The best utility is selected and the corresponding action is chosen as the best action for defining the policy. The `state_set` dictionary also stores information about the best action and it's utility. The final policy is determined after repeating this process until the maximum absolute difference between expected utility values for consecutive iterations is less than or equal to the bellman error `delta`.

##### ***Interpretation of Results***

The program was able to converge to `3 decimal places` (`gamma = 0.001`) in `115 iterations`.

`Discounting Factor (Gamma)`: The closer the value of gamma is to `1`, the slower the iterations will be. Since the value of `gamma` is `0.999`, it is reasonable to expect that the policy chosen will focus on long-term goals. Since the value of the discounting factor determines how the the future reward is valued, a value close to `1` will wait for the reward if necessary, as opposed to taking the action that returns the greatest reward without considering future rewards.

`Step Cost`: The step cost was -5 which was relatively expensive compared to the reward and penalty. As a consequence, a significant portion of the actions - about `20%` - had to do with attacking the monster or getting materials for attacking the monster from a safe distance.

`Choice of Action`: The actions changed according to the state variables. Given the choice to go East, a lot of times this choice was not preferred, most prominently when the monster was in ready state. In these cases, if the monster chose to attack, `IJ` would suffer a penalty of `-40`, along with loss of all arrows, and an increase in the monster's health. Additionally, in the East position, `IJ` usually tended to attack the monster by hitting it with his blade, because the damage dealt was very high (`50`) and the probability was also highest in this region. Additionally, if the monster was in `Ready State`, `IJ` would always try to leave the Center and East positions because he is likely to get attacked here. When `IJ` had  materials, if he was present in the North position, he would tend to craft arrows, especially when he had very few arrows. This was exacerbated by the monster being in ready state, since crafting arrows is useful, and going anywhere else is dangerous. In case there were no materials, `IJ` would choose to stay due to the danger associated with both the future positions. However, when the monster was dormant, `IJ` would choose to go down when he had no materials. Similarly, `IJ` would prefer to gather in the South position if he didn't have any materials, especially when the monster was ready. However, if the monster was dormant, he would move up most of the time. In the East position, `IJ` gets very aggressive, especially when the monster is dormant. He prefers to hit more often due to the greater quantity of damage dealt, however depending on the availability of arrows, he chooses to shoot as well due to high probability. In essence, `IJ` is guided by long term rewards as opposed to short term benefits because he chooses to take actions that would help him defeat the monster optimally in the long run. 

`Rate of Convergence`: The policy was able to converge relatively fast considering how large the discount factor was and how small the bellman error `delta` was. In 115 iterations, the values went from the order $10^2$ to $10^0$ within $<10$ iterations, following which the difference between values decreased further to $10^{-1}$ and so on until the required difference was achieved. The greatest discrepancy between utilities was calculated each time for two consecutive iterations, and once this value was surpassed by the bellman error `delta`, the value was stored and the utilities had converged.

`Policy Observations`: Overall, the policy devised was quite effective because it was geared towards maximizing the overall rewards in the long term as opposed to taking the action with the highest expected utility for the short term, which may or may not have led to greater losses in the future. Consequently, actions such as gathering materials and crafting arrows, which have no apparent utility in the short term, are still undertaken in order to ensure that these actions lead to better results in the longer term. For exanple, crafting arrows will enable `IJ` to shoot the monster with greater probability and quite possibly defeat him, thereby fulfilling the purpose of the game. This is mainly due to the high `gamma` value and low `delta` value. 

  
#### **Simulations**
  
In each simulation, `IJ` begins at a given start state. Then, using the last iteration of the trace file created, we decide which is the best action to take from a given position. Using the probabilities given and the action decided, we find out what the next state is, and then the best action from there is found out. This continues until the monster has zero health and `IJ` wins the game. Probabilities for the success of the next state, the state of the monster, and the possibility of an attack are generated randomly to simulate the game.

##### ***Simulation 1***

    ('W', 0, 0, 'D', 100): RIGHT
    ('C', 0, 0, 'D', 100): RIGHT
    ('E', 0, 0, 'D', 100): HIT
    ('E', 0, 0, 'R',  50): HIT
    ('E', 0, 0, 'D',  75): HIT
    ('E', 0, 0, 'D',  50): HIT
    ('E', 0, 0, 'D',   0): NONE

The first two actions lead `IJ` to the East square because the monster is still dormant and hitting it from the east square would deal significant damage to its health, especially because `IJ`'s accuracy increases by a lot, so the expected utility is quite high. Then, `IJ` hits the monster, reducing its health by `50` but the monster now reaches a ready state. `IJ` then attempts to again hit the monster, which if successful would have ended the game but the monster now attacks. This leads to the monster regaining 25 health and becoming dormant again, and the hit action fails. `IJ` then attempts to hit two more times, both of which are successful and the monster dies.


##### ***Simulation 2***
    ('C', 2, 0, 'R', 100): UP
    ('N', 2, 0, 'R', 100): CRAFT
    ('N', 1, 1, 'D', 100): CRAFT
    ('N', 0, 2, 'D', 100): DOWN
    ('C', 0, 2, 'D', 100): RIGHT
    ('E', 0, 2, 'R', 100): HIT
    ('E', 0, 0, 'D', 100): HIT
    ('E', 0, 0, 'D',  50): HIT
    ('E', 0, 0, 'D',   0): NONE

`IJ` starts off with `2` materials in the center, and the monster in ready state capable of attacking `IJ`, hence the action chosen is to go up to North square. In the North square, first IJ uses `1` material and gets 1 arrow. During this action, the monster has attacked and gone to dormant state but this attack has not affected `IJ`. `IJ` then uses 1 material and again gets `1` arrow. He now has `0` materials and 2 arrows, and since the monster is still dormant, the action chosen is to go down to the center and then to the right. Now, `IJ` is in the East square and the monster is ready. `IJ` tries to hit but the monster attacks and the hit fails, and he loses all his arrows as well. However, since the monster had health `100` already, its health cannot increase any more. Now the monster is in dormant state after attacking. `IJ` hits the monster twice consecutively and both the hits are successful, so the monster dies.


### Task 2

This task involved changing various parameters which had a direct impact on the policy of the game. As a result, the number of iterations required for convergence, expected utilities and best course of action differed quite often.

#### Task 2.1

    Taking the Left action from the East position would transfer `IJ` to the West position as opposed to centre.

This change highly increased the number of times that the left action was taken from East position. When the monster was in ready state, and `IJ` was in the East position, his probability of going to the West position was increased. This contrasts with his previous tendency to attack when he was in a similar position due to guaranteed safety in the West. Since earlier `IJ` would rarely go to Centre, especially when he had no way of attacking the monster, and Centre was equally unsafe, he had no reason to go Left. However, with an increased possibility of safety in the West position, and the ability to wait passively or shoot from a safe position ensured that `IJ` would be safe from incurring the `-40` penalty, and might be able to inflict damage on the monster. Since decreasing the monster's health would bring `IJ` closer to achieving the objective of the game, which is to kill the monster, this change has also decreased the number of iterations required for convergence.

This change increased the number of iterations for convergence to 129 due to the increased benefits provided by this change, as explained above.

#### Task 2.2
    The step cost for the Stay action would be changed from -5 to 0

As explained in previous sections, the step cost is relatively high when compared to the rewards and penalties. As a result, every movement requires some form of action, because it would be 'wasteful' for `IJ` to be passive if he has the choice to take initiative and do something with high total utility as opposed to none, or even negative utlity. However, all of this changes when the step cost for the stay action is reduced to a value of zero. This is significant for two reasons - firstly, because the stay action is very different from other actions in terms of its utility both in the short term and long term, and the fact that the utility of all other actions remains the same. Since essentially the cost of this action is `0`, the policy changes towards a more passive approach. As a result, if the monster is in the ready state for an indefinite amount of time, and `IJ` is in a relatively safe position, the best and safest approach would always be to stay in the same position because there is no cost to it. Moreover, this would result in a tendency to wait for a better opportunity for an infinite amount of time. Additionally, if this reduction in step cost was applied to other actions such as shoot or hit, the result would have been the opposite - a very aggressive approach that would result in moves that would attempt to finish the game as soon as possible. Additionally, the main reason this change has led to a passive policy is because the cost is now 0, so in effect, it makes virtually no difference provided `IJ` is in a safe position. In the event that he is not in a safe position, he would gravitate towards the nearest safe position and wait indefinitely.

This change decreased the number of iterations for convergence to 104, because it was relatively easier to find the ideal state since in so many cases, it was to stay in the same position, particularly for the West position.

#### Task 2.3
    The discounting factor would decrease from 0.999 to 0.25

The discounting factor `gamma` is used to determine how much we value long term rewards as opposed to instant gratification, and which one delivers the maximum utility. Essentially, a `gamma` value closer to `1` would attempt to yield rewards over, theoretically, an infinite time span. On the other hand, a lower `gamma` value would attempt to yield rewards in a much shorter time frame, such as the next few steps rather than waiting and finding the best overall course of action. Since over here, we are decreasing the `gamma` value from 0.999 to 0.25, which is reducing it by almost `75%`, there is a huge difference now in priorities with respect to the time over which utility is accumulated. Due to this change, the new `gamma` values would ensure that the action that produces the best reward in the short term would be favored over an action that is more utilitarian in the longer term. This is not necessarily the best policy for this game, however the assessment may vary depending on different contexts where in some cases short term rewards may be the goal. Since this game is complicated, and contains actions that may not have any utility in the short term but may turn out to be enormously useful in the longer term, this change in `gamma` may discount these actions in favor of other actions that may not lead to the same reward. Therefore, the previous policy is better.

This change decreased the number of iterations for convergence to 8, which is an enormous reduction. This can be attributed to the fact that a `gamma` value close to `0` would attempt to gain rewards in a short term, leading to a very short amount of time for convergence since in each case, the best course of action is already evident.
