all:
	python bootstrap.py -d
	bin/buildout

clean:
	rm -rf bin/ eggs/ develop-eggs/ parts/ downloads/
	rm -rf build/ dist/
	rm -rf .installed.cfg
