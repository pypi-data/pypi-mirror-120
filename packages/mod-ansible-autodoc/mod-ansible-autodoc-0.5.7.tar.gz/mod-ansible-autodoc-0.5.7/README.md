# Ansible Autodoc Version

A spin of ansible-autodoc that only documents variables

## Install
```sh
pip3 install mod-ansible-autodoc
```

## How to use?
```sh
mod-ansible-autodoc
```

## Optional Args
### Custom titles
There are 4 optional args for this, one per markdown file:

1. --todo-title
2. --actions-title
3. --tags-title
4. --variables-title

The value of an argument has to be wrapped around ''. Example:
```sh
mod-ansible-autodoc --todo-title '## IMPROVEMENTS FILE'
```

### Variables' Title Prefix, Postfix and Example Comment Prefix
It's possible to add a prefix and/or postfix to `ansible_variables.md`'s subheaders and a prefix to the example comment. Simply run:
```sh
mod-ansible-autodoc --variable-title-prefix '###' --variable-title-postfix ' <!-- VARIABLE_FIX -->' --variable-example-comment-prefix '##PREFIX##'
```

Then, expect something like the following:
```
### `sdk_location` <!-- VARIABLE_FIX -->

yaml
##PREFIX## Example implementation of the sdk_location variable
sdk_location: ~/Android/Sdk

```