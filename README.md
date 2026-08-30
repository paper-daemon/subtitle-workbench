# Subtitle Workbench

SRT字幕を読み込み、重なり・長すぎる空白・不正な時間・長文をチェックしながら、番号正規化と一括タイムシフトまで行う無料OSSです。

```bash
python subtitle_workbench.py input.srt --output cleaned.srt --shift-ms 500 --html report.html --json report.json
```

## できること
- SRTの読み込みと番号正規化
- 字幕同士の時間重複を検出
- 5秒超の空白を検出
- 開始 >= 終了の不正cueを検出
- 長すぎる字幕テキストを検出
- ミリ秒単位で一括タイムシフト
- HTML / JSONレポート

Python 3.10+ / 外部ライブラリ不要 / MIT License。
- BOOTH 0円DL: https://amase-memo.booth.pm/items/8778719
- 作者サイト: https://paper-daemon.github.io/

## 入力境界

非空のSRT cue blockに `-->` を含むtiming lineが無い場合は、cueを黙って捨てずエラー終了します。エラー時はcleaned SRTやreportを部分生成しません。

## Shifted-output QA boundary

`--shift-ms` を使った場合、HTML/JSON reportは入力元ではなく**実際に書き出すshift後のcue**を解析します。大きな負shiftで開始/終了が0msへclampされ、出力SRTにzero-duration cueが生じた場合も `bad-duration` として検出します。
