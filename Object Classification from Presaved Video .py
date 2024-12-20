import cv2
import numpy as np

#loading the video file
file_video_stream = cv2.VideoCapture('C:\\Users\\tezzy\\Desktop\\yolo_opencv\\input_video\\Pexels Videos 1721294.mp4')
#Detecting the height and the width
while (file_video_stream.isOpened):
    ret, current_frame = file_video_stream.read()
    img_to_detect=current_frame
    img_height = img_to_detect.shape[0]
    img_width = img_to_detect.shape[1]

#Converting the image into a blob so we can pass it into the model
    img_blob=cv2.dnn.blobFromImage(img_to_detect, 0.0003922, (416, 416), swapRB= True, crop=False)
    #get list of clas labels from coco dataset.
    class_labels=  ["person","bicycle","car","motorcycle","airplane","bus","train","truck","boat","trafficlight",
                "firehydrant","stopsign","parkingmeter","bench","bird","cat","dog","horse","sheep","cow","elephant",
                "bear","zebra","giraffe","backpack","umbrella","handbag","tie","suitcase","frisbee","skis","snowboard",
                "sportball","kite","basketballbat","basketballglove","skateboard","surfboard","tennisracket","bottle",
                "wineglass","cup","fork","knife","spoon","bowl","banana","apple","sandwich","orange","broccoli",
                "carrot","hotdog","pizza","donut","cake","chair","sofa","pottedplant","bed","dinningtable","toilet",
                "tvmonitor","laptop","mouse","remote","keyboard","cellphone","microwave","oven","toaster","sink",
                "refrigerator","book","clock","vase","scissors","teddybear","hairdryer","tootbrush"]

#Declaring a color list so the bounding boxes can have different colors for different objects detected
    class_colors = ["0,255,0","0,0,255","255,0,0", "255,255,0","0,255,255"]
    class_colors =[np.array(every_color.split(",")).astype("int") for every_color in class_colors]
    class_colors=np.array(class_colors)
    class_colors=np.tile(class_colors,(16,1))


#loading the pretrained model using opencv method readNetFromDarknet
    yolo_model =cv2.dnn.readNetFromDarknet('C:\\Users\\tezzy\\Desktop\\yolo_opencv\\model_data\\yolov3.cfg', 'C:\\Users\\tezzy\\Desktop\\yolo_opencv\\model_data\\yolov3.weights')
#get all layers from the yolo network
    yolo_layers =yolo_model.getLayerNames()
    yolo_output_layer =  [yolo_layers[yolo_layer[0] -1] for yolo_layer in yolo_model.getUnconnectedOutLayers ()]
#input the processed blob into model and pass through the model
    yolo_model.setInput(img_blob)
#Obtain the detection layer by forwarding through until the output layer
    obj_detection_layers = yolo_model.forward(yolo_output_layer)
#declare list for [ class_id], box_center, width and height[], confidences]
    class_ids_list=[]
    boxes_list = []
    confidences_list=[]
#Loop over each of the layer outputs because we will be having multiple detections
    for object_detection_layer in obj_detection_layers:
        for object_detection in object_detection_layer:
#object_detection[1 to 4] will have two center points, box width and box heigth
#object detections[5] will have scores for all the bounding boxes
            all_scores=object_detection[5:]
            predicted_class_id=np.argmax(all_scores)
            prediction_confidence = all_scores[predicted_class_id]
#take only predictions with confidence more than 20%
            if prediction_confidence>0.50:
#get the predicted label
                predicted_class_label = class_labels[predicted_class_id]
#obtain the bounding box co-ordinates for actual image for resized image size
                bounding_box = object_detection[0:4]* np.array([img_width, img_height,img_width,img_height])
                (box_center_x_pt,box_center_y_pt,box_width,box_height)=bounding_box.astype("int")
                start_x_pt=int(box_center_x_pt - (box_width/2))
                start_y_pt= int(box_center_y_pt - (box_height/2))
           
           
                class_ids_list.append(predicted_class_id)
                confidences_list.append(float(prediction_confidence))
                boxes_list.append([start_x_pt, start_y_pt, int(box_width), int(box_height)])
#Applying the NMS will return onlt the selected max value ids while surpressing the non max weak
#Non-Maxima Suppression confidence set as  0.5 &mas suppression threshold for NMS as 0.4
    max_value_ids= cv2.dnn.NMSBoxes(boxes_list,confidences_list, 0.5, 0.4)          
    for max_valueid in max_value_ids:
        max_class_id = max_valueid[0]
        box=boxes_list[max_class_id]
        start_x_pt= box[0]
        start_y_pt=box[1]
        box_width=box[2]
        box_height=box[3]
       
        predicted_class_id = class_ids_list[max_class_id]
        predicted_class_label=class_labels[predicted_class_id]
        prediction_confidence = confidences_list[max_class_id]
           
        end_x_pt =start_x_pt +box_width
        end_y_pt = start_y_pt +box_height
#get a random mask color from the numpy array of colors          
        box_color=class_colors[predicted_class_id]
        box_color = [int (c) for c in box_color]
#print the prediction in console        
        predicted_class_label="{}: {:.2f}%".format(predicted_class_label, prediction_confidence*100)
        print("predicted object{}". format(predicted_class_label))
#draw a rectangle and text in the image          
        cv2.rectangle(img_to_detect, (start_x_pt, start_y_pt), (end_x_pt, end_y_pt), box_color, 1)
        cv2.putText(img_to_detect, predicted_class_label, (start_x_pt, start_y_pt -5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color,1)
           
    cv2.imshow("Detection Output", img_to_detect)
       
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
   
file_video_stream.release()
cv2.destroyAllWindows()
