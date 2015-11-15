#!/usr/bin/python

import cgi
import smtplib

from datetime import datetime

print "Content-type: text/html\n\n";

def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()

# gather data here
form = cgi.FieldStorage()

userName = form["name"].value.upper()
userEmail = form["email"].value.upper()
userComments = form["comments"].value.upper()

if userName == '':
    userName = 'None Provided'
if userEmail == '':
    userEmail = 'None Provided'
if userComments == '':
    userComments = 'None Provided'

# save feedback + info to text file
fname = '//var//www//lighttpd//feedback//feedback_'
fname += datetime.now().strftime('%Y-%m-%d__%H:%M:%S')
fname += '.txt'

with open(fname, 'w') as fs:
    fs.write('Name: ')
    fs.write(userName)
    fs.write('\n\nEmail: ')
    fs.write(userEmail)
    fs.write('\n\nComments: ')
    fs.write(userComments)


print '''<html>
        <head>
        <meta charset=utf-8 />
        <link href="../css.css" rel="stylesheet">

        <!-- Bootstrap core CSS -->
        <link href="../Bootstrap/css/bootstrap.min.css" rel="stylesheet">
        <link href="../Bootstrap/css/bootstrap-theme.min.css" rel="stylesheet">
        <link href="../theme.css" rel="stylesheet">

        <script src="../list.js"></script>
        <script src="../jquery.js"></script>

        <title>Crimson Bids</title>
        </head>
        <body>
            <div style="position: relative; left: 71%; top:115px">
                <a href="../about.html"> About</a> /
                <a href="../faq.html"> FAQ </a> /
                <a href="../feedback.html"> Send us your feedback </a>
            </div>
            <div class="container">
              <div class="page-header">
                <a href="../index.html"><img src="../logo.jpg" ><br></a>
                <h4>Quality Product Listings</h4>
              </div>
        <h2>Thank you for your feedback!</h2>
        <h5>If you had a comment that required a response, we will get back to you in less than 24 hours.</h5>
	</body>
</html>'''