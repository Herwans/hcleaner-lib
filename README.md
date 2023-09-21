
# HCleaner Library

The library for the (future ?) HCleaner GUI and HCleaner CLI projects

## Features
### Detect
Based on the rules defined for the rename function, it checks the similar file name after cleaning.

### Dispatch
Move videos and images in separate folder based on the configuration file (only 1 for each can be defined at the moment).
If the element is a folder, if it's content is full of one of the type of file (images or videos), it's moved too.

### Garbage
Remove unwanted elements and empty folders.

### Integrity
Check if images are broken (basically the one that can be open by windows but not displayed).

### Rename
Rename file based on regex expression define in the configuration file

### Simplify
Check if a folder can be emptied because contains only 1 video, or if it contains only a folder with the same name.

## Configuration file
1. Copy config.json.sample to `~/.horn/config.json`
2. Define the name `{profile}`. The test use the `test` profile, but it can be anything. Just take note that the profile use in application made by me are define the hard way in the code.  
3. Fill the configuration fields :
   * **extensions** : indicate the extension manage for images or videos. Format `"images": ["jpg", "jpeg","png", "gif", "webp"]`
   * **extension-sets** : group of extensions, regardless the files type, use for file's rules application. Format : `"set-name": ["ext1", "ext2", "ext3"]`
   * **folder-rules** : contains the rules apply to folders. Format : `[ "regex", "replacement value" ]` 
   * **file-rules** : contains the rules apply to files. Format : `[ "regex", "replacement value", "extension-set name|*", "exclusion when *" ]`
   * **to-delete** : indicate the regex for deletable elements
   * **dispatch** : specify the folders to move videos and images elements


```json
{
    "{profile}": {
        "extensions": {
            "images": ["jpg", "jpeg","png", "gif"],
            "videos": ["mp4", "avi"]
        },
        "extension-set": {
            "videos": ["mp4", "mkv", "avi"],
            "images": ["jpg", "jpeg", "png", "gif"]
        },
        "folder-rules": [
            ["{regex}","{replacement}"]
        ],
        "file-rules": [
          ["{regex}","{replacement}", "{[extensions-set] or * for all}", "{exclusion (only when *)}"]
        ],
        
        "to-delete": ["{regex}"],
        "dispatch": {
            "videos": "{explorer path}",
            "images": "{explorer path}"
        }
    }
}
```

## Build

```bash
python setup.py bdist_wheel
```

## Authors

- [@Herwans](https://www.github.com/Herwans)
