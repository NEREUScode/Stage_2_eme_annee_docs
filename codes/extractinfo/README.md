# 📍 Drone Image GPS Extractor & Heatmap Generator

This script extracts GPS coordinates from drone images and combines them with density values from a CSV file to generate a heatmap in **GeoJSON format**.

## 🔧 What It Does

- Reads image metadata (EXIF) to extract **latitude** and **longitude**.
- Reads a CSV file that contains:
  - Image file names
  - Associated density values
- Converts GPS data to **decimal format**.
- Outputs a **GeoJSON** file containing points with density info.

## 📁 Input Files

- `images/` – Folder with drone images (JPEG format with GPS metadata).
- `results.csv` – CSV file with columns:  
  `Image`, `Count`, `Density`

Example row:
image1.jpg,12,0.65

## 📤 Output

- `heatmap_data.json` – A **GeoJSON** file structured like this:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [longitude, latitude]
      },
      "properties": {
        "density": 0.65
      }
    }
  ]
}
```

## ▶️ How to Run

Make sure the following Python packages are installed:

```bash
pip install pandas exifread
```

Run the script:

```bash
python your_script.py
```

It will:

Process each image listed in the CSV

Extract GPS info

Write a heatmap GeoJSON to heatmap_data.json

## 📌 Notes

Images must contain GPS EXIF data (e.g., from DJI drones).

Density values should be numeric (dots or commas are accepted).

The script ignores rows with invalid or missing data.
