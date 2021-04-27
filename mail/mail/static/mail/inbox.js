document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(reply = false, id = 1) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#show-mail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  if (reply == true) {
    fetch(`/emails/${id}`)
      .then(response => response.json())
      .then(email => {
        // Show full Email content:
        let sender = email["sender"];
        let recipient = email["recipients"];
        let subject = email["subject"];
        let timestamp = email["timestamp"];
        let body = email["body"];

        // Fill-in composition 
        document.querySelector('#compose-recipients').value = recipient;
        document.querySelector('#compose-subject').value = `Re: ${subject}`;
        document.querySelector('#compose-body').value = `On ${timestamp} ${sender} wrote: ${body}`;

      })
  } else {
    // Clear out composition 
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }
};

function view_email(mailbox, id) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#show-mail-view').style.display = 'block';

  //Get email and create a div element out of it.
  document.querySelector('#show-mail-view').innerHTML = '';

  //append respective buttons:
  //Create Archive Button
  if (mailbox === 'archive') {
    //Create Archive Button
    const button = document.createElement('button');
    button.innerText = 'Un-Archive';
    button.addEventListener('click', () => {
      //Archive the email if a user clicks the button.
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: false
        })
      })
      load_mailbox('inbox');
    })
    document.querySelector('#show-mail-view').append(button);

  } else if (mailbox === 'inbox') {
    //create archive button
    const button = document.createElement('button');
    button.innerText = 'Archive';
    button.addEventListener('click', () => {
      //Archive the email if a user clicks the button.
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: true
        })
      })
      load_mailbox('inbox');
    })
    document.querySelector('#show-mail-view').append(button);

    //create reply button
    const reply_button = document.createElement('button');
    reply_button.innerText = 'Reply';
    reply_button.addEventListener('click', () => {
      //allow editing of email:
      compose_email(true, id);
    })
    document.querySelector('#show-mail-view').append(reply_button);

  }
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      // Show full Email content:
      let sender = email["sender"];
      let recipient = email["recipients"];
      let subject = email["subject"];
      let timestamp = email["timestamp"];
      let body = email["body"];

      const element = document.createElement('div');
      element.innerHTML = `<strong>Time: </strong>${timestamp}<br><strong>Sender: </strong>${sender}<br><strong>Sent to: </strong>${recipient}<br><strong>Subject </strong>${subject}<br><strong>Message: </strong>${body}<br>`;
      document.querySelector('#show-mail-view').append(element);
    })
  //Mark email read = true after user clicks on it.
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
};

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#show-mail-view').style.display = 'none';

  if (mailbox === 'inbox') {
    fetch('/emails/inbox')
      .then(response => response.json())
      .then(emails => {
        // Print emails
        console.log(emails);
        // alert(`These are the emails is ${emails}`);
        emails.forEach(function (mail) {
          const element = document.createElement('div');
          element.style.border = "solid";
          element.addEventListener('click', () => {
            //load full view of email here along with put request (which is included in view email function):
            let id = mail["id"];
            view_email(mailbox, id);
          });
          let from = mail["sender"];
          let subject = mail["subject"];
          let body = mail["body"];
          element.innerHTML = `<strong>From: </strong>${from}<br><strong>Subject </strong>${subject}<br><strong>Message: </strong>${body}<br>`;

          //check to see if it has been read or not
          if (mail["read"]) {
            element.style.backgroundColor = 'lightgray';
          }

          document.querySelector('#emails-view').append(element);
        });
      });
  }
  if (mailbox === 'sent') {
    fetch('/emails/sent')
      .then(response => response.json())
      .then(emails => {
        // Print emails
        console.log(emails);
        // alert(`These are the emails is ${emails}`);
        emails.forEach(function (mail) {
          const element = document.createElement('div');
          element.style.border = "solid";
          element.addEventListener('click', () => {
            element.style.backgroundColor = "lightgray";
          });
          let to = mail["recipients"];
          let subject = mail["subject"];
          let body = mail["body"];
          element.innerHTML = `<strong>Sent to: </strong>${to}<br><strong>Subject </strong>${subject}<br><strong>Message: </strong>${body}<br>`;
          element.addEventListener('click', () => {
            //load full view of email here along with put request (which is included in view email function):
            let id = mail["id"];
            view_email(mailbox, id);
          });
          document.querySelector('#emails-view').append(element);
        })
      })
  }

  if (mailbox === 'archive') {
    fetch('/emails/archive')
      .then(response => response.json())
      .then(emails => {
        // Print emails
        console.log(emails);
        // alert(`These are the emails is ${emails}`);
        emails.forEach(function (mail) {
          const element = document.createElement('div');
          element.style.border = "solid";
          element.addEventListener('click', () => {
            element.style.backgroundColor = "lightgray";
          });
          let from = mail["sender"];
          let to = mail["recipients"];
          let subject = mail["subject"];
          let body = mail["body"];
          element.innerHTML = `<strong>Sender: </strong>${from}<br><strong>Sent to: </strong>${to}<br><strong>Subject </strong>${subject}<br><strong>Message: </strong>${body}<br>`;
          element.addEventListener('click', () => {
            //load full view of email here along with put request (which is included in view email function):
            let id = mail["id"];
            view_email(mailbox, id);
          });
          document.querySelector('#emails-view').append(element);
        });
      });
  }

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
};