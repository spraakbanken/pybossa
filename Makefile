setup-translations:
	cd pybossa; ln -s themes/spraakbanken/translations

setup-pybossa-js:
	mv -v pybossa/themes/spraakbanken/static/js/pybossa/pybossa.{js,js.orig}
	sed "s/var url = '\/'/var url = '\/ws\/tools\/crowd-tasking\/'/" pybossa/themes/spraakbanken/static/js/pybossa/pybossa.js.orig > pybossa/themes/spraakbanken/static/js/pybossa/pybossa.js
