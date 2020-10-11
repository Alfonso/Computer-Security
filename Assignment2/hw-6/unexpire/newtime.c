#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <dlfcn.h>
// Name: Alfonso Buono
// netID: ajb393
// RUID: 179008754
// your code for time() goes here
int test = 0;

time_t time(time_t *tloc){
    if( test == 0 ){
        // creating tm struct to format the date easily
        struct tm tm;
        memset(&tm, 0, sizeof(struct tm));

        if( strptime("2020-5-15 12:00:00", "%Y-%m-%d %H:%M:%S", &tm) == NULL ){
            printf("error setting struct\n");
            return 0;
        }

        // check if tloc is null
        if(tloc == NULL){
            tloc = (time_t*) malloc(sizeof(time_t));
        }
        *tloc = mktime(&tm);
        test = 1;
        return *tloc;
    }
    
    time_t (*new_time) (time_t* tloc);
    new_time = dlsym(RTLD_NEXT, "time");

    return new_time(tloc);

}
