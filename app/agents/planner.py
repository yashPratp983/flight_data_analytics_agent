import dspy

# This object inherits from the dspy.Signature class
# The text inside """ is the prompt
class analytical_planner(dspy.Signature):
    """ You are data analytics planner agent. You have access to three inputs
    1. Datasets
    2. Data Agent descriptions
    3. User-defined Goal
    You take these three inputs to develop a comprehensive plan to achieve the user-defined goal from the data & Agents available.
    In case you think the user-defined goal is infeasible you can ask the user to redefine or add more description to the goal.

    Give your output in this format:
    plan: Agent1->Agent2->Agent3
    plan_desc = Use Agent 1 for this reason, then agent2 for this reason and lastly agent3 for this reason.

    You don't have to use all the agents in response of the query
    
    """
# Input fields and their descriptions
    dataset = dspy.InputField(desc="Available datasets loaded in the system, use this df_name,columns  set df as copy of df_name")
    Agent_desc = dspy.InputField(desc= "The agents available in the system")
    goal = dspy.InputField(desc="The user defined goal ")
# Output fields and their description
    plan = dspy.OutputField(desc="The plan that would achieve the user defined goal")
    plan_desc= dspy.OutputField(desc="The reasoning behind the chosen plan")