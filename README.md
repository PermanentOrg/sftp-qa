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

### Challenging Names

Run `./generate-tree.py` to generate test data, which will be placed
in a new subdirectory named `test-tree/challenging-names`.

Then run `./upload-test.py test-tree/challenging-names --archive-path "/archives/rclone QA 1 (0a0j-0000)/My Files/"` to try uploading the data (you'll need to
[configure
rclone](https://github.com/PermanentOrg/sftp-service#running-rclone-against-permanentorg-instances)
first, of course).  See the long comment at the top of
[upload-test.sh](upload-test.sh) for information about what it's
trying to do and what problems we know about so far.

## Web Interface

For prod, just go to the site as per usual.  For dev, go to
https://dev.permanent.org/app and then log in.

## License

This code and data is open source under the [MIT license](LICENSE).
