from typing import Iterable

from PIL import ImageDraw

from docling.datamodel.base_models import Page
from docling.models.abstract_model import AbstractPageModel


class PagePreprocessingModel(AbstractPageModel):
    def __init__(self, config):
        self.config = config

    def __call__(self, page_batch: Iterable[Page]) -> Iterable[Page]:
        for page in page_batch:
            page = self._populate_page_images(page)
            page = self._parse_page_cells(page)
            yield page

    # Generate the page image and store it in the page object
    def _populate_page_images(self, page: Page) -> Page:
        # default scale
        page.get_image(
            scale=1.0
        )  # puts the page image on the image cache at default scale

        images_scale = self.config["images_scale"]
        # user requested scales
        if images_scale is not None:
            page._default_image_scale = images_scale
            page.get_image(
                scale=images_scale
            )  # this will trigger storing the image in the internal cache

        return page

    # Extract and populate the page cells and store it in the page object
    def _parse_page_cells(self, page: Page) -> Page:
        page.cells = page._backend.get_text_cells()

        # DEBUG code:
        def draw_text_boxes(image, cells):
            draw = ImageDraw.Draw(image)
            for c in cells:
                x0, y0, x1, y1 = c.bbox.as_tuple()
                draw.rectangle([(x0, y0), (x1, y1)], outline="red")
            image.show()

        # draw_text_boxes(page.get_image(scale=1.0), cells)

        return page
