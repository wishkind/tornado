<script>

export default {
  data () {
    return {
      bstart: false,
      pusher: null
    }
  },
  created () {
    document.addEventListener('plusready', this.plusReady, false);
  },
  methods: {
    plusReady () {
      // 创建视频播放控件
      video = new plus.video.VideoPlayer('video', {
        src: 'http://192.168.100.14:8080/live/hello.m3u8'
      });
      video.addEventListener('play', function () {
        updatePlaying(true);
      }, false);
      video.addEventListener('pause', function () {
        updatePlaying(false);
      }, false);
    },
    // 播放
    playVideo1 () {
      var path = document.getElementById('path1').value;
      if (path && path.length > 0) {
        video.setOptions({ src: path });
        video.play();
      }
    }
    , playVideo2 () {
      var path = document.getElementById('path2').value;
      if (path && path.length > 0) {
        video.setOptions({ src: path });
        video.play();
      }
    },
    // 更新为播放状态
    updatePlaying (play) {
      playing = play;
      document.getElementById('pp').innerText = playing ? '暂停' : '播放';
    },
    // 播放/暂停
    ppVideo () {
      playing ? video.pause() : video.play();
    }
  }
}
</script>
