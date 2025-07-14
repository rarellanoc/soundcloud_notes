# README VLC

You can burn the webm waveform with audio and subtitles with VLC using this:

```bash
vlc -I lua waveform_bars.webm :input-slave=audio.m4a --sub-file=subtitle.srt --file-caching=10000 --sout-mux-caching=10000 --video-filter=subtitles --sout="#transcode{vcodec=h264,acodec=mp4a,soverlay,scodec=subt,sub-filter=packetizer_input}:standard{access=file,mux=mp4,dst=output.mp4}"
```
