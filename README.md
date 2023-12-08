# Video Search
Basically just allows you to search through videos and find an image based on a description of the scene you are looking for. For example, if you have a video such as Avatar the Last Airbender trailer, you can search for "bald kid" and find and image of Aang lol.

## How to setup

1. Make sure you are using python 3.10
2. You may need to first run `pip install --upgrade pip`.
3. Install the dependencies in requirements.txt

## How to run
1. Run with `python3.10 main.py`
2. To upload a new video for processing, it needs to be added under data/videos
3. If you are processing a new video, only enter the name of the video. For example if I added `avatar.mov` under `data/videos` when I run the program I should only enter `avatar.mov`.
4. Note queries that don't exist at all are likely to return irrelevant images.
5. To quit the program just enter `quit` into the query.

## Future
Currently the model uses Haystacks EmbeddingsRetriever, while this works, models like gpt-4's image description give much more elaborate descriptions and better context for SemanticSearch. This, however, is much more expensive and ideally I will just create a better model for getting image context.