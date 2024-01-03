import os
import json
from PIL import Image
import random

# Define the layers and their corresponding directories
layers = {
    'tops': 'frog-layers/tops',
    'bottoms': 'frog-layers/bottoms',
    'flies': 'frog-layers/flies',
    'pads': 'frog-layers/pads',
    'flowers': 'frog-layers/flowers',
    'frogs': {
        'secondary': 'frog-layers/frogs/secondary',
        'primary': 'frog-layers/frogs/primary',
        'tongue': 'frog-layers/frogs/tongue',
        'eyes': 'frog-layers/frogs/eyes',
        'outlines': 'frog-layers/frogs/outlines'
    }
}

# Function to get a random image from a directory
def get_random_image(directory, rarity=None):
    files = os.listdir(directory)
    if 'rare.png' in files:
        # If the directory contains a rare image, return that 1% of the time
        if random.random() < 0.01:
            return Image.open(os.path.join(directory, 'rare.png'))
        else:
            # Exclude 'rare.png' from the list of files for the general selection
            files.remove('rare.png')
    return Image.open(os.path.join(directory, random.choice(files)))

# Function to merge images
def merge_images(images):
    result = Image.new('RGBA', images[0].size)
    for img in images:
        result.paste(img, (0, 0), img)
    return result

# Keep track of the combinations that have been used
used_combinations = set()

# Generate the NFTs
for i in range(100):  # Change this to generate the number of NFTs you want
    while True:
        images = []
        metadata = {}
        # Iterate over the layers in the correct order
        for layer in ['tops', 'bottoms', 'flies', 'pads', 'flowers', 'frogs']:
            if layer == 'frogs':
                # Iterate over the sub-layers of frogs
                for sub_layer in ['secondary', 'primary', 'tongue', 'eyes', 'outlines']:
                    images.append(get_random_image(layers['frogs'][sub_layer], 2 if sub_layer in ['outlines', 'eyes'] else None))
                    metadata[sub_layer] = images[-1].filename.split('/')[-1].split('.')[0]                
            else:
                images.append(get_random_image(layers[layer], 2 if layer == 'flies' else None))
                metadata[layer] = images[-1].filename.split('/')[-1].split('.')[0]
        
        # Convert the metadata to a frozenset so it can be added to a set
        metadata_set = frozenset(metadata.items())
        
        # If the combination has not been used before, break the loop
        if metadata_set not in used_combinations:
            used_combinations.add(metadata_set)
            break
    
    final_image = merge_images(images)
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    final_image.save(os.path.join(output_dir, f'frog-{i}.png'))
    with open(os.path.join(output_dir, f'frog-{i}.json'), 'w') as f:
        f.write(str(metadata))
