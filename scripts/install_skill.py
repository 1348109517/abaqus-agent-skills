from pathlib import Path
import argparse
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from abaqus_agent_demo.installer import execute_install, list_skills, plan_install


SKILLS_ROOT = ROOT / "skills"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="List or safely install a public Abaqus skill."
    )
    parser.add_argument("--list", action="store_true", dest="list_only")
    parser.add_argument("skill_name", nargs="?")
    parser.add_argument("--target", type=Path)
    parser.add_argument("--apply", action="store_true")
    return parser


def main(argv=None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)

    if args.list_only:
        if args.skill_name or args.target is not None or args.apply:
            parser.error("--list cannot be combined with a skill, --target, or --apply")
        for name in list_skills(SKILLS_ROOT):
            print(name)
        return 0

    if args.skill_name is None:
        parser.error("a skill_name is required unless --list is used")
    if args.target is None:
        parser.error("--target is required for an installation plan")

    try:
        plan = plan_install(SKILLS_ROOT, args.skill_name, args.target)
        print(f"Plan: {plan.skill_name}")
        print(f"Source: {plan.source}")
        print(f"Destination: {plan.destination}")
        applied = execute_install(plan, apply=args.apply)
    except (ValueError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if applied:
        print(f"APPLIED: {plan.skill_name}")
    else:
        print(f"DRY RUN: {plan.skill_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
