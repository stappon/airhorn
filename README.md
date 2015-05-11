# Disruptive web-enabled air horn technology

You tweet #disrupt, it goes BRAAAAAAP. Welcome to the Internet of Loud Things.

Using:
* Heroku
* Tweepy
* Spark Core
* servo
* air horn

[!!!!WEBSITE!!!!](https://disruptor.herokuapp.com)

Created for the [Stupid Shit No One Needs and Terrible Ideas Hackathon](http://stupidhackathon.github.io/), May 9-10th, 2015.

## Manually Trigger the Spark Core
You can use curl to manually trigger the Spark Core if you get tired of tweeting at it.
```
 curl https://api.spark.io/v1/devices/[your_device_id]/disrupt \
  -d access_token=your_access_token
```
