
# 31

31 is a simple tool you can use to run code in the background on a server.

For example

```
31 c 'sleep 100; echo 2'
```

runs the command `sleep 100; echo 2` in a screen session then sends you an email with the output of the command once it is complete.

## Setup

Install 31 by running

```
pip install 31
```

Then set up your email address by running

```
31 config email youremail@example.com
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
31 config mail_program <mail program name>
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

## Options

See `31 -h` for a full list of options. This section covers only some of the more complicated ones

### Foreach

This option allows you to run multiple commands with text substitution. As a basic usage example, the code

```sh
31 c -f %x 1,2,3 'touch %x.txt'
```

Creates each of the files `1.txt`, `2.txt`, and `3.txt`. The variable substitution is managed via direct text-substitution,
and thus your variables do not need to begin with %, this works equally well (though is far less readable)

```sh
31 c -f 2 1,2,3 'touch 2.txt'
```

You can also modify two variables in tandem like this:

```sh
31 c -f2 %x %ext 1,2,3 txt,png,py 'touch %x.%ext'
```

This creates the files `1.txt`, `2.png`, `3.py`. If you instead want to create all combinations, you can run:

```sh
31 c -f %x 1,2,3 -f %ext txt,png,py 'touch %x.%ext'
```

This creates the files `1.txt`, `1.png`, `1.py`, `2.txt`, `2.png`, `2.py`, `3.txt`, `3.png`, `3.py`.

The values field is in comma-separated-value form, which means you can use `"` as a CSV escape, as such:

```sh
31 -c -f %x '",",2' `touch %x.txt`
```

which creates the files `,.txt` and `2.txt`.
