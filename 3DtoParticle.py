import numpy as np
from PIL import Image

_3dModelLocation = 'put it here'
texture_image = 'the texture of the 3d model'

# The size of the model compared to the minecarft world
# Requires testing to get used to how it affects the model
scale_factor =  2

def parse_ply_ascii(file_path):
    vertices = []
    tex_coords = []
    with open(file_path, encoding='utf-8') as file:
        header = True
        for line in file:
            if header:
                if line.startswith('end_header'):
                    header = False
            else:
                parts = line.split()
                if len(parts) >= 8:
                    vertices.append([float(parts[0]), float(parts[1]), float(parts[2])])
                    tex_coords.append([float(parts[6]), float(parts[7])])
    vertices = np.array(vertices)
    tex_coords = np.array(tex_coords)
    print(f"Number of vertices: {len(vertices)}")
    return vertices, tex_coords

def normalize_and_scale_vertices(vertices, scale):
    if vertices.size == 0:
        raise ValueError("Vertices array is empty.")
    min_coords = np.min(vertices, axis=0)
    normalized_vertices = (vertices - min_coords)
    scaled_vertices = normalized_vertices * scale
    return scaled_vertices

def sample_texture_color(texture_image, uv_coords):
    img = Image.open(texture_image)
    img = img.convert('RGB')
    width, height = img.size
    
    x = int(uv_coords[0] * width)
    y = int((1 - uv_coords[1]) * height)

    x = max(0, min(x, width - 1))
    y = max(0, min(y, height - 1))
    
    return img.getpixel((x, y))

def generate_particle_commands(vertices, tex_coords, texture_image, scale=1.0):
    commands = []
    for vertex, uv_coord in zip(vertices, tex_coords):
        x, y, z = vertex
        r, g, b = sample_texture_color(texture_image, uv_coord)
        r, g, b = [round(c / 255.0, 2) for c in (r, g, b)]
        x, y, z = [round(coord, 7) for coord in [x, y, z]]
        commands.append(f"particle minecraft:dust {r} {g} {b} {scale} ~{x} ~{y} ~{z} 0 0 0 0 1 force @a")
    return commands

vertices, tex_coords = parse_ply_ascii(_3dModelLocation)

scaled_vertices = normalize_and_scale_vertices(vertices, scale_factor)
commands = generate_particle_commands(scaled_vertices, tex_coords, texture_image, scale=1.0)

with open('commands.txt', 'w') as file:
    file.write('\n'.join(commands))

print("Particle commands have been saved")
