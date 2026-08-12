"""Plan and execute safe, no-overwrite copies of public skills."""

from dataclasses import dataclass
from pathlib import Path
import shutil


@dataclass(frozen=True)
class InstallPlan:
    skill_name: str
    source: Path
    destination: Path
    collision: bool


def _exists(path: Path) -> bool:
    """Treat dangling symlinks as collisions as well as existing paths."""

    return path.exists() or path.is_symlink()


def list_skills(skills_root: Path) -> tuple[str, ...]:
    """Return the public skill directory names in stable sorted order."""

    root = Path(skills_root)
    return tuple(
        sorted(
            path.name
            for path in root.iterdir()
            if path.is_dir()
            and not path.is_symlink()
            and (path / "SKILL.md").is_file()
            and not (path / "SKILL.md").is_symlink()
        )
    )


def plan_install(
    skills_root: Path, skill_name: str, target_root: Path
) -> InstallPlan:
    """Build an installation plan without changing the filesystem."""

    root = Path(skills_root)
    if skill_name not in list_skills(root):
        raise ValueError(f"unknown skill: {skill_name}")
    source = root / skill_name
    destination = Path(target_root) / skill_name
    return InstallPlan(
        skill_name=skill_name,
        source=source,
        destination=destination,
        collision=_exists(destination),
    )


def execute_install(plan: InstallPlan, apply: bool) -> bool:
    """Execute an installation plan, or report a dry run without changes."""

    if _exists(plan.destination):
        raise FileExistsError(f"destination already exists: {plan.destination}")
    if not apply:
        return False
    plan.destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(plan.source, plan.destination)
    return True
