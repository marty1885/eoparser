import unittest
import eoparser

parser = eoparser.eoparser()
parse = lambda s: parser.parse(s, keep_ending_marker=True)

class TestProcessing(unittest.TestCase):
        def test_tolower(self):
                self.assertEqual(eoparser.to_lower("ABCDEFGHIJKLMNOPQRSTUVZŜŬĜĤĈ"), "abcdefghijklmnopqrstuvzŝŭĝĥĉ")

        def test_xsystem(self):
                self.assertEqual(eoparser.xsystem_to_hats("naux"), "naŭ")
                self.assertEqual(eoparser.xsystem_to_hats("pomo"), "pomo")
                self.assertEqual(eoparser.xsystem_to_hats("cxar"), "ĉar")

class TestParsing(unittest.TestCase):
        def test_basic_numbers(self):
                numbers = ['nul', 'unu', 'du', 'tri', 'kvar', 'kvin', 'ses', 'sep', 'ok', 'naux', 'dek', 'mil']
                for num in numbers:
                        res = parse(num)
                        self.assertEqual(len(res), 1, f"{num} is not a single particle?")
                        self.assertEqual(res[0][1], "root")

        def test_composed_numbers(self):
                self.assertEqual(len(parse("dudek")), 2)
                self.assertEqual(len(parse("centdudekok")), 4) # cent du dek ok

        def test_basic(self):
                # Some random tests I came up
                self.assertEqual(parse("pomo"), [["pom", "root"], ["o", "pos_marker"]])
                self.assertEqual(parse("hundo"), [["hund", "root"], ["o", "pos_marker"]])
                self.assertEqual(parse("panoj"), [["pan", "root"], ["oj", "pos_marker"]])
                self.assertEqual(parse("iras"), [["ir", "root"], ["as", "pos_marker"]])
                self.assertEqual(parse("diru"), [["dir", "root"], ["u", "pos_marker"]])
                self.assertEqual(parse("saluton"), [["salut", "root"], ["on", "pos_marker"]])
                self.assertEqual(parse("librojn"), [["libr", "root"], ["ojn", "pos_marker"]])
                self.assertEqual(parse("granda"), [["grand", "root"], ["a", "pos_marker"]])
                self.assertEqual(parse("lia"), [["li", "root"], ["a", "pos_marker"]])
                self.assertEqual(parse("cxar"), [["ĉar", "word"]])
                self.assertEqual(parse("tia"), [["tia", "word"]])

        def test_malformed(self):
                self.assertRaises(ValueError, parse, "aaaaaaaaaaaaaaaaaaa")
                self.assertRaises(ValueError, parse, "panooooooooooooo")
                # eoparser parses the entire word. Not for roots
                self.assertRaises(ValueError, parse, "pom")
                self.assertRaises(ValueError, parse, "irasu") # -as -u should make no sense
                self.assertRaises(ValueError, parse, "amasas") # -as -as should make no sense


        def test_composed(self):
                self.assertListEqual(parse("patrino"), [["patr", "root"], ["in", "suffix"], ["o", "pos_marker"]])
                self.assertListEqual(parse("bopatrino")
                                     , [["bo", "prefix"], ["patr", "root"], ["in", "suffix"], ["o", "pos_marker"]])
if __name__ == '__main__':
        unittest.main()
