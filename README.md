# Analysis of Cherry Picker POS Malware (De)Obfuscation
This article is laid out to go from overview to specifics then to low level
details. Read as far as you want and realize that everything below is more
technical than what is above.

You might have heard about a bit of malware called Cherry Picker POS that
targets point-of-sale systems. It’s been around since 2011 but it
[remained largely undetected by antivirus solutions](http://www.darkreading.com/vulnerabilities---threats/cherry-picker-pos-malware-has-remained-hidden-for-four-years/d/d-id/1323128)
until about this time last year.

A couple weeks back I was introduced to the Cherry Picker POS deobfuscator
code written by Eric Merritt at Trustwave. I felt it would be fun to deep
dive into his code and to see if I could write my own version.

In addition Trustwave provided a [deobfuscator](https://github.com/SpiderLabs/malware-analysis/blob/master/Python/CherryPicker/cherryConfig.py)
to decode the malware payload only; I supplemented this functionality by
building my own obfuscator. By writing an obfuscator we can take numerous
existing file formats and run them through the obfuscator. We can then use
the results to build signatures for detection. If anybody tries to use this
obfuscator again we should have a better chance of knowing.

This is an analysis of how this algorithm works to better understand some of
the goals and methods used by the malware author(s) in addition to providing
information to help map new malware to a threat actor or organization.
Malware authors tend to use the same algorithms or slight variants on a theme
repeatedly.
