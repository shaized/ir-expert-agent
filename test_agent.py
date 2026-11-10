import copy
import json
from pathlib import Path
import unittest

from agent import analyze


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(Path(__file__).with_name("example.json").read_text())

    def test_action_remains_a_proposal(self):
        action = analyze(self.data)["findings"][-1]
        self.assertEqual(action["type"], "proposal_only")
        self.assertEqual(action["execution"], "not_performed")

    def test_unknown_evidence_reference_is_rejected(self):
        self.data["proposed_actions"][0]["evidence_ids"] = ["missing"]
        with self.assertRaises(ValueError):
            analyze(self.data)

    def test_action_without_evidence_is_rejected(self):
        self.data["proposed_actions"][0]["evidence_ids"] = []
        with self.assertRaises(ValueError):
            analyze(self.data)

    def test_fractional_timeline_is_chronological(self):
        self.data["evidence"][0]["timestamp"] = "2026-01-15T10:00:00.1Z"
        self.data["evidence"][1]["timestamp"] = "2026-01-15T12:00:00+02:00"
        self.assertEqual(
            [row["id"] for row in analyze(self.data)["findings"][:2]], ["ev-2", "ev-1"]
        )

    def test_unknowns_survive_in_the_brief(self):
        gap = self.data["unknowns"][0]
        self.assertIn(gap, analyze(self.data)["limitations"])

    def test_duplicate_evidence_is_rejected(self):
        self.data["evidence"].append(copy.deepcopy(self.data["evidence"][0]))
        with self.assertRaises(ValueError):
            analyze(self.data)


if __name__ == "__main__":
    unittest.main()
