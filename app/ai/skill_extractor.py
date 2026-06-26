import re

from app.utils.constants import SKILLS


def _skill_pattern(skill: str) -> re.Pattern[str]:
    if skill == "c++":
        return re.compile(r"c\s*\+\+", re.IGNORECASE)
    if skill == "c":
        return re.compile(r"\bc\b(?!\+\+)", re.IGNORECASE)
    if " " in skill:
        return re.compile(re.escape(skill), re.IGNORECASE)
    return re.compile(rf"\b{re.escape(skill)}\b", re.IGNORECASE)


def extract_skills(text: str) -> list[str]:
    found: set[str] = set()

    for skill in sorted(SKILLS, key=len, reverse=True):
        if _skill_pattern(skill).search(text):
            found.add(skill)

    return sorted(found)
