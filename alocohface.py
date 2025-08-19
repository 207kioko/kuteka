import os
from deepface import DeepFace

# -------- CONFIG --------
image_folder = "images"  # Folder containing your images
valid_extensions = (".jpg", ".jpeg", ".png")  # Supported file types
# ------------------------

def analyze_folder(folder_path):
    # List all image files
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)]

    if not image_files:
        print("No images found in the folder.")
        return

    for img_name in image_files:
        img_path = os.path.join(folder_path, img_name)
        print(f"\nProcessing: {img_name}")

        try:
            # Analyze gender
            result = DeepFace.analyze(img_path=img_path, actions=['gender'])

            # DeepFace returns a list of results
            for idx, face in enumerate(result):
                print(f"  Face {idx+1}: {face['dominant_gender']} ({face['gender']})")

        except Exception as e:
            print(f"  Error processing {img_name}: {e}")

if __name__ == "__main__":
    analyze_folder(image_folder)
