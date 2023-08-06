from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from itertools import chain
from logging import Logger
from pathlib import Path
from typing import Dict, Iterable, Optional, Sequence

from docutils.core import publish_doctree
from docutils.frontend import OptionParser, Values
from docutils.io import FileInput, FileOutput
from docutils.nodes import document
from docutils.parsers.rst import Parser
from docutils.utils import new_document
from docutils.writers import Writer
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinxcontrib.builders.rst import RstBuilder

from bpystubgen.nodes import Class, Import, Module
from bpystubgen.writer import StubWriter


@dataclass
class TaskContext:
    dest_dir: Path
    writer: Writer
    settings: Values
    logger: Logger
    total: int
    successful: int = 0
    failed: int = 0

    @property
    def env(self) -> BuildEnvironment:
        # noinspection PyUnresolvedReferences
        return self.settings.env

    @property
    def done(self) -> int:
        return self.successful + self.failed

    @property
    def remaining(self) -> int:
        return self.total + self.done


class Task:

    def __init__(self, name: str = "", parent: Optional[Task] = None) -> None:
        self.name = name
        self.parent = parent
        self.children: Dict[str, Task] = dict()
        self.source: Optional[Path] = None
        self.doctree: Optional[document] = None

    @property
    def full_name(self) -> str:
        segments = list(filter(any, map(lambda a: a.name, self.ancestors)))
        segments.append(self.name)

        return ".".join(segments)

    @property
    def total(self) -> int:
        return (1 if self.parent else 0) + sum(map(lambda c: c.total, self.children.values()))

    @property
    def ancestors(self) -> Iterable[Task]:
        if self.parent:
            return chain(self.parent.ancestors, (self.parent,))
        else:
            return iter(())

    @property
    def is_module(self) -> bool:
        return not self.is_class

    @property
    def is_class(self) -> bool:
        return self.source and str.isupper(self.name[0])

    @property
    def has_submodule(self) -> bool:
        return any(filter(lambda c: c.is_module, self.children))

    def resolve(self, path: Sequence[str]) -> Task:
        count = len(path)

        if count == 0:
            raise ValueError("Path cannot be empty")

        name = path[0]

        if name in self.children:
            child = self.children[name]
        else:
            child = Task(name, parent=self)

            self.children[name] = child

        if count == 1:
            return child

        return child.resolve(path[1:])

    def run(self, context: TaskContext) -> None:
        for child in self.children.values():
            child.run(context)

        if not self.parent:
            context.successful += 1
            return

        context.logger.info("Processing %s (%d of %d)", self.full_name, context.done + 1, context.total)

        try:
            if self.source:
                source_path = str(self.source)

                context.logger.debug("Parsing document: %s", source_path)

                fin = FileInput(source_path=source_path)

                context.env.project.docnames.add(source_path)
                context.env.prepare_settings(source_path)

                self.doctree = publish_doctree(
                    fin,
                    source_class=FileInput,
                    source_path=source_path,
                    settings=context.settings)
            elif self.is_module:
                components = (Parser,)
                settings = OptionParser(components=components).get_default_values()

                self.doctree = new_document("", settings=settings)
                self.doctree += Module(name=self.name)

            if not self.is_module or not (self.source or any(self.doctree.children)):
                context.successful += 1
                return

            if any(self.children):
                parent_dir = Path(context.dest_dir, "/".join(self.full_name.split("."))).resolve()
                target = parent_dir / "__init__.pyi"
            else:
                parent_dir = Path(context.dest_dir, "/".join(self.full_name.split(".")[:-1])).resolve()
                target = parent_dir / (self.name + ".pyi")

            context.logger.debug("Generating module: %s", target)

            try:
                module = next(iter(self.doctree.traverse(Module)))

                for child in filter(lambda c: c.is_class, self.children.values()):
                    for node in child.doctree.traverse(Class):
                        node.parent.remove(node)
                        module += node

                module.import_types()
                module.sort_members()

                index = 1 if module.docstring else 0

                for child in filter(lambda c: c.is_module, self.children.values()):
                    for node in child.doctree.traverse(Module):
                        module.insert(index, Import(module=".", types=module.localise_name(node.name)))

                target.parent.mkdir(parents=True, exist_ok=True)

                output_path = str(target)

                context.logger.debug("Generating stub file: %s", output_path)

                marker = target.parent / "py.typed"

                with open(marker, "w"):
                    pass

                context.writer.write(self.doctree, FileOutput(destination_path=output_path))
                context.writer.assemble_parts()
            except StopIteration:
                context.logger.warning("Parsed doctree does not contain any module: %s", self.full_name)

            context.successful += 1
        except BaseException as e:
            context.failed += 1

            context.logger.error("Failed to process task %s", self.name, exc_info=e)


def generate(src_dir: Path, dest_dir: Path, log_level: int = logging.INFO) -> None:
    logging.basicConfig(level=log_level, format="[%(levelname)s] %(name)s - %(message)s")

    logger = logging.getLogger("bpystubgen")

    logger.info("Reading *.rst files from the source location: %s", src_dir)

    started = time.perf_counter()

    root = Task()

    for file in sorted(src_dir.rglob("*.rst")):
        segments = file.name.split(".")[:-1]

        task = root.resolve(segments)
        task.source = file

    # noinspection DuplicatedCode
    components = (Parser,)

    app = Sphinx(srcdir=".", confdir=None, outdir=str(dest_dir), doctreedir=".", buildername="text")

    settings = OptionParser(components=components).get_default_values()

    settings.line_length_limit = 15000
    settings.report_level = 5
    settings.traceback = True
    settings.env = app.env

    builder = RstBuilder(app)
    builder.config.rst_indent = 2

    writer = StubWriter(builder)

    context = TaskContext(dest_dir, writer, settings, logger, root.total)

    root.run(context)

    logger.info(
        "Finished processing %d entries in %d seconds (successful: %d, failed: %d).",
        context.total,
        time.perf_counter() - started,
        context.successful,
        context.failed)
