# <cite>iCloud Console</cite>

<p align="center">
    <img width="300" src="assets/41166dada6559cb93c7a4ff0ea681e52.png">
</p>

English | [简体中文](README.zh.md)




| <img src="assets/sync.gif" alt="Image 1"  height="400"/> | <img src="assets/login_page.png" alt="Image 1"  height="400"/> |
|:--------------------------------------------------------:|:--------------------------------------------------------------:|
|         *Preview of home page and interactions*          |                    *Preview of login page*                     |


## Usage

```shell
Usage: icloud.py [OPTIONS] COMMAND [ARGS]...

Options:
  -u, --username <username>  Your iCloud username or email address  [required]
  -p, --password <password>  Your iCloud password (default: use PyiCloud
                             keyring or prompt for password)  [required]

  --china-account            Specify the "HOME_ENDPOINT" and "SETUP_ENDPOINT"
                             for the "China Mainland Accounts".

  --version                  Show the version and exit.
  --help                     Show this message and exit.

Commands:
  device          Device and Location, Find device Location, Get device...
  photo-download  Manage Photos on your icloud.
  test            Do some experimental tes.
```

## <img width="50" src="assets/1c11f0fa22d4e93f8dc179b8ff84791d.png"> Photos Download （2FA）

```shell
Usage: icloud.py photo-download <options>

Options:
  -d, --directory <directory>    Local directory that should be used for
                                 download

  --recent INTEGER RANGE         Number of recent photos to download (default:
                                 download all photos)

  --auto-delete                  Scans the "Recently Deleted" folder and
                                 deletes any files found in there. (If you
                                 restore the photo in iCloud, it will be
                                 downloaded again.)

  --modify-olds                  Modify the "Created Time" of the old files
                                 that already been in the folder.

  --workers INTEGER RANGE        Number of the thread to download
                                 photo.(Default is 3)

  --transfer-album <album_name>  Determine the album that will be downloaded.
  --help                         Show this message and exit.
```

Example 1

```shell
icloud -d /external/SADAM/icloud/photos/ --recent 500
```

Example 2

```shell
icloud -u <username> -p <password> -d /external/SADAM/icloud/photos/ --recent 500
```

Example 3

```shell
icloud -u <username> -p <password>
--china-account
photo-download
-d
/Volumes/share/SADAM/icloud/photos
--transfer-album
Hidden
--modify-olds
--auto-delete
--workers
1
```

### Automatically start every half hour through crontab

```shell
*/30 * * * * /<python absolute path>/python3.9 /<project absolute path>/icloud.py -u <icloud account> -p <password> --china-account photo-download -d /external /SADAM/icloud/photos/ --transfer-album Transfer --auto-delete >> /opt/icloud-killer/logs/last-$(date "+%Y%m%d%H%M").log 2>&1
```

## <img width="50" src="assets/dccb81ba3f0f63e9a50c162007f59c4a.png"> Driver And Files (2FA)

## <img width="50" src="assets/ddc3380f93d44a376c586796bb7c16a7.png"> Reminds (2FA)

## <img width="50" src="assets/4b1d90456b68a8d4d4b91adb39e60b70.png"> Contact (2FA)

## <img width="50" src="docs/statics/location.png"> Device And Location (Weak 2FA: Just send)

* Get device info.
    * location
    * Status
    * Battery level
    * Device model
    * Device name
    * Device ID
* Remote Control
    * locking device
    * Show message
    * Play sound

```python
api.iphone.location()
```

```json
{
  'isOld': True,
  'isInaccurate': False,
  'positionType': 'Wifi',
  'secureLocation': None,
  'secureLocationTs': 0,
  'altitude': 0.0,
  'latitude': 43.894873066105184,
  //纬度
  'longitude': 87.58595865485619,
  //经度
  'horizontalAccuracy': 65.0,
  //水平精度
  'verticalAccuracy': 0.0,
  //垂直精度
  'timeStamp': 1670048465162,
  //时间戳
  'floorLevel': 0,
  'locationType': '',
  'locationFinished': True,
  'locationMode': None
}
```

## Development Plan
* [ ] implements displaying Assets in different orders.
* [ ] Implement a visual GUI interface that is easy for novice users to operate (no need to set up an environment, just download the Release of the corresponding platform to use it, and the command line function is still retained).
* [ ] Implement the function of migrating Assets to Immich with one click.
* [ ] Data migration function
   * [ ] One-click migration and synchronization removed from iCloud (free up iCloud space)
   * [ ] Support migration to local hard disk (directory)
   * [ ] Support migration to third-party platforms:
     * [ ] [immich-app/immich](https://github.com/immich-app/immich)
     * [ ] [NextCloud](https://github.com/nextcloud)
## Star History

<a href="https://star-history.com/#haoke98/icloud-killer&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=haoke98/icloud-killer&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=haoke98/icloud-killer&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=haoke98/icloud-killer&type=Date" />
  </picture>
</a>

## Problems:

* Missing apple_id field
    * Detailed error message:
      ```shell
      Traceback (most recent call last):
        File "test.py", line 10, in <module>
          api = PyiCloudService("***", "***")
        File "/usr/local/lib/python3.9/site-packages/pyicloud/base.py", line 268, in __init__
          self.authenticate()
        File "/usr/local/lib/python3.9/site-packages/pyicloud/base.py", line 328, in authenticate
          self._authenticate_with_token()
        File "/usr/local/lib/python3.9/site-packages/pyicloud/base.py", line 350, in _authenticate_with_token
          raise PyiCloudFailedLoginException(msg, error)
      pyicloud.exceptions.PyiCloudFailedLoginException: ('Invalid authentication token.', PyiCloudAPIResponseException('Missing apple_id field'))
      ```
    * solution:
        * [Apparently `apple_id` and `password` are now required on method:`_authenticate_with_token`](https://github.com/picklepete/pyicloud/issues/349#issuecomment-943885985)

## Related Links

1. [PyiCloud PyPI Home Page](https://pypi.org/project/pyicloud/)
2. [PyiCloud GitHub Home Page](https://pypi.org/project/pyicloud/)
