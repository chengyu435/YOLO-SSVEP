from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO("yolo11n.pt")

    results = model.train(
        data="data.yaml",
        epochs=10,
        imgsz=640,
    )