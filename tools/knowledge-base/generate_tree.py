"""Write the compact docs index for the local uiflow2-coder skill copy."""

from pathlib import Path

from sync_uiflow2_skill import LOCAL_SKILL_DIR, compact_doc_index


TARGET_DIR = LOCAL_SKILL_DIR / "docs"
OUTPUT_FILE = LOCAL_SKILL_DIR / "file_tree.txt"


def main() -> None:
    if not TARGET_DIR.is_dir():
        raise FileNotFoundError(f"Skill docs directory not found: {TARGET_DIR}")
    OUTPUT_FILE.write_text(compact_doc_index(TARGET_DIR, "docs"), encoding="utf-8", newline="\n")
    print(f"Compact docs index saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
