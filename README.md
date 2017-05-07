# Mi5_logo_image_Maker
generate logo.img file for Mi5


### How to use Logo_img_Maker for Linux

download the Logo_img_Maker_Linux.tar and untar it to your homefolder.
In the Logo_img_Maker_Linux folder check that the makeLogo.sh script is marked executeable.
Now start the Script with a double click ( run in terminal ) or start it with "./makeLogo.sh"

On start the script check if all necessary additional software is installed and if not try to install it with the apt-get tool.
To run the script succesful following programms are needed:
python; python-imaging; python-pit; imagemagick; zenity; zip

If a error occur the script shows it in the terminal window and maybe ask for your superuser password to install the missing things.
You can also run: "sudo apt-get install python python-imaging python-pit imagemagick zenity zip -y" first to set up your system.

### How it works:
At first you see a Welcome screen. Click ok to get to a file selection dialog where you can select the .png file which will get your new bootlogo.
After that you can adjust the resolution if you like. Your original picture dont get edited (the script copy it first to a temporary folder). 
If you dont want to let the "keep_size" radiobutton active and only press ok then.

So now you can decide if you want to use the selected picture for all slots in the logo.img file or to put a different for every single slot.
If you want more to know about it read "logo.img explained" in this readme

If you select 
one4all:
your before selected picture get used for logo Nr.1 
The Script resizes the other 4 to 161x321 to save space on disc

add more:
you have to select the other 4 pictures one after another and set its size like you did with the first one. Of course the sizes can differ 
for each picture.

When you are done with one of the two options the logo.img get build.

If that was successful you will get asked if you want to generate a update.zip for your custom recovery.
If you dont want to the logo.img can be found in the output folder.
If you click yes the flashable zip get generated in the output folder too.

Have fun






### logo.img explained:


the original logo.img header got explained by **GokuINC** from xda-developers.com - big thanks 
                                          - without him this all could not have been possible!
                                          
### The header from ori file is: 



SPLASH!!

Width (of 5 pictures)

Height (of 5 pictures)

SUPPORT_RLE24_COMPRESSIONT (of 5 pictures) (1 means it is RLE encoded, 0 means RGB24)

Payload size/4096 (of 5 pictures)

(Offset/4096)-1 (of 5 pictures)





### And the funny thing my script do:


SPLASH!!

Width (of 5 pictures)

Height (of 5 pictures)

SUPPORT_RLE24_COMPRESSIONT (of 5 pictures) (1 means it is RLE encoded, 0 means RGB24)

(Offset/4096)-1 (of 5 pictures)





and it works on "MIUI V8 Android 7" with a Mi5 (gemini)
I first tried to rebuild it like Gokus example ( and of course - in the hex editor -
it was clear the same as in the original logo.img ..
ok different sizes but all was calculatebale and logical)
but it didnt work.... 
So i poked around and got this working solution - tested on **@HOSCHI@**s Mi5
There are many things that arent clear as they should - but it works somehow ;)

It shows the bootlogo equal if you boot to your system or your recovery.
I dont know really if the 5 pictures are all the same but different sizes or if they are different. 
The original resolutions are:

logo picture 1 = 161x321 

logo picture 2 = 558x992

logo picture 3 = 178x350

logo picture 4 = 1080x1920

logo picture 5 = 1080x1920


