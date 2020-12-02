# CTF Writeup: NATAS #11 Weak Encryption

I started with capture the flag (CTF) excercises to practice my web hacking skills. This post is about one of the interesting challenges I faced in solving [NATAS](https://overthewire.org/wargames/natas/) CTF.

Levels 1 to 10 are quite simple so I won't get into them. I really got stuck at level 11. While solving this level, I learned about XOR encryption, regular expressions and their weaknesses.

NATAS 11 presents you with a simple application which takes user input of color that you want to set as background. You can view the source code of how this works. Here is the source code, before jumping to the solution give it another try based on above hint (:

```
$defaultdata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");

function xor_encrypt($in) {
    $key = '<censored>';
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

function loadData($def) {
    global $_COOKIE;
    $mydata = $def;
    if(array_key_exists("data", $_COOKIE)) {
    $tempdata = json_decode(xor_encrypt(base64_decode($_COOKIE["data"])), true);
    if(is_array($tempdata) && array_key_exists("showpassword", $tempdata) && array_key_exists("bgcolor", $tempdata)) {
        if (preg_match('/^#(?:[a-f\d]{6})$/i', $tempdata['bgcolor'])) {
        $mydata['showpassword'] = $tempdata['showpassword'];
        $mydata['bgcolor'] = $tempdata['bgcolor'];
        }
    }
    }
    return $mydata;
}

function saveData($d) {
    setcookie("data", base64_encode(xor_encrypt(json_encode($d))));
}

$data = loadData($defaultdata);

if(array_key_exists("bgcolor",$_REQUEST)) {
    if (preg_match('/^#(?:[a-f\d]{6})$/i', $_REQUEST['bgcolor'])) {
        $data['bgcolor'] = $_REQUEST['bgcolor'];
    }
}

saveData($data);

?>

<h1>natas11</h1>
<div id="content">
<body style="background: <?=$data['bgcolor']?>;">
Cookies are protected with XOR encryption<br/><br/>

<?
if($data["showpassword"] == "yes") {
    print "The password for natas12 is <censored><br>";
}

?>

<form>
Background color: <input name=bgcolor value="<?=$data['bgcolor']?>">
<input type=submit value="Set color">
</form>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>

```

## What are possible ways to break this?

* First thing that came to my mind was to somehow inject malicious content using bgcolor parameter to get access to the flag.  ```<body style="background: <?=$data['bgcolor']?>;">``` This line is taking user input and passing it directly to a PHP code. Can I inject more PHP code to change the value of $data["showpassword"] to yes? Probably...
Injecting PHP code is not possible since there is a regular expression used for validating user input. It allows us to only enter 6 charaters/digits which could be either between a to f or 0-9.
* Can I bypass the regex validation? 
This question lead me down the path of understanding how regular expressions work and a known weakness in preg_match function. preg_match functions expects a string as input, if we pass an array- ```http://natas11.natas.labs.overthewire.org/?bgcolor[]=%23ffffff``` the function breaks. Well, breaking the function is not enough and does not allow us to bypass the check. This only gives us an error message disclosing the full file path of the code. But that's about it, nothing much can be done with this.
* Allright! I figured there is no easy way to solve this challenge but to do the hard work and understand how XOR encryption is being done and possible try to reverse it. I am quite new in programming and cryptography so I had no idea about how XOR encryption works and if it is reversable. A quick google search reveals that XOR encryption can be eaily broken. Read - https://en.wikipedia.org/wiki/XOR_cipher

```
a XOR b = c
b XOR c = a
```

Boom! If you have values of two elements, you can easily derive 3rd element ($key).

In above code, $key is censored, but we already know values of $text and $outText. $text is the array with default values and $outText is the cookie set by the application in your browser.

So to determine the key, I made a small change to the code as shown below -

```
function xor_encrypt($in) {
    $key = json_encode(array( "showpassword"=>"no", "bgcolor"=>"#ffffff"));
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

echo(xor_encrypt(base64_decode("ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw="))); //this is the default cookie value

```
To run this code, I do following in the directory where I saved xor_decrypt.php with above code -
```
php -S localhost:8000 
```
Open localhost:8000/xor_decrypt.php in the browser. This returns ```qw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jq```. Hmm, looks like our key is ```qw8j``` and it is repeated multiple times because of the small size of the key as compared to the message.

The final step is to create a cookie value with showpassword=>yes and send it in our request. To do that, modify above code to following

```
function xor_encrypt($in) {
    $key = "qw8j";
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

echo(base64_encode((xor_broken(json_encode(array( "showpassword"=>"yes", "bgcolor"=>"#ffffff"))))));
```
This returns ```ClVLIh4ASCsCBE8lAxMacFMOXTlTWxooFhRXJh4FGnBTVF4sFxFeLFMK```

Now, I intercepted the request using BurpSuite and modified the cookie to above value which gives you the flag.
