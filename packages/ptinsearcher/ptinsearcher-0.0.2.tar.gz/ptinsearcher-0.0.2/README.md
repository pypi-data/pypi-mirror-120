![penterepTools](https://www.penterep.com/external/penterepToolsLogo.png)


# PTINSEARCHER
> Web sources information extractor

ptinsearcher is a tool for extracting information from web sources. This tool allows dumping of HTML comments, e-mail addresses, phone numbers, IP addresses, subdomains, HTML forms, links and metadata of documents.

## Installation
```
pip install ptinsearcher
```

## Add to PATH
```bash
# If you cannot invoke the script in your terminal, its probably because its not in your PATH. Fix it by running commands below
echo "export PATH=\"`python3 -m site --user-base`/bin:\$PATH\"" >> ~/.bashrc
source ~/.bashrc
```

## Usage examples

```
ptinsearcher -u https://www.example.com/            # Dump information from URL
ptinsearcher -u https://www.example.com/ -e H       # Extract HTML comments from URL
ptinsearcher -u https://www.example.com/ -e HSE     # Extract HTML comments, subdomains, emails from URL
ptinsearcher -f urlList.txt                         # Load list of sources to grab from file
ptinsearcher -f urlList.txt -gc -e E                # Group findings of all sources
```

## Options
```
-u   --url                 <url>           Test specified URL
-f   --file                <file>          Load list of URLs from file
-d   --domain              <domain>        Domain, used when any line in <file> doesn't contain valid URL, but path to file
-e   --extract             <extract>       Specify types of data to extract [E, S, H, F, I, X, P, M, L, Q, A] (default A)
-o   --output              <output>        Output to file
-op  --output-parts                        Output each result section to separate file
-gp  --group-parameters                    Group parameters
-wp  --without-parameters                  Without parameters
-g   --grouping                            One output table for all sites
-gc  --grouping-complete                   Merge results from all sites into one result
-r   --redirects                           Follow redirects (default False)
-c   --cookie              <cookie=value>  Set cookie(s)
-H   --headers             <header:value>  Set custom headers
-p   --proxy               <proxy>         Set proxy (e.g. http://127.0.0.1:8080)
-ua  --user-agent          <user-agent>    Set user agent
-j   --json                                Output in JSON format
-v   --version                             Show script version and exit
-h   --help                                Show this help message and exit
```

## Extract arguments
```

    A - grab all (default)
    E - emails
    S - subdomains
    H - HTML comments
    F - HTML Forms
    I - IP addresses
    X - External links
    L - Internal links
    Q - Internal links with parameters
    P - Phone numbers
    M - metadata
```

## Dependencies
- requests
- bs4
- pyexiftool
- tldextract
- ptlibs

We use [ExifTool](https://exiftool.org/) to extract metadata.

## Version History

* 0.0.1 - 0.0.2
    * Alpha releases

## License

Copyright (c) 2020 HACKER Consulting s.r.o.

ptinsearcher is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ptinsearcher is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ptinsearcher.  If not, see <https://www.gnu.org/licenses/>.

## Warning

You are only allowed to run the tool against the websites which
you have been given permission to pentest. We do not accept any
responsibility for any damage/harm that this application causes to your
computer, or your network. Penterep is not responsible for any illegal
or malicious use of this code. Be Ethical!