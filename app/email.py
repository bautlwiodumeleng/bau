
from flask_mail import Message
from app import mail

def send_reset_email(user):

    print("Inside send_reset_email()")

    token = user.get_reset_token()

    print("Token:", token)

    reset_url = (
        f"http://127.0.0.1:5000/reset_password/{token}"
    )

    msg = Message(
        "Reset Your Customer Portal Password",
        recipients=[user.email]
    )

    msg.body = f"""
Hello {user.username},

We received a request to reset the password for your Customer Portal account.

Please use the link below to create a new password:

{reset_url}

If you did not request a password reset, you can safely ignore this email.

For your security, please do not share this link with anyone.

Portal Help
Customer Portal Support
Powered by BAU Digital Technologies Pty Ltd
"""

    msg.html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
</head>

<body style="
    margin: 0;
    padding: 0;
    background-color: #f4f6f8;
    font-family: Arial, Helvetica, sans-serif;
">

    <div style="
        width: 100%;
        padding: 40px 0;
    ">

        <div style="
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        ">

            <!-- Header -->

            <div style="
                background-color: #1f4e79;
                padding: 28px 30px;
                text-align: center;
            ">

                <h1 style="
                    margin: 0;
                    color: #ffffff;
                    font-size: 28px;
                    font-weight: 600;
                ">
                    Portal Help
                </h1>

                <p style="
                    margin: 8px 0 0 0;
                    color: #e8f1f8;
                    font-size: 14px;
                ">
                    Customer Portal Support
                </p>

            </div>


            <!-- Main Content -->

            <div style="
                padding: 40px 35px;
                color: #333333;
            ">

                <h2 style="
                    margin-top: 0;
                    color: #1f2933;
                    font-size: 24px;
                ">
                    Reset Your Password
                </h2>

                <p style="
                    font-size: 16px;
                    line-height: 1.6;
                ">
                    Hello {user.username},
                </p>

                <p style="
                    font-size: 16px;
                    line-height: 1.6;
                ">
                    We received a request to reset the password
                    for your Customer Portal account.
                </p>

                <p style="
                    font-size: 16px;
                    line-height: 1.6;
                ">
                    Click the button below to create a new password.
                </p>


                <!-- Reset Button -->

                <div style="
                    text-align: center;
                    margin: 35px 0;
                ">

                    <a href="{reset_url}"
                       style="
                           display: inline-block;
                           background-color: #1f4e79;
                           color: #ffffff;
                           text-decoration: none;
                           padding: 14px 30px;
                           border-radius: 7px;
                           font-size: 16px;
                           font-weight: bold;
                       ">

                        Reset My Password

                    </a>

                </div>


                <!-- Security Notice -->

                <div style="
                    background-color: #f8f9fa;
                    border-left: 4px solid #1f4e79;
                    padding: 15px 18px;
                    margin-top: 25px;
                ">

                    <p style="
                        margin: 0;
                        font-size: 14px;
                        line-height: 1.6;
                        color: #555555;
                    ">

                        <strong>Security notice:</strong><br>

                        If you did not request a password reset,
                        you can safely ignore this email.
                        Please do not share this password-reset
                        link with anyone.

                    </p>

                </div>


                <!-- Fallback Link -->

                <p style="
                    margin-top: 30px;
                    font-size: 13px;
                    line-height: 1.6;
                    color: #777777;
                ">

                    If the button does not work, copy and paste
                    the following link into your browser:

                </p>

                <p style="
                    word-break: break-all;
                    font-size: 12px;
                    color: #1f4e79;
                ">

                    {reset_url}

                </p>

            </div>


            <!-- Footer -->

            <div style="
                background-color: #f4f6f8;
                padding: 25px 30px;
                text-align: center;
            ">

                <p style="
                    margin: 0;
                    color: #555555;
                    font-size: 14px;
                    font-weight: bold;
                ">
                    Portal Help
                </p>

                <p style="
                    margin: 6px 0 0 0;
                    color: #777777;
                    font-size: 13px;
                ">
                    Customer Portal Support
                </p>

                <p style="
                    margin: 10px 0 0 0;
                    color: #777777;
                    font-size: 12px;
                ">
                    Powered by BAU Digital Technologies Pty Ltd
                </p>

            </div>

        </div>

    </div>

</body>
</html>
"""

    print("About to call mail.send()")

    mail.send(msg)

    print("mail.send() completed")

