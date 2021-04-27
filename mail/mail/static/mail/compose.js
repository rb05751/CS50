document.addEventListener('DOMContentLoaded', function () {
    //Form submission handling
    const form = document.querySelector("#compose-form");
    form.addEventListener('submit', (event) => {
        let recipient = document.querySelector('#compose-recipients').value;
        let subject = document.querySelector('#compose-subject').value;
        let body = document.querySelector('#compose-body').value;
        if (recipient.length == 0 && body.length == 0) return;
        alert(`Recipients: ${recipient}`);
        send_email(recipients = recipient, subject = subject, body = body);
        load_mailbox('sent');
        event.preventDefault();

    });
    return false
});

function send_email(recipients, subject, body) {
    //Use information to send email via API request
    alert(`This is the recipients ${recipients}`);
    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body,
        })
    })
        .then((response) => response.json())
        .then(result => { // Print
            console.log(result)
        });
};