import os
from PIL import Image


def get_metadata():
    files = []
    json_object = {"files": []}
    with open("saved_files.txt", "r") as file:
        while True:
            line = file.readline()
            if not line:
                break
            else:
                files.append(line.strip())
    for i in files:
        metadata = {}
        metadata['Name'] = i.split("uploads")[-1].replace("/", "")
        metadata['Size'] = os.stat(i).st_size/1000000
        im = Image.open(i)
        width, height = im.size
        metadata['Resolution'] = str(width) + "x" + str(height)
        metadata['URL'] = "/img/" + metadata['Name']

        json_object['files'].append(metadata)

    os.remove("saved_files.txt")
    # [os.remove(i) for i in files]

    return json_object
