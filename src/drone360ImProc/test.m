%%

rosinit
sub = rossubscriber('/drone/drone/camera1/image_raw','sensor_msgs/Image');
image = readImage(receive(sub));
imshow(image)

while 1
image = readImage(receive(sub));
imshow(image);
drawnow;
end

rosshutdown


%%

