# Fuck RegEx, fuck TOML parsing, fuck DRY principles. Let's brute force.
import sys

ENCODING = "utf-8"

def bump_pyproject(major: int, minor: int, patch: int) -> None:
    fname = "pyproject.toml"
    
    with open(fname, "r", encoding=ENCODING) as f:
        lines = f.read().splitlines()
        for idx, line in enumerate(lines):
            if line.startswith("version"):
                lines[idx] = f'version = "{major}.{minor}.{patch}"'
                break
    
    with open(fname, "w", encoding=ENCODING) as f:
        f.write("\n".join(lines))


def bump_init(major: int, minor: int, patch: int) -> None:
    fname = "amongusbot/__init__.py"
    
    with open(fname, "r", encoding=ENCODING) as f:
        lines = f.read().splitlines()
        # __version__ should be on the first line, but let's make sure we get it right
        for idx, line in enumerate(lines): 
            if line.startswith("__version__"):
                lines[idx] = f"__version__ = '{major}.{minor}.{patch}'"
                break
    
    with open(fname, "w", encoding=ENCODING) as f:
        f.write("\n".join(lines))


def bump_readme(major: int, minor: int, patch: int) -> None:
    fname = "README.md"
    
    with open(fname, "r", encoding=ENCODING) as f:
        lines = f.read().splitlines()
        # __version__ should be on the first line, but let's make sure we get it right
        for idx, line in enumerate(lines): 
            if line.startswith("pip install"):
                lines[idx] = f"pip install https://github.com/PederHA/AmongUsBot/releases/download/{major}.{minor}.{patch}/amongusbot-{major}.{minor}.{patch}.tar.gz"
                break
    
    with open(fname, "w", encoding=ENCODING) as f:
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
