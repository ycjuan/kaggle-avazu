#!/bin/sh

cd mark
make clean all
cd ..

if [ -s "mark18" ]
then 
	rm mark18
	ln -s mark/mark18 
else
	ln -s mark/mark18 
fi

ln -sf ../tr.r$1.csv .
ln -sf ../va.r$1.csv .
ln -sf ../base/tr.r$1.site.new.csv .
ln -sf ../base/tr.r$1.app.new.csv .
ln -sf ../base/va.r$1.site.new.csv .
ln -sf ../base/va.r$1.app.new.csv .

./util/count_feat.py tr.r$1.csv va.r$1.csv 2 fc.trva.r0.t2.pkl
./run/6.py app $1
./run/6.py site $1
./util/cat_submit.py va.r$1.app.submit va.r$1.site.submit bag.r$1.prd
