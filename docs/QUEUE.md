# Queue

## How it works right now
_Note: This is more for my own use. I just need to write this down so I can see whether it makes sense or not._

Users can configure the number of posts per day, and the earliest and latest post times. The rest of the posts are divided evenly between those two times.

When the script pulls posts from an RSS feed, it sorts the post by date and excludes any posts that are older than the `currency_limit`.

It then assigns the posts to a slot from oldest to newest and checks the scheduled time against the `currency_limit` to ensure that the post is not too old by the time it is posted.

Right now, scheduling the post through Facebook's [scheduled_publish_time](https://developers.facebook.com/docs/pages-api/posts/#publish-posts) parameter seems to be the easiest.

After the posts are scheduled, the script will log information about them. Assuming the IDs 