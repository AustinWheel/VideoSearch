import os
from io import BytesIO
from haystack import Document, Pipeline
from haystack.nodes.retriever.multimodal import MultiModalRetriever
from haystack.document_stores import InMemoryDocumentStore
from PIL import Image, ImageDraw, ImageOps
from IPython.display import display, Image as IPImage
import warnings
warnings.filterwarnings("ignore")

class VideoSearch:
    def __init__(self, doc_dir: str) -> None:
        self.doc_dir = doc_dir

    def preprocess(self):
        def get_mean_pixel_value(image):
            grayscale_image = image.convert('L')

            pixel_data = grayscale_image.getdata()

            mean_pixel_value = sum(pixel_data) / len(pixel_data)

            return mean_pixel_value

        def is_almost_black_or_white(image):
            mean_pixel_value = get_mean_pixel_value(image)

            if mean_pixel_value < 30 or mean_pixel_value > 225:
                return True
            else:
                return False

        def delete_almost_black_or_white_images(directory):
            for filename in os.listdir(directory):
                if filename.endswith('.jpg') or filename.endswith('.png'):
                    image_path = os.path.join(directory, filename)

                    # Load the image
                    image = Image.open(image_path)

                    if is_almost_black_or_white(image):
                        # Delete the image
                        os.remove(image_path)

        directory = self.doc_dir
        delete_almost_black_or_white_images(directory)

    def train(self, updatedVideo=False):
        if updatedVideo: self.preprocess()
        document_store = InMemoryDocumentStore(embedding_dim=512)
        doc_dir = self.doc_dir

        images = [
            Document(content=f"./{doc_dir}/{filename}", content_type="image")
            for filename in os.listdir(f"./{doc_dir}/")
        ]

        document_store.write_documents(images)

        retriever_text_to_image = MultiModalRetriever(
            document_store=document_store,
            query_embedding_model="sentence-transformers/clip-ViT-B-32",
            query_type="text",
            document_embedding_models={"image": "sentence-transformers/clip-ViT-B-32"},
        )

        document_store.update_embeddings(retriever=retriever_text_to_image)

        self.pipeline = Pipeline()
        self.pipeline.add_node(component=retriever_text_to_image, name="retriever_text_to_image", inputs=["Query"])


    def run_query(self, query: str):
        results = self.pipeline.run(query=query, params={"retriever_text_to_image": {"top_k": 1}})

        results = sorted(results["documents"], key=lambda d: d.score, reverse=True)

        for doc in results:
            print(doc.score, doc.content)

        images_array = [doc.content for doc in results]
        scores = [doc.score for doc in results]
        for ima, score in zip(images_array, scores):
            self.display_img_array(ima, score)
    
    def display_img_array(self, ima, score):
        im = Image.open(ima)
        img_with_border = ImageOps.expand(im, border=20, fill="white")

        # Add Text to an image
        img = ImageDraw.Draw(img_with_border)
        img.text((20, 0), f"Score: {score},    Path: {ima}", fill=(0, 0, 0))

        bio = BytesIO()
        img_with_border.save(bio, format="png")
        display(IPImage(bio.getvalue(), format="png"))
        img_with_border.show()