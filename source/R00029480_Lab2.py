# ======================================================================================
# 2) Specify a state diagram that realizes the above solution
# ======================================================================================
# River Crossing – State Diagram (Comment-Only)
# A = Left bank, B = Right bank
# Items: Farmer, Fox, Chicken, Feed
#
# States:
#   S1: A[Chicken, Farmer, Feed, Fox] | B[]
#   S2: A[Feed, Fox]                  | B[Chicken, Farmer]
#   S3: A[Farmer, Feed, Fox]          | B[Chicken]
#   S4: A[Feed]                       | B[Chicken, Farmer, Fox]
#   S5: A[Chicken, Farmer, Feed]      | B[Fox]
#   S6: A[Chicken]                    | B[Farmer, Feed, Fox]
#   S7: A[Chicken, Farmer]            | B[Feed, Fox]
#   S8: A[]                           | B[Chicken, Farmer, Feed, Fox]
#
# ======================================================================================

# ======================================================================================
# 3) Derive the list of percepts that would be experienced by a farmer agent to include location, chicken, feed and fox.
# ======================================================================================
#   - Farmers location
#   - Chicken location
#   - Feed location
#   - Fox location
#
# ======================================================================================

# ======================================================================================
# 4) Define the appropriate actions needed for solving the problem.
# ======================================================================================
# Actions:
#   S1 -> S2 : Take Chicken across
#   S2 -> S3 : Return alone
#   S3 -> S4 : Take Fox across
#   S4 -> S5 : Bring Chicken back
#   S5 -> S6 : Take Feed across
#   S6 -> S7 : Return alone
#   S7 -> S8 : Take Chicken across
# ======================================================================================

# ======================================================================================
# 4) Generate the percept sequence necessary map the appropriate actions for the problem to be solved
# ======================================================================================
# Farmer_location, Chicken_location, Feed_location, Fox_location
#   S1: [A,A,A,A] -> Take Chicken across
#   S2: [B,B,A,A] -> Return alone
#   S3: [A,B,A,A] -> Take Fox across
#   S4: [B,B,A,B] -> Bring Chicken back
#   S5: [A,A,A,B] -> Take Feed across
#   S6: [B,A,B,B] -> Return alone
#   S7: [A,A,B,B] -> Take Chicken across
#   S7: [B,B,B,B] -> noop
# ======================================================================================

from agents import *
import logging as log
log.basicConfig(level=log.INFO, format="%(levelname)s: %(message)s")

class RiverCrossingEnvironment(Environment):

    def __init__(self):
        super().__init__()
        # Location array: [Farmer, Chicken, Feed, Fox]
        self.status = ['A','A','A','A']

    def thing_classes(self):
        return [TableDrivenFarmerAgent]

    def percept(self, agent):
        farmer_location = self.status[0]
        chicken_location = self.status[1]
        feed_location = self.status[2]
        fox_location = self.status[3]
        return farmer_location, chicken_location, feed_location, fox_location

    def execute_action(self, agent, action):
        if action == 'Take Chicken across':
            self.status[0] = 'B'
            self.status[1] = 'B'
        elif action == 'Return alone':
            self.status[0] = 'A'
        elif action == 'Take Fox across':
            self.status[0] = 'B'
            self.status[3] = 'B'
        elif action == 'Bring Chicken back':
            self.status[0] = 'A'
            self.status[1] = 'A'
        elif action == 'Take Feed across':
            self.status[0] = 'B'
            self.status[2] = 'B'
        elif action is None:
            action = 'Farmer Relaxing'

        log.info(f"{action} - {self.status}")


def TableDrivenFarmerAgent():
    s1 = ('A', 'A', 'A', 'A')
    s2 = ('B', 'B', 'A', 'A')
    s3 = ('A', 'B', 'A', 'A')
    s4 = ('B', 'B', 'A', 'B')
    s5 = ('A', 'A', 'A', 'B')
    s6 = ('B', 'A', 'B', 'B')
    s7 = ('A', 'A', 'B', 'B')
    s8 = ('B', 'B', 'B', 'B')

    table = {
        (s1,): 'Take Chicken across',
        (s1, s2): 'Return alone',
        (s1, s2, s3): 'Take Fox across',
        (s1, s2, s3, s4): 'Bring Chicken back',
        (s1, s2, s3, s4, s5): 'Take Feed across',
        (s1, s2, s3, s4, s5, s6): 'Return alone',
        (s1, s2, s3, s4, s5, s6, s7): 'Take Chicken across'
    }

    return Agent(TableDrivenAgentProgram(table))

if __name__ == "__main__":
    agent = TableDrivenFarmerAgent()
    environment = RiverCrossingEnvironment()
    environment.add_thing(agent)
    environment.run(steps=10)
    assert environment.status == ['B','B','B','B']
