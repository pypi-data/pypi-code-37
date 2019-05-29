from peer_socket import PeerSocket

if __name__ == "__main__":
    addr_a = ('localhost', 5000)
    addr_b = ('localhost', 6000)

    peer_a = PeerSocket(addr_a)
    peer_b = PeerSocket(addr_b)


    def greeting(sender_addr, message):
        print(str(sender_addr) + ' said ' + message)
        return 'hello!'


    def response(message):
        print('Got response ' + message)


    event = 'GREETING'
    peer_a.on(event, greeting)
    peer_b.on(event, greeting)

    peer_a.send(addr_b, event, 'hi there!', response)
    peer_b.send(addr_a, event, 'hello sir!', response)