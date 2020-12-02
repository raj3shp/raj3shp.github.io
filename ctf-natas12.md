# CTF Writeup: NATAS #12 Exploiting Basic file upload vulnerability

Level 12 presents you with a simple file upload functionality. You can upload an image and file and view it later in /upload directory.

Here is the sourcecode available to us 

```
<? 

function genRandomString() {
    $length = 10;
    $characters = "0123456789abcdefghijklmnopqrstuvwxyz";
    $string = "";    

    for ($p = 0; $p < $length; $p++) {
        $string .= $characters[mt_rand(0, strlen($characters)-1)];
    }

    return $string;
}

function makeRandomPath($dir, $ext) {
    do {
    $path = $dir."/".genRandomString().".".$ext;
    } while(file_exists($path));
    return $path;
}

function makeRandomPathFromFilename($dir, $fn) {
    $ext = pathinfo($fn, PATHINFO_EXTENSION);
    return makeRandomPath($dir, $ext);
}

if(array_key_exists("filename", $_POST)) {
    $target_path = makeRandomPathFromFilename("upload", $_POST["filename"]);


        if(filesize($_FILES['uploadedfile']['tmp_name']) > 1000) {
        echo "File is too big";
    } else {
        if(move_uploaded_file($_FILES['uploadedfile']['tmp_name'], $target_path)) {
            echo "The file <a href=\"$target_path\">$target_path</a> has been uploaded";
        } else{
            echo "There was an error uploading the file, please try again!";
        }
    }
} else {
?>

<form enctype="multipart/form-data" action="index.php" method="POST">
<input type="hidden" name="MAX_FILE_SIZE" value="1000" />
<input type="hidden" name="filename" value="<? print genRandomString(); ?>.jpg" />
Choose a JPEG to upload (max 1KB):<br/>
<input name="uploadedfile" type="file" /><br />
<input type="submit" value="Upload File" />
</form>
<? } ?> 
```

To understand how to break this code, I looked some of the common vulnerabilities in file upload. One of the vulnerabilities is that you can upload a file containing PHP code and execute it by visiting the path where file is uploaded. We can upload PHP code to get a reverse shell or a simple command execution backdoor.

In my kali linux machine, I found such code in ```/usr/share/webshells/php/simple-backdoor.php```.

Now, let's look at the code above

* If ```$_POST[filename]``` exists, a target path is created using ```makeRandomPathFromFilename``` function.
* In ```makeRandomPathFromFilename``` function, ```$ext = pathinfo($fn, PATHINFO_EXTENSION);``` sets the variable $ext with the file extension submitted by the user. And this ```$ext``` variable is used to call ```makeRandomPath``` function which appends the extension to the random file name generated.
* There is also a file size check and we need to keep our file size below 1 KB. This is not a problem since the backdoor file we selected is only ~300 bytes.
* Let's try to upload the simple-backdoor.php file. Upload works, but when we access the file at given location, we get an error message saying "File cannot be displayed because it contains error". Hmm, why is the server still thinking of this as an image file?
* Here is the reason ```<input type="hidden" name="filename" value="<? print genRandomString(); ?>.jpg" />```. In the client side code, the extension is being overwritten to ```.jpg```. Ah! We can easily bypass this by using BurpSuite.
* So, let's intercept the request to upload simple-backdoor.php and change the randomly generated .jpg filename to .php and fordward the requst.
* Boom! We got a backdoor working. Now you can grab the password to NATAS 13 by 
```
http://natas12.natas.labs.overthewire.org/upload/rhhxz8iupf.php?cmd=cat+/etc/natas_webpass/natas13
```
