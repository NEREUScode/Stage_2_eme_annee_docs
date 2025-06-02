import os
import exifread
import pandas as pd
import json

DRONE_IMAGE_DIR = "maptiler/backend/images"
CSV_PATH = "maptiler/backend/results.csv"
OUTPUT_MAP = "maptiler/frontend/public/heatmap_data.json"


def extract_dji_coordinates(image_path):
    try:
        with open(image_path, "rb") as f:
            tags = exifread.process_file(f, details=False)

        # Extract GPS coordinates with fallbacks
        gps_lat = tags.get("GPS GPSLatitude") or tags.get("XMP:GPSLatitude")
        gps_lon = tags.get("GPS GPSLongitude") or tags.get("XMP:GPSLongitude")

        # Extract reference directions as strings
        lat_ref = str(tags.get("GPS GPSLatitudeRef", "N")).strip().upper()
        lon_ref = str(tags.get("GPS GPSLongitudeRef", "E")).strip().upper()

        # Convert to decimal degrees
        lat = dji_gps_to_decimal(gps_lat) if gps_lat else None
        lon = dji_gps_to_decimal(gps_lon) if gps_lon else None

        # Apply reference directions
        if lat and lat_ref == "S":
            lat = -lat
        if lon and lon_ref == "W":
            lon = -lon

        return lat, lon

    except Exception as e:
        print(f"Error processing {os.path.basename(image_path)}: {str(e)}")
        return None, None


def dji_gps_to_decimal(gps_tag):
    try:
        if not gps_tag:
            return None

        # Handle both rational and float formats
        if isinstance(gps_tag.values[0], exifread.utils.Ratio):
            degrees = gps_tag.values[0].num / gps_tag.values[0].den
            minutes = gps_tag.values[1].num / gps_tag.values[1].den
            seconds = gps_tag.values[2].num / gps_tag.values[2].den
            return degrees + (minutes / 60) + (seconds / 3600)
        return float(gps_tag.values[0])
    except Exception as e:
        print(f"GPS conversion error: {str(e)}")
        return None


def process_data():
    try:
        df = pd.read_csv(
            CSV_PATH,
            skiprows=1,
            names=["Image", "Count", "Density"],
            encoding="utf-8-sig",
        )
        df = df[df["Image"] != "MOYENNE"]
        df["Image"] = df["Image"].str.strip()  # Clean whitespace
    except Exception as e:
        print(f"CSV Error: {str(e)}")
        return []

    heat_data = []

    for idx, row in df.iterrows():
        img_name = row["Image"].strip()
        img_path = os.path.join(DRONE_IMAGE_DIR, img_name)

        if not os.path.exists(img_path):
            print(f"Missing image: {img_name}")
            continue

        lat, lon = extract_dji_coordinates(img_path)
        if lat is None or lon is None:
            print(f"Invalid GPS in {img_name}")
            continue

        try:
            density = float(str(row["Density"]).replace(",", "."))
            heat_data.append([lat, lon, density])
            print(f"Processed {img_name} | Lat: {lat:.6f}, Lon: {lon:.6f}")
        except ValueError:
            print(f"Invalid density value: {row['Density']}")

    return heat_data


def create_highres_heatmap(heat_data):
    """convert heat data to a high-resolution heatmap"""
    if not heat_data:
        print("No data to create heatmap")
        return

    # conert to geojson format
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": {"density": density},
            }
            for lat, lon, density in heat_data
        ],
    }

    with open(OUTPUT_MAP, "w") as f:
        json.dump(geojson, f)


if __name__ == "__main__":
    data = process_data()
    if data:
        create_highres_heatmap(data)
    else:
        print("No valid data processed")