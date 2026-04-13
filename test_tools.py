#### Rupee Conversation Tool ########

from langchain_core.tools import tool,InjectedToolArg
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
import requests
from typing import Annotated

@tool
def getConversationRatio(BaseCurrency: str,TargetCurrency: str) -> float:
    """Function will fetch only fetch realtime conversation rate between base currency and target currency"""
    url = f'https://v6.exchangerate-api.com/v6/1412473e690df8a142e5bd27/pair/{BaseCurrency}/{TargetCurrency}'
    response = requests.get(url).json()
    conversation_rate = response.get("conversion_rate")
    print(f"Conversation rate between {BaseCurrency} and {TargetCurrency} is {conversation_rate}")
    return conversation_rate

@tool
def convert(conversation_rate: Annotated[float,InjectedToolArg], base_currency_value: float) -> float:
    """Given real time conversation rate , this function will calculate currency value from given base currency value"""

    return conversation_rate * base_currency_value

llm = ChatOpenAI()
llm_with_tools = llm.bind_tools([getConversationRatio,convert])
print(llm_with_tools)

query = HumanMessage("what is the the current conversation rate between USD and INR. Based on conversation rate convert 80 USD to INR")
messages = []
messages.append(query)
print(messages)

ai_result = llm_with_tools.invoke(messages)
messages.append(ai_result)
print(messages)
print(ai_result.tool_calls)

for tool_call in ai_result.tool_calls:
    if tool_call.get("name") == "getConversationRatio":
        response1 = getConversationRatio.invoke(tool_call)
        messages.append(response1)
        currency_conv_rate = response1.content
        print(currency_conv_rate)
    if tool_call.get("name") == "convert":
        tool_call.get("args")["conversation_rate"] = currency_conv_rate
        print(tool_call)
        response2 = convert.invoke(tool_call)
        messages.append(response2)

final_llm_response = llm.invoke(messages)
print(final_llm_response)
print(final_llm_response.content)

# #######ToolBinding######

# from langchain_openai import ChatOpenAI
# from langchain.tools import tool
# from langchain_core.messages import HumanMessage

# @tool
# def multiply(a: int , b: int) -> int:
#     "Function will provide product of 2 provided numbers"
#     return a * b

# result = multiply.invoke({"a":10 ,"b" : 10})
# print(result)

# llm = ChatOpenAI()

# llm_with_tools = llm.bind_tools([multiply])
# messages = []
# query = HumanMessage("What is a product of 10 & 10")
# messages.append([query])
# result = llm_with_tools.invoke(query)
# messages.append(result.tool_calls[0])
# tool_call = multiply.invoke(result.tool_calls[0])
# messages.append(tool_call)
# final_result = llm.invoke(messages)
# print(final_result.content)



# ###########ToolKit#################

# from langchain.tools import tool


# @tool
# def add(a:int,b:int) -> int:
#     return a + b

# @tool
# def multiply(a:int , b:int) -> int:
#     return a * b

# class MathtoolKit():
#     def get_tools(self):
#         return [add,multiply]
    
# mathtool = MathtoolKit()
# tools = mathtool.get_tools()

# for tool in tools:
#     print(tool.name)
#     print(tool.description)
#     print(tool.args)
    


# ##############BaseTool###########
# from langchain.tools import BaseTool
# from typing import Type
# from pydantic import BaseModel, Field

# class MultiplyInput(BaseModel):
#     a: int = Field(required= True, description="first number to add")
#     b: int = Field(required=True, description="second number to add")
    
# class MultiplyTool(BaseTool):
#     name: str = "Multiply"
#     description: str = "get multiply of 2 numbers"
    
#     args_schema: Type[BaseModel] = MultiplyInput
    
#     def _run(self, a:int ,b:int)->int:
#         return a*b
    

# multiply_tools = MultiplyTool()

# result = multiply_tools.invoke({"a":10,"b":10})

# print(result)


########StructuredTool#############

# from langchain.tools import StructuredTool
# from pydantic import BaseModel,Field

# class MultiplyInput(BaseModel):
#     a: int = Field(required=True,description="First number to add")
#     b: int = Field(required=True,description="Second number to add")

# def multiply_func(a:int , b:int) -> int:
#     return a*b

# multiply_model = StructuredTool.from_function(func=multiply_func,description="Multiply two numbers",args_schema=MultiplyInput,name="multiply")

# result = multiply_model.invoke({"a":5,"b":10})

# print(result)