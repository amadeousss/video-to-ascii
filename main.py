from PIL import Image
from frames import video_to_frames, ascii_frames_to_images, frames_to_video
import os

# CHARS = " `^\",;li~+?[}{1)(\\/tzXZ*#&8%@$"
CHARS = " .:-=+*#%@"


def correct_round(val):
    if val - int(val) == 0.5:
        return int(val) + 1
    else:
        return round(val)


def map_to_char(val):
    return CHARS[int(val / 255 * (len(CHARS) - 1))]


def image_to_ascii(image_path):
    im = Image.open(image_path)
    width, height = im.size
    new_width = 40
    new_height = round(new_width * height / width)
    im = im.resize((new_width, new_height))
    width, height = im.size
    grid = list(im.getdata())
    grid = [grid[i:i + im.width] for i in range(0, len(grid), im.width)]
    content = ""
    for y in range(height):
        for x in range(width):
            grid[y][x] = map_to_char(sum(grid[y][x]) / 3)
    for y in range(height):
        for x in range(width):
            content += grid[y][x] * 2
        content += "\n"
    # print(content)
    return content


def video_to_ascii(video_path):
    video_to_frames(video_path, 'frames/')

    if not os.path.exists('frames_ascii_txt'):
        os.makedirs('frames_ascii_txt')

    for index, filename in enumerate(os.listdir('frames/')):
        content = image_to_ascii(os.path.join('frames/', f"{index}.jpg"))
        with open(f'frames_ascii_txt/{index}.txt', 'w') as f:
            f.write(content)


def main():
    video_to_ascii('video.MP4')
    ascii_frames_to_images('frames_ascii_txt', 'frames_ascii_img', 'video.mp4')
    frames_to_video('frames_ascii_img', 'video_ascii.mp4', 'video.mp4')

    for f in os.listdir('frames_ascii_txt/'):
        os.remove(os.path.join('frames_ascii_txt/', f))

    for f in os.listdir('frames/'):
        os.remove(os.path.join('frames/', f))

    for f in os.listdir('frames_ascii_img/'):
        os.remove(os.path.join('frames_ascii_img/', f))


if __name__ == '__main__':
    main()
