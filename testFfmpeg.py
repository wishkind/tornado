import ffmpeg


#提取图片
ffmpeg –i test.avi –r 1 –f image2 image-%3d.jpeg        

#剪切视频
ffmpeg -ss 0:1:30 -t 0:0:20 -i input.avi -vcodec copy -acodec copy output.avi    
#-r 提取图像的频率，-ss 开始时间，-t 持续时间


#视频转换
#比如一个avi文件，想转为mp4，或者一个mp4想转为ts。 
ffmpeg -i input.avi output.mp4 
ffmpeg -i input.mp4 output.ts


#提取音频
ffmpeg -i test.mp4 -acodec copy -vn output.aac

#提取视频
ffmpeg -i input.mp4 -vcodec copy -an output.mp4

#bitrate = file size / duration 
#比如一个文件20.8M，时长1分钟，那么，码率就是： 
#3biterate = 20.8M bit/60s = 20.8*1024*1024*8 bit/60s= 2831Kbps 
#一般音频的码率只有固定几种，比如是128Kbps， 
#那么，video的就是 
#video biterate = 2831Kbps -128Kbps = 2703Kbps。
ffmpeg -i input.mp4 -b:v 2000k -bufsize 2000k output.mp4
ffmpeg -i input.mp4 -b:v 2000k -bufsize 2000k -maxrate 2500k output.mp4


#将输入的1920x1080缩小到960x540输出:
#scale=960:-1, ffmpeg会通知缩放滤镜在输出时保持原始的宽高比
ffmpeg -i input.mp4 -vf scale=960:540 output.mp4 


#只提取视频ES数据
ffmpeg –i input.mp4 –vcodec copy –an –f m4v output.h264

#为视频添加logo
ffmpeg -i input.mp4 -i iQIYI_logo.png -filter_complex overlay output.mp4 
#右上角： 
ffmpeg -i input.mp4 -i logo.png -filter_complex overlay=W-w output.mp4 
#左下角： 
ffmpeg -i input.mp4 -i logo.png -filter_complex overlay=0:H-h output.mp4 
#右下角： 
ffmpeg -i input.mp4 -i logo.png -filter_complex overlay=W-w:H-h output.mp4


#去掉视频的logo
ffmpeg -i input.mp4 -vf delogo=0:0:220:90:100:1 output.mp4 


#ffmpeg如何控制profile&level
#H.264有四种画质级别,分别是baseline, extended, main, high
#除了上面提到的，强行配置biterate，或者强行配置profile/level，还有2个参数可以控制编码效率。 
#一个是preset，一个是crf。 
#preset也挺粗暴，基本原则就是，如果你觉得编码太快或太慢了，想改改，可以用profile。 
#$preset有如下参数可用：

#ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow and placebo. 
#举3个例子吧 
ffmpeg -i input.mp4 -profile:v baseline -level 3.0 output.mp4

ffmpeg -i input.mp4 -profile:v main -level 4.2 output.mp4

ffmpeg -i input.mp4 -profile:v high -level 5.1 output.mp4




#将文件当做直播送至live
ffmpeg -re -i localFile.mp4 -c copy -f flv rtmp://server/live/streamName

#将直播媒体保存至本地文件
ffmpeg -i rtmp://server/live/streamName -c copy dump.flv


#将其中一个直播流，视频改用h264压缩，音频改用faac压缩，送至另外一个直播服务流
ffmpeg -i rtmp://server/live/originalStream -c:a libfaac -ar 44100 -ab 48k -c:v libx264 -vpre slow -vpre baseline -f flv rtmp://server/live/h264Stream

#将其中一个直播流，视频不变，音频改用faac压缩，送至另外一个直播服务流
ffmpeg -i rtmp://server/live/originalStream -acodec libfaac -ar 44100 -ab 48k -vcodec copy -f flv rtmp://server/live/h264_AAC_Stream


#将一个高清流，复制为几个不同视频清晰度的流重新发布，其中音频不变
fmpeg -re -i rtmp://server/live/high_FMLE_stream -acodec copy -vcodec x264lib -s 640×360 -b 500k -vpre medium -vpre baseline rtmp://server/live/baseline_500k -acodec copy -vcodec x264lib -s 480×272 -b 300k -vpre medium -vpre baseline rtmp://server/live/baseline_300k -acodec copy -vcodec x264lib -s 320×200 -b 150k -vpre medium -vpre baseline rtmp://server/live/baseline_150k -acodec libfaac -vn -ab 48k rtmp://server/live/audio_only_AAC_48k


#将当前摄像头及音频通过DSSHOW采集，视频h264、音频faac压缩后发布
ffmpeg -r 25 -f dshow -s 640×480 -i video=”video source name”:audio=”audio source name” -vcodec libx264 -b 600k -vpre slow -acodec libfaac -ab 128k -f flv rtmp://server/application/stream_name

#采集usb摄像头视频命令：
ffmpeg -t 20 -f vfwcap -i 0 -r 8 -f mp4 cap1111.mp4


#最简单的抓屏
ffmpeg -f gdigrab -i desktop out.mpg 

#从屏幕的（10,20）点处开始，抓取640x480的屏幕，设定帧率为5
ffmpeg -f gdigrab -framerate 5 -offset_x 10 -offset_y 20 -video_size 640x480 -i desktop out.mpg 

#ffmpeg从视频中生成gif图片
ffmpeg -i capx.mp4 -t 10 -s 320x240 -pix_fmt rgb24 jidu1.gif

  #转码为码流原始文件 
ffmpeg –i test.mp4 –vcodec h264 –s 352*278 –an –f m4v test.264          
ffmpeg –i test.mp4 –vcodec h264 –bf 0 –g 25 –s 352*278 –an –f m4v test.264  

#转码为封装文件
ffmpeg –i test.avi -vcodec mpeg4 –vtag xvid –qsame test_xvid.avi            
#-bf B帧数目控制，-g 关键帧间隔控制，-s 分辨率控制

#分离视频音频流
ffmpeg -i input_file -vcodec copy -an output_file_video　　
ffmpeg -i input_file -acodec copy -vn output_file_audio　　

#视频解复用
ffmpeg –i test.mp4 –vcodec copy –an –f m4v test.264
ffmpeg –i test.avi –vcodec copy –an –f m4v test.264


#视频封装
ffmpeg –i video_file –i audio_file –vcodec copy –acodec copy output_file
