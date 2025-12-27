from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from app.core import settings
from azure.ai.vision.imageanalysis.models import VisualFeatures



class OCRClient:
    def __init__(self):
        self.image_client = ImageAnalysisClient(
            endpoint=settings.VISION_ENDPOINT,
            credential=AzureKeyCredential(settings.VISION_KEY),
        )

        self.doc_client = DocumentAnalysisClient(
            endpoint=settings.DOCUMENT_INTELLIGENCE_ENDPOINT,
            credential=AzureKeyCredential(settings.DOCUMENT_INTELLIGENCE_KEY),
        )

    def extract_from_image(self, url: str) -> dict:
          result = self.image_client.analyze_from_url(
               image_url=url,
               visual_features=[VisualFeatures.READ],
          )

          lines = []
          if result.read and result.read.blocks:
               for block in result.read.blocks:
                    for line in block.lines:
                         lines.append(line.text)

          return {"source": "image", "full_text": "\n".join(lines)}

    def extract_from_pdf(self, url: str) -> dict:
          poller = self.doc_client.begin_analyze_document_from_url(
               model_id="prebuilt-read",
               document_url=url,
          )

          lines = []
          for page in poller.result().pages:
               for line in page.lines:
                    lines.append(line.content)

          return {"source": "pdf", "full_text": "\n".join(lines)}
