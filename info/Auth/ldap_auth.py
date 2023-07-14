import ldap

def Auth_ldap(user,passwd):
    conn = ldap.initialize('ldap://127.0.0.1:27800')
    conn.simple_bind_s('CN=oe.ldap,OU=Admins,OU=OE,DC=oe,DC=bio', 'xnxjdhf')
    result = conn.search_s('OU=OEStaff,DC=oe,DC=bio', ldap.SCOPE_SUBTREE, '(sAMAccountName={})'.format(user))

    if len(result) == 1:
        # 获取用户DN
        dn = result[0][0]
        #print(dn[3:6])
        try:
            # 使用用户账号和密码进行绑定
            conn.simple_bind_s(dn, passwd)
            print('Authentication succeeded')
            return "True"
        except ldap.INVALID_CREDENTIALS:
            print('Authentication failed')
            return "Fail"
    else:
        print('User not found')
        return "User not found"
    conn.unbind_s()
