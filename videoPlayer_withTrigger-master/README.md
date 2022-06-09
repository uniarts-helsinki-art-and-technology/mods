# Videosoitin Raspberry Pi:lle
(english: see below)


Riippuvuudet:
* omxplayer
* python


## Asennus


Avaa Terminal ja siirry kansioon videoPlayer-master

	$ cd /polku/kansioon/videoPlayer-master

Asenna makella:

	$ make install

Poistaaksesi asennuksen:

	$ make uninstall

Huom! Tämä ei poista videotiedostoa eikä ladattua videoPlayer kansiota.


## Videon tuottaminen


Suositeltu formaatti on:

* resoluutio: 	1920x1080
* muoto: 	H.264
* profiili: 	High 4.0
* frame rate: 	60 fps

Käytä esimerkiksi [Handbrake](https://handbrake.fr/)-ohjelmaa videon tuottamiseen näillä parametreilla.


## Videon laittaminen raspberry pi:lle

1. Laita videotiedosto muistitikulle. Siellä ei pidä olla muita tiedostoja, ja tiedoston ei pidä olla kansion sisällä.
2. Liitä muistitikku Raspberry Pi:hin
3. Käynnistä Raspberry Pi.
Video siirtyy Raspberry Pi:n muistikortille ja lähtee pyörimään.

Tämän jälkeen kun Raspberry Pi käynnistetään ilman muistitikkua, video lähtee automaattisesti pyörimään.

Laittaaksesi toisen videon toista sama menettely. Silloin aiemmin ladatut videot poistetaan.


## Lisätietoja

Jos muistitikulla on muita tiedostoja, käytetään aakkosjärjestyksessä ensimmäistä.

Jos tiedosto ei ole kelvollinen videotiedosto, se kopioidaan ja toistetaan silti. Jos toistaminen epäonnistuu, tarkista että oikea tiedosto ladattiin.

Muistitikku kannattaa varmuuden vuoksi irrottaa vasta, kun Raspberry Pi on sammutettu.


*****************************************************************************************************


# Video player for the Raspberry Pi


Dependencies:
* omxplayer
* python


## How to install


Download and go to the videoPlayer path
	
	$ cd /path/to/videoPlayer-master
	
Install with make:

	$ make install

To uninstall:

	$ make uninstall

Note: 'make uninstall' does not remove the loaded video or the videoPlayer folder.


## How to export a video


The recommended format is:
* Resolution:	1920x1080
* Format:	H.264
* Profile:	High 4.0
* Frame rate:	60 fps

Use, for example, [Handbrake](https://handbrake.fr/) to export video with these parameters.


## How to play the video file on the Raspberry Pi

1. Put the file on a USB drive. There should be no other files, and it should not be inside a folder.
2. Insert the USB drive to the Raspberry Pi.
3. Turn the Raspberry Pi on. The video will be copied on the Raspberry Pi local storage, and start playing.

After this the video will play automatically when the Raspberry Pi is started with no USB drive attached.

To load another video, repeat the same process. Any previously loaded files will be removed.


## Additional information

If there are multiple files on the USB drive, the first file in alphanumeric order will be used.

Any file will be used whether or not it is a valid video file. If playing fails, make sure the right file was loaded.

The USB drive should be removed only after the Raspberry Pi is turned off, just to be sure.
