# define the schema for festival data
band = {
    "name": str,
    "recordLabel": str
}

music_festival = {
    "name": str,
    "bands": [band]
} 

festivals = [music_festival]