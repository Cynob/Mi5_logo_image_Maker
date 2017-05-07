#! /bin/bash
WORKING_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

startuptest() {
	echo "test if needed software is installed"
	softest=""
    softest=`dpkg-query -W -f='${Status} \n' python && echo "true" || echo "false"`
    if [ "$softest" == "false" ]
    then
		echo "Phyton not installed yet .... try to install"
		sudo apt-get install python -y
	fi	
	softest=""
    softest=`dpkg-query -W -f='${Status} \n' python-imaging && echo "true" || echo "false"`
    if [ "$softest" == "false" ]
    then
		echo "python-imaging not installed yet .... try to install"
		sudo apt-get install python-imaging -y
	fi	
	softest=""
    softest=`dpkg-query -W -f='${Status} \n' python-pil && echo "true" || echo "false"`
    if [ "$softest" == "false" ]
    then
		echo "python-pil not installed yet .... try to install"
		sudo apt-get install python-pil -y
	fi	
	softest=""
    softest=`dpkg-query -W -f='${Status} \n' zenity && echo "true" || echo "false"`
    if [ "$softest" == "false" ]
    then
		echo "zenity not installed yet .... try to install"
		sudo apt-get install zenity -y
	fi	
	softest=""
    softest=`dpkg-query -W -f='${Status} \n' imagemagick && echo "true" || echo "false"`
    if [ "$softest" == "false" ]
    then
		echo "imagemagick not installed yet .... try to install"
		sudo apt-get install imagemagick -y
	fi
	softest=""
	    softest=`dpkg-query -W -f='${Status} \n' zip && echo "true" || echo "false"`
    if [ "$softest" == "false" ]
    then
		echo "zip not installed yet .... try to install"
		sudo apt-get install zip -y
	fi
	softest=""
    echo "selftest..."
    mkdir -p $WORKING_DIR/output
    
    if [ -d $WORKING_DIR/logotmp ]
	then
		rm -rf $WORKING_DIR/logotmp
	fi
	
	mkdir -p $WORKING_DIR/logotmp
	
    if [ -e $WORKING_DIR/logobin/logo_gen.py ]
	then
		echo "logo_gen.py available"
	else
		echo "ERROR logo_gen.py not found! ...Exiting" 
		sleep 2 && exit
	fi
	
	if [ -e $WORKING_DIR/logobin/skeleton.zip ]
	then
		echo "update.zip available"
	else
		echo "ERROR update.zip not found! ...Exiting" 
		sleep 2 && exit
	fi
	
clear
	
}

setPicture() {
fileselection=`zenity --file-selection --title="logo.img Maker" --file-filter=*.png --text="name of the file"`
if [ "$fileselection" == "" ]
then
	echo "no file selected..." && sleep 1 && exit 
else
	cp $fileselection $WORKING_DIR/logotmp/$1_ori.png
fi

fileinfo=`identify $WORKING_DIR/logotmp/$1_ori.png | awk '{ printf $2"  "$3"  "$5"  "$7 }'`
picsize=$(zenity  --list --title="logo.img Maker" --height=400 --text "Convert Picture to specific resolution?  -Try to preserve the aspect ratio! \n \n your selected picture properties: \n $fileinfo" \
	--radiolist \
	--column "Pick" \
	--column "resolution" \
	TRUE "keep_size" \
	FALSE "161x321" \
	FALSE "178x350" \
	FALSE "558x992" \
	FALSE "720x1280" \
	FALSE "1080x1920"); 
	
case "$picsize" in
	keep_size)	cp $WORKING_DIR/logotmp/$1_ori.png $WORKING_DIR/logotmp/$1.png	;;
	161x321)	convert $WORKING_DIR/logotmp/$1_ori.png -resize 161x321 $WORKING_DIR/logotmp/$1.png	;;
	178x350)	convert $WORKING_DIR/logotmp/$1_ori.png -resize 178x350 $WORKING_DIR/logotmp/$1.png	;;
	558x992)	convert $WORKING_DIR/logotmp/$1_ori.png -resize 558x992 $WORKING_DIR/logotmp/$1.png	;;
	720x1280)	convert $WORKING_DIR/logotmp/$1_ori.png -resize 720x1280 $WORKING_DIR/logotmp/$1.png	;;
	1080x1920)	convert $WORKING_DIR/logotmp/$1_ori.png -resize 1080x1920 $WORKING_DIR/logotmp/$1.png	;;
		*)		echo "Error in set resolution >> $1" && sleep 3 && exit ;;
esac	

}

buildsinglepic() {
zenity --info --title="logo.img Maker" --text "You selected \"one 4 all\" ! \n The pictures 2 till 5 get resized to 161x321 to save disk space! \n click ok to start generating logo.img"
convert $WORKING_DIR/logotmp/$1_ori.png -resize 161x321 $WORKING_DIR/logotmp/logo2.png	
cp $WORKING_DIR/logotmp/logo2.png $WORKING_DIR/logotmp/logo3.png
cp $WORKING_DIR/logotmp/logo2.png $WORKING_DIR/logotmp/logo4.png
cp $WORKING_DIR/logotmp/logo2.png $WORKING_DIR/logotmp/logo5.png

}

buildmultipic() {
zenity --info --title="logo.img Maker" --text "You selected \"add multiple pictures\" ! \n Now select picture Number 2 and set its size if you like"
setPicture logo2
zenity --info --title="logo.img Maker" --text "That was Nr.2 now select picture Nr.3"
setPicture logo3
zenity --info --title="logo.img Maker" --text "That was Nr.3 now select picture Nr.4"
setPicture logo4
zenity --info --title="logo.img Maker" --text "That was Nr.4 now select picture Nr.5"
setPicture logo5
zenity --info --title="logo.img Maker" --text "Thats all - click ok to start building logo.img"

}

startbuilding() {
if [ ! -e $WORKING_DIR/logotmp/logo1.png ]
then
	echo "Error no logo01.png to build" && sleep 3 && exit 
fi
if [ ! -e $WORKING_DIR/logotmp/logo2.png ]
then
	echo "Error no logo02.png to build" && sleep 3 && exit 
fi
if [ ! -e $WORKING_DIR/logotmp/logo3.png ]
then
	echo "Error no logo03.png to build" && sleep 3 && exit 
fi
if [ ! -e $WORKING_DIR/logotmp/logo4.png ]
then
	echo "Error no logo04.png to build" && sleep 3 && exit 
fi
if [ ! -e $WORKING_DIR/logotmp/logo5.png ]
then
	echo "Error no logo05.png to build" && sleep 3 && exit 
fi
python $WORKING_DIR/logobin/logo_gen.py $WORKING_DIR/logotmp/logo1.png $WORKING_DIR/logotmp/logo2.png $WORKING_DIR/logotmp/logo3.png $WORKING_DIR/logotmp/logo4.png $WORKING_DIR/logotmp/logo5.png
sync
	
}

donebuilding() {
zipit=`zenity --question --title="logo.img Maker" --ok-label="generate zipfile" --cancel-label="End" --text " logo.img file got created succesfull! \n Do you want a update.zip or end here?"; echo $?`
case "$zipit" in
	1) zenity --info --title="logo.img Maker" --text " Done! \n Your logo.img can be found in: $WORKING_DIR/output \n \n Thanks for using Logo_Maker script ..exit now" ;; 
	0) generateupdatezip ;;
	*) echo "Error in set zip..." && sleep 3 && exit ;;
esac

}

generateupdatezip() {
cp $WORKING_DIR/logobin/skeleton.zip $WORKING_DIR/output/logoimg_update.zip
cd $WORKING_DIR/output && zip -r logoimg_update.zip logo.img
minimumsize=239106
actualsize=$(wc -c <"$WORKING_DIR/output/logoimg_update.zip")
if [ $actualsize -ge $minimumsize ]; then
    zenity --info --title="logo.img Maker" --text " Done! \n \n Your logo.img and update.zip can be found in: $WORKING_DIR/output \n \n Thanks for using Logo_Maker script ..exit now"	
else
    echo "Error in gen zip..." && sleep 3 && exit
fi
}


###starthere
startuptest
zenity --info --title="logo.img Maker" --text "Welcome to logo.img Maker for Mi5 \n \n Chose your new bootlogo picture! \n it must be a png file."
setPicture logo1
one4all=`zenity --question --title="logo.img Maker" --ok-label="one4all" --cancel-label="add more" --text "So you have 5 slots for pictures in the logo.img  \n\n At now we know only the first pic get used! \n \n Would you like to add several pictures for each other slot \n or use one picture for all?"; echo $?`
case "$one4all" in
	1) buildmultipic ;; # add more
	0) buildsinglepic logo1 ;; # goto build
	*) echo "Error in set multiple..." && sleep 3 && exit ;;
esac

startbuilding 
sync && sleep 1
if [ -f "$WORKING_DIR/output/logo.img" ]
then
	donebuilding
else
	zenity --info --title="logo.img Maker" --text "Error - no logo.img build found ..exit now"
	sleep 1 && exit
fi

