
# 🌍 ZoraVision - Environmental Deep Learning Project

This project focuses on environmental monitoring using Deep Learning techniques for waste detection through image analysis and geospatial mapping.

---

## 📁 Project Structure

```yaml
.
├── codes/ # Python scripts for preprocessing and formatting
│ ├── datasplitter/ # Split and format dataset into YOLO format
│ ├── extractinfo/ # Extract GPS and density info into GeoJSON
│ └── renameimages/ # Rename images and update COCO annotations
├── data/ # Raw image datasets (V1, V2)
├── documents/ # Project report in PDF
├── guides/ # User guides and deployment instructions
├── metrics/ # Model training results and performance metrics
└── README.md # You are here
```

---

## 🔧 Components Overview

- `codes/` – Python tools to:
  - Rename and clean image filenames
  - Convert COCO annotations to YOLO format
  - Extract GPS + density data for mapping

- `data/` – Contains annotated datasets (versioned)

- `metrics/` – Visualizations and statistics from model training (F1, PR, confusion matrix...)

- `guides/` – Manuals for the ZoraAnnotator app, YOLO training modules, and hosting the web app

- `documents/` – Final PDF report for the internship

---

## 🚀 Getting Started

To process or convert datasets, go to the relevant folder under `codes/` and follow the `README.md` inside each.

---

## 🧑‍💻 Authors

- Benyamna Mohammed
- Makkour Israe  
