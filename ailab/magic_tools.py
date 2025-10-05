def magic_tool_1(input:int):
    return input ** 2

def magic_tool_2(input:int):
    return input + 2

magic_tools = [
    {
        "name":"magic_tool_1",
        "description":"take an integer as input and call a function called magic_tool_1",
        "parameters":{
            "type":"object",
            "properties":{
                "input":{
                    "type":"integer"
                }
            },
            "required":["input"]
        }

    },
    {
        "name":"magic_tool_2",
        "description":"take an integer as input and call a function called magic_tool_2",
        "parameters":{
            "type":"object",
            "properties":{
                "input":{
                    "type":"integer"
                }
            },
            "required":["input"]
        }

    }
]

