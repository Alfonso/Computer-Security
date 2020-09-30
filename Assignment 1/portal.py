import sys
import json
from json.decoder import JSONDecodeError
from os import path


def main():

    # error check argument lengths?
    if len(sys.argv) < 2:
        print('Error: Please provide proper input')
        return
    elif sys.argv[1] == 'AddUser' and len(sys.argv) == 4:
        add_user( sys.argv[2], sys.argv[3] )
    elif sys.argv[1] == 'AddUser' and len(sys.argv) != 4:
        if len(sys.argv) < 4:
            print("Error: too few arguments - ",end="")
        else:
            print("Error: too many arguements - ",end="")
        print("usage: AddUser name password")

    elif sys.argv[1] == 'Authenticate' and len(sys.argv) == 4:
        authenticate( sys.argv[2], sys.argv[3] )
    elif sys.argv[1] == 'Authenticate' and len(sys.argv) != 4:
        if len(sys.argv) < 4:
            print("Error: too few arguments - ",end="")
        else:
            print("Error: too many arguements - ",end="")
        print("usage: Authenticate name password")

    elif sys.argv[1] == 'SetDomain' and len(sys.argv) == 4:
        set_domain( sys.argv[2], sys.argv[3] )
    elif sys.argv[1] == 'SetDomain' and len(sys.argv) != 4:
        if len(sys.argv) < 4:
            print("Error: too few arguments - ",end="")
        else:
            print("Error: too many arguements - ",end="")
        print("usage: SetDomain user domain")

    elif sys.argv[1] == 'DomainInfo' and len(sys.argv) == 3:
        domain_info( sys.argv[2] )
    elif sys.argv[1] == 'DomainInfo' and len(sys.argv) != 3:
        if len(sys.argv) < 3:
            print("Error: too few arguments - ",end="")
        else:
            print("Error: too many arguements - ",end="")
        print("usage: DomainInfo domain")

    elif sys.argv[1] == 'SetType' and len(sys.argv) == 4:
        set_type( sys.argv[2], sys.argv[3] )
    elif sys.argv[1] == 'SetType' and len(sys.argv) != 4:
        if len(sys.argv) < 4:
            print("Error: too few arguments - ",end="")
        else:
            print("Error: too many arguements - ",end="")
        print("usage: SetType object type")

    elif sys.argv[1] == 'TypeInfo' and len(sys.argv) == 3:
        type_info( sys.argv[2] )
    elif sys.argv[1] == 'TypeInfo' and len(sys.argv) != 3:
        if len(sys.argv) < 3:
            print("Error: too few arguments - ",end="")
        else:
            print("Error: too many arguements - ",end="")
        print("usage: TypeInfo type")

    elif sys.argv[1] == 'AddAccess' and len(sys.argv) == 5:
        add_access( sys.argv[2], sys.argv[3], sys.argv[4] )
    elif sys.argv[1] == 'AddAccess' and len(sys.argv) != 5:
        if len(sys.argv) < 5:
            print("Error: too few arguments - ",end="")
        else:
            print("Error: too many arguements - ",end="")
        print("usage: AddAccess operation domain type")

    elif sys.argv[1] == 'CanAccess' and len(sys.argv) == 5:
        can_access( sys.argv[2], sys.argv[3], sys.argv[4] )
    elif sys.argv[1] == 'CanAccess' and len(sys.argv) != 5:
        if len(sys.argv) < 5:
            print("Error: too few arguments - ",end="")
        else:
            print("Error: too many arguements - ",end="")
        print("usage: CanAccess operation user object")
    else:
        print("Error: invalid command")

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

def check_permission(operation):
    if not path.exists( './tables/permissions.json' ):
        return False
    f = open( './tables/permissions.json' )
    try:
        types = json.load(f)
        if operation in types:
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
    # check if username is blank
    if username == "":
        print("Error: Empty username")
        return

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
            print('Error: Username in use') 
            return

        # add the new user
        users[username] = { "UserName" : username, "Password" : password, "Domains" : [] }

        # open the file to write
        f = open( "./tables/users.json", "w+" )

        # dump the dict
        json.dump( users, f, indent=5 )

    except JSONDecodeError:
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
        print("Error: No such user")
        return
    
    f = open( "./tables/users.json", "r" )

    # check if empty
    try:
        users = json.load( f )

        if username in users:
            if users[username]["Password"] != password:
                print("Error: Bad password")
                return
        else:
            print("Error: No such user")
            return

    except JSONDecodeError:
        print("Error: No such user")
        return
    
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
        print("Error: Missing domain")
        return

    # check if the user exists
    if not check_user(username):
        print("Error: No such user")
        return

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
            domains[domain_name] = {"Name" : domain_name,  "Users" : [username]}
        else:
            # add user to the current domain
            if username not in domains[domain_name]["Users"]:
                domains[domain_name]["Users"].append(username)
        
        json.dump( domains, f, indent=5 )

    except JSONDecodeError:
        # file is empty
        domains = { domain_name : {"Name" : domain_name, "Users" : [username]} }
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
'''
def domain_info(domain_name):
    # check if the domain name is empty
    if domain_name == "":
        print("Error: Missing domain")
        return

    # check if the file exists
    if not path.exists( './tables/domains.json' ):
        open( "./tables/domains.json", "w+" )
        return

    f = open( './tables/domains.json', 'r' )
    
    try:
        domains = json.load( f )

        # check if the domain name is in domains
        if domain_name in domains:
            # loop through the length of users
            for user in domains[domain_name]["Users"]:
                print(user)

    except JSONDecodeError:
        return


'''
SetType
Params:

Returns:

Todo:
    Check if we throw an error when we are adding an already existing object into a type
'''
def set_type(object_name, type_name):
    if object_name == "":
        print("Error: Object name is empty")
        return
    if type_name == "":
        print("Error: Type name is empty")
        return

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
                return
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
'''
def type_info(type_name):
    # check that type_name is not empty
    if type_name == "":
        print("Error: Type name is empty")
        return
    
    # check if the file exists
    if not path.exists( './tables/types.json' ):
        open( "./tables/types.json", "w+" )
        return

    f = open( './tables/types.json', 'r' )

    try:
        types = json.load( f )

        # check if the domain name is in domains
        if type_name in types:
            # loop through the length of users
            for _object in types[type_name]["Objects"]:
                print(_object)

    except JSONDecodeError:
        return

'''
AddAccess
Params:

Returns:

Todo:
'''
def add_access(operation, domain_name, type_name):
    # check if domain and type are not null
    if domain_name == "":
        print("Error: Domain name is empty")
        return
    if type_name == "":
        print("Error: Type name is empty")
        return
    if operation == "":
        print("Error: Operation is empty")
        return

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
            domains[domain_name] = { "Name" : domain_name, "Users" : []}
        except JSONDecodeError:
            # emtpy file
            domains = { domain_name : { "Name" : domain_name, "Users" : []} }
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

    
    # check if the permissions json exists
    if not path.exists( './tables/permissions.json' ):
        open( "./tables/permissions.json", "w+" )
    
    f = open( "./tables/permissions.json", "r" )
    try:
        permissions = json.load( f )
        # File is not empty

        # check if permission exists
        if operation not in permissions:
            # add operation into permissions
            permissions[operation] = { "Name" : operation, "Domains" : { domain_name : [type_name]} }
        else:
            
            # check if the domain exists already
            if domain_name in permissions[operation]["Domains"]:
                # check if the type exists already
                if type_name not in permissions[operation]["Domains"][domain_name]:
                    # append the new type to the list
                    permissions[operation]["Domains"][domain_name].append(type_name)
            else:
                # New domain so create new list
                permissions[operation]["Domains"][domain_name] = [type_name]


    except JSONDecodeError:
        # File is empty
        permissions = { operation : { "Name" : operation, "Domains" : { domain_name : [type_name] } } }

    f = open( "./tables/permissions.json", "w+" )
    json.dump( permissions, f, indent=5 )

    # add it to the Access Permissions in the Domain



    print("Success")
    
'''
CanAccess
Params:

Returns:

Todo:
'''
def can_access(operation, username, object_name):
    
    if username == "":
        print("Error: Username is empty")
        return
    if object_name == "":
        print("Error: Object name is empty")
        return
    if operation == "":
        print("Error: Operation name is empty")
        return

    # check if the file exists
    if not path.exists( './tables/users.json' ):
        open( "./tables/users.json", "w+" )
        return

    if not check_user(username):
        print("Error: Username is not valid")
        return

    # Check what domains the user is a part of
    f = open( "./tables/users.json", "r" )
    try:
        users = json.load( f )

        user_domains = users[username]["Domains"]

    except JSONDecodeError:
        # file is empty
        print("Error: Username is not valid")
        return


    # check if the file exists
    if not path.exists( './tables/permissions.json' ):
        open( "./tables/permission.json", "w+" )
        return

    if not check_permission(operation):
        print("Error: Operation is not valid")
        return

    # check what domains are associated with that operation
    f = open( "./tables/permissions.json", "r" )
    try:
        permissions = json.load( f )

        permission_domains = permissions[operation]["Domains"]

    except JSONDecodeError:
        # file is empty
        print("Error: Operaton is not valid")
        return
        
    # check which of the user_domains are in permission domains
    shared_domains = []
    for u_domain in user_domains:
        if u_domain in permission_domains:
            shared_domains.append(u_domain)

    # print("shared domains: {}".format(shared_domains))

    # Using shared domains, find the types associated
    shared_types = []
    for s_domain in shared_domains:
        for _type in permission_domains[s_domain]:
            # check if we already have the type in our list
            # check if it exists in our types json
            if _type not in shared_types and check_type(_type):
                shared_types.append(_type)
    # print("shared types: {}".format(shared_types))

    # get the types
    # check if the file exists
    if not path.exists( './tables/types.json' ):
        open( "./tables/types.json", "w+" )
        return
    
    # get types
    f = open( "./tables/types.json", "r" )
    try:
        types = json.load( f )

    except JSONDecodeError:
        # file is empty
        print("Error: Object is not valid")
        return

    # go through all of the shared types and see if object exists in it
    for _type in shared_types:
        if object_name in types[_type]["Objects"]:
            print("Success")
            return
    print("Error: Access Denied")



if __name__ == '__main__':
    main()

