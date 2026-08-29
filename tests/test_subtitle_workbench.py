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

if __name__=='__main__': unittest.main()
