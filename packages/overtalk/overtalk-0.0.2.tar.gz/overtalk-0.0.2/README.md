# overtalk
This module computes total overtalk time in seconds in a stereo WAV file, which occurs when both channels carry audio event. In addition, it also calculates total silence time, when none of the channels contain audio event and total talk time for both channels, when audio event was detected. It can also accept two mono WAV files. Consult https://auditok.readthedocs.io for supported keyword arguments. This is meant to analyze audio files of phone conversations, one channel carrying the audio of caller and the other of the callee.

### example ###
```
>>> from overtalk import Overtalk
>>> overtalk = Overtalk(
        energy_threshold=50,
        analysis_window=0.1,
        min_dur=0.2,
        max_dur=10,
        max_silence=0.2
    )
>>> overtalk.load("sample.wav")
>>> print(overtalk.overtalk)
3.25
```
## Requirements

- Python 3.x
- Auditok

## License

MIT, see: LICENSE.txt

## Author

Szabolcs Szokoly <a href="mailto:sszokoly@pm.me">sszokoly@pm.me</a>
