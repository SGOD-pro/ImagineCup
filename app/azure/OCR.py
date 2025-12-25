# import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from app.config.main import settings
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
        image_url=image_url,   # FIXED
        visual_features=[VisualFeatures.CAPTION, VisualFeatures.READ],
        gender_neutral_caption=True,
    )

    response: Dict[str, Any] = {
        "caption": None,
        "ocr": {
            "full_text": "",
            "lines": []
        }
    }

    # ----- Caption -----
    if result.caption:
        response["caption"] = {
            "text": result.caption.text,
            "confidence": round(result.caption.confidence, 4)
        }

    # ----- OCR -----
    if result.read and result.read.blocks:
        lines_text = []

        for block in result.read.blocks:
            for line in block.lines:
                words = [
                    {
                        "text": word.text,
                        "confidence": round(word.confidence, 4)
                    }
                    for word in line.words
                ]

                line_text = line.text
                lines_text.append(line_text)

                response["ocr"]["lines"].append({
                    "text": line_text,
                    "bounding_polygon": line.bounding_polygon,
                    "words": words
                })

        response["ocr"]["full_text"] = "\n".join(lines_text)

    return response

    result = client.analyze_from_url(
        image_url="/image.png",
        visual_features=[VisualFeatures.CAPTION, VisualFeatures.READ],
        gender_neutral_caption=True,  # Optional (default is False)
    )
    
    print("Image analysis results:")
    # Print caption results to the console
    print(" Caption:")
    if result.caption is not None:
        print(f"   '{result.caption.text}', Confidence {result.caption.confidence:.4f}")

    # Print text (OCR) analysis results to the console
    print(" Read:")
    if result.read is not None:
        for line in result.read.blocks[0].lines:
            print(f"   Line: '{line.text}', Bounding box {line.bounding_polygon}")
            for word in line.words:
                print(f"     Word: '{word.text}', Bounding polygon {word.bounding_polygon}, Confidence {word.confidence:.4f}")


def blob_doc_result(pdf_url: str) -> dict:
    poller = doc_client.begin_analyze_document_from_url(
        model_id="prebuilt-read",
        document_url=pdf_url
    )

    result = poller.result()

    pages = []
    full_text = []

    for page in result.pages:
        page_lines = []
        for line in page.lines:
            page_lines.append(line.content)
            full_text.append(line.content)

        pages.append({
            "page_number": page.page_number,
            "text": "\n".join(page_lines)
        })

    return {
        "source": "pdf",
        "pages": pages,
        "full_text": "\n".join(full_text)
    }
