#include <ros/ros.h>
#include <sensor_msgs/Image.h>
#include <cv_bridge/cv_bridge.h>
#include <image_transport/image_transport.h>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

int main(int argc, char** argv)
{
    // Initialize the ROS node
    ros::init(argc, argv, "camera_node");
    ros::NodeHandle nh;
    ros::NodeHandle pnh("~");
    
    // Get parameters
    int camera_device_id;
    int frame_rate;
    std::string frame_id;
    
    pnh.param("camera_device_id", camera_device_id, 0);
    pnh.param("frame_rate", frame_rate, 30);
    pnh.param("frame_id", frame_id, std::string("camera_link"));
    
    // Create image transport publisher
    image_transport::ImageTransport it(nh);
    image_transport::Publisher image_pub = it.advertise("camera/image_raw", 1);
    
    // Open the camera
    cv::VideoCapture cap(camera_device_id);
    if (!cap.isOpened()) {
        ROS_ERROR("Could not open camera with device ID %d", camera_device_id);
        return -1;
    }
    
    // Set camera properties if needed
    cap.set(cv::CAP_PROP_FPS, frame_rate);
    
    // Create rate limiter
    ros::Rate loop_rate(frame_rate);
    
    // Main loop
    cv::Mat frame;
    sensor_msgs::ImagePtr msg;
    
    ROS_INFO("Camera node started. Publishing to camera/image_raw topic.");
    
    while (ros::ok()) {
        // Capture frame
        cap >> frame;
        
        if (!frame.empty()) {
            // Convert OpenCV image to ROS message
            msg = cv_bridge::CvImage(std_msgs::Header(), "bgr8", frame).toImageMsg();
            msg->header.stamp = ros::Time::now();
            msg->header.frame_id = frame_id;
            
            // Publish the image
            image_pub.publish(msg);
        }
        
        ros::spinOnce();
        loop_rate.sleep();
    }
    
    return 0;
}
