
from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessageState, END, START
from langgraph.prebuilt import Toolnode, tools_condition
# from tools.weather_info_tool import WeatherInfoTool
# from tool.place_search_tool import PlaceSearchTool
# from tool.expense_calculator_tool import CalculatorTool
# from tool.currency_conversion_tool import CurrencyConverterTool

class GraphBuilder():
    def __init__(self):
        self.tools = [
            #WeatherInfoTool(),
            #PlaceSearchTool(),
            #CalculatorTool(),
            #CurrencyConverterTool()
        ]
        self.system_prompt = SYSTEM_PROMPT

    def agent_function(self,state: MessagesState):
        """Main agent function"""
        user_question = state["messages"]
        input_question = state["messages"]
        response = self.llm_with_tools.invoke(input_question)
        return {"messages": [response]}
    def build_graph(self):
        graph_builder = StateGraph(MessageState)
        graph_builder.add_node("agent",self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools = self.tools))
        graph_builder.add_edge(START,"agent")
        graph_builder.add_conditional_edges("agent",tools_condition)
        graph_builder.add_edge("tools","agent")
        graph_builder.add_edge("agent",END)
        self.graph = graph_builder.compile()
        return self.graph

    def __call__(self):
        pass