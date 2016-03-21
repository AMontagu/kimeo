/**
 * Created by Adrien on 21/03/2016.
 */

jQuery(function($) {
    var csrftoken = $.cookie('csrftoken');
    console.log(csrftoken);

    var currentRobotId = 0; //TODO need to be change : 0 = french robot, 1 = corean robot
    var currentUserName = "adrien"; //TODO need to be automatized xith python variable or in server side
    $(document).ready(function() {
        $('#happyMessage').on('click', function () {
            console.log('press btn');
            $.ajax({
                type: 'POST',
                url: "/api/messages",
                data:{"robotId": currentRobotId, "userName": currentUserName, "content": "happyMessage"},
                timeout: 3000,
                success: function (result) {
                    alert(result);
                    console.log(result);
                },
                error: function() {
                    alert('Not Working');
                }
            });
        });
    });
});