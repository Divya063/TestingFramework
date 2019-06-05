# copy test files to eos/user/u/user2/ and checks if eos directory is present
if [ "$2" = "EOS" ];then
	if [ -d "eos" ]; then
		#to easily switch between use2 and root
		sudo -u user2 echo "directory exists"
		sudo -u user2 cp -r tests/ eos/user/u/user2/
		echo "Started"
		python3 eos/user/u/user2/tests/run.py $1 $2
		echo "Finished"
	fi	
fi
