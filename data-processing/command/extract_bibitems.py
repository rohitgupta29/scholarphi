import logging
import os.path
from typing import Iterator, NamedTuple

import common.directories as directories
from command.command import ArxivBatchCommand
from common import file_utils
from common.parse_tex import BibitemExtractor
from common.types import ArxivId, Bibitem, FileContents


class ExtractionTask(NamedTuple):
    arxiv_id: ArxivId
    file_contents: FileContents


class ExtractBibitems(ArxivBatchCommand[ExtractionTask, Bibitem]):
    @staticmethod
    def get_name() -> str:
        return "extract-bibitems"

    @staticmethod
    def get_description() -> str:
        return "Extract bibitems from TeX sources"

    @staticmethod
    def get_entity_type() -> str:
        return "citations"

    def get_arxiv_ids_dirkey(self) -> str:
        return "sources"

    def load(self) -> Iterator[ExtractionTask]:
        for arxiv_id in self.arxiv_ids:
            sources_dir = directories.arxiv_subdir("sources", arxiv_id)
            file_utils.clean_directory(directories.arxiv_subdir("bibitems", arxiv_id))
            for path in file_utils.find_files(sources_dir, [".tex", ".bbl"]):
                file_contents = file_utils.read_file_tolerant(path)
                if file_contents is None:
                    continue
                yield ExtractionTask(arxiv_id, file_contents)

    def process(self, item: ExtractionTask) -> Iterator[Bibitem]:
        extractor = BibitemExtractor()
        for bibitem in extractor.parse(item.file_contents.contents):
            yield bibitem

    def save(self, item: ExtractionTask, result: Bibitem) -> None:
        logging.debug(
            "Extracted bibitem %s from file %s", result, item.file_contents.path
        )
        results_dir = directories.arxiv_subdir("bibitems", item.arxiv_id)
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        results_path = os.path.join(results_dir, "bibitems.csv")
        file_utils.append_to_csv(results_path, result)