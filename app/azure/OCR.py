# import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from app.core import settings
from typing import Dict, Any

# import dotenv
# dotenv.load_dotenv()
# Set the values of your computer vision endpoint and computer vision key
# as environment variables:
try:
    # endpoint = os.environ["VISION_ENDPOINT"]
    # key = os.environ["VISION_KEY"]
    endpoint=settings.VISION_ENDPOINT
    key=settings.VISION_KEY
except KeyError:
    print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
    print("Set them before running this sample.")
    exit()

client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)


from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

doc_client = DocumentAnalysisClient(
    endpoint=settings.DOCUMENT_INTELLIGENCE_ENDPOINT,
    credential=AzureKeyCredential(settings.DOCUMENT_INTELLIGENCE_KEY)
)

def blob_image_result(image_url: str) -> Dict[str, Any]:
    result = client.analyze_from_url(
        image_url=image_url,
        visual_features=[VisualFeatures.READ],
    )

    lines = []

    if result.read and result.read.blocks:
        for block in result.read.blocks:
            for line in block.lines:
                lines.append(line.text)

    return {
        "source": "image",
        "full_text": "\n".join(lines)
    }



def blob_doc_result(pdf_url: str) -> Dict[str, Any]:
    poller = doc_client.begin_analyze_document_from_url(
        model_id="prebuilt-read",
        document_url=pdf_url
    )

    result = poller.result()
    lines = []

    for page in result.pages:
        for line in page.lines:
            lines.append(line.content)

    return {
        "source": "pdf",
        "full_text": "\n".join(lines)
    }
