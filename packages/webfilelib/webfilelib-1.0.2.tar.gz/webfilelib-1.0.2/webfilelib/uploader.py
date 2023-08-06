import api
myUploader=api.Uploader()
def uploadOpenedFile(file):
    url=api.uploadOpened(file)
    return url
def uploadFile(name):
    url=api.uploadAny(name)
    return url