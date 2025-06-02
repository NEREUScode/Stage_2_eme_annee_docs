# 📦 COCO to YOLO Dataset Converter with Class Merging

This script converts a COCO-formatted annotation file into multiple YOLO-style datasets, grouped by **merged classes**, with optional train/val (and test) splits.

---

## ✅ Features

- Converts **COCO annotations** to **YOLOv8 format**.
- Groups categories into **merged classes** (e.g., all plastic types into `"Plastique"`).
- Creates **train/val splits** (and test if enabled).
- Generates YOLO-compatible folder structures.
- Writes `classes.txt` and optional COCO JSON per merged class.

---

## 📁 Input Files

- `coco_final.json` – COCO-format annotation file.
- `images/` – Folder containing the original images.

> ⚠️ Image filenames must match those referenced in the COCO JSON.

---

## 📤 Output Structure

A folder named `yolo_dataset/` will be created with one subfolder per merged class. Each class folder contains:
