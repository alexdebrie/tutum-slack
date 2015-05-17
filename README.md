# Tracking Tutum Events with Slack

[![Deploy to Tutum](https://s.tutum.co/deploy-to-tutum.svg)](https://dashboard.tutum.co/stack/deploy/)

This is a service that can be quickly deployed to Tutum to monitor your
Tutum Events and post them to Slack. You can configure entirely through
environmental variables in the Stack file.

To deploy, hit the Deploy to Tutum button above. Change the environment
variables to your desired settings, and hit Create and Deploy! For events
you want tracked, a message will be posted to Slack in the following format
(using an event showing a Service whose state is 'Running'):

    You had a Service event on Tutum!
    Your Service's state is Running.
    Check "/api/v1/service/09cbcf8d-a727-40d9-b420-c8e18b7fa55b/" to see more details.

# Configuration

### Setting event types and states to monitor

In the Stack file, there is an environment variable set for each of the event
types that Tutum monitors (other than 'auth' and 'error'). For each event type
you would like to monitor, change the environment variable for that type to
include a comma-separated list of states that you would like to monitor.

For example, if i would like to know when a Service is "stopped" or "terminated",
or when a Node is "deployed", I would set the environment variables as follows:

    SERVICE="stopped,terminated"
    NODE="deployed"

Check out the [Tutum API documentation](https://docs.tutum.co/v2/api/) for more
information on the different types and states to monitor. You can also look at
the following blog posts on the Tutum Stream API:

* [Presenting the Tutum Stream API](http://blog.tutum.co/2015/04/07/presenting-tutum-stream-api/)
* [Using the New Tutum Stream API -- Part 1](http://blog.tutum.co/2015/05/06/using-the-new-tutum-stream-api-part-1/)
* [Using the New Tutum Stream API -- Part 2](http://blog.tutum.co/2015/05/12/using-the-new-tutum-stream-api-part-2-pagerduty-and-slack-notifications/)

### Other configuration options

You will need to include a `SLACK_URL` environment variable which is the url to
which you can post messages. See the [Incoming Webhooks](https://api.slack.com/incoming-webhooks)
documentation to set up a Slack URL. 

There is also a `VERBOSE` environment variable that controls what the service will
log. By default, the service prints all messages received from the Tutum Stream.
This ensures all messages will be in your logs, which you can handle as you please.
If you prefer to not print these messages, you can set `VERBOSE=False`.

# Acknowledgements

Thanks to @bighead in the [Tutum community Slack channel](https://tutum-community.slack.com/messages/)
for inspiration!
