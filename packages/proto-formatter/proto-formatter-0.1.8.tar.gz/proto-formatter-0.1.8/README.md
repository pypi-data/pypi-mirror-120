# proto-formatter
Protocol Buffers file formatter.

## Install
```shell
pip install proto-formatter
```
## Usage
Format all proto files under current folder and sub-folders with default configs
```shell
proto_formatter format
```
Help message
```shell
*****************************************************
*  Format protobuf file(s) from a specific target.  *
*****************************************************

usage:
  proto_formatter <command> [options]

commands:
  format                   format protobuf files
  view                     view file

general options:
  -h                       show this help message and exit
  --help                   show this help message and exit
  --files                  target protobuf files need to be formatted.
  --folder                 target folder or path, default is current folder, all protubuf files under it and its' subdirectories will be formatted.
  --indents                the number of indented spaces
  --top-comment            format all comments as top comments(above the target line)
  --align-by-equal-sign    align the code by equal sign
  --flatten                flatten nested objects
  --comment-max-length     the max length of comment line, defalut is 999999.
  --file                   target protobuf file, only used for command 'view'
```
It also provides a method ``format_str`` to format a protobuf string.
```python
from proto_formatter import format_str

proto_str = """
    /*
    Person balabala
*/
    message Person {
    // comment of name a
required string name = 1; // comment of name b
/* 
comment of id a
// comment of id b
         */
        required int32 id = 2;// comment of id c
       optional string email = 3;// comment of email
}
"""
formatted_proto_str = format_str(proto_str, align_by_equal_sign=True)
print(formatted_proto_str)
```
The formatted_proto_str is:
```protobuf
/*
**    Person balabala
*/
message Person {
  /*
  **    comment of name a
  */
  required string name  = 1;  // comment of name b
  /*
  **    comment of id a
  **    comment of id b
  */
  required int32 id     = 2;  // comment of id c
  optional string email = 3;  // comment of email
}
```