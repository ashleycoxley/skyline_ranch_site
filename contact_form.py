import smtplib
import os
from email.mime.text import MIMEText
from email.utils import formataddr


def format_contact_message(subject, sender_name, sender_email, message):
    formatted_message = """<p><b>%s</b></p>
        <p>%s</p>

        <br>
        <p>%s</p>
        <p>%s</p>
        """ % (subject, message, sender_name, sender_email)
    return formatted_message


def format_sender_confirmation(message):
    formatted_confirmation = """<p>Thanks for getting in touch with us at Skyline Ranch Equestrian Center. We'll get back to you soon!</p>

        <br>
        <p>Your message:</p>

        <br>
        <p>%s</p>

        <br>
        <p><i>This is an automated email. Please do not reply to this message.</i></p>
        """ % message
    return formatted_confirmation


def build_contact_email(system_email_formatted, skyline_manager, subject, sender_name, sender_email, message):
    contact_message = format_contact_message(subject,
                                             sender_name,
                                             sender_email,
                                             message)

    email = MIMEText(contact_message, 'HTML')
    email['Subject'] = '[Skyline Contact Form] %s' % subject
    email['From'] = system_email_formatted
    email['To'] = skyline_manager
    email.add_header('reply-to', sender_email)

    return email


def build_confirmation_email(system_email_formatted, sender_email, message):
    confirmation_message = format_sender_confirmation(message)

    email = MIMEText(confirmation_message, 'HTML')
    email['Subject'] = 'Your message to Skyline Ranch'
    email['From'] = system_email_formatted
    email['To'] = sender_email

    return email


def email_server(email, password):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    return server


def send_emails(subject, sender_name, sender_email, message):
    try:
        system_email = os.environ['SKYLINE_GMAIL_ADDRESS']
        system_password = os.environ['SKYLINE_GMAIL_PASSWORD']
        skyline_manager = os.environ['SKYLINE_MANAGER_EMAIL_ADDRESS']
    except KeyError:
        raise EnvironmentError("Environment variables for email addresses and password not set.")

    system_email_formatted = formataddr(('Skyline Ranch', system_email))

    contact_email = build_contact_email(system_email_formatted, skyline_manager, subject, sender_name, sender_email, message)
    confirmation_email = build_confirmation_email(system_email_formatted, sender_email, message)

    server = email_server(system_email, system_password)
    server.sendmail(system_email, [skyline_manager], contact_email.as_string())
    server.sendmail(system_email, [sender_email], confirmation_email.as_string())
    server.quit()
