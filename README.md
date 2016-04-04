This is the web server for the padding oracle attack assignment used in CS 458
(Computer Security and Privacy) at the University of Waterloo.  The most recent
version of the assignment can be found
[here](https://crysp.uwaterloo.ca/courses/cs458/W16-material/a3.pdf) (the
programming section was written by me).  You can use this server to try out the
assignment for yourself.  I won't be publishing solutions to the assignment.

This web server is vulnerable to a padding oracle attack as described in [1].
The server sets a cookie named `user` which is encrypted with AES in CBC mode.
This cookie can be modified and sent back to the server, which will respond
with a 200 code if the cookie has valid padding and a 500 if it does not.  The
server is currently configured to use the NIST padding scheme described in the
assignment (and Section 4 of the linked article), but this can be changed to
several other schemes by commenting/uncommenting the appropriate lines in
crypto.py.  Note that this code uses a different hardcoded key than the actual
server used in the assignment.

The server is written for Python 2.6/2.7 and depends on
[PyCrypto](https://www.dlitz.net/software/pycrypto/) and the
[Tornado](http://www.tornadoweb.org/) web framework.  To install these
dependencies, run `pip install -r requirements.txt`.  The server can be run
with `python server.py`, and will listen on port 4555.

[1] S. Vaudenay, “[Security Flaws Induced by CBC Padding—Applications to SSL,
IPSEC,
WTLS...](https://www.iacr.org/archive/eurocrypt2002/23320530/cbc02_e02d.pdf),”
in Advances in Cryptology—EUROCRYPT 2002, 2002, pp. 534–545.
