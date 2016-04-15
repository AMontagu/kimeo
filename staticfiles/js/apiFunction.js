/**
 * Created by Adrien on 21/03/2016.
 */

jQuery(function($) {
    var csrftoken = Cookies.get('csrftoken');
    console.log(csrftoken);

    var currentRobotId = 0; //TODO need to be change : 0 = french robot, 1 = corean robot
    var currentUserName = "adrien"; //TODO need to be automatized xith python variable or in server side

    var ipAdressOtherRobot = '0.0.0.0' //TODO when robot will have ip adresse change here for send message to other server

    $(function () {
        $.ajaxSetup({
            headers: { "X-CSRFToken": csrftoken }
        });
    });

    $(document).ready(function() {

        $('#happyMessage').on('click', function () {
            console.log('press btn');
            var data = {"robotId": currentRobotId, "userName": currentUserName, "content": "happyMessage"};
            ajaxLauncher("messages/", data);
        });

        $('#angryMessage').on('click', function () {
            console.log('press btn');
            var data = {"robotId": currentRobotId, "userName": currentUserName, "content": "angryMessage"};
            ajaxLauncher("messages/", data);
        });




        $('#btnSendMovement').on('click', function() {
            var sliderSpeedRight = ($('#speedRight').val() == "") ? 100 : $('#speedRight').val();
            var sliderSpeedLeft = ($('#speedLeft').val() == "") ? 100 : $('#speedLeft').val();
            var sliderHeadPosition = ($('#headPosition').val() == "") ? 45 : $('#headPosition').val();
            var direction = $('#selectDirection').val();
            var duration = ($('#inputDuration').val() == "") ? 0 : parseInt($('#inputDuration').val());
            var continu = false;
            console.log('press btn');
            console.log('sliderSpeedRight = ' + sliderSpeedRight);
            console.log('sliderSpeedLeft = ' + sliderSpeedLeft);
            console.log('sliderHeadPosition = ' + sliderHeadPosition);
            console.log('direction = ' + direction);
            console.log('duration = ' + duration);
            var data = {"direction": direction, "rightSpeed": sliderSpeedRight, "leftSpeed": sliderSpeedLeft, "headPosition": sliderHeadPosition, "duration": duration, "continu": continu};
            ajaxLauncher("movements/", data);
        });
        
        $('#btnForward').on('click', function() {
            var sliderSpeedRight =  200;
            var sliderSpeedLeft = 200;
            var sliderHeadPosition = 45; //useless
            var direction = "Forward";
            var duration = 10; //useless
            var continu = true;
            console.log('press btn');
            console.log('sliderSpeedRight = ' + sliderSpeedRight);
            console.log('sliderSpeedLeft = ' + sliderSpeedLeft);
            console.log('sliderHeadPosition = ' + sliderHeadPosition);
            console.log('direction = ' + direction);
            console.log('duration = ' + duration);
            console.log('continu = ' + continu);
            var data = {"direction": direction, "rightSpeed": sliderSpeedRight, "leftSpeed": sliderSpeedLeft, "headPosition": sliderHeadPosition, "duration": duration, "continu": continu};
            ajaxLauncher("movements/", data);
        });

        $('#btnBackward').on('click', function() {
            var sliderSpeedRight =  200;
            var sliderSpeedLeft = 200;
            var sliderHeadPosition = 45; //useless
            var direction = "Backward";
            var duration = 10; //useless
            var continu = true;
            console.log('press btn');
            console.log('sliderSpeedRight = ' + sliderSpeedRight);
            console.log('sliderSpeedLeft = ' + sliderSpeedLeft);
            console.log('sliderHeadPosition = ' + sliderHeadPosition);
            console.log('direction = ' + direction);
            console.log('duration = ' + duration);
            console.log('continu = ' + continu);
            var data = {"direction": direction, "rightSpeed": sliderSpeedRight, "leftSpeed": sliderSpeedLeft, "headPosition": sliderHeadPosition, "duration": duration, "continu": continu};
            ajaxLauncher("movements/", data);
        });

        $('#btnTurnRight').on('click', function() {
            var sliderSpeedRight =  200;
            var sliderSpeedLeft = 200;
            var sliderHeadPosition = 45; //useless
            var direction = "TurnRight";
            var duration = 10; //useless
            var continu = true;
            console.log('press btn');
            console.log('sliderSpeedRight = ' + sliderSpeedRight);
            console.log('sliderSpeedLeft = ' + sliderSpeedLeft);
            console.log('sliderHeadPosition = ' + sliderHeadPosition);
            console.log('direction = ' + direction);
            console.log('duration = ' + duration);
            console.log('continu = ' + continu);
            var data = {"direction": direction, "rightSpeed": sliderSpeedRight, "leftSpeed": sliderSpeedLeft, "headPosition": sliderHeadPosition, "duration": duration, "continu": continu};
            ajaxLauncher("movements/", data);
        });

        $('#btnTurnLeft').on('click', function() {
            var sliderSpeedRight =  200;
            var sliderSpeedLeft = 200;
            var sliderHeadPosition = 45; //useless
            var direction = "TurnLeft";
            var duration = 10; //useless
            var continu = true;
            console.log('press btn');
            console.log('sliderSpeedRight = ' + sliderSpeedRight);
            console.log('sliderSpeedLeft = ' + sliderSpeedLeft);
            console.log('sliderHeadPosition = ' + sliderHeadPosition);
            console.log('direction = ' + direction);
            console.log('duration = ' + duration);
            console.log('continu = ' + continu);
            var data = {"direction": direction, "rightSpeed": sliderSpeedRight, "leftSpeed": sliderSpeedLeft, "headPosition": sliderHeadPosition, "duration": duration, "continu": continu};
            ajaxLauncher("movements/", data);
        });

        $('#btnStop').on('click', function() {
            var sliderSpeedRight =  200; //useless
            var sliderSpeedLeft = 200; //useless
            var sliderHeadPosition = 45; //useless
            var direction = "Stop";
            var duration = 10; //useless
            var continu = true; //useless
            console.log('press btn');
            console.log('sliderSpeedRight = ' + sliderSpeedRight);
            console.log('sliderSpeedLeft = ' + sliderSpeedLeft);
            console.log('sliderHeadPosition = ' + sliderHeadPosition);
            console.log('direction = ' + direction);
            console.log('duration = ' + duration);
            console.log('continu = ' + continu);
            var data = {"direction": direction, "rightSpeed": sliderSpeedRight, "leftSpeed": sliderSpeedLeft, "headPosition": sliderHeadPosition, "duration": duration, "continu": continu};
            ajaxLauncher("movements/", data);
        });

        $('#turnOnLight').on('click', function() {
            var turnOn = true;
            var blink = false;
            var repeat = 1;
            var intervalBlinking = 0;
            var data = {"turnOn": turnOn, "blink": blink, "repeat": repeat, "intervalBlinking": intervalBlinking};
            ajaxLauncher("lights/", data);
        });

        $('#turnOffLight').on('click', function() {
            var turnOn = false;
            var blink = false;
            var repeat = 1;
            var intervalBlinking = 0;
            var data = {"turnOn": turnOn, "blink": blink, "repeat": repeat, "intervalBlinking": intervalBlinking};
            ajaxLauncher("lights/", data);
        });

        $('#playCuteSound').on('click', function() {
            var soundName = "cute";
            var repeat = 1;
            var data = {"soundName": soundName, "repeat": repeat};
            ajaxLauncher("sounds/", data);
        });

        $('#playOtherSound').on('click', function() {
            var soundName = "other";
            var repeat = 1;
            var data = {"soundName": soundName, "repeat": repeat};
            ajaxLauncher("sounds/", data);
        });

        $('#angryFace').on('click', function() {
            var imageName = "angry";
            var stay = true;
            var timeToStay = 1;
            var data = {"imageName": imageName, "stay": stay, "timeToStay": timeToStay};
            ajaxLauncher("screens/", data);
        });

        $('#happyFace').on('click', function() {
            var imageName = "happy";
            var stay = true;
            var timeToStay = 1;
            var data = {"imageName": imageName, "stay": stay, "timeToStay": timeToStay};
            ajaxLauncher("screens/", data);
        });

        
        
        function ajaxLauncher(url, data){
            $.ajax({
                type: 'POST',
                url: "/api/" + url,
                headers: {
                     Accept : "*/*",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data:data,
                timeout: 900000000,
                success: function (result) {
                    alert("message sended");
                    console.log(result);
                },
                error: function(err) {
                    alert('Not Working ' + err.responseText);
                    console.log(err);
                }
            });
        }

    });
});