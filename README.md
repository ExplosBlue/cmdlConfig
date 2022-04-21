# CMDLConfig
A tool to generate and apply configurations to CMDL files

## Features
- Can generate and apply material configurations

## Usage
### Generating a config from a CMDL file
> python cmdlConfig.py exampleFile.cmdl

This will generate a config file called "exampleFile.conf" in the same directory as the "exampleFile.cmdl"

You can alternatively specify the output location of the config file
> python cmdlConfig.py exampleFile.cmdl path/to/output/example.conf

### Applying a config to a CMDL file
> python cmdlConfig.py exampleCMDL.cmdl --apply exampleConfig.conf

This will apply the selected config "exampleConfig.conf" to the selected CMDL file "exampleCMDL.cmdl" and replace it

## TODO
- Support for userdata
- Support for render order
- More flexibility on what elements are stored in a config
- Allow output location for modified CMDL to be specified
- Other stuff