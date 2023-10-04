sudo apt-get update
sudo apt-get install ksh
sudo apt install libtbb-dev
sudo apt install libomp-13-dev
wget https://raw.githubusercontent.com/aguther/nmonchart/master/nmonchart
chmod +x nmonchart
sudo mv nmonchart /usr/local/bin
sh test.sh test 32 128000 32000 16
nmonchart *.nmon
