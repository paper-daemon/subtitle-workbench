# Changelog

## Unreleased
- Analyze the time-shifted cues that are actually written to the cleaned SRT, instead of reporting only on the pre-shift input.
- Detect zero-duration cues introduced by large negative shifts after timestamp clamping.
- Add regression coverage proving JSON findings match the generated shifted output.

## v1.0.0
- Initial public release.
