import logging

from docling.backend.abstract_backend import (
    AbstractDocumentBackend,
    DeclarativeDocumentBackend,
)
from docling.datamodel.base_models import (
    ConversionStatus,
    PdfPipelineOptions,
    PipelineOptions,
)
from docling.datamodel.document import ConversionResult, InputDocument
from docling.pipeline.base_model_pipeline import BaseModelPipeline

_log = logging.getLogger(__name__)


class SimpleModelPipeline(BaseModelPipeline):

    def __init__(self, pipeline_options: PdfPipelineOptions):
        super().__init__(pipeline_options)

    def execute(self, in_doc: InputDocument) -> ConversionResult:
        conv_res = ConversionResult(input=in_doc)

        _log.info(f"Processing document {in_doc.file.name}")

        if not in_doc.valid:
            conv_res.status = ConversionStatus.FAILURE
            return conv_res

        if not isinstance(in_doc._backend, DeclarativeDocumentBackend):
            conv_res.status = ConversionStatus.FAILURE
            return conv_res

        conv_res.experimental = in_doc._backend.convert()

        # Do other stuff with conv_res.experimental

        conv_res = self.assemble_document(in_doc, conv_res)

        conv_res.status = ConversionStatus.SUCCESS

        return conv_res

    def assemble_document(
        self, in_doc: InputDocument, conv_res: ConversionResult
    ) -> ConversionResult:
        return conv_res

    @classmethod
    def get_default_options(cls) -> PipelineOptions:
        return PipelineOptions()

    @classmethod
    def is_backend_supported(cls, backend: AbstractDocumentBackend):
        return isinstance(backend, DeclarativeDocumentBackend)
