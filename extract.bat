set fps=4
set inbetween=15
set /a total="%fps%*%inbetween%"

mkdir frames
ffmpeg -i black-white.mp4 -r %fps% frames/out%%04d.png

mkdir black_frames
python lain.py -i frames -o black_frames -f %inbetween%

del out.mp4
ffmpeg -framerate %total% -i black_frames/out%%04d.png -i audio.m4a -vcodec libx264 -pix_fmt yuv420p -acodec copy out.mp4

rmdir /s /q black_frames
rmdir /s /q frames