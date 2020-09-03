
# 31

31 is a simple tool you can use to run code in the background on a server.

For example

```
31 -c 'sleep 100; echo 2'
```

runs the command `sleep 100; echo 2` then sends you an email with the output of the command once it is complete.

## Setup

Install 31 by running

```
pip install 31
```

Then set up your email address by running

```
31 --config email youremail@example.com
```
