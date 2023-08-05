/**
 * 
 * Originally from `aiortc` example. With modifications for webopencv.
 * 
 * https://github.com/aiortc/aiortc/tree/main/examples/server
 * 
 */

window.onload = function() {
    
    // get required DOM elements
    var button = document.getElementById('action'),
        video = document.getElementById('video');

    // initialize the action button
    var isVideoRunning = false;
    button.innerHTML = 'Start';
    button.addEventListener('click', function() {
        if (isVideoRunning) {
            console.log('stopping...')
            stop();
            isVideoRunning = false;
        } else {
            console.log('starting...')
            start();
            isVideoRunning = true;
        }
    })

    // get optional DOM elements
    var dataChannelLog = getElementByIdSafe('data-channel'),
        iceConnectionLog = getElementByIdSafe('ice-connection-state'),
        iceGatheringLog = getElementByIdSafe('ice-gathering-state'),
        signalingLog = getElementByIdSafe('signaling-state');

    // peer connection
    var pc = null;

    // data channel
    var dc = null, dcInterval = null;

    /**
    * Returns a dummy element if the element is not found.
    */
    function getElementByIdSafe(id, tag='p') {
        var el = document.getElementById(id);
        if (el) return el;
        return document.createElement(tag);
    }

    function createPeerConnection() {
        var config = {
            sdpSemantics: 'unified-plan'
        };

        if (getElementByIdSafe('use-stun', 'input').checked) {
            config.iceServers = [{urls: ['stun:stun.l.google.com:19302']}];
        }

        pc = new RTCPeerConnection(config);

        // register some listeners to help debugging
        pc.addEventListener('icegatheringstatechange', function() {
            iceGatheringLog.textContent += ' -> ' + pc.iceGatheringState;
        }, false);
        iceGatheringLog.textContent = pc.iceGatheringState;

        pc.addEventListener('iceconnectionstatechange', function() {
            iceConnectionLog.textContent += ' -> ' + pc.iceConnectionState;
        }, false);
        iceConnectionLog.textContent = pc.iceConnectionState;

        pc.addEventListener('signalingstatechange', function() {
            signalingLog.textContent += ' -> ' + pc.signalingState;
        }, false);
        signalingLog.textContent = pc.signalingState;

        // connect audio / video
        pc.addEventListener('track', function(evt) {
            if (evt.track.kind == 'video')
                document.getElementById('video').srcObject = evt.streams[0];
        });

        return pc;
    }

    function negotiate() {
        return pc.createOffer().then(function(offer) {
            return pc.setLocalDescription(offer);
        }).then(function() {
            // wait for ICE gathering to complete
            return new Promise(function(resolve) {
                if (pc.iceGatheringState === 'complete') {
                    resolve();
                } else {
                    function checkState() {
                        if (pc.iceGatheringState === 'complete') {
                            pc.removeEventListener('icegatheringstatechange', checkState);
                            resolve();
                        }
                    }
                    pc.addEventListener('icegatheringstatechange', checkState);
                }
            });
        }).then(function() {
            var offer = pc.localDescription;
            var codec;

            codec = getElementByIdSafe('video-codec').value || 'default';
            if (codec !== 'default') {
                offer.sdp = sdpFilterCodec('video', codec, offer.sdp);
            }

            getElementByIdSafe('offer-sdp').textContent = offer.sdp;
            return fetch('/offer', {
                body: JSON.stringify({
                    sdp: offer.sdp,
                    type: offer.type,
                    video_transform: getElementByIdSafe('video-transform').value || 'none'
                }),
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'POST'
            });
        }).then(function(response) {
            return response.json();
        }).then(function(answer) {
            getElementByIdSafe('answer-sdp').textContent = answer.sdp;
            return pc.setRemoteDescription(answer);
        }).catch(function(e) {
            alert(e);
        });
    }

    function start() {
        button.style.display = 'none';

        pc = createPeerConnection();

        var time_start = null;

        function current_stamp() {
            if (time_start === null) {
                time_start = new Date().getTime();
                return 0;
            } else {
                return new Date().getTime() - time_start;
            }
        }

        if (getElementByIdSafe('use-datachannel').checked) {
            var parameters = JSON.parse(getElementByIdSafe('datachannel-parameters').value);

            dc = pc.createDataChannel('chat', parameters);
            dc.onclose = function() {
                clearInterval(dcInterval);
                dataChannelLog.textContent += '- close\n';
            };
            dc.onopen = function() {
                dataChannelLog.textContent += '- open\n';
                dcInterval = setInterval(function() {
                    var message = 'ping ' + current_stamp();
                    dataChannelLog.textContent += '> ' + message + '\n';
                    dc.send(message);
                }, 1000);
            };
            dc.onmessage = function(evt) {
                dataChannelLog.textContent += '< ' + evt.data + '\n';

                if (evt.data.substring(0, 4) === 'pong') {
                    var elapsed_ms = current_stamp() - parseInt(evt.data.substring(5), 10);
                    dataChannelLog.textContent += ' RTT ' + elapsed_ms + ' ms\n';
                }
            };
        }

        var constraints = {
            video: true
        };

        var resolution = getElementByIdSafe('video-resolution').value;
        if (resolution) {
            resolution = resolution.split('x');
            constraints.video = {
                width: parseInt(resolution[0], 0),
                height: parseInt(resolution[1], 0)
            };
        } else {
            constraints.video = true;
        }

        navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
            stream.getTracks().forEach(function(track) {
                pc.addTrack(track, stream);
            });
            return negotiate();
        }, function(err) {
            alert('Could not acquire media: ' + err);
        });

        button.style.display = 'inline-block';
        button.innerHTML = 'Stop';
    }

    function stop() {
        button.style.display = 'none';

        // close data channel
        if (dc) {
            dc.close();
        }

        // close transceivers
        if (pc.getTransceivers) {
            pc.getTransceivers().forEach(function(transceiver) {
                if (transceiver.stop) {
                    transceiver.stop();
                }
            });
        }

        // close local audio / video
        pc.getSenders().forEach(function(sender) {
            sender.track.stop();
        });

        // close peer connection
        setTimeout(function() {
            pc.close();
        }, 500);

        button.style.display = 'inline-block';
        button.innerHTML = 'Start';
    }

    function sdpFilterCodec(kind, codec, realSdp) {
        var allowed = []
        var rtxRegex = new RegExp('a=fmtp:(\\d+) apt=(\\d+)\r$');
        var codecRegex = new RegExp('a=rtpmap:([0-9]+) ' + escapeRegExp(codec))
        var videoRegex = new RegExp('(m=' + kind + ' .*?)( ([0-9]+))*\\s*$')

        var lines = realSdp.split('\n');

        var isKind = false;
        for (var i = 0; i < lines.length; i++) {
            if (lines[i].startsWith('m=' + kind + ' ')) {
                isKind = true;
            } else if (lines[i].startsWith('m=')) {
                isKind = false;
            }

            if (isKind) {
                var match = lines[i].match(codecRegex);
                if (match) {
                    allowed.push(parseInt(match[1]));
                }

                match = lines[i].match(rtxRegex);
                if (match && allowed.includes(parseInt(match[2]))) {
                    allowed.push(parseInt(match[1]));
                }
            }
        }

        var skipRegex = 'a=(fmtp|rtcp-fb|rtpmap):([0-9]+)';
        var sdp = '';

        isKind = false;
        for (var i = 0; i < lines.length; i++) {
            if (lines[i].startsWith('m=' + kind + ' ')) {
                isKind = true;
            } else if (lines[i].startsWith('m=')) {
                isKind = false;
            }

            if (isKind) {
                var skipMatch = lines[i].match(skipRegex);
                if (skipMatch && !allowed.includes(parseInt(skipMatch[2]))) {
                    continue;
                } else if (lines[i].match(videoRegex)) {
                    sdp += lines[i].replace(videoRegex, '$1 ' + allowed.join(' ')) + '\n';
                } else {
                    sdp += lines[i] + '\n';
                }
            } else {
                sdp += lines[i] + '\n';
            }
        }

        return sdp;
    }

    function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
    }
}