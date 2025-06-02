import os
import json
from pathlib import Path

# === Configuration ===
image_dir = 'images'  # your image folder
json_path = 'coco_final.json'  # your COCO JSON file
output_json = 'updated_annotations.json'

# === Load JSON ===
with open(json_path, 'r') as f:
    coco_data = json.load(f)

# === Prepare output ===
new_images = []
file_name_map = {}
pad = len(str(len(coco_data['images'])))

# === Rename images and update JSON ===
for idx, image_info in enumerate(coco_data['images']):
    old_name = image_info['file_name']
    old_path = os.path.join(image_dir, old_name)

    # Generate new name
    ext = Path(old_name).suffix
    new_name = f'image_{str(idx+1).zfill(pad)}{ext}'
    new_path = os.path.join(image_dir, new_name)

    # Rename file on disk
    if os.path.exists(old_path):
        os.rename(old_path, new_path)

    # Update the image info
    image_info['file_name'] = new_name
    new_images.append(image_info)
    file_name_map[old_name] = new_name

# === Replace images in JSON ===
coco_data['images'] = new_images

# === Save updated JSON ===
with open(output_json, 'w') as f:
    json.dump(coco_data, f, indent=2)

print(f"Images renamed and annotations updated. Saved to: {output_json}")
