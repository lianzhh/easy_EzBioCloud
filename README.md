# EZBioCloud_ID_Selenium
With batch uploads, 16S rRNA sequences can be automatically searched against EzBioCloud's database for identification.

# Requirements
python ≥ 3.8 
java runtime environment 

# Installation
pip install -r requirements.txt

## chrome driver installation
ChromeDriver is a separate executable that Selenium WebDriver uses to control Chrome. Follow these steps to setup your tests for running with Chrome Driver:
1) Determine the version number of browser
In the address bar, enter > chrome://settings/help
2) Chrome Driver expects you have Chrome installed in the default location for your platform, otherwise you can force ChromeDriver to use a custom location by setting a special capability.
```
ChromeOptions options = new ChromeOptions();
options.setBinary("/path/to/other/chrome/binary");
```
3) Download the ChromeDriver binary for your platform under the downloads section of [this site](https://chromedriver.chromium.org/).
## browsermob-proxy installation
BrowserMob Proxy allows you to manipulate HTTP requests and responses, capture HTTP content, and export performance data as a HAR file.
The latest version of BrowserMob Proxy is 2.1.5, we installed the released version [2.1.4](https://github.com/lightbody/browsermob-proxy/releases). After unzipping, modify the line 28 of script EZbiocloud_16S_ID.py to write the install location.

# Usage
```
python EZBioCloud_ID_Selenium.py [-i input.fa] [-a account] [-p password]
```
**Options**


      -input
                 input fasta file
      -a account
                 the email address you registered to sign to EZBioCloud, e.g. lianzhh90@foxmail.com
      -p password
                 a magic strings, you know! 
                 
# Contact
If you have any questions, please email us: lianzhh90@foxmail.com
