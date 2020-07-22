# About
Python script to forward emails using Gmail.

## Reason
As Gmail doesn't allow to forward multiple emails at once, I've created this script to help me do it.

## Description
The script makes use of `imaplib` and `smtplib` libraries that are built-in in python.

## Usage
To use the script there are a few changes you need to make:
1. Change the `USERNAME` and the `PASSWORD` for your email account.
2. Gmail, fortunately, by default, doesn't allow IMAP connections, as it is considered risky and unsecure. 
You will have to enable this manually. Google `gmail enable less secure apps` and you'll find a way. 
Also, if you'll try the script before enabling "Less secure apps", 
Gmail will send you an email describing the problem and will show you the way to enable it.
3. Change the `SEARCH_CRITERIA` according to your needs.
You can find more documentation for this here: [search command documentation](https://tools.ietf.org/html/rfc3501#section-6.4.4)
4. Don't forget to disable `less secure apps` when you're done, for your safey.

## Considerations
This script creates a new SMTP connection for each email forwarding. 
Gmail has lots of limits, among which, limits on how many emails you can send per minute or per day.
I've also figured that Gmail didn't manage to execute each forward command when many commands were sent consecutively.

You can disable this limitation on your own and try sending more emails during a single connection,
if you don't have lost of emails.
I had 200+ emails and this is what worked for me.
I've also enabled a 5 seconds time delay between each forward command, but you can easily change it.
The constant name is `TIME_DELAY`.

## Resources
Following articles can help get more knowledge on the topics: 
- [Reading Emails](https://www.thepythoncode.com/article/reading-emails-in-python)
- [Forwarding Emails](https://stackoverflow.com/questions/2717196/forwarding-an-email-with-python-smtplib)