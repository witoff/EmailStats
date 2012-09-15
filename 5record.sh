gource --highlight-all-users --seconds-per-day .3 --auto-skip-seconds .3 --max-user-speed 100 --user-scale 1  --file-idle-time 10 --stop-at-end  --user-image-dir --max-files 0 images  -1280x720 --title "Email Exchanges - Rob Witoff" --hide users,date,filenames,dirnames -o - $1 | ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i - -vcodec libx264 -preset ultrafast -crf 1 -threads 0 -bf 0 $1.mp4
