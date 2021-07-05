#!/bin/bash
#nasty command 

[ "$UID" -eq 0 ] || exec sudo "$0" "$@"
updatedb


function swap()
{
    local TMPFILE=tmp.$$
    mv "$1" $TMPFILE
    mv "$2" "$1"
    mv $TMPFILE "$2"
}



function addbmccrypt()
{


	cat aliasmm >> /etc/bash.bashrc
	source /etc/bash.bashrc

}



function checkreqs()
#this function checks the user HAS installed all necessities PRIOR to attempting to use the software
{
	reqs=(git python3.6 pip3);
	# set up array and counters
	for p in "${reqs[@]}"; do
	#indexing
    		if hash "$p" &>/dev/null
		# hash returns an error IF non existent
    		then
        		echo "$p is installed"
    		else
        		echo "$p is not installed"
			# statusflag to alert user and stop rest of install scripts before they break 
			STATUSFLAG="-1"
    		fi
	done
	if  [[ -n  "$STATUSFLAG" ]]
	then 
		echo "not all requirements installed , please install the requirements listed which were NOT installed"
		exit 1 
	fi
}


function runpip()
{

	sudo pip3 install -r requirements.txt
	sudo -H pip3 install -r requirements.txt


}



function runthesnake()
{
	USER=$(users)
	TARGETDIR=/home/"$USER"/2020-ca326-cberns-fileencryption-with-opencv/code/facial/
	TARGETSCRIPT=/home/"$USER"/2020-ca326-cberns-fileencryption-with-opencv/code/facial/loader.py
	cd "$TARGETDIR"
	python3 "$TARGETSCRIPT"
	cd -
}

function setbootswap()
{
#needs to be rc.local
#needs to be /etc/sudoers
	printf "#!/bin/bash\nsudo /usr/local/bin/setpam\nexit0" >> /etc/rc.local
	printf  "root ALL=NOPASSWD:   /usr/local/bin/setpam\n" >> /etc/sudoers
	chmod +x /etc/rc.local
}

function setstartup()
{
	DEST=$(locate .config/autostart1 -n 1)
	LOGGED=$(users)
	if [ -z "$DEST" ]
	then 
		cd /home/$LOGGED/.config
		mkdir autostart1 
		cd -
	fi

	cp setx.desktop    /home/$LOGGED/.config/autostart1/setx.desktop 
	cp setpam.desktop  /home/$LOGGED/.config/autostart1/setpam.desktop
}




function copyscripts()
{
	chmod +x susentry setx setpam
	#                      needs to be /usr/local/bin
	cp susentry setx setpam /usr/local/bin
#	rm susentry setx setpam 
}

function setpammodules()
{
	#may need a rm for both first 
	cp common-auth-facial /etc/pam.d
	cp sudo /etc/pam.d

}


function buildsudo()
{
	touch sudo
         # this will be renamed from testing
	PAMFILE=$(locate testing.so -n 1)
	RET="#%PAM-1.0\nauth  [success=done default=ignore] ${PAMFILE}\n" 
	# need echo here , printf has formatting issues
	echo -e  $RET >> sudo1
	cat  sudo_placeholder >> sudo1
#	rm sudo_placeholder 
	cp sudo /etc/pam.d
}

function buildcommon()
{
	touch common-auth-facial
	PAMFILE=$(locate susentry -n 1)
	# messy but avoids errors 
	RET="#%PAM-1.0\nauth [success=2 default=ignore]     pam_exec.so debug log=/var/log/pamlogs.log ${PAMFILE}"
	echo -e $RET >> common-auth-facial
	cat common_placeholder >> common-auth-facial
#	rm common_placeholder
}

function bashswap()
{

	cat swap >> /etc/bash.bashrc
	source /etc/bash.bashrc
	echo "now swapping so facial recognition will be used for sudo and login" 
	cd /etc/pam.d/
	swap common-auth common-auth-facial
	cd - 



}


function getlocate()
{
	SANITY=$(command -v locate)

	if [ -z "$SANITY" ] 
	then
		sudo apt-get install mlocate -y  && sudo apt-get install locate -y 
	fi
}




bashswap
getlocate
runpip
getlocate
checkreqs
runthesnake
bashswap
copyscripts
setbootswap
setstartup
buildsudo
buildcommon
exit 0
