#!/usr/bin/env python3
# coding: utf-8

import sys, requests, ast


class GiteaAPI:
    def __init__(self, gtUrl, gtUser, gtPass):
        self.gtUrl = gtUrl
        self.gtUser = gtUser
        self.gtPass = gtPass

    def Request(self, url, method, headers, data):
        auth = (self.gtUser, self.gtPass)
        result = ""

        if method == "post":
            result = requests.post(url, headers=headers,
                                    auth=auth, json=data)
        elif method == "get":
            result = requests.get(url, headers=headers,
                                    auth=auth, json=data)
        elif method == "put":
            result = requests.put(url, headers=headers, 
                                    auth=auth, json=data)
        elif method == "delete":
            result = requests.delete(url, headers=headers, 
                                    auth=auth, json=data)

        return result
    
    def getToken(self):
        url = self.gtUrl \
                + '/api/v1/users/' \
                + self.gtUser \
                + '/tokens'

        headers = {"Content-Type": "application/json"}
        data = {
            "name": self.gtUser
        }

        return self.Request(url, "post",
                            headers, data)
    
    def delToken(self, id):
        url = self.gtUrl \
                + '/api/v1/users/' \
                + self.gtUser \
                + '/tokens/' \
                + str(id)

        headers = {"Content-Type": "application/json"}
        data = {}

        return self.Request(url, "delete",
                            headers, data)
    
    def addOrg(self, authorization, data):
        url = self.gtUrl + '/api/v1/orgs/'

        headers = {"Content-Type": "application/json",
                    "accept": "application/json",
                    "Authorization": authorization}
        
        return self.Request(url, "post",
                            headers, data)
    
    def addUser(self, authorization, data):
        url = self.gtUrl + '/api/v1/admin/users/'

        headers = {"Content-Type": "application/json",
                    "accept": "application/json",
                    "Authorization": authorization}
        
        return self.Request(url, "post",
                            headers, data)
    
    def addRepoToOrg(self, authorization, data, org):
        url = self.gtUrl \
                + '/api/v1/orgs/' \
                + org \
                + '/repos'

        headers = {"Content-Type": "application/json",
                    "accept": "application/json",
                    "Authorization": authorization}
        
        return self.Request(url, "post",
                            headers, data)
    
    def getTeam(self, authorization, org, q):
        url = self.gtUrl \
                + '/api/v1/orgs/' \
                + org \
                + '/teams/search?q=' \
                + q

        headers = {"Content-Type": "application/json",
                    "accept": "application/json",
                    "Authorization": authorization}
        data = {}
        
        return self.Request(url, "get",
                            headers, data)
    
    def addUserToTeam(self, authorization, id, user):
        url = self.gtUrl \
                + '/api/v1/teams/' \
                + str(id) \
                + '/members/' \
                + user

        headers = {"Content-Type": "application/json",
                    "accept": "application/json",
                    "Authorization": authorization}
        data = {}
        
        return self.Request(url, "put",
                            headers, data)

def main():

    host = sys.argv[1]
    user = sys.argv[2]
    pasw = sys.argv[3]
    comm = sys.argv[4]

    gt = GiteaAPI(host, user, pasw)
    response = gt.getToken()
    tokenID = (response.json())['id']
    authorization = "token " + str((response.json())['sha1'])

    if comm == "create_organization":
        data = ast.literal_eval(sys.argv[5])
        response = gt.addOrg(authorization, data)
        print("create_organization")
        print("status:", response.status_code)
        print("output:", response.json())
    elif comm == "create_user":
        data = ast.literal_eval(sys.argv[5])
        response = gt.addUser(authorization, data)
        print("create_user")
        print("status:", response.status_code)
        print("output:", response.json())
    elif comm == "add_repo_to_org":
        data = ast.literal_eval(sys.argv[5])
        org = sys.argv[6]
        response = gt.addRepoToOrg(authorization, data, org)
        print("add_repo_to_org")
        print("status:", response.status_code)
        print("output:", response.json())
    elif comm == "add_user_to_org":
        user = sys.argv[5]
        org = sys.argv[6]
        q = "owners"
        response = gt.getTeam(authorization, org, q)
        team_id = (response.json())['data'][0]['id']
        response = gt.addUserToTeam(authorization, team_id, user)
        print("add_user_to_org")
        print("status:", response.status_code)

    response = gt.delToken(tokenID)

if __name__ == "__main__":
    main()
