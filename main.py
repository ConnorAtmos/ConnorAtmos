import gif_maker

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
output_path = "gifs/experience.gif"

# This is the dictionary that will be used to create the animation.
# You can set the dict values to None if you don't want to include image folder path
data_dict = {"Coding Languages": "images/languages",
             "IDEs and Software": "images/ides",
             "Operating Systems": "images/operating_systems",
             "Additional Experience": "images/additional_experience",
             }

gif_maker.run(output_path, data_dict, width, ratio, action_images, pause_time, blinking_images, indicator_slowing)
print(f"Finished creating gif at {output_path}")

# Output path
output_path = "gifs/introduction.gif"

data_dict = {"ConnorAtmos": "images/atmos",
             "connor.sw.personal@gmail.com": None,
             "linkedin: connor-s-white": None,
             }

gif_maker.run(output_path, data_dict, width, ratio, action_images, pause_time, blinking_images, indicator_slowing)
print(f"Finished creating gif at {output_path}")