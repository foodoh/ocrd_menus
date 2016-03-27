# echoes the number of images in `menu_images` dir and the number of ocr'd
# hotel images
images=`ls menu_images/ | wc -l`
text=`ls menu_text/ | wc -l`
echo "menu images: $images "
zero=`find menu_text -size 0 | wc -l`
echo "files with 0 bytes size: $zero"
final=$(echo "$text-$zero" | bc)
echo "ocrd files: $final "
