# DNS enumeration with ChatGPT integrated

---

## The nead

Enumerating DNS usign Chat GPT (GPT 3.5 turbo) for finding subdomains names

### The schematics

1. Asking ChagGPT to write 50 subdomains for specific domain.
2. Filtering only subdomains.
3. Removing duplicates.
4. Reading subdomains wordlist from user file, and adding to the list.
5. Doing DNS lookup on list.
6. When found valid DNS- searching for subdomain with additional number(1 to 10).
7. On valid DNS record doing a reverse lookup.
8. Printing and saving results.

before using:

update your openAI api key value

```python
api_key = 'your_OpenAI_API_key'
```

requirments:

```bash
pip install dns
pip install openai
```

# parameters

-d [requierd] - domain to emunerate

-l [not requierd] - file with subdomain wordlist

-o [not requierd] - output file

run:

```bash
python DNSenumAI.py -d [domian]
```
