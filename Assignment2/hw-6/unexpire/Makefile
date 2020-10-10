all:	newtime.so

newtime.so:	newtime.c
	gcc -shared -fPIC newtime.c -o newtime.so -ldl

clean:
	rm -f newtime.so *.o

test:	all
	export LD_PRELOAD=$$PWD/newtime.so; ./unexpire
