# dbackuper
A Python tool to help automating MySQL database backups from remote databases.

## Running the tool
1. Copy `access.example.json` to `access.json` and start filling it with data.
2. Run `python backuper.py`.
3. Wait for it to complete.

You can consider running it via crontab in order to have scheduled backups.

## Considerations
The default retention rate of backups is 5. This means that if you just created a fifth backup, the others will be deleted.

## Known issues and plans for the future
1. The backup might fail, and the backup file will still be created.
2. It would be nice to store backups in some sort of directory (or even make it configurable).
3. Logging. I might actually start with this one...
