import os
import shutil
import requests
import tarfile
import json
import xml.etree.ElementTree as ET

# from PIL import Image, ImageDraw

ROOT_DIR = os.environ.get("ROOT_DIR")
if ROOT_DIR == "":
    ROOT_DIR = "./"

IMAGE_DIR = f"{ROOT_DIR}/Images"
ANNOTATION_DIR = f"{ROOT_DIR}/Annotation"
OUTPUT_DIR = f"{ROOT_DIR}/edge-impulse"

IMAGES_URL = "http://vision.stanford.edu/aditya86/ImageNetDogs/images.tar"
ANNOTATIONS_URL = "http://vision.stanford.edu/aditya86/ImageNetDogs/annotation.tar"
IMAGE_ARCHIVE = f"{ROOT_DIR}/images.tar"
ANNOTATION_ARCHIVE = f"{ROOT_DIR}/annotations.tar"


# Download dog image archive
if not os.path.exists(IMAGE_ARCHIVE):
    print("Downloading image archive...")
    response = requests.get(IMAGES_URL, stream=True)
    if response.status_code == 200:
        with open(IMAGE_ARCHIVE, "wb") as f:
            f.write(response.raw.read())


# Download annotation archive
if not os.path.exists(ANNOTATION_ARCHIVE):
    print("Downloading annotation archive...")
    response = requests.get(ANNOTATIONS_URL, stream=True)
    if response.status_code == 200:
        with open(ANNOTATION_ARCHIVE, "wb") as f:
            f.write(response.raw.read())

# Extract image archive
if not os.path.exists(IMAGE_DIR):
    print("Extracting image archive...")
    image_tar = tarfile.open(IMAGE_ARCHIVE)
    image_tar.extractall(ROOT_DIR)  # specify which folder to extract to
    image_tar.close()


# Extract annotation archive
if not os.path.exists(ANNOTATION_DIR):
    print("Extracting annotation archive...")
    annotation_tar = tarfile.open(ANNOTATION_ARCHIVE)
    annotation_tar.extractall(ROOT_DIR)  # specify which folder to extract to
    annotation_tar.close()

# Choose breeds close to your dog based on available labels
breeds = [
    "Maltese_dog",
    "toy_terrier",
    "Irish_terrier",
    "miniature_schnauzer",
    "standard_schnauzer",
    "Scotch_terrier",
    "cocker_spaniel",
    "French_bulldog",
    "chow",
    "toy_poodle",
    "miniature_poodle",
    "Chihuahua",
    "Japanese_spaniel",
    "Pekinese",
    "Shih-Tzu",
    "Rhodesian_ridgeback",
    "rebone",
    "borzei",
    "whippet",
]

# Consolidate target images into a single folder
if not os.path.exists(OUTPUT_DIR):
    print(f"Consolidating files")
    os.mkdir(OUTPUT_DIR)
    # For every breed folder in the Images folder
    for folder in os.listdir(IMAGE_DIR):
        # Skip breeds we don't care about
        if folder.split("-")[1] not in breeds:
            continue
        # For every file in the folder
        for file in os.listdir(f"{IMAGE_DIR}/{folder}"):
            # If the file is a jpeg
            if file.endswith(".jpg"):
                # Copy it to the new upload folder
                shutil.copy(f"{IMAGE_DIR}/{folder}/{file}", f"{OUTPUT_DIR}/{file}")

# https://towardsdatascience.com/convert-pascal-voc-xml-to-yolo-for-object-detection-f969811ccba5
# Build label file for Edge Impulse
if not os.path.exists(f"{OUTPUT_DIR}/bounding_boxes.labels"):
    # For every folder in the Annotation directory
    for input_dir in os.listdir(ANNOTATION_DIR):
        # For every annotation in the folder
        for filename in os.listdir(f"{ANNOTATION_DIR}/{input_dir}"):
            # Check if the label contains the corresponding image filenamee
            if not os.path.exists(f"{IMAGE_DIR}/{input_dir}/{filename}.jpg"):
                print(f"{filename} image does not exist!")
                continue

            # Parse the content of the xml filenamee
            tree = ET.parse(os.path.join(f"{ANNOTATION_DIR}/{input_dir}", filename))
            root = tree.getroot()
            width = int(root.find("size").find("width").text)
            height = int(root.find("size").find("height").text)

            # Initialize annotation file
            # https://docs.edgeimpulse.com/docs/edge-impulse-cli/cli-uploader#bounding-boxes
            annotation = {
                "version": 1,
                "type": "bounding-box-labels",
                "boundingBoxes": {},
            }

            objects = []
            # For every class detected in the annotation
            for obj in root.findall("object"):
                # Extract label name
                label = obj.find("name").text
                # Get bbox corners in FOMO-friendly format
                pil_bbox = [int(x.text) for x in obj.find("bndbox")]
                # Add the bounding box to the image annotation
                objects.append(
                    {
                        "label": "dog",
                        "x": pil_bbox[0],
                        "y": pil_bbox[1],
                        "width": pil_bbox[2],
                        "height": pil_bbox[3],
                    }
                )

            annotation["boundingBoxes"][f"{filename}.jpg"] = objects

    # Generate bounding_boxes.labels file for Edge Impulse
    with open(
        os.path.join(OUTPUT_DIR, f"bounding_boxes.labels"), "w", encoding="utf-8"
    ) as f:
        f.write(json.dumps(annotation))
        f.close()


"""
def draw_image(img, bboxes):
    draw = ImageDraw.Draw(img)
    for bbox in bboxes:
        box_sequence = [
            int(bbox["x"] - bbox["width"] / 2),
            int(bbox["y"] - bbox["height"] / 2),
            int(bbox["width"] + bbox["x"] / 2),
            int(bbox["height"] + bbox["y"] / 2),
        ]

        draw.rectangle(box_sequence, outline="green", width=1)
    return img


print("Creating sample images...")
# generate a YOLO format text filenamee for each xml filenamee
with open(os.path.join(OUTPUT_DIR, f"bounding_boxes.labels"), "r") as f:
    bboxJSON = json.loads(f.read())
    f.close()

for filename in os.listdir(OUTPUT_DIR)[:5]:
    image_filename = f"{OUTPUT_DIR}/{filename}"
    if image_filename.endswith(".labels"):
        continue
    img = Image.open(image_filename)

    bboxes = bboxJSON["boundingBoxes"][f"{filename}"]

    new_img = draw_image(img, bboxes)
    if not os.path.exists(f"{OUTPUT_DIR}/samples"):
        os.mkdir(f"{OUTPUT_DIR}/samples")
    image_name = image_filename.split("/")[-1]
    new_img.save(f"{OUTPUT_DIR}/samples/{image_name}")
"""
