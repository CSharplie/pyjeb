variables = {
    "first_color": "red",
    "second_color" : "blue"
}

functions = {
    "function_x10": lambda x: int(x) * 10,
    "function_x100": lambda x: int(x) * 100,
}

controls = [
    {
        "name": "path",
        "type": "string"
    },
    {
        "name": "pattern",
        "type": "string",
        "default" : "*",
    },
    {
        "name": "colors",
        "type": "dict",
    },
    {
        "name": "colors.cold",
        "type": "string",
        "validset" : ["blue", "green"]
    },
    {
        "name": "colors.hot",
        "type": "string",
        "default" : "red",
        "validset" : ["red", "yellow"]
    },
    {
        "name": "phone",
        "type": "string",
        "default": "+33712345678",
        "regex": "[+]33[67]\\d{8}"
    },
    {
        "name": "count",
        "type": "integer",
        "default" : 0
    },
    {
        "name": "threshold",
        "type": "decimal",
        "default" : 0.90
    },
    {
        "name": "active",
        "type": "boolean",
        "default" : True
    },
    {
        "name": "options",
        "type": "dict",
        "default" : {}
    },
    {
        "name": "options.ignore",
        "type": "list",
        "default" : []
    }
]

controls_nested = [
    { "name": "vehicles", "type": "dict" },
    { "name": "vehicles.cars", "type": "list" },
    { "name": "vehicles.cars.color", "validset": ["red", "blue"] },
    { "name": "vehicles.cars.is_broken", "type": "boolean", "default": False },
    { "name": "vehicles.cars.buy_date" },
    { "name": "vehicles.cars.type", "default": "usual", "expressions": ["if color == 'red' return 'sportive'"] }
]

controls_deep_array = [
    { "name": "workspaces", "type": "dict" },
    { "name": "workspaces.name", "type": "string" },
    { "name": "workspaces.sources", "type": "list" },
    { "name": "workspaces.sources.hidden", "type": "boolean", "default": False },
    { "name": "workspaces.sources.name", "type": "string"},
    { "name": "workspaces.sources.files", "type": "list"},
]