#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <dlfcn.h>
#include <string.h>
// Name: Alfonso Buono 
// netID: ajb393
// RUID: 179008754

// helper functions for the EC
int numFiles(char* fileNames){
    int fileNum = 1;
    int counter = 0;
    // have to go until null terminator because we
    // cannot get the length of the enviroment variable
    while( fileNames[counter] != '\0' ){
        if( fileNames[counter] == ':' )
            fileNum += 1;
        counter += 1;
    }


    return fileNum;
}

// return array of file names
char** getFiles(char* env, int fileNum){
    // initialize array with fileNum indices
    char** fileNames = (char**) malloc(fileNum * sizeof(char*));

    int fileCounter = 0;
    int idx = 0;
    int strLen = 0;
 
    // initalize each string in array
    while( env[idx] != '\0' ){
        // check if we hit a colon
        if( env[idx] == ':' ){
            //initailize string
            fileNames[fileCounter] = (char*) malloc(sizeof(char) * (strLen+1));
            fileNames[fileCounter][strLen] = '\0';
            strLen = 0;
            idx += 1;
            fileCounter += 1;
        }else{
            // still in the same word
            strLen += 1;
            idx += 1;
        }
    }

    // if fileCounter == 0 then we need to malloc
    fileNames[fileCounter] = (char*) malloc(sizeof(char) * (strLen+1));
    fileNames[fileCounter][strLen] = '\0';

    // loop through copying names
    fileCounter = 0;
    idx = 0;
    int stringIdx = 0;

    while( env[idx] != '\0' ){
        if( env[idx] == ':' ){
            fileCounter += 1;
            stringIdx = 0;
            idx += 1;
        }else{
            fileNames[fileCounter][stringIdx] = env[idx];
            idx += 1;
            stringIdx += 1;
        }
    }    

    return fileNames;
}

// create array comparison thing
int strComp(char** fileNames,int fileNum,char* file){
    int counter = 0;
    for(counter = 0; counter < fileNum; counter++){
        if( strcmp(file, fileNames[counter]) == 0 )
            return 0;
    }
    return 1;
}

// your code for readdir goes here
struct dirent* readdir(DIR* dirp){
    // get the environment variable
    char* env = getenv("HIDDEN");

    // get the num files
    int fileNum = numFiles(env);
    
    // get an array of file names
    char** fileNames = getFiles(env, fileNum);

    // create the old readdir call
    struct dirent* (*new_readdir) (DIR* dirp);
    new_readdir = dlsym(RTLD_NEXT, "readdir");

    // need to call the real readdir to see if the file exists
    int fileExists = 0;
    struct dirent* curr = new_readdir(dirp);
    while( curr != NULL ){
        // check if the file matches
        if( strComp(fileNames, fileNum, curr->d_name ) != 0 ){
            printf("%s\n",curr->d_name);
        }
        curr = new_readdir(dirp);
    }
    
}
