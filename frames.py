import cv2
import os
from PIL import Image, ImageDraw, ImageFont
import moviepy.video.io.ImageSequenceClip


def video_to_frames(input_loc, output_loc):
    if not os.path.exists(output_loc):
        os.makedirs(output_loc)

    vidcap = cv2.VideoCapture(input_loc)
    success, image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite(f"{output_loc}/{count}.jpg", image)  # save frame as JPEG file
        success, image = vidcap.read()
        count += 1


def ascii_frames_to_images(input_loc, output_loc, original_video):
    # Create output directory
    if not os.path.exists(output_loc):
        os.makedirs(output_loc)

    vcap = cv2.VideoCapture(original_video)
    width = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Sample line of text
    with open(f'{input_loc}/0.txt', 'r') as f:
        sample_line = f.readlines()[0]

    # Compute font size
    fontsize = 1
    img_fraction = 1
    font = ImageFont.truetype("cour.ttf", fontsize)
    image = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(image)
    while draw.textlength(sample_line[0], font=font) * len(sample_line) < img_fraction * width:
        print(f"Fontsize: {fontsize}")
        fontsize += 1
        font = ImageFont.truetype("cour.ttf", fontsize)

    # Put text on black bg and save frames
    for index, filename in enumerate(os.listdir(input_loc)):
        with open(f'{input_loc}/{index}.txt', 'r') as f:
            content = f.read()
            image = Image.new('RGB', (width, height), color='black')
            ImageDraw.Draw(
                image
            ).text(
                (0, 0),
                content,
                (255, 255, 255),
                font=font
            )
            image.save(f"{output_loc}/{index}.png")


def frames_to_video(input_loc, output_name, original_video):
    cap = cv2.VideoCapture(original_video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    image_files = []
    for index, filename in enumerate(os.listdir(input_loc)):
        image_files.append(os.path.join(input_loc, f"{index}.png"))
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile(output_name)
