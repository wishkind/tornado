<script>

export default {
  data () {
    return {
      bstart: false,
      pusher: null
    }
  },
  created () {
    document.addEventListener("plusready", this.plusReady, false);
  },
  methods: {
    switchCamera () {
      this.pusher.switchCamera();
    },
    plusReady () {
      // 创建直播推流控件
      this.pusher = new plus.video.LivePusher("pusher", {
        url: "rtmp://testlivesdk.v0.upaiyun.com/live/upyunb"
      });
      // 监听状态变化事件
      this.pusher.addEventListener(
        "statechange",
        function (e) {
          console.log("statechange: " + JSON.stringify(e));
        },
        false
      );
    },
    ppPusher () {
      if (this.bstart) {
        this.pusher.stop();
        this.bstart = false;
      } else {
        var path = document.getElementById("path").value;
        if (path && path.length > 0) {
          this.pusher.setOptions({ url: path });
          this.pusher.start();
          this.bstart = true;
        } else {
          plus.nativeUI.toast("请输入直播服务器地址");
        }
      }
      var pp = document.getElementById("pp");
      pp.innerText = this.bstart ? "停止" : "开始";
    }
  }
}
</script>
