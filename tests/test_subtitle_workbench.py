import tempfile, unittest
from pathlib import Path
from subtitle_workbench import parse_srt, analyze, shifted, fmt

class T(unittest.TestCase):
    def test_parse_overlap_shift(self):
        p=Path(tempfile.mktemp(suffix='.srt'))
        p.write_text('1\n00:00:01,000 --> 00:00:03,000\nhello\n\n2\n00:00:02,500 --> 00:00:04,000\nworld\n',encoding='utf-8')
        cues=parse_srt(p); r=analyze(cues)
        self.assertEqual(len(cues),2)
        self.assertEqual(r['findings'][0]['kind'],'overlap')
        self.assertEqual(shifted(cues,500)[0]['start'],1500)
        self.assertEqual(fmt(1500),'00:00:01,500')

    def test_rejects_out_of_range_timestamp(self):
        p=Path(tempfile.mktemp(suffix='.srt'))
        p.write_text('1\n00:61:00,000 --> 00:61:01,000\nbad\n',encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'bad timestamp'):
            parse_srt(p)

if __name__=='__main__': unittest.main()
