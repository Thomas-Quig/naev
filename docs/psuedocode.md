# Equivilance Checking
```
pkg-vers = open('package.json')
for pkg in pkg-vers:
    base-ver = pkg.split(' ')[0]
    mod = pkg.split(' ')[1]
    switch mod:
        case '+':
            use_latest_version(base_ver)
        case '^':
            use_security_patches(base_ver) # Use the security patches of the version
        case '*':
            use_functionally_equivilant_version(base_ver)
```