function start_phone(caller, callee, autocall = false) {
    var video_out = document.getElementById('vid-box');
    $('#vid-box').empty();
    var video_thumb = document.getElementById('vid-thumb');
    $('#vid-thumb').empty();
    var phone = window.phone = PHONE({
        number: caller + '-incall',
        publish_key: 'pub-c-84d6b42f-9d4d-48c1-b5a7-c313289e1792',
        subscribe_key: 'sub-c-2ebd9ad8-6cdb-11e8-902b-b2b3cb3accda',
        ssl: true
    });
    var ctrl = window.ctrl = CONTROLLER(phone);
    ctrl.ready(() => {
        if (autocall) ctrl.dial(callee + '-incall')
    });
    ctrl.receive(session => {
        session.connected(session => {
            $('#videoCallModal').modal({
                closable: false
            }).modal('show');
            $('#vid-box').empty();
            $('#vid-thumb').empty();
            ctrl.addLocalStream(video_thumb);
            video_out.appendChild(session.video);
        });
        session.ended(session => {
            $('#vid-box').empty();
            $('#vid-thumb').empty();
            phone.unsubscribe();
            ctrl.unsubscribe();
            delete ctrl;
            delete phone;
            $('#videoCallModal').modal('hide')
        })
    });
    ctrl.videoToggled((session, isEnabled) => {
        ctrl.getVideoElement(session.number).toggle(isEnabled);
    });
    ctrl.audioToggled((session, isEnabled)=> {
        ctrl.getVideoElement(session.number).css('opacity', isEnabled ? 1: 0.75);
    });
    $('#endCallButton').click(() => {
        if (phone) ctrl.hangup();
    });
    $('#muteCallButton').click(() => {
        if (ctrl) {
            const audio = ctrl.toggleAudio();
            if (!audio) $('#muteCallButton').html('' +
                '<i class="unmute icon"></i>\n' +
                'Unmute');
            else $('#muteCallButton').html('' +
                '<i class="mute icon"></i>\n' +
                'Mute');
        }
    });
    $('#pauseCallButton').click(() => {
        if (ctrl) {
            const video = ctrl.toggleVideo();
            if (!video) $('#pauseCallButton').html('' +
                '<i class="play icon"></i>\n' +
                'Play');
            else $('#pauseCallButton').html('' +
                '<i class="pause icon"></i>\n' +
                'Pause');
        }
    });
}