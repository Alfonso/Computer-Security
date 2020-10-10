all:	random myrand.so

random:	random.c
	gcc -o random random.c

myrand.so:	myrand.c
	gcc -shared -fPIC myrand.c -o myrand.so -ldl

clean:
	rm -f myrand.so random

test:	all
	@ echo "running random without our replacement of rand()"
	@ unset LD_PRELOAD
	./random
	@ echo "running random with our replacement of rand()"
	export LD_PRELOAD=$$PWD/myrand.so;./random
	@ unset LD_PRELOAD
