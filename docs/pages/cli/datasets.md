# Datasets

## Download

Command that provides the capability to download the STIX datasets from different providers.

```bash
$ openstix datasets download --help

Usage: openstix datasets download [OPTIONS]

  Download datasets from STIX providers.

Options:
  --provider [mitre|oasis-open]   Download the specified provider.
  --datasets [atlas|tlp20|industries|capec|locations|vulnerabilities|attack]
                                  Download the specified datasets.
  --help                          Show this message and exit.
```

**Note:** all datasets will be stored in `$HOME/.openstix/`.

### Examples

Download all datasets
```bash
openstix datasets download
```

Download datasets from a provider
```bash
openstix datasets download --provider mitre
```

## Sync

Command that provides the capability to sync the STIX datasets from one source to a sink (destination).

```bash
$ openstix datasets sync --help

Usage: openstix datasets sync [OPTIONS]

  Sync datasets to a TAXII server or a directory.

Options:
  --source TEXT  The source dataset to sync.  [required]
  --sink TEXT    The TAXII server or directory to sync to.  [required]
  --send-bundle  Send all objects as a single bundle to the sink instead of
                 individual objects.
  --help         Show this message and exit.
```

### Examples

Send all MITRE objects
```bash
openstix datasets sync --source $HOME/.openstix/mitre --sink https://taxii.example.com/taxii2/mitre/
```