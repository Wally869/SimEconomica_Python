RECIPES_RAW = {
    0: {
        "Name": "Harvest Wheat",
        "JobsRequired": [0],
        "Inputs": [],
        "Outputs": [[0, 2]]  # (elementID, quantity)
    },
    1: {
        "Name": "Bake Bread",
        "JobsRequired": [1],
        "Inputs": [[0, 1]],  # (elementID, quantity)
        "Outputs": [[1, 1]]  
    },
    2: {
        "Name": "Cut Oak",
        "JobsRequired": [2],
        "Inputs": [],  # (elementID, quantity)
        "Outputs": [[2, 1]]  
    },
    3: {
        "Name": "Craft Oak Cabinet",
        "JobsRequired": [3],
        "Inputs": [[2, 2]],  # (elementID, quantity)
        "Outputs": [[3, 1]]  
    }
}