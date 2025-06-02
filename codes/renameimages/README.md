# 🖼️ COCO Image Renamer & Annotation Updater

This script renames image files in a folder to a standardized format and updates the corresponding COCO annotation JSON file with the new filenames.

## 📌 What It Does

- Renames images in a specified folder using the format:  
  `image_001.jpg`, `image_002.jpg`, etc.
- Updates the `file_name` field in each `image` entry in a COCO-format JSON file.
- Saves a new JSON file with the updated image filenames.

## 📁 Inputs

- `images/` – Folder containing the original images.
- `coco_final.json` – Original COCO-format annotation file.

## 📤 Output

- `updated_annotations.json` – Updated annotation file with renamed image references.
- All images in the folder will be renamed.

## ⚙️ How to Use

1. Install Python (if not already installed).

2. Place the script in the same directory as:
   - The image folder (default: `images/`)
   - The COCO JSON file (default: `coco_final.json`)

3. Run the script:

```bash
python rename_and_update_json.py
