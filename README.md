# soundcloud_notes

A way to bookmark comments

This is way too simple, but I had this need of using soundcloud to comment my own audio files. It has this feature of poping out the comments as they happen (timestamped) 

I didn't found anything useful. MKV chapters almost made it, but there is a deceptevely more simple approach. Bookmarks and subtitles. 

So with Elmedia Player on mac (or your video player that supports bookmarks) you add one, then save all of them on a .txt and use this script to convert it to .srt

The input format is

>timestamp, comment

then your second watch has all the comments as subtitles. 



### double input

I recently added the possibility to use two different bookmark sources, like a 'conversation' of two people in one file:

>potplayer_pbt_dual_to_srt.py input1.pbt input2.pbt output.srt 
