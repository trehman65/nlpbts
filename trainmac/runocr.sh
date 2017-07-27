files=$( ls *.png )


for i in $files
do
    echo $i
 curl -F name=@$i -o $i.txt http://ec2-35-165-99-224.us-west-2.compute.amazonaws.com/OCRTools/ocrtext.jsp
    #curl -F file=@$i -o $i.json http://35.165.99.224:8091/VisionX2/analyze
done
