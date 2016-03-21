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
            $.ajax({
                type: 'POST',
                url: "/api/messages/",
                headers: {
                     Accept : "*/*",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data:{"robotId": currentRobotId, "userName": currentUserName, "content": "happyMessage"},
                timeout: 3000,
                success: function (result) {
                    alert("message sended");
                    console.log(result);
                },
                error: function(err) {
                    alert('Not Working' + err.message);
                    console.log(err);
                }
            });
        });

        $('#angryMessage').on('click', function () {
            console.log('press btn');
            $.ajax({
                type: 'POST',
                url: "/api/messages/",
                headers: {
                     Accept : "*/*",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data:{"robotId": currentRobotId, "userName": currentUserName, "content": "angryMessage"},
                timeout: 3000,
                success: function (result) {
                    alert("message sended");
                    console.log(result);
                },
                error: function(err) {
                    alert('Not Working' + err.message);
                    console.log(err);
                }
            });
        });




        $('#btnSendMovement').on('click', function() {
            var sliderSpeedRight = ($('#speedRight').val() == "") ? 100 : $('#speedRight').val();
            var sliderSpeedLeft = ($('#speedLeft').val() == "") ? 100 : $('#speedLeft').val();
            var direction = $('#selectDirection').val();
            var duration = ($('#inputDuration').val() == "") ? 0 : parseInt($('#inputDuration').val());
            console.log('press btn');
            console.log('sliderSpeedRight = ' + sliderSpeedRight);
            console.log('sliderSpeedLeft = ' + sliderSpeedLeft);
            console.log('direction = ' + direction);
            console.log('duration = ' + duration);
            $.ajax({
                type: 'POST',
                url: "/api/movements/",
                headers: {
                     Accept : "*/*",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data:{"direction": direction, "rightSpeed": sliderSpeedRight, "leftSpeed": sliderSpeedLeft, "duration": duration},
                timeout: 3000,
                success: function (result) {
                    alert("message sended");
                    console.log(result);
                },
                error: function(err) {
                    alert('Not Working ' + err.responseText);
                    console.log(err);
                }
            });
        })

    });
});