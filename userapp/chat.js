const {location, WebSocket} = global
url = "http://192.168.100.109"
connectWebsocket() {
    this.ws = new WebSocket(url)
    this.ws.onopen = () => {
        console.log(url, 'websocket connected')
    }


    this.ws.onmessage = (msg) => {
        console.log("message received success", msg.data)
        let res = JSON.parse(msg.data)
    }

    this.ws.onerror = () => {
        console.log('message not received')
    }

    this.ws.onclose = (msg) => {
        console.log('webSocket disconncected')
        setTimeout(() => {
            this.connectWebsocket()
            }, 3000)
        }

}
