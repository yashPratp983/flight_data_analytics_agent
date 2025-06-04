import dspy
from app.agents.planner import analytical_planner
from app.agents.combiner import code_combiner_agent
from app.agents.goal_refiner import goal_refiner_agent
import pandas as pd# This module takes only one input on initiation
class auto_analyst(dspy.Module):
    def __init__(self,agents,flight_bookings_path='Flight Bookings.csv', airline_mapping_path='Airline ID to Name.csv'):
# Defines the available agents, their inputs, and description
        self.agents = {}
        self.agent_inputs ={}
        self.agent_desc =[]
        i =0
        for a in agents:
            name = a.__pydantic_core_schema__['schema']['model_name']
# Using CoT prompting as from experience it helps generate better responses
            self.agents[name] = dspy.ChainOfThought(a)
            self.agent_inputs[name] ={x.strip() for x in str(agents[i].__pydantic_core_schema__['cls']).split('->')[0].split('(')[1].split(',')}
            self.agent_desc.append(str(a.__pydantic_core_schema__['cls']))
            i+=1
# Defining the planner, refine_goal & code combiner agents seperately
# as they don't generate the code & analysis they help in planning, 
# getting better goals & combine the code
        self.planner = dspy.ChainOfThought(analytical_planner)
        self.refine_goal = dspy.ChainOfThought(goal_refiner_agent)
        self.code_combiner_agent = dspy.ChainOfThought(code_combiner_agent)
# these two retrievers are defined using llama-index retrievers
# you can customize this depending on how you want your agents
        self.flight_bookings=pd.read_csv(flight_bookings_path)
        
    def forward(self, query):
# This dict is used to quickly pass arguments for agent inputs
        dict_ ={}
# retrieves the relevant context to the query
        dict_['dataset'] = self.flight_bookings
        dict_['goal']=query
        dict_['Agent_desc'] = str(self.agent_desc)
# output_dictionary that stores all agent outputs
        output_dict ={}
# this comes up with the plan
        plan = self.planner(goal =dict_['goal'], dataset=dict_['dataset'], Agent_desc=dict_['Agent_desc'] )
        output_dict['analytical_planner'] = plan
        plan_list =[]
        code_list =[]
# if the planner worked as intended it should give agents seperated by ->
        if '->' in plan.plan:
            plan_list = plan.plan.split('->')
# in case the goal is unclear, it sends it to refined goal agent
        else:
            refined_goal = self.refine_goal(dataset=dict_['dataset'], goal=dict_['goal'], Agent_desc= dict_['Agent_desc'])
            return self.forward(query=refined_goal)
# passes the goal and other inputs to all respective agents in the plan
        for p in plan_list:
            inputs = {x:dict_[x] for x in self.agent_inputs[p.strip()]}
            output_dict[p.strip()]=self.agents[p.strip()](**inputs)
# creates a list of all the generated code, to be combined as 1 script
            code_list.append(output_dict[p.strip()].code)
# Stores the last output
        output_dict['code_combiner_agent'] = self.code_combiner_agent(agent_code_list = str(code_list))
        
        return output_dict
