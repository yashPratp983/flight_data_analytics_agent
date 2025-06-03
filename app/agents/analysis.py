import dspy
# I define analysis agents as those agents that are in the middle-layer
# they produce code for a specialised data analysis task
class preprocessing_agent(dspy.Signature):
    """ You are a data pre-processing agent, your job is to take a user-defined goal and available dataset,
    to build an exploratory analytics pipeline. You do this by outputing the required Python code. 
    You will only use numpy and pandas, to perform pre-processing and introductory analysis

    """
    dataset = dspy.InputField(desc="Available datasets loaded in the system, use this df_name,columns  set df as copy of df_name")
    goal = dspy.InputField(desc="The user defined goal ")
    commentary = dspy.OutputField(desc="The comments about what analysis is being performed")
    code = dspy.OutputField(desc ="The code that does the data preprocessing and introductory analysis")

class statistical_analytics_agent(dspy.Signature):
    """ You are a statistical analytics agent. 
    Your task is to take a dataset and a user-defined goal, and output 
    Python code that performs the appropriate statistical analysis to achieve that goal.
    You should use the Python statsmodel library"""
    dataset = dspy.InputField(desc="Available datasets loaded in the system, use this df_name,columns  set df as copy of df_name")
    goal = dspy.InputField(desc="The user defined goal for the analysis to be performed")
    commentary = dspy.OutputField(desc="The comments about what analysis is being performed")
    code = dspy.OutputField(desc ="The code that does the statistical analysis using statsmodel")

class sk_learn_agent(dspy.Signature):
# Prompt
    """You are a machine learning agent. 
    Your task is to take a dataset and a user-defined goal, and output Python code that performs the appropriate machine learning analysis to achieve that goal. 
    You should use the scikit-learn library."""
# Input Fields
    dataset = dspy.InputField(desc="Available datasets loaded in the system, use this df_name,columns. set df as copy of df_name")
    goal = dspy.InputField(desc="The user defined goal ")
# Output Fields
    commentary = dspy.OutputField(desc="The comments about what analysis is being performed")
    code = dspy.OutputField(desc ="The code that does the Exploratory data analysis")

## I worked on the data-viz agent and already optimized using DSPy.
## The only big difference is that this agents takes another input of styling index
