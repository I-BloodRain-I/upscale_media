from subprocess import run, check_output
from os import path, listdir
from re import search

# getting a list of media files
_dirname_ = path.dirname(__file__)
files = listdir(_dirname_ + "\\Source")
print("Working started...")
# loop through each media file
for file in files:
    scale = 1 # how many times to enlarge the file

    # get media file resolution [Width, Height]
    result = str(check_output(_dirname_ + "\\ffprobe.exe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 " + _dirname_ + "\\Source\\" + file))
    size_temp = search(r'\d{3,4},\d{3,4}', result)
    size_temp = result[size_temp.start() : size_temp.end()]
    size = size_temp.split(',')

    # if the initial resolution is less than 750 px on one of the sides, increasse it by 7 times
    if int(size[0]) < 750 and int(size[1]) < 750:
        scale = 7
    # if the initial resolution is less than 1500 px on one of the sides, increasse it by 4 times
    if int(size[0]) < 1500 and int(size[1]) < 1500:
        scale = 4
    # if the initial resolution is less than 3000 px on one of the sides, increase it by 2 times
    elif int(size[0]) < 3000 and int(size[1]) < 3000:
        scale = 2

    # if the file has a .gif extension, execute the first script
    if file.find("gif") != -1:
        run(_dirname_ + '\\ffmpeg -hide_banner -v warning -i "' + _dirname_ + '\\Source\\' + file + '" -filter_complex "[0:v] ' + 
            'scale=' + str(int(size[0]) * scale) + ':-1:flags=lanczos,split [a][b]; [a] palettegen=reserve_transparent=on:transparency_color=ffffff [p]; [b][p] paletteuse" "' +
            _dirname_ + '\\Result\\' + file + '"')
        pass

    # if the file has a different extension (in this case mp4), the second script is executed
    # IMPORTANT. If you have 3 extensions (.gif, .mp4, and something else) uncomment the line below and remove "else:".
    # elif file.find("mp4") != -1:
    else:
        # since each video can have a different fps, in this area we will recognize it
        result = str(check_output(_dirname_ + '\\ffprobe -v 0 -of csv=p=0 -select_streams v:0 -show_entries stream=r_frame_rate "' + _dirname_+ '\\Source\\' + file + '"'))
        fps_temp = search(r'\d{1,3}/\d{1,3}', result)
        fps_temp = result[fps_temp.start() : fps_temp.end()]
        fps = fps_temp.split('/')

        run(_dirname_ + '\\ffmpeg -i "' + _dirname_ + '\\Source\\' + file + '" -vf scale=' + str(int(size[0]) * scale) + 'x' + str(int(size[1]) * scale) + 
            ':flags=lanczos -c:v libx264 -preset slow -crf ' + str(int(fps[0])/int(fps[1])) + ' "' + _dirname_  + '\\Result\\' + file + '')

    # output to the console when work with a particular file is completed. The line is optional and can be deleted.
    print(file + " finished.")