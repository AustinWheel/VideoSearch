import os
from image_describe import ImageDescribe
from image_convert import ImageConvert
from store_context import VideoSearch

def process_photo(photo_path):
    try:
        data = ImageDescribe(photo_path).getContext()
        context = data['choices'][0]['message']['content']
        context = context.replace("\n", "")
    except: context = ""
    return photo_path, context

def process_all_photos(directory, output_file="output.txt"):
    files = os.listdir(directory)
    photo_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    with open(output_file, "w") as f:
        for photo_file in photo_files:
            photo_path = os.path.join(directory, photo_file)
            path, context = process_photo(photo_path)
            f.write(f"{path}:{context}\n")

if __name__ == "__main__":
    print(" Welcome to Video Search! \n you can process a video to add it to your search context \n or you can search already processed videos for an image.")
    process_video = input("Upload a video for processing? (y/n): ")
    if process_video not in ("yn"): 
        print("Invalid selection. Assuming No")
    else: process_video = True if process_video == "y" else False
    if process_video:
        try:
            video_name = input("Enter name for video for processing (place video in data/videos/): ")
            frames_skipped = int(input("Enter the number of frames to skip (int): "))
            ImageConvert(f"data/videos/{video_name}").generateImages(frames_skipped)
            print("Video processed!!!")
        except Exception as e:
            print("Error, not processing video")
            print(e)
    model = VideoSearch("data/photos")
    model.train(updatedVideo=True)
    query = ""
    print("Enter 'quit' to terminate")
    while query != "quit":
        query = input("Enter a query to search video: ")
        if query != "quit": model.run_query(query)
    
    print("Come again :D")