import secrets


print(f'SECRET KEY{secrets.token_urlsafe(256)}')
print(f'SALT{secrets.token_urlsafe(256)}')