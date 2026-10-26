from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from zipfile import BadZipFile, ZipFile

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = (ROOT / 'SKILL.md').read_text().split('```python\n', 1)[1].split('```', 1)[0]


class SkillExampleTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.source = Path(temporary.name) / 'report.docx'
        self.target = Path(temporary.name) / 'report.md'
        self.source.write_bytes((ROOT / 'examples/markitdown-sample.docx').read_bytes())

    def convert(self):
        code = EXAMPLE.replace('/absolute/path/report.docx', str(self.source))
        code = code.replace('/absolute/path/report.md', str(self.target))
        exec(compile(code, str(ROOT / 'SKILL.md'), 'exec'), {})

    def assert_rejected(self):
        before = self.source.read_bytes()
        with patch('markitdown.MarkItDown.convert_local') as converter:
            with self.assertRaises((BadZipFile, ValueError)):
                self.convert()
            converter.assert_not_called()
        self.assertFalse(self.target.exists())
        self.assertEqual(self.source.read_bytes(), before)

    def test_valid_document(self):
        before = self.source.read_bytes()
        self.convert()
        self.assertEqual(self.target.read_bytes(), (ROOT / 'examples/markitdown-sample.md').read_bytes())
        self.assertEqual(self.source.read_bytes(), before)

    def test_existing_output_is_preserved(self):
        self.target.write_text('existing content')
        with self.assertRaises(FileExistsError):
            self.convert()
        self.assertEqual(self.target.read_text(), 'existing content')

    def test_truncated_zip_is_rejected(self):
        self.source.write_bytes(b'PK\x03\x04broken archive')
        self.assert_rejected()

    def test_renamed_text_is_rejected(self):
        self.source.write_text('This is text, not a DOCX')
        self.assert_rejected()

    def test_zip_missing_document_part_is_rejected(self):
        with ZipFile(self.source, 'w') as archive:
            archive.writestr('[Content_Types].xml', '<Types/>')
        self.assert_rejected()

    def test_bad_member_crc_is_rejected(self):
        with ZipFile(self.source, 'w') as archive:
            archive.writestr('[Content_Types].xml', '<Types/>')
            archive.writestr('word/document.xml', 'unique test document data')
        self.source.write_bytes(self.source.read_bytes().replace(b'unique test document data', b'broken test document data'))
        self.assert_rejected()


if __name__ == '__main__':
    unittest.main()
