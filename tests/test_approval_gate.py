"""Regression checks for observable approval-boundary behavior."""

import unittest

from examples.approval_gate import decide


class ApprovalGateTests(unittest.TestCase):
    def request(self, **changes):
        record = dict(
            revision="example-v2",
            checks={"required_fields": True, "output_format": True, "destination": True},
            evaluation="pass", evaluated_revision="example-v2",
            approved_revision="example-v2",
        )
        record.update(changes)
        return decide(**record)

    def test_current_checks_and_approval_are_ready(self):
        self.assertEqual(self.request().state, "ready")

    def test_missing_revision_blocks(self):
        for value in ["", "  ", None, 2]:
            with self.subTest(revision=value):
                self.assertEqual(self.request(revision=value).state, "blocked")

    def test_missing_required_check_blocks(self):
        self.assertEqual(self.request(checks={"output_format": True}).state, "blocked")

    def test_failed_or_non_boolean_check_blocks(self):
        for value in [False, "true", 1, None]:
            with self.subTest(value=value):
                checks = {"required_fields": True, "output_format": value, "destination": True}
                self.assertEqual(self.request(checks=checks).state, "blocked")

    def test_failed_evaluation_blocks_even_with_approval(self):
        self.assertEqual(self.request(evaluation="fail").state, "blocked")

    def test_ambiguous_evaluation_needs_review_even_with_approval(self):
        self.assertEqual(self.request(evaluation="review").state, "needs_human_review")

    def test_unknown_evaluation_blocks(self):
        self.assertEqual(self.request(evaluation="probably fine").state, "blocked")

    def test_stale_evaluation_blocks_even_with_current_approval(self):
        self.assertEqual(self.request(evaluated_revision="example-v1").state, "blocked")

    def test_missing_approval_requires_review(self):
        self.assertEqual(self.request(approved_revision=None).state, "needs_human_review")

    def test_edit_after_approval_requires_new_review(self):
        self.assertEqual(self.request(approved_revision="example-v1").state, "needs_human_review")


if __name__ == "__main__":
    unittest.main()
