# Read Url from txt,each line is a link
def UrlReader(FileName):
    with open(FileName) as f:
        UrlLists = f.read().splitlines()
        return UrlLists
