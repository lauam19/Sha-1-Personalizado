import unittest
from algorithm.sha1_nl import sha1_nl, pad_message

class SHA1NLTests(unittest.TestCase):
    def test_digest_format(self):
        digest = sha1_nl("hola")
        self.assertEqual(len(digest), 40)
        int(digest, 16)

    def test_deterministic(self):
        self.assertEqual(sha1_nl("mismo texto"), sha1_nl("mismo texto"))

    def test_different_messages_usually_differ(self):
        self.assertNotEqual(sha1_nl("mensaje A"), sha1_nl("mensaje B"))

    def test_padding_is_multiple_of_64_bytes(self):
        for message in (b"", b"a", b"a" * 55, b"a" * 56, b"a" * 64):
            padded = pad_message(message)
            self.assertEqual(len(padded) % 64, 0)
            self.assertEqual(padded[-8:], (len(message) * 8).to_bytes(8, "big"))

if __name__ == "__main__":
    unittest.main()


class AnalysisTraceTests(unittest.TestCase):
    def test_analysis_contains_80_rounds_and_80_words(self):
        from algorithm.sha1_nl import sha1_nl_analysis
        report = sha1_nl_analysis(b"hola")
        self.assertEqual(len(report["blocks"]), 1)
        self.assertEqual(len(report["blocks"][0]["words"]), 80)
        self.assertEqual(len(report["blocks"][0]["rounds"]), 80)
        self.assertEqual(report["digest"], sha1_nl("hola"))

    def test_analysis_handles_multiple_blocks(self):
        from algorithm.sha1_nl import sha1_nl_analysis
        report = sha1_nl_analysis(b"a" * 100)
        self.assertEqual(report["block_count"], 2)
        self.assertEqual(sum(len(block["rounds"]) for block in report["blocks"]), 160)
