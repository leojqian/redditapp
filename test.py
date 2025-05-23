import praw

reddit = praw.Reddit(
    client_id="Yl764s-6k88VD35HH_0Blg",
    client_secret="ERcLaAGDDypF0OQolfKcF9_aPlS0iA",
    user_agent="test by u/Silly_Inspection5308"
)

submission = reddit.submission(url="https://www.reddit.com/r/AITAH/comments/1ktn15f/update_aitah_for_walking_out_on_a_date_after_he/")
submission_text = submission.selftext
submission_title = submission.title

print(submission_title)
print(submission_text)
