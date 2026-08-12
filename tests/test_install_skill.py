import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "install_skill.py"


class SkillInstallerTests(unittest.TestCase):
    def run_cli(self, *arguments):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_list_skills_is_sorted_and_contains_public_catalog(self):
        from abaqus_agent_demo.installer import list_skills

        names = list_skills(ROOT / "skills")
        self.assertEqual(tuple(sorted(names)), names)
        self.assertIn("abaqus-mesh", names)
        self.assertEqual(17, len(names))

    def test_list_skills_ignores_decoy_directory_without_direct_skill_file(self):
        from abaqus_agent_demo.installer import list_skills, plan_install

        with TemporaryDirectory() as directory:
            skills_root = Path(directory) / "skills"
            skills_root.mkdir()
            real_skill = skills_root / "real-skill"
            real_skill.mkdir()
            (real_skill / "SKILL.md").write_text("real", encoding="utf-8")
            decoy = skills_root / "decoy"
            decoy.mkdir()
            (decoy / "README.md").write_text("not a skill", encoding="utf-8")

            self.assertEqual(("real-skill",), list_skills(skills_root))
            with self.assertRaisesRegex(ValueError, "unknown skill"):
                plan_install(skills_root, "decoy", Path(directory) / "target")

    def test_list_skills_ignores_symlinked_skill_directory_when_supported(self):
        from abaqus_agent_demo.installer import list_skills, plan_install

        with TemporaryDirectory() as directory:
            skills_root = Path(directory) / "skills"
            skills_root.mkdir()
            real_skill = skills_root / "real-skill"
            real_skill.mkdir()
            (real_skill / "SKILL.md").write_text("real", encoding="utf-8")
            linked_skill = skills_root / "linked-skill"
            try:
                linked_skill.symlink_to(real_skill, target_is_directory=True)
            except (NotImplementedError, OSError) as error:
                self.skipTest(f"symlink creation denied: {error}")

            self.assertEqual(("real-skill",), list_skills(skills_root))
            with self.assertRaisesRegex(ValueError, "unknown skill"):
                plan_install(skills_root, "linked-skill", Path(directory) / "target")

    def test_plan_contains_explicit_paths_and_plan_time_collision(self):
        from abaqus_agent_demo.installer import plan_install

        with TemporaryDirectory() as directory:
            target = Path(directory)
            plan = plan_install(ROOT / "skills", "abaqus-mesh", target)
            self.assertEqual("abaqus-mesh", plan.skill_name)
            self.assertEqual(ROOT / "skills" / "abaqus-mesh", plan.source)
            self.assertEqual(target / "abaqus-mesh", plan.destination)
            self.assertFalse(plan.collision)
            plan.destination.mkdir()
            self.assertTrue(plan_install(ROOT / "skills", "abaqus-mesh", target).collision)

    def test_unknown_skill_is_rejected_without_modifying_target(self):
        from abaqus_agent_demo.installer import plan_install

        with TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            with self.assertRaisesRegex(ValueError, "unknown skill"):
                plan_install(ROOT / "skills", "not-a-public-skill", target)
            self.assertFalse(target.exists())

    def test_dry_run_does_not_copy_or_create_target(self):
        from abaqus_agent_demo.installer import execute_install, plan_install

        with TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            plan = plan_install(ROOT / "skills", "abaqus-mesh", target)
            self.assertFalse(execute_install(plan, apply=False))
            self.assertFalse(target.exists())

    def test_apply_copies_complete_skill_directory(self):
        from abaqus_agent_demo.installer import execute_install, plan_install

        with TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            source = ROOT / "skills" / "abaqus-mesh"
            plan = plan_install(ROOT / "skills", "abaqus-mesh", target)
            self.assertTrue(execute_install(plan, apply=True))
            copied = target / "abaqus-mesh"
            self.assertTrue((copied / "SKILL.md").is_file())
            source_files = {
                path.relative_to(source)
                for path in source.rglob("*")
                if path.is_file()
            }
            copied_files = {
                path.relative_to(copied)
                for path in copied.rglob("*")
                if path.is_file()
            }
            self.assertEqual(source_files, copied_files)
            for relative_path in source_files:
                self.assertEqual(
                    (source / relative_path).read_bytes(),
                    (copied / relative_path).read_bytes(),
                )

    def test_collision_is_rejected_without_overwrite(self):
        from abaqus_agent_demo.installer import execute_install, plan_install

        with TemporaryDirectory() as directory:
            target = Path(directory)
            destination = target / "abaqus-mesh"
            destination.mkdir(parents=True)
            marker = destination / "keep.txt"
            marker.write_text("keep", encoding="utf-8")
            plan = plan_install(ROOT / "skills", "abaqus-mesh", target)
            self.assertTrue(plan.collision)
            with self.assertRaisesRegex(FileExistsError, "already exists"):
                execute_install(plan, apply=True)
            self.assertEqual("keep", marker.read_text(encoding="utf-8"))

    def test_execute_rechecks_collision_after_plan(self):
        from abaqus_agent_demo.installer import execute_install, plan_install

        with TemporaryDirectory() as directory:
            target = Path(directory)
            plan = plan_install(ROOT / "skills", "abaqus-mesh", target)
            self.assertFalse(plan.collision)
            destination = target / "abaqus-mesh"
            destination.mkdir(parents=True)
            marker = destination / "keep.txt"
            marker.write_text("keep", encoding="utf-8")
            with self.assertRaisesRegex(FileExistsError, "already exists"):
                execute_install(plan, apply=True)
            self.assertEqual("keep", marker.read_text(encoding="utf-8"))

    def test_cli_lists_sorted_public_catalog(self):
        result = self.run_cli("--list")
        self.assertEqual(0, result.returncode, result.stderr)
        names = tuple(line for line in result.stdout.splitlines() if line)
        self.assertEqual(tuple(sorted(names)), names)
        self.assertEqual(17, len(names))

    def test_cli_dry_run_requires_target_and_does_not_copy(self):
        with TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            result = self.run_cli("abaqus-mesh", "--target", str(target))
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("DRY RUN", result.stdout)
            self.assertIn(f"Source: {ROOT / 'skills' / 'abaqus-mesh'}", result.stdout)
            self.assertIn(f"Destination: {target / 'abaqus-mesh'}", result.stdout)
            self.assertFalse(target.exists())

    def test_cli_apply_copies_skill(self):
        with TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            result = self.run_cli(
                "abaqus-mesh", "--target", str(target), "--apply"
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("APPLIED", result.stdout)
            self.assertTrue((target / "abaqus-mesh" / "SKILL.md").is_file())

    def test_cli_apply_failure_does_not_report_applied(self):
        with TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            target.write_text("target must be a directory", encoding="utf-8")
            result = self.run_cli(
                "abaqus-mesh", "--target", str(target), "--apply"
            )
            self.assertEqual(2, result.returncode)
            self.assertIn("Source:", result.stdout)
            self.assertIn("Destination:", result.stdout)
            self.assertNotIn("APPLIED", result.stdout)
            self.assertIn("error:", result.stderr)

    def test_cli_unknown_skill_returns_two_without_changes(self):
        with TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            result = self.run_cli(
                "not-a-public-skill", "--target", str(target), "--apply"
            )
            self.assertEqual(2, result.returncode)
            self.assertIn("unknown skill", result.stderr)
            self.assertFalse(target.exists())

    def test_cli_collision_returns_two_without_overwrite(self):
        with TemporaryDirectory() as directory:
            target = Path(directory)
            destination = target / "abaqus-mesh"
            destination.mkdir(parents=True)
            marker = destination / "keep.txt"
            marker.write_text("keep", encoding="utf-8")
            result = self.run_cli(
                "abaqus-mesh", "--target", str(target), "--apply"
            )
            self.assertEqual(2, result.returncode)
            self.assertIn("already exists", result.stderr)
            self.assertEqual("keep", marker.read_text(encoding="utf-8"))

    def test_cli_requires_explicit_target(self):
        result = self.run_cli("abaqus-mesh")
        self.assertEqual(2, result.returncode)
        self.assertIn("--target", result.stderr)

    def test_cli_does_not_offer_overwrite_option(self):
        result = self.run_cli("--help")
        self.assertEqual(0, result.returncode)
        self.assertNotIn("overwrite", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
