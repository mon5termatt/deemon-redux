---
layout: default
title: Queue
parent: Troubleshooting
---

# Queue
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---
Each time Deemon Redux finds new releases, they are dumped to `queue.csv` inside the Deemon Redux application directory. This provides a way to recover a failed job.

To redownload a queue, you can manually extract the `album_id` or `track_id` column and save it into a new file to pass to deemon:

Album IDs: `deemon download --album-file file.csv`

Track IDs: `deemon download --track-file file.csv`