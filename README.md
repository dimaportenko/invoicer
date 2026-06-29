# Invoicer

Python script to generate invoice pdf from the google doc template and send it over gmail. 


## Local usage 

```bash
# enter to virtual env with `venv` alias
venv

python main.py
```

### Flags

By default `python main.py` keeps the original behaviour: it copies the standard
template, creates a Gmail draft, saves the PDF to `./docs/`, increments the
invoice number and records it in the sheet. The following flags modify that
behaviour and can be combined:

| Flag | Effect |
| --- | --- |
| `--signed` | Use the signed invoice template (`TEMPLATE_DOC_ID_SIGNED`) instead of `TEMPLATE_DOC_ID`. |
| `--no-draft` | Don't create the Gmail draft. |
| `--download` | Also save the final PDF into `~/Downloads` (in addition to `./docs/`). |
| `--no-track` | Don't increment the invoice number and don't add a record to the sheet. |

```bash
# full dry preview: signed template, no draft, copy to Downloads, no tracking
python main.py --signed --no-draft --download --no-track
```

## TODO
- [x] reauth on failed refresh token action
