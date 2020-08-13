# Fuck RegEx, fuck TOML parsing, fuck good build scripts. 
# Let's bump version numbers on the relevant files the easy and flimsy way.
import sys

ENCODING = "utf-8"


def bump_pyproject(major: int, minor: int, patch: int) -> None:
    replace(
        "pyproject.toml",
        "version",
        f'version = "{major}.{minor}.{patch}"'
    )


def bump_init(major: int, minor: int, patch: int) -> None:
    replace(
        "amongusbot/__init__.py",
        "__version__",
        f"__version__ = '{major}.{minor}.{patch}'"
    )


def bump_readme(major: int, minor: int, patch: int) -> None:
    replace(
        "README.md", 
        "pip install", 
        f"pip install https://github.com/PederHA/AmongUsBot/releases/download/{major}.{minor}.{patch}/amongusbot-{major}.{minor}.{patch}.tar.gz"
    )


def replace(filename: str, startswith: str, replacement: str) -> None:
    with open(filename, "r", encoding=ENCODING) as f:
        lines = f.read().splitlines()
        for idx, line in enumerate(lines): 
            if line.startswith(startswith):
                lines[idx] = replacement
                break
    
    with open(filename, "w", encoding=ENCODING) as f:
        f.write("\n".join(lines))


def main() -> None:
    if not len(sys.argv) > 1:
        print("Usage: bump_version.py '<major>.<minor>.<patch>'")
        exit(1)
    
    try:
        mj, mn, pt = sys.argv[1].split(".")
        major, minor, patch = int(mj), int(mn), int(pt)
    except ValueError:
        print(
            "Malformed argument. Must be in the form of'<major>.<minor>.<patch>'. "
            "Example: bump_version.py 1.0.0"
        )
        exit(1)

    bump_pyproject(major, minor, patch)
    bump_init(major, minor, patch)
    bump_readme(major, minor, patch)


if __name__ == "__main__":
    main()
