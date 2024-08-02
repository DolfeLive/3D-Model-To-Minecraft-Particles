import numpy as np
from PIL import Image

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
                if len(parts) >= 8:  # Ensure there are x, y, z, s, t values
                    vertices.append([float(parts[0]), float(parts[1]), float(parts[2])])
                    tex_coords.append([float(parts[6]), float(parts[7])])  # Assuming s, t are the 7th and 8th columns
    vertices = np.array(vertices)
    tex_coords = np.array(tex_coords)
    print(f"Number of vertices: {len(vertices)}")  # Debugging line
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
    
    # Convert UV coordinates to pixel coordinates
    x = int(uv_coords[0] * width)
    y = int((1 - uv_coords[1]) * height)  # Invert Y axis for image coordinates

    # Clamp coordinates to image size
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

# Replace 'path/to/your/model_ascii.ply' with the actual path to your ASCII PLY file
# Replace 'path/to/your/texture.png' with the path to your texture image
vertices, tex_coords = parse_ply_ascii('v1.ply')
texture_image = 'v1.png'

# Define the scale factor: 1 Blender meter = 0.01 Minecraft blocks
scale_factor =  2

# Normalize and scale the vertices
scaled_vertices = normalize_and_scale_vertices(vertices, scale_factor)

# Generate particle commands with the scaled vertices and sampled colors
commands = generate_particle_commands(scaled_vertices, tex_coords, texture_image, scale=1.0)

# Save the commands to a text file
with open('commands.txt', 'w') as file:
    file.write('\n'.join(commands))

print("Particle commands have been saved to commands.txt")
