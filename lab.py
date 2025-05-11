from ultralytics import YOLO
from collections import Counter
import json

def collect_data_by_train_model(image_path):
    model = YOLO('./best.pt')
    image_path = 'img/' + image_path
    result = model(image_path, save=True)[0]

    print()
    print("----START HERE----")
    # Step 1: Get class indices from result
    class_ids = result.boxes.cls.int().tolist()
    print("---CLASS ID---")
    print(class_ids)

    # Step 2: Map class IDs to class names
    names = result.names
    detected_names = [names[i] for i in class_ids]
    print("---DETECTED NAME---")
    print(detected_names)

    # Step 3: Count occurrences of each class name
    counts = Counter(detected_names)
    print("---COUNT---")
    print(counts)

    # Step 4: Format like "5 car-intersections, 1 east-car, ..."
    summary = ", ".join(f"{v} {k}" for k, v in counts.items())
    print("----GET SUMMARY----")
    print(summary)
    print()

    return summary

def readJsonFile(name):
    with open('traffic.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data[name]
        

