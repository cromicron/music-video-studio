# Restoring optional production media

A normal clone includes the working edit, its media and the vertical hybrid Short with lyrics. Use the original downloads below to recover any of the additional exports or historical art. Each input works independently.

| Download | What it restores |
| --- | --- |
| [Join_Me_in_Life_Camera_Blender.zip](https://chatgpt.com/library?file_id=libfile_2274ce5316bc8191a100c74357986b58&account_id=personal) | The six camera exports under `current/exports/`, including the primary Short. The three hybrid exports carry the Revision 4 corrections. The three restrained exports provide the Revision 3 comparison. |
| [Join_Me_in_Life_Waiting_Room_Fix.mp4](https://chatgpt.com/library?file_id=libfile_b8c7e4755f808191adf3031e375a49da&account_id=personal) | The standalone preview of the waiting-room camera change, under `current/exports/`. |
| [Music_Video_Consolidated_Package.zip](https://chatgpt.com/library?file_id=libfile_0cc55104dfd88191a8fd837fac7ec36f&account_id=personal) | The earlier illustrations, visual index and notes under `archive/visual-development-v1/`, plus the consolidated package's original checksums. |
| [Join_Me_in_Life_Full_Package.zip](https://chatgpt.com/library?file_id=libfile_9c99c58d80f4819190d7145c6d9c718f&account_id=personal) | The same historical art, index and notes. Choose this smaller download if you only need the visual-development archive. |

Keep the original download names. From the repository root, point the script at one folder, or pass individual paths. It checks the top level of each folder. On Windows, `py -3` can be used in place of `python3`.

```sh
python3 tools/restore_media.py "/path/to/downloads"
```

All destination paths in the table are relative to `productions/join-me-in-life/`. The script verifies the SHA-256 of each download and restored file. Matching local copies are skipped. If a local copy differs, it stays in place and the script reports its path.
