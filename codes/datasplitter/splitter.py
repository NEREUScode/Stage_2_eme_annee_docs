import os
import json
import random
import shutil
from pathlib import Path
from PIL import Image
from collections import defaultdict
from copy import deepcopy

# === Configuration ===
COCO_JSON_PATH = 'coco_final.json'        # ← Change this
IMAGE_DIR = 'images'                      # ← Change this
OUTPUT_DIR = 'yolo_dataset'               # ← Output folder
SPLIT_RATIO = (0.8, 0.2)                  # (train, val)
INCLUDE_TEST = False                      # Optional test split

# === Class Merging Map ===
combined_classes = {
    "Plastique": [1, 2, 3, 7, 8, 9, 12],
    "Metal": [5, 10],
    "Papier": [6],
    "Verre": [4],
    "Bois": [0],
    "Caoutchouc": [11]
}

# === Utilities ===
def convert_bbox_coco2yolo(bbox, img_width, img_height):
    x, y, w, h = bbox
    x_center = (x + w / 2) / img_width
    y_center = (y + h / 2) / img_height
    w /= img_width
    h /= img_height
    return [x_center, y_center, w, h]

def get_merged_class_map(combined_classes):
    merged_map = {}
    for new_class, id_list in combined_classes.items():
        for old_id in id_list:
            merged_map[old_id] = new_class
    return merged_map

# === Main Logic ===
def convert_and_split_per_class():
    with open(COCO_JSON_PATH, 'r') as f:
        coco = json.load(f)

    merged_class_map = get_merged_class_map(combined_classes)

    images = coco['images']
    annotations = coco['annotations']
    image_id_to_info = {img['id']: img for img in images}

    # Organize annotations by merged class
    merged_data = defaultdict(lambda: {
        'images': [],
        'annotations': [],
        'categories': [],
        'image_set': set()
    })

    img_ann_map = defaultdict(list)
    for ann in annotations:
        img_ann_map[ann['image_id']].append(ann)

    img_counter = 0
    for image in images:
        img_id = image['id']
        img_anns = img_ann_map[img_id]

        anns_by_class = defaultdict(list)
        for ann in img_anns:
            original_cat_id = ann['category_id']
            if original_cat_id in merged_class_map:
                merged_class = merged_class_map[original_cat_id]
                anns_by_class[merged_class].append(ann)

        for merged_class, anns in anns_by_class.items():
            new_img = deepcopy(image)
            new_img_id = f"{img_id}_{merged_class}"
            new_img['id'] = new_img_id
            new_file_name = f"{Path(image['file_name']).stem}_{merged_class}{Path(image['file_name']).suffix}"
            new_img['file_name'] = new_file_name

            merged_data[merged_class]['images'].append(new_img)
            merged_data[merged_class]['image_set'].add(img_id)

            for ann in anns:
                new_ann = deepcopy(ann)
                new_ann['image_id'] = new_img_id
                merged_data[merged_class]['annotations'].append(new_ann)

    # Create YOLO datasets per merged class
    for merged_class, data in merged_data.items():
        class_output = os.path.join(OUTPUT_DIR, merged_class)
        os.makedirs(class_output, exist_ok=True)
        os.makedirs(os.path.join(class_output, 'train', 'images'), exist_ok=True)
        os.makedirs(os.path.join(class_output, 'train', 'labels'), exist_ok=True)
        os.makedirs(os.path.join(class_output, 'val', 'images'), exist_ok=True)
        os.makedirs(os.path.join(class_output, 'val', 'labels'), exist_ok=True)
        if INCLUDE_TEST:
            os.makedirs(os.path.join(class_output, 'test', 'images'), exist_ok=True)
            os.makedirs(os.path.join(class_output, 'test', 'labels'), exist_ok=True)

        imgs = data['images']
        random.shuffle(imgs)

        total = len(imgs)
        train_end = int(SPLIT_RATIO[0] * total)
        val_end = train_end + int(SPLIT_RATIO[1] * total)

        splits = {
            'train': imgs[:train_end],
            'val': imgs[train_end:val_end]
        }

        if INCLUDE_TEST:
            splits['test'] = imgs[val_end:]

        class_list = [merged_class]
        with open(os.path.join(class_output, 'classes.txt'), 'w') as f:
            f.write('\n'.join(class_list))

        for split, imgs_in_split in splits.items():
            for img in imgs_in_split:
                src_path = os.path.join(IMAGE_DIR, img['file_name'].rsplit("_", 1)[0] + Path(img['file_name']).suffix)
                dst_path = os.path.join(class_output, split, 'images', img['file_name'])

                if not os.path.exists(src_path):
                    print(f"❌ Missing image: {src_path}")
                    continue

                shutil.copy(src_path, dst_path)

                anns = [a for a in data['annotations'] if a['image_id'] == img['id']]
                if not anns:
                    continue

                label_path = os.path.join(class_output, split, 'labels', Path(img['file_name']).stem + '.txt')
                with open(label_path, 'w') as f:
                    for ann in anns:
                        img_width = img['width']
                        img_height = img['height']
                        bbox = convert_bbox_coco2yolo(ann['bbox'], img_width, img_height)
                        f.write(f"0 {' '.join(f'{x:.6f}' for x in bbox)}\n")

        # Optional: Save updated COCO json
        updated_json = {
            'images': data['images'],
            'annotations': data['annotations'],
            'categories': [{'id': 0, 'name': merged_class}]
        }
        with open(os.path.join(class_output, f'{merged_class}_coco.json'), 'w') as f:
            json.dump(updated_json, f, indent=4)

    print("✅ Merged and split dataset created successfully.")

# 🔁 Run
convert_and_split_per_class()
