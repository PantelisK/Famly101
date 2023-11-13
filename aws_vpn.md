git clone git@github.com:samm-git/aws-vpn-client.git
git clone git@github.com:OpenVPN/openvpn.git
cd openvpn
git checkout release/2.5.1
nano autogen.sh

------------------------------------------------------------
#!/bin/sh

# Run autoreconf to generate configure script and other files
autoreconf --force --install || exit 1

# Optionally run autoheader if needed
autoheader || exit 1

# Inform the user about the next steps
echo "Now you are ready to run ./configure"
------------------------------------------------------------

chmod +x autogen.sh
sudo apt-get install autoconf automake libtool
./autogen.sh
./configure
make
sudo make install
openvpn --version

# Find the VPN_HOST from this page and file.

https://www.notion.so/famly/Central-routing-in-AWS-and-central-VPN-32d681508bf14c40998c4584620409e7

https://file.notion.so/f/s/d54badc3-e19b-420f-aece-d12756100e15/AWSCentralVPN.ovpn?id=484f5bcd-02da-47c4-8023-fc02a9bb3b1d&table=block&spaceId=873b2b9f-1f6f-4721-b25d-a8088c91a842&expirationTimestamp=1699747200000&signature=vAY2r0sk284E9DPPzeJp5lSjTKgO3rOZSn2wOAmJ69Q&downloadName=AWSCentralVPN.ovpn

# change vpn.conf to the file above but only keep these lines:
client
dev tun
proto udp
resolv-retry infinite
nobind
remote-cert-tls server
cipher AES-256-GCM
verb 3
<ca>
KEEP THE CERTIFICATES
</ca>

auth-nocache
reneg-sec 0

# now you can run the go server and then the script
go run server.go &
./aws-connect.sh

# you will get a prompt and  the SSO will complete

# you can test by browsing https://backoffice.familyapp.brighthorizons.co.uk/#/login