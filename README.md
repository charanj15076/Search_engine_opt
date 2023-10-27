# SEO Keyword Tracker and Analyzer

## Setting up the environment
- Install the following requirements:
	- Python 3.11+
	- Geckodriver 0.33+
	- Xvfb & Firefox
	```
		FIREFOX_SETUP=firefox-setup.tar.bz2 && \
        wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-112.0.1&os=linux64" && \
        sudo tar xjf $FIREFOX_SETUP -C /opt/ && \
        sudo ln -s /opt/firefox/firefox /usr/bin/firefox && \
        rm $FIREFOX_SETUP && \
        sudo apt install libasound2 libdbus-glib-1-2:amd64
	```
- Run `pip install -r requirements.txt`
- Create a directory in api called `static`
- Run `python init.py` to download nltk data


## Deployment
- Run `ng build --configuration production` from the `app` directory
- Move files in `/dist/my-app` to the nginx static directory:
	- if applicable, also remove the whatever is on the static directory:
		```
			sudo rm -r /var/www/html/* && \
			sudo mv dist/my-app/* /var/www/html/
		```
