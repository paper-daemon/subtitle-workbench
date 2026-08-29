# SRT字幕QA、最初にどこを見るか

字幕の見た目を直す前に、まず時間軸が壊れていないかを見る。
誤字より先にここを確認しておくと、後で動画に当てた時の「なんかズレる」を減らしやすい。

## 最初の4項目

1. **overlap**: 前の字幕が消える前に次の字幕が始まっていないか。
2. **bad duration**: 開始時刻が終了時刻以上になっていないか。
3. **long gap**: 字幕が長時間抜けている区間がないか。
4. **long text**: 1 cue に文字を詰め込みすぎていないか。

Subtitle Workbench はこの4種類をローカルで確認できる。入力SRT自体は書き換えず、正規化後のSRTとHTML/JSONレポートを別に出す。

```bash
python subtitle_workbench.py input.srt \
  --output cleaned.srt \
  --html report.html \
  --json report.json
```

## 小さい再現テスト

4 cue の人工SRTで実際に確認したところ、4 findings が出た。

- cue 2: `overlap` 500 ms
- cue 3: `bad-duration` 10500→9500 ms
- cue 3: `long-gap` 6500 ms
- cue 4: `long-gap` 10500 ms

これは実案件の品質値ではなく、検出器の動作確認用fixtureの結果。字幕の良し悪しを自動採点するものではない。

## 自動チェックだけで終わらせない

時間軸が正常でも、読みやすさ、改行位置、固有名詞、話者切り替え、画面内テロップとの衝突は実映像を見ないと判断できない。

なので順番は、**機械チェックで壊れを拾う → 実映像で見た目と意味を確認する** が使いやすい。

- OSS: https://github.com/paper-daemon/subtitle-workbench
- Release: https://github.com/paper-daemon/subtitle-workbench/releases/tag/v1.0.0
