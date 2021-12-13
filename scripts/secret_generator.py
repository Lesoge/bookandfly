import secrets
'''
Script to gernerate Secret Keys

__author__ = L.F.
'''
print(f'SECRET KEY:{secrets.token_urlsafe(256)}')
print('\n')
print(f'SALT:{secrets.token_urlsafe(256)}')