srcPath = src/
serviceSrc = service/
service = playVideo.service

executable = playVideo_withTrigger.sh

installationPath = $(HOME)/Desktop/videoPlayer_withTrigger/
servicePath = $(HOME)/.config/systemd/user/

all: install

install:
	mkdir -p $(installationPath)
	cp -vf $(srcPath)* $(installationPath)
	chmod +x $(installationPath)$(executable)
	
	mkdir -p $(servicePath)
	cp -vf $(serviceSrc)$(service) $(servicePath)$(service)
	
	systemctl --user daemon-reload
	systemctl --user enable $(service)

	pip install pynput	
	
	sudo apt-get update && sudo apt-get install -y libdbus-1{,-dev}
	sudo apt-get install libglib2.0-dev
	sudo apt install -y libdbus-1-3 libdbus-1-dev
	sudo pip3 install omxplayer-wrapper

uninstall:
	systemctl --user stop $(service)
	systemctl --user disable $(service)
	rm -vf $(servicePath)$(service)
	systemctl --user daemon-reload
	systemctl --user reset-failed
	
	rm -rvf $(installationPath)

remove:
	rm -vf $(servicePath)$(service)
	rm -rvf $(installationPath)