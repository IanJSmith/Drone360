
folder_frame_string = 'drone_images/frame';

filename = [folder_frame_string sprintf('%04d',1) '.jpg'];

drone_frame = imread(filename);
[im_rows,im_cols,depth] = size(drone_frame);

panorama = im2double(drone_frame);
old_frame = im2double(drone_frame);
% figure
% imshow(old_frame);
%transformations = [1 ; -1];
transformations = -1;

for i = 2:324
    transformations1 = transformations;
    filename = [folder_frame_string sprintf('%04d',i) '.jpg'];
    current_frame = im2double(imread(filename));
%     figure
%     imshow(current_frame);
    dx = 0;
    
%     A = [1 0 0; 0 1 0; dx 0 1];  
%     tform = affine2d(A);
%     sameAsInput = affineOutputView(size(current_frame),tform,'BoundsStyle','SameAsInput');
%     frameTform = imwarp(current_frame, tform,'cubic','FillValues',zeros(1,channels),'OutputView',sameAsInput);%, 'bilinear', 'XData', [1 width], 'YData', [1 height],'FillValues', zeros(1,channels));

    error = immse(current_frame,old_frame);
    
    min = error;
    scale = 1;
    
    dx_min = 0;
    
    while (min ~= 0 && scale <= 60)
        %for j = 1:2

            A = [1 0 0; 0 1 0; transformations1 0 1];  
            tform = affine2d(A);
            sameAsInput = affineOutputView(size(current_frame),tform,'BoundsStyle','SameAsInput');
            current_Tform = imwarp(current_frame, tform,'cubic','FillValues',zeros(1,depth),'OutputView',sameAsInput);%, 'bilinear', 'XData', [1 width], 'YData', [1 height],'FillValues', zeros(1,channels));
            tempError = immse( old_frame(:,1:im_cols+transformations1,:)...
                              ,current_Tform(:,1:im_cols+transformations1,:));
%             figure
%             imshow(current_Tform);
            if tempError <= min
                dx_min = transformations1(j);
                min = tempError;
            end
            
        %end
        scale = scale+1;
        %transformations1 = transformations*scale + dx_min;
        transformations1 = transformations*scale;
        j = 1;
        
    end
    
    if dx_min ~= 0
        padding = current_frame(:,1:abs(dx_min),:);
        panorama = cat(2,padding,panorama); 
    end
    
    old_frame = current_frame;
    
end

figure;
imshow(panorama);
imwrite(panorama,'panorama.tif');

