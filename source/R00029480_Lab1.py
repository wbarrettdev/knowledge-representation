from agents import *
from utils import Bool
import logging as log
import random
log.basicConfig(level=log.INFO, format="%(levelname)s: %(message)s")

class Floor(Environment):
    def __init__(self):
        super().__init__()
        self._dirty = {}
        self.LOCATIONS = ('A', 'B')

    def set_dirty(self, location, value: bool):
        key = tuple(location) if isinstance(location, (list, tuple)) else location
        self._dirty[key] = Bool(1 if value else 0)

    def mark_clean(self, location):
        self.set_dirty(location, False)

    def is_dirty_at(self, location) -> Bool:
        key = tuple(location) if isinstance(location, (list, tuple)) else location
        return self._dirty.get(key, Bool(0))

    def default_location(self, thing):
        start_location = random.choice(self.LOCATIONS)
        log.info(f"Agent spawns at {start_location}")
        return start_location

    def percept(self, agent):
        status = 'Dirty' if self.is_dirty_at(agent.location) else 'Clean'
        return agent.location, status

    def execute_action(self, agent, action):
        # The only available actions are Left, Right, and Suck.
        if action == 'Left':
            if agent.location == 'B':
                agent.location = 'A'
                log.info(f"Agent moved Left to {agent.location}")
        elif action == 'Right':
            if agent.location == 'A':
                agent.location = 'B'
                log.info(f"Agent moved Right to {agent.location}")
        elif action == 'Suck':
            self.mark_clean(agent.location)
            log.info(f"Agent Sucking {agent.location}")
        # Award performance: +1 for each clean square by time step.
        if not self.is_dirty_at('A'):
            agent.performance += 1
        if not self.is_dirty_at('B'):
            agent.performance += 1

class SimpleVacuumCleanerAgent(Agent):
    performance = 0

def agent_program(percept):
    location, status = percept
    if status == 'Dirty':
        return 'Suck'
    return 'Right' if location == 'A' else 'Left'

if __name__ == "__main__":
    env = Floor()
    env.set_dirty('A', random.choice((True, False)))
    env.set_dirty('B', random.choice((True, False)))
    log.info(f"Dirt: A[{env.is_dirty_at('A')}], B[{env.is_dirty_at('B')}]")

    agent = Agent(agent_program)
    env.add_thing(agent)

    log.info("Starting run...")
    env.run(steps=1000)
    log.info(f"Finished. Agent performance = {agent.performance}")
#======================================================================================================================
# Question 1) Show that the simple vacuum-cleaner agent function
#             described in Figure 3 is indeed rational under the
#             assumptions listed below.
#
# - The performance measure awards one point for each clean square at each time step, over a “lifetime” of 1000 time
#   steps.
# - The “geography” of the environment is known a priori Figure 3, but the dirt distribution and the initial
#   location of the agent are not. Clean squares stay clean and sucking cleans the current square. The
#   Left and Right actions move the agent left and right except when this would take the agent outside the
#   environment, in which case the agent remains where it is.
# - The only available actions are Left, Right, and Suck.
# - The agent correctly perceives its location and whether that location contains dirt.
#----------------------------------------------------------------------------------------------------------------------
# Answer 1)
# Rationality: "For each possible percept sequence, a rational agent
#                   should select an action that is expected to maximize its performance measure, given
#                   the evidence provided by the percept sequence and whatever built-in knowledge the
#                   agent has."
# What is rational at any given time depends on four things:
#   • The performance measure that defines the criterion of success.
#     - Our agent successfully uses a performance measure to define success.
#     - clean stays clean (static)
#     - sucking cleans dirt (deterministic)
#   • The agent’s prior knowledge of the environment.
#      - The agent uses its prior knowledge of the environment (it knows the geography) to determine the direction to go.
#   • The actions that the agent can perform.
#      - It has three actions; left,right and suck. Our agent successfully picks the correct action.
#   • The agent’s percept sequence to date.
#      - Our agent correctly perceives its location and whether that location contains dirt.
#
# Given the above, I believe the agent is rational.
# I wasn't sure that performing an action once all tiles were clean was rational (the agent can determine when all tiles are clean from history).
# This made me think the agent is not rational due to not using its history data to stop performing actions.
# But Rationality is making the best possible decision in the given circumstances.
# The vacuum doesn't have an idle action, and it must perform an action each of the 1000 time steps.
# Moving to the other location makes more sense than sucking dirt when a location is already clean.
# ======================================================================================================================


# ======================================================================================================================
# Question 2) Describe a rational agent function for the case in
#             which each movement costs one point. Does the
#             corresponding agent program require an internal state?
# ----------------------------------------------------------------------------------------------------------------------
# Answer 2) The introduction of point deduction is known as a cost function. The agent now needs two things.
# - An idle or stop action.
# - And it needs an internal state to store the history of actions.
# This internal state would be used to determine when to stop moving.
# ======================================================================================================================


# ======================================================================================================================
# Question 3) Discuss possible agent designs for the cases in which
#             clean squares can become dirty and the geography
#             of the environment is unknown. Does it make sense
#             for the agent to learn from its experience in these
#             cases? If so, what should it learn? If not, why not?
# ----------------------------------------------------------------------------------------------------------------------
# Answer 3)
# If clean squares become dirty again. Then the environment becomes dynamic. Suck would still clean, so it is still deterministic.
# However, the agent no longer knows the geography of the environment. This means it can't hold an internal state of when all tiles are clean.
# Without knowing when the env is clean or its geography, It would need to run indefinitely and in random directions.
# It can't really learn anything in this scenario.
# ======================================================================================================================