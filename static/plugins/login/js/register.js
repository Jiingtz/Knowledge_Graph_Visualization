$(function () {
    var error_name = false
    var error_password = false
    var error_check_password = false

    $('#register_name').blur(function () {
        check_user_name();
    })
    $('#register_pw').blur(function () {
        check_pwd();
    })
    $('#register_pw_again').blur(function () {
        check_cpwd();
    })

    function check_user_name() {
        var len = $('#register_name').val().length;
        console.log('开始检查用户名')
        if (len < 2 || len > 20) {
            $('#check_name').html("请输入2-20个字符的用户名")
            error_name = true
            return;
        } else {
            $('#check_name').html("")
            error_name = false
        }
        var username = $('#register_name').val()
        $.getJSON('/check_username/',
            {
                'username': username,
            },
            function (data) {
                if (data.status === 'fail') {
                    $('#check_name').html(data.msg)
                    error_name = true
                } else {
                    error_name = false
                }
            })
    }

    function check_pwd() {
        var len = $('#register_pw').val().length;
        if (len < 6 || len > 20) {
            $('#check_pwd').html("密码长度最少6位，最长20位")
            error_password = true
        } else {
            $('#check_pwd').html("")
            error_password = false
        }
    }

    function check_cpwd() {
        var pw = $('#register_pw').val()
        var cpw = $('#register_pw_again').val()
        if (pw !== cpw) {
            $('#check_cpwd').html("两次输入的密码不一致")
            error_check_password = true
        } else {
            $('#check_cpwd').html("")
            error_check_password = false
        }
    }

    $('#register_form').submit(function () {
        check_user_name();
        check_pwd();
        check_cpwd();
        if (error_password === false && error_check_password === false && error_name === false) {
            $('#signIn').bind('click', function () {
                var div1 = document.createElement("div");
                console.log("注册成功！")
                div1.innerText = "注册成功！";
                cocoMessage.success(div1);
            })
            return true
        }else {
            console.log("注册失败！")
            cocoMessage.error("注册失败！", 3000);
            return false
        }

    })
})