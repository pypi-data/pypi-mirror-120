

from copy import deepcopy
import pandas as pd
import numpy as np
import itertools

class Environment:

    def __init__(self,agents):

        if isinstance(agents,list):
            self._agents = {agent.id:agent for agent in agents}
        else:
            self._agents = agents

    @property
    def agents(self):
        return list(self._agents.values())

    @property
    def ids(self):
        return iter(deepcopy(list(self._agents.keys())))
    

    def __iter__(self):
        return iter(self._agents.values())


    def __getitem__(self,key):
        return self.get(key)


    def loc(self,key):
        return self._agents.get(key)

    def get(self,key,as_array = True):
        if as_array:
            return np.array([x[key] for x in self.agents])
        else:
            series = {x.id:x[key] for x in self.agents}
            return pd.Series(series)

    def to_df(self):
        agents = [x.to_dict() for x in self.agents]
        return pd.DataFrame(agents).set_index("id")

    def inverse_loc(self,key):
        for agent in self:
            if agent.id != key and agent.alive:
                yield agent

    def remove(self,key):
        self._agents.pop(key)


    def destroy(self):
        for _id in self.ids:
            agent = self.loc(_id)
            if agent.destroyed:
                self.remove(_id)


    def step(self):
        for agent in self.agents:

            # Equivalent to agent?
            if agent.alive:
                agent.step(self)

        self.destroy()


    def interactions(self):
        combinations = itertools.combinations(self.ids,2)
        interactions = []
        for agent1,agent2 in combinations:
            agent1,agent2 = self.loc(agent1),self.loc(agent2)
            inter_comb,interaction = agent1.interacts_with(agent2)
            if inter_comb:
                interactions.append((agent1,agent2,interaction))
        return interactions
