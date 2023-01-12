# This file MUST be configured in order for the code to run properly

# Make sure you put all your input images into an 'assets' folder. 
# Each layer (or category) of images must be put in a folder of its own.

# CONFIG is an array of objects where each object represents a layer
# THESE LAYERS MUST BE ORDERED.

# Each layer needs to specify the following
# 1. id: A number representing a particular layer
# 2. name: The name of the layer. Does not necessarily have to be the same as the directory name containing the layer images.
# 3. directory: The folder inside assets that contain traits for the particular layer
# 4. required: If the particular layer is required (True) or optional (False). The first layer must always be set to true.
# 5. rarity_weights: Denotes the rarity distribution of traits. It can take on three types of values.
#       - None: This makes all the traits defined in the layer equally rare (or common)
#       - "random": Assigns rarity weights at random. 
#       - array: An array of numbers where each number represents a weight. 
#                If required is True, this array must be equal to the number of images in the layer directory. The first number is  the weight of the first image (in alphabetical order) and so on...
#                If required is False, this array must be equal to one plus the number of images in the layer directory. The first number is the weight of having no image at all for this layer. The second number is the weight of the first image and so on...

# Be sure to check out the tutorial in the README for more details.                

CONFIG = [
    {
        'id': 1,
        'name': 'Kadcar',
        'directory': 'kadcars',
        'required': True,
        'rarity_weights': [70,30],
    },
    {
        'id': 2,
        'name': 'Rim',
        'directory': 'rims',
        'required': True,
        'rarity_weights': [30,15,25,10,20],
    },
    {
        'id': 3,
        'name': 'Spoiler',
        'directory': 'spoilers',
        'required': True,
        'rarity_weights':[70,30],
    },
    {
        'id': 4,
        'name': 'Trim',
        'directory': 'trims',
        'required': True,
        'rarity_weights': [40,60],
    },
    {
        'id': 5,
        'name': 'Color',
        'directory': 'colors',
        'required': True,
        'rarity_weights': [14,5,5,9,13,5,8,7,12,8,11,3],
    },
    {
        'id': 6,
        'name': 'Material',
        'directory': 'materials',
        'required': True,
        'rarity_weights': [34,15,20,31],
    },
    {
        'id': 7,
        'name': 'Background',
        'directory': 'bg_names',
        'required': True,
        'rarity_weights': [30,25,15,20,10],
    },
    {
        'id': 8,
        'name': 'Headlights',
        'directory': 'headlights',
        'required': True,
        'rarity_weights': [10,90],
    },
    {
        'id': 9,
        'name': 'Headlight_Panels',
        'directory': 'headlight_panels',
        'required': True,
        'rarity_weights': [25,75],
    }
]
