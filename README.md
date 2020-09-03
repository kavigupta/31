
# 31

31 is a simple tool you can use to run code in the background on a server.

For example

```
31 -c 'sleep 100; echo 2'
```

runs the command `sleep 100; echo 2` in a screen session then sends you an email with the output of the command once it is complete.

## Setup

Install 31 by running

```
pip install 31
```

Then set up your email address by running

```
31 --config email youremail@example.com
```

### Quick dependency setup

On ubuntu you can run

```
sudo apt install screen mailutils
```

to quickly set up the dependencies needed.

### Detailed dependency setup

#### Mail program

By default, `31` searches for a mail program to use from the following list. You
can also force it to use one of the programs by using the command

```
31 --config mail_program <mail program name>
```

- `gnu_mail`. To install on ubuntu you can run
```
sudo apt install mailutils
```
- `mutt`. To install on ubuntu you can run
```
sudo apt install mutt
```

#### Screen Manager

Currently 31 only supports `screen`. To install screen on ubuntu run
```
sudo apt install screen
```
