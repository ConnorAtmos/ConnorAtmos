import os, imageio, math, glob, contextlib
from PIL import Image, ImageDraw, ImageFont

width = 1920
ratio = "16:3"

# Action images are the number of images that will be used during the animation
action_images = 10

# Pause time is the number of images after the animation is complete that the text will remain on the screen
pause_time = 15

# Number of images that will be used for the blinking effect after it is done with one animation cycle
blinking_images = 5

# Every xth frame will have the indicator
indicator_slowing = 3

# Output path
output_path = "experience.gif"

# This is the dictionary that will be used to create the animation.
# You can set the dict values to None if you don't want to include image folder path
data_dict = {"Coding Languages": "images/languages",
             "IDEs and Software": "images/ides",
             "Operating Systems": "images/operating_systems",
             "Additional Experience": "images/additional_experience",
             }

# ================== DO NOT EDIT BELOW THIS LINE ================== #

# Calculate height based on ratio
height = int(width / int(ratio.split(":")[0]) * int(ratio.split(":")[1]))

# This is for the total width of the image icons
established_total_width = width * 0.9
max_height = height * 0.2
buffer_between_images = width * 0.05


def draw_icons(img, icon_folder, height, width, buffer_between_images, established_total_width, step=0.0):
    # Get all images from languages folder
    languages = os.listdir(icon_folder)

    # Calculate width of each image
    image_width = (established_total_width - (buffer_between_images * (len(languages) - 1))) / len(languages)

    if image_width > max_height:
        image_width = max_height
        image_height = max_height
        established_total_width = image_width * len(languages) + buffer_between_images * (len(languages) - 1)
    else:
        image_height = image_width

    for i in range(len(languages)):
        # Get image
        language_image = Image.open(os.path.join(icon_folder, languages[i]))

        # Resize image
        language_image = language_image.resize((int(image_width), int(image_height)))

        # X Position
        x = int((image_width + buffer_between_images) * i + (width - established_total_width) / 2)

        # Y Position
        y = int(height - image_height - height * 0.05) + int(step * height / 100)

        # Paste image
        img.paste(language_image, (x, y))

    return img


def draw_animation(text, icon_folder) -> list:
    total_images = action_images + pause_time

    # Set font to a 9 pin dot matrix font
    font_size = int(height / 3.5)
    font = ImageFont.truetype("ninepin.ttf", font_size)

    tick = True
    images = []
    for k in range(total_images):

        if k < action_images:
            i = k
        else:
            i = action_images

        # Create image
        img = Image.new('RGB', (width, height), color=(0, 0, 0))

        text_to_write = text[:math.ceil(len(text) * i / action_images)]

        # Write "Hello World" on the center of the image
        draw = ImageDraw.Draw(img)

        # Calculate position of left side of text
        text_width = draw.textlength(text_to_write, font=font)
        x = (width - text_width) / 2
        y = height / 3

        if k % indicator_slowing == 0:
            tick = not tick

        if tick:
            text_to_write += "|"

        # Draw text
        draw.text((x, y), text_to_write, font=font, fill=(255, 255, 255))

        # Get "languages" from images folder
        if icon_folder is not None:
            step = math.floor((1 - (i + 1) / action_images) * 50)
            img = draw_icons(img, icon_folder, height, width, buffer_between_images, established_total_width, step)

        images.append(img)

    # Copy and reverse images
    images += images[::-1]

    # Add random blinking effect
    for i in range(blinking_images):
        img = Image.new('RGB', (width, height), color=(0, 0, 0))

        text_to_write = ""

        # Write text_to_write on the center of the image
        draw = ImageDraw.Draw(img)

        text_width = draw.textlength(text_to_write, font=font)
        x = (width - text_width) / 2
        y = height / 3

        if i % indicator_slowing == 0:
            tick = not tick

        if tick:
            text_to_write += "|"

        draw.text((x, y), text_to_write, font=font, fill=(255, 255, 255))
        images.append(img)

    return images


def run(out_path: str, image_data: dict, screen_width: int = 1920, screen_ratio: str = "19:3",
        num_action_images: int = 10, num_pause_time: int = 15, num_blinking_images: int = 5,
        blinking_indicator_slowing: int = 3):
    global width, ratio, action_images, pause_time, blinking_images, indicator_slowing, output_path, data_dict
    width = screen_width
    ratio = screen_ratio
    action_images = num_action_images
    pause_time = num_pause_time
    blinking_images = num_blinking_images
    indicator_slowing = blinking_indicator_slowing
    output_path = out_path
    data_dict = image_data

    images = []
    for key in data_dict:
        print(key)
        images += draw_animation(key, data_dict[key])

    # Remove first image
    img = images.pop(0)
    img.save(output_path, save_all=True, append_images=images, duration=100, loop=0)
