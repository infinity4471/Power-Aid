install:
	@echo "Installing dependencies"
	sh install.sh
	@echo "Finished installing dependencies"
files:
	@echo "Downloading files for database"
	wget https://www.dropbox.com/s/kn8mwyize7jv0hb/10daysData.zip?dl=0
	unzip 10daysData.zip?dl=0 -d ../tendays
	rm -rf ../tendays/__MACOSX
	rm 10daysData.zip\?dl\=0
	@echo "Downloaded files successfully"
db:
	@echo "Creating database"
	python3 init_db.py
	@echo "Database has been created"
test:
	@echo "Running tests"
	sh run_tests.sh
	@echo "Finished tests"
run:
	python3 app.py

clean:
	@echo "Cleaning up data"
	rm -rf ../tendays
	@echo "Finished cleaning up"

all: install files db run
