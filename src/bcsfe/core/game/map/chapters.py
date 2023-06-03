from typing import Any
from bcsfe.core import io


class Stage:
    def __init__(self, clear_times: int):
        self.clear_times = clear_times

    @staticmethod
    def read(data: io.data.Data) -> "Stage":
        clear_times = data.read_int()
        return Stage(clear_times)

    def write(self, data: io.data.Data):
        data.write_int(self.clear_times)

    def serialize(self) -> dict[str, Any]:
        return {
            "clear_times": self.clear_times,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> "Stage":
        return Stage(
            data["clear_times"],
        )

    def __repr__(self):
        return f"Stage({self.clear_times})"

    def __str__(self):
        return self.__repr__()


class Chapter:
    def __init__(self, selected_stage: int):
        self.selected_stage = selected_stage

    @staticmethod
    def read_selected_stage(data: io.data.Data) -> "Chapter":
        selected_stage = data.read_int()
        return Chapter(selected_stage)

    def write_selected_stage(self, data: io.data.Data):
        data.write_int(self.selected_stage)

    def read_clear_progress(self, data: io.data.Data):
        self.clear_progress = data.read_int()

    def write_clear_progress(self, data: io.data.Data):
        data.write_int(self.clear_progress)

    def read_stages(self, data: io.data.Data, total_stages: int):
        self.stages = [Stage.read(data) for _ in range(total_stages)]

    def write_stages(self, data: io.data.Data):
        for stage in self.stages:
            stage.write(data)

    def read_chapter_unlock_state(self, data: io.data.Data):
        self.chapter_unlock_state = data.read_int()

    def write_chapter_unlock_state(self, data: io.data.Data):
        data.write_int(self.chapter_unlock_state)

    def serialize(self) -> dict[str, Any]:
        return {
            "selected_stage": self.selected_stage,
            "clear_progress": self.clear_progress,
            "stages": [stage.serialize() for stage in self.stages],
            "chapter_unlock_state": self.chapter_unlock_state,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> "Chapter":
        chapter = Chapter(data["selected_stage"])
        chapter.clear_progress = data["clear_progress"]
        chapter.stages = [Stage.deserialize(stage) for stage in data["stages"]]
        chapter.chapter_unlock_state = data["chapter_unlock_state"]
        return chapter

    def __repr__(self):
        return f"Chapter({self.selected_stage}, {self.clear_progress}, {self.stages}, {self.chapter_unlock_state})"

    def __str__(self):
        return self.__repr__()


class ChaptersStars:
    def __init__(self, chapters: list[Chapter]):
        self.chapters = chapters

    @staticmethod
    def read_selected_stage(data: io.data.Data, total_stars: int) -> "ChaptersStars":
        chapters = [Chapter.read_selected_stage(data) for _ in range(total_stars)]
        return ChaptersStars(chapters)

    def write_selected_stage(self, data: io.data.Data):
        for chapter in self.chapters:
            chapter.write_selected_stage(data)

    def read_clear_progress(self, data: io.data.Data):
        for chapter in self.chapters:
            chapter.read_clear_progress(data)

    def write_clear_progress(self, data: io.data.Data):
        for chapter in self.chapters:
            chapter.write_clear_progress(data)

    def read_stages(self, data: io.data.Data, total_stages: int):
        for chapter in self.chapters:
            chapter.read_stages(data, total_stages)

    def write_stages(self, data: io.data.Data):
        for chapter in self.chapters:
            chapter.write_stages(data)

    def read_chapter_unlock_state(self, data: io.data.Data):
        for chapter in self.chapters:
            chapter.read_chapter_unlock_state(data)

    def write_chapter_unlock_state(self, data: io.data.Data):
        for chapter in self.chapters:
            chapter.write_chapter_unlock_state(data)

    def serialize(self) -> dict[str, Any]:
        return {
            "chapters": [chapter.serialize() for chapter in self.chapters],
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> "ChaptersStars":
        chapters = [Chapter.deserialize(chapter) for chapter in data["chapters"]]
        return ChaptersStars(chapters)

    def __repr__(self):
        return f"ChaptersStars({self.chapters})"

    def __str__(self):
        return self.__repr__()


class Chapters:
    def __init__(self, chapters: list[ChaptersStars]):
        self.chapters = chapters

    @staticmethod
    def read(data: io.data.Data, read_every_time: bool = True) -> "Chapters":
        total_stages = 0
        total_chapters = 0
        total_stars = 0
        if read_every_time:
            total_chapters = data.read_int()
            total_stars = data.read_int()
        else:
            total_chapters = data.read_int()
            total_stages = data.read_int()
            total_stars = data.read_int()

        chapters = [
            ChaptersStars.read_selected_stage(data, total_stars)
            for _ in range(total_chapters)
        ]

        if read_every_time:
            total_chapters = data.read_int()
            total_stars = data.read_int()

        for chapter in chapters:
            chapter.read_clear_progress(data)

        if read_every_time:
            total_chapters = data.read_int()
            total_stages = data.read_int()
            total_stars = data.read_int()

        for chapter in chapters:
            chapter.read_stages(data, total_stages)

        if read_every_time:
            total_chapters = data.read_int()
            total_stars = data.read_int()

        for chapter in chapters:
            chapter.read_chapter_unlock_state(data)

        return Chapters(chapters)

    def write(self, data: io.data.Data, write_every_time: bool = True):
        if write_every_time:
            data.write_int(len(self.chapters))
            data.write_int(len(self.chapters[0].chapters))
        else:
            data.write_int(len(self.chapters))
            data.write_int(len(self.chapters[0].chapters[0].stages))
            data.write_int(len(self.chapters[0].chapters))
        for chapter in self.chapters:
            chapter.write_selected_stage(data)

        if write_every_time:
            data.write_int(len(self.chapters))
            data.write_int(len(self.chapters[0].chapters))
        for chapter in self.chapters:
            chapter.write_clear_progress(data)

        if write_every_time:
            data.write_int(len(self.chapters))
            data.write_int(len(self.chapters[0].chapters[0].stages))
            data.write_int(len(self.chapters[0].chapters))
        for chapter in self.chapters:
            chapter.write_stages(data)

        if write_every_time:
            data.write_int(len(self.chapters))
            data.write_int(len(self.chapters[0].chapters))
        for chapter in self.chapters:
            chapter.write_chapter_unlock_state(data)

    def serialize(self) -> dict[str, Any]:
        return {
            "chapters": [chapter.serialize() for chapter in self.chapters],
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> "Chapters":
        chapters = [ChaptersStars.deserialize(chapter) for chapter in data["chapters"]]
        tower_chapters = Chapters(chapters)
        return tower_chapters

    def __repr__(self):
        return f"Chapters({self.chapters})"

    def __str__(self):
        return self.__repr__()