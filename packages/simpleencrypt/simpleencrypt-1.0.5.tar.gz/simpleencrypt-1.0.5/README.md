# About SimpleEncrypt

[SimpleEncrypt](https://github.com/shreyasnayak/SimpleEncrypt) is a Cross-Language Encryption Library that provides the ability to encrypt and decrypt data in C++ and Python 3

# Installing Dependency library

SimpleEncrypt Python package has a dependency on C++ shared library. Before running the simple encrypt python package, build and install C++ shared library.

## Build and install C++ shared library

- Install dependencies `sudo apt-get install libssl-dev openssl`
- Download or clone simple encrypt [C++ shared library](https://github.com/shreyasnayak/SimpleEncrypt/tree/main/CPP)
- Compile and install

```
git clone https://github.com/shreyasnayak/SimpleEncrypt
mkdir CPP/Build && cd CPP/Build
cmake ..
make
sudo make install
```

# Install python package [SimpleEncrypt](https://pypi.org/project/simpleencrypt/)

Installation

```
python3 -m pip install simpleencrypt
```

### Usage

```python
from simpleencrypt import aes256

# encryption
iv = b'171A065A7675A09AECEC118DBC008A822A041FC2EBF2B3E4CF7A4C966E5D5897'
key = b'2B5442AD8739992F'
plainText = b'Hello World'
encrypted = aes256.encrypt(plainText,iv,key)
print(encrypted)

# decryption
iv = b'171A065A7675A09AECEC118DBC008A822A041FC2EBF2B3E4CF7A4C966E5D5897'
key = b'2B5442AD8739992F'
print(aes256.decrypt(encrypted,iv,key))
```
