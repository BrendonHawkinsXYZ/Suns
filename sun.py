import numpy as np
from PIL import Image, ImageFilter, ImageDraw
import random
from datetime import datetime

def generate_organic_glowing_circles(image_size=(1024, 1024), 
                                     min_layers=3, max_layers=7, 
                                     blur_range=(20, 80),
                                     color_variation=True):
    """
    Generates glowing, organic layered circles with randomized colors, offsets, and density variations.
    """
    # Initialize base image
    img = Image.new('RGB', image_size, color='black')
    width, height = img.size
    center = (width // 2, height // 2)
    
    # Randomize the number of layers
    num_layers = random.randint(min_layers, max_layers)
    
    for _ in range(num_layers):
        # Create a new layer
        layer = Image.new('RGB', image_size, color='black')
        mask = Image.new('L', image_size, color=0)
        draw = ImageDraw.Draw(mask)
        
        # Randomized parameters
        radius = random.randint(width // 8, width // 2)
        blur_radius = random.randint(*blur_range)
        alpha = random.randint(100, 255)  # Opacity
        
        # Random offsets for layering to avoid symmetry
        offset_x = random.randint(-50, 50)
        offset_y = random.randint(-50, 50)
        layer_center = (center[0] + offset_x, center[1] + offset_y)
        
        # Generate random color with optional gradient variation
        if color_variation:
            color = (
                random.randint(0, 255),  # Red
                random.randint(0, 255),  # Green
                random.randint(0, 255)   # Blue
            )
        else:
            color = (255, 255, 255)  # Default white color
        
        # Draw radial gradient with varying opacity and densities
        for r in range(radius, 0, -1):
            alpha_step = int(alpha * (r / radius))
            draw.ellipse(
                (layer_center[0] - r, layer_center[1] - r, 
                 layer_center[0] + r, layer_center[1] + r),
                fill=alpha_step
            )
        
        # Apply transparency mask and Gaussian blur for softness
        layer.paste(color, (0, 0), mask.filter(ImageFilter.GaussianBlur(blur_radius)))
        
        # Blend with base image, using alpha for more dynamic layering
        img = Image.blend(img, layer, alpha=0.5)
    
    # Apply additional blur for global softness
    img = img.filter(ImageFilter.GaussianBlur(15))
    return img

# Generate and save image with timestamped filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"organic_glowing_circles_{timestamp}.png"

image = generate_organic_glowing_circles(image_size=(1024, 1024))
image.save(filename)
image.show()

filename  # Return the filename for download reference
