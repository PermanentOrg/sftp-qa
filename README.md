# Permanent rclone QA Resources

This code generates sample data for testing the [SFTP
service](https://github.com/PermanentOrg/sftp-service) for
[Permanent.org](Permanent.org).  It creates test trees containing
files with various pathological names, which are meant to be uploaded
to Permanent via [rclone](https://rclone.org/) using the SFTP
protocol.

For more context, see [this
discussion](https://chat.opentechstrategies.com/#narrow/stream/73-Permanent/topic/QA/near/155527).

## Usage

You would have to install the python requirements used in this repo.

1. `python -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`

*It's possible to just install the requirements on your workspace however steps 1 and  2 would create and activate a virtual environment for this project alone! Recommended!*

### APOD

Run `./apod-downloader.py` to download a set of Astronomy Of The Day
photos, in a new directory called `test-tree/apod`.

Run `./upload-test.py test-tree/apod --archive-path "/archives/rclone QA 1 (0a0j-0000)/My Files/"` to try uploading the APOD photos
(and some html) all at once to a directory on the server.

**NB: The `--archive-path` argument specifies the route to the the specific permanent archive to which uploads would be made. So how do you get the archive path? See [Constructing archive path](https://github.com/permanentOrg/sftp-service/#downloading-from-permanent)**

*That said, the archive path used in the sample command would have to be updated to match some archive created on Permanent.org*

## Testing scope

The scope of testing via the test cases documented below verifies the possibility of correctly uploading and downloading
 a defined set of file types in a particular size range to [Permanent.org](Permanent.org) using [rclone](https://rclone.org/)
 which talks to permanent using the [SFTP service](https://github.com/PermanentOrg/sftp-service)

### What file types are tested?

- Text and png images with obscure names generated via [generate-tree.py](generate-tree.py)
- Images in `.jpg` and `.png` format downloaded from [APOD](https://apod.nasa.gov/apod) via [apod-downloader.py](apod-downloader.py)
- Compressed files in `.zip` and `.tar`
- Videos in `.mp4`, `.webm`, `.gifs` and `.3gp` common in mobile devices.
- Executable files in `.exe`, `.run`, `.sh`, `.dep` and extension-less bin executables.

## Test Cases?

### Challenging Names

Run `./generate-tree.py` to generate test data, which will be placed
in a new subdirectory named `test-tree/challenging-names`.

Then run `./upload-test.py test-tree/challenging-names --archive-path "/archives/rclone QA 1 (0a0j-0000)/My Files/"` to try uploading the data (you'll need to
[configure
rclone](https://github.com/PermanentOrg/sftp-service#running-rclone-against-permanentorg-instances)
first, of course).  See the long comment at the top of
[upload-test.sh](upload-test.sh) for information about what it's
trying to do and what problems we know about so far.

### Duplicates

A duplicate is a file/folder with exactly the same name. Of course this is not possible on regular file systems but Permanent does support it.
There is a deduplication algorithm from Permanent that the `sftp-service` relies to ensure that files with identical names on Permanent won't be 
 be considered as the same on regular file systems.

#### How test duplicate

- Create a folder in the test archive of the remote (permanent.org or permanent.dev depending on your test target) e.g 'duplicates'.
- Upload at least two copies of multiple identical files into the folder `duplicates` for example (`file.txt`, `file.txt`, `file.txt` and `photo.png`, `photo.png` ...)
- Run the download test script against the duplicate folder. In this case:

```
`./test-download.py --remote=prod --archive-path "/archives/rclone QA 1 (0a0j-0000)/My Files/" --remote-dir=duplicates`
```
#### Expected results

- Check downloads folder in `test-tree/downloads` and ensure that results looks like:

*Result from `tree` program*
```
├── file (1).txt
├── file (2).txt
├── file.txt
├── Photo (1).png
└── Photo.png

0 directories, 5 files
```
#### Multiple Identical Uploads

This test case captures what happens if you sync the same path with unchanged content multiples times.

#### How test identical uploads

- Generate challenging names if not generated earlier, see [Challenging Names](#challenging-names)

Run `./upload-test.py test-tree/challenging-names --only=414 --remote-dir=test-414 --log-file=log-duplicate-upload.txt --remote=prod --archive-path="/archives/QA (0a21-0000)/My Files/"`

*Notice the use of the `--only` flag which specifies only files containing the number `414` should be uploaded, you can change this number to follow a string pattern in the generated challenging names but the provide example works just fine.*

#### Expected results

- `rclone` should report `Sizes identical` and `Unchanged skipping`

```
2023/03/29 14:54:00 DEBUG : 002-dupe-test.txt: Sizes identical
2023/03/29 14:54:00 DEBUG : 002-dupe-test.txt: Unchanged skipping
```
- No duplicates should be be seen on Permanent UI.

#### Large uploads
##### Uploads

To test large file (`400MB` +) uploads, a couple of large files are required. Some ready-made test files can be downloaded via:

`./special-files-downloader.py --large`

If you have your own large files or other kinds of files you would like to run tests with, you can list the links to those files in a text file like so:

'my_files.txt'
```
https://link.com/to/file_1.extension
https://link.com/to/file_2.extension
https://link.com/to/file_3.extension
```

and then run `./special-files-downloader.py --my-source my_files.txt`

- *You can specify as many paths as you want inside the file*
- *You can name the the source text file anything you want but pass the right name and path to `--my-source`*

**You don't need to download any files if you already have some special files on your computer, simply copy such files into one of these directories `test-tree/special-files/`, `test-tree/special-files/large`, `test-tree/special-files/zips`,  or `test-tree/special-files/custom`**

Once the files are on disk:

Run `./upload-test.py test-tree/special-files/large --remote-dir=large-files --log-file=log-large-files.txt --remote=prod --archive-path="/archives/QA (0a21-0000)/My Files/"`

#### Nested folders/files

##### Nested uploads

We have a default nest of folders that goes down 4 levels.

Run `./upload-test.py test-tree/misc/nested/ --remote-dir=nested --log-file=log-nested.txt --remote=prod --archive-path="/archives/QA (0a21-0000)/My Files/"`

Verify in the Permanent UI that the folder set to remote dir `--remote-dir` in this case `nested` contains the nested folder with the following structure.

*Result from `tree` program*

```
test-tree/misc/nested/
├── nested-level-1
│   ├── nested-level-2
│   │   ├── nested-level-3
│   │   │   └── record-level-3.txt
│   │   └── record-level-2.txt
│   └── record-level-1.txt
└── record-level-0.txt
```

To test a nest with more levels, simply paste a nested folder structure inside `test-tree/misc/nested` or manually create more folder levels in the existing nest.

##### Nested downloads

*The steps in the upload section above must be completed before this step*

Run

`./test-download.py --remote=prod --archive-path="/archives/rclone QA 1 (0a21-0000)/My Files/" --remote-dir=nested`

Check the downloads folder in `test-tree/downloads` and ensure that the `downloads/nested` directory has a structure like the nested directory uploaded in the [nested uploads test](#nested-uploads).


### What file types and scenarios are left out?

Anything not included in the section above describing what is currently covered is by implication excluded from these tests.

## Troubleshooting

- Remember that the commands are examples and some of the arguments may not apply to your specific environment.
    - *For example ensure that arguments such as `--remote`, `--archive-path` are updated and correct*

## Web Interface

For prod, just go to the site as per usual.  For dev, go to
https://dev.permanent.org/app and then log in.

## License

This code and data is open source under the [MIT license](LICENSE).
