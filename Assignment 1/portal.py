import sys
import json
from json.decoder import JSONDecodeError
from os import path


def main():

    # error check argument lengths?
    if len(sys.argv) < 2:
        print('Please provide proper input')
        exit()
    elif sys.argv[1] == 'AddUser' and len(sys.argv) == 4:
        add_user( sys.argv[2], sys.argv[3] )
    elif sys.argv[1] == 'Authenticate' and len(sys.argv) == 4:
        authenticate( sys.argv[2], sys.argv[3] )
    elif sys.argv[1] == 'SetDomain' and len(sys.argv) == 4:
        set_domain( sys.argv[2], sys.argv[3] )
    elif sys.argv[1] == 'DomainInfo' and len(sys.argv) == 3:
        domain_info( sys.argv[2] )
    elif sys.argv[1] == 'SetType' and len(sys.argv) == 4:
        set_type( sys.argv[2], sys.argv[3] )
    elif sys.argv[1] == 'TypeInfo' and len(sys.argv) == 3:
        type_info( sys.argv[2] )
    elif sys.argv[1] == 'AddAccess' and len(sys.argv) == 5:
        add_access( sys.argv[2], sys.argv[3], sys.argv[4] )
    elif sys.argv[1] == 'CanAccess' and len(sys.argv) == 5:
        can_access( sys.argv[2], sys.argv[3], sys.argv[4] )

# Helpers
def check_user(username):
    if not path.exists( './tables/users.json' ):
        return False
    f = open( './tables/users.json', 'r' )
    try:
        users = json.load(f)
        if username in users:
            return True
    except JSONDecodeError:
        return False
    return False

def check_domain(domain_name):
    if not path.exists( './tables/domains.json' ):
        return False
    f = open( './tables/domains.json' )
    try:
        domains = json.load(f)
        if domain_name in domains:
            return True
    except JSONDecodeError:
        return False
    return False

def check_type(type_name):
    if not path.exists( './tables/types.json' ):
        return False
    f = open( './tables/types.json' )
    try:
        types = json.load(f)
        if type_name in types:
            return True
    except JSONDecodeError:
        return False
    return False

'''
AddUser
Params:

Returns:

Todo:
'''
def add_user(username, password):
    # print('adding user')

    # check if the file exists
    if not path.exists( './tables/users.json' ):
        open( "./tables/users.json", "w+" )

    # read the user table
    f = open( "./tables/users.json", "r" )
    try:
        # convert from json to dict
        users = json.load(f)

        # need to check if the user already exists
        if check_user(username):
            print('Username in use') 
            exit()

        # add the new user
        users[username] = { "UserName" : username, "Password" : password, "Domains" : [] }

        # open the file to write
        f = open( "./tables/users.json", "w+" )

        # dump the dict
        json.dump( users, f, indent=5 )

    except JSONDecodeError:
        # print('file empty')
        # need to write to file now
        f = open( "./tables/users.json", "w+" )
        # if the file is empty create a new dict
        users = { username : { "UserName" : username, "Password" : password, "Domains" : [] } }
        # dump to file
        json.dump( users, f , indent=5)

    print("Success")

'''
Authenticate
Params:

Returns:

Todo:
'''
def authenticate(username, password):
    # check if the file exists
    if not path.exists( './tables/users.json' ):
        print("No such user")
        exit()
    
    f = open( "./tables/users.json", "r" )

    # check if empty
    try:
        users = json.load( f )

        if username in users:
            if users[username]["Password"] != password:
                print("Bad password")
                exit()
        else:
            print("No such user")
            exit()

    except JSONDecodeError:
        print("No such user")
        exit()
    
    print("Success")

'''
SetDomain
Params:

Returns:

Todo:
'''
def set_domain(username, domain_name):
    
    # check if domain name is empty
    if domain_name == '':
        print("Missing domain")
        exit()

    # check if the user exists
    if not check_user(username):
        print("No such user")
        exit()

    # check if the file exists
    if not path.exists( './tables/domains.json' ):
        open( "./tables/domains.json", "w+" )

    # check if the domain exists, if it does not create it
    f = open( "./tables/domains.json", "r" )

    try:
        domains = json.load( f )
        f = open( "./tables/domains.json", "w+" )

        # domain is not in the table. So add it
        if domain_name not in domains:
            domains[domain_name] = {"Name" : domain_name, "AccessPermissions" : [], "Users" : [username]}
        else:
            # add user to the current domain
            if username not in domains[domain_name]["Users"]:
                domains[domain_name]["Users"].append(username)
        
        json.dump( domains, f, indent=5 )

    except JSONDecodeError:
        # file is empty
        domains = { domain_name : {"Name" : domain_name, "AccessPermissions" : [], "Users" : [username]} }
        f = open( "./tables/domains.json", "w+" )
        json.dump( domains, f, indent=5 )


    # add the domain to the user
    f = open( './tables/users.json', "r" )
    users = json.load(f)
    # check if the domain already exists in the user
    if domain_name not in users[username]["Domains"]:
        users[username]["Domains"].append(domain_name)
    f = open( './tables/users.json', "w+" )
    json.dump( users, f, indent=5 )
    print("Success")

'''
DomainInfo
Params:

Returns:

Todo:
    Do I need a comma when listing?
    Can I just print out the list?
'''
def domain_info(domain_name):
    # check if the domain name is empty
    if domain_name == "":
        print("Missing domain")
        exit()

    # check if the file exists
    if not path.exists( './tables/domains.json' ):
        open( "./tables/domains.json", "w+" )
        exit()

    f = open( './tables/domains.json', 'r' )
    
    try:
        domains = json.load( f )

        # check if the domain name is in domains
        if domain_name in domains:
            # loop through the length of users
            for user in domains[domain_name]["Users"]:
                print(user, end=" ")
            print("")

    except JSONDecodeError:
        exit()


'''
SetType
Params:

Returns:

Todo:
    Check if we throw an error when we are adding an already existing object into a type
'''
def set_type(object_name, type_name):
    if object_name == "":
        print("Object name is empty")
        exit()
    if type_name == "":
        print("Type name is empty")
        exit()

    # check if the file exists
    if not path.exists( './tables/types.json' ):
        open( "./tables/types.json", "w+" )
    
    f = open( "./tables/types.json", "r" )
    try:
        types = json.load( f )

        # check if the type already exists
        if type_name in types:
            # check if the object already exists
            if object_name not in types[type_name]["Objects"]:
                # add the object to the existing type
                types[type_name]["Objects"].append( object_name )
            else:
                print("Object already exists in type")
                exit()
        else:
            # Create the type and add the object
            types[type_name] = { "Name" : type_name, "Objects" : [object_name] }
            
    except JSONDecodeError:
        # create the dict and add the type to it with the object
        types = { type_name : { "Name" : type_name, "Objects" : [object_name] } }

    f = open( "./tables/types.json", "w+" )
    json.dump( types, f, indent=5 )

    print("Success")

'''
TypeInfo
Params:

Returns:

Todo:
    Do I need a comma when listing?
    Can I just print out the list?
'''
def type_info(type_name):
    # check that type_name is not empty
    if type_name == "":
        print("Type name is empty")
        exit()
    
    # check if the file exists
    if not path.exists( './tables/types.json' ):
        open( "./tables/types.json", "w+" )
        exit()

    f = open( './tables/types.json', 'r' )

    try:
        types = json.load( f )

        # check if the domain name is in domains
        if type_name in types:
            # loop through the length of users
            for _object in types[type_name]["Objects"]:
                print(_object, end=" ")
            print("")

    except JSONDecodeError:
        exit()

'''
AddAccess
Params:

Returns:

Todo:
'''
def add_access(operation, domain_name, type_name):
    # check if domain and type are not null
    if domain_name == "":
        print("Domain name is empty")
        exit()
    if type_name == "":
        print("Type name is empty")
        exit()
    if operation == "":
        print("Operation is empty")
        exit()

    # Check if domain name exists
    if not check_domain( domain_name ):
        # create the domain

        # check if the file exists
        if not path.exists( './tables/domains.json' ):
            open( "./tables/domains.json", "w+" )
        f = open( "./tables/domains.json", "r" )
        try:
            domains = json.load( f )
            # add to domains (dont have to check if it exists bc we already did)
            domains[domain_name] = { "Name" : domain_name, "AccessPermissions" : [], "Users" : []}
        except JSONDecodeError:
            # emtpy file
            domains = { domain_name : { "Name" : domain_name, "AccessPermissions" : [], "Users" : []} }
        f = open( "./tables/domains.json", "w+" )
        json.dump( domains, f, indent=5 )

    # Check if type name exists
    if not check_type( type_name ):
        # create the type

        # check if the file exists
        if not path.exists( './tables/types.json' ):
            open( "./tables/types.json", "w+" )
        f = open( "./tables/types.json", "r" )
        try:
            types = json.load( f )
            # add to domains (dont have to check if it exists bc we already did)
            types[type_name] = { "Name" : type_name, "Objects" : []}
        except JSONDecodeError:
            # emtpy file
            types = { type_name : { "Name" : type_name, "Objects" : []} }
        f = open( "./tables/types.json", "w+" )
        json.dump( types, f, indent=5 )

    print("Success")
    
'''
CanAccess
Params:

Returns:

Todo:
'''
def can_access(opertion, username, object):
    print('can access')


if __name__ == '__main__':
    main()

