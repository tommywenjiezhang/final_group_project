from hashlib import sha224

def hashIdandTitle(title,id):
    raw = title + str(id)
    return sha224(raw.encode('utf-8')).hexdigest()

if __name__ == "__main__":
    stringValue = hashIdandTitle('hello world', 5)
    print(stringValue)