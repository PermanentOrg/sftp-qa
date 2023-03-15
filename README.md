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

Run `./generate-tree.py` to generate test data, which will be placed
in a new subdirectory named `test-tree/challenging-names`.

Then run `./upload-test.sh` to try uploading the data (you'll need to
[configure
rclone](https://github.com/PermanentOrg/sftp-service#running-rclone-against-permanentorg-instances)
first, of course).  See the long comment at the top of
[upload-test.sh](upload-test.sh) for information about what it's
trying to do and what problems we know about so far.

## License

This code and data is open source under the [MIT license](LICENSE).
