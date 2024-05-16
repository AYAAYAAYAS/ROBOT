from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from flask import Flask
import rclpy
from rclpy.node import Node
class ImageSubscriber(Node):
    def _init_(self, topicname):
        super()._init_('image_subscriber')
        self.bridge = CvBridge()
        self.subscriber = self.create_subscriber(Image, topicname,self.image_callback,10)
    
    def image_callback(self , msg):
        global current_image
        cv_image = self.bridge.imgmsg_to_cv2(msg,"bgr8")
        buffer = cv2.imencode('.jpg',cv_image)
        current_image = buffer.tobytes()

@app.route('/video_stream')
def video_stream():
    return Response(generate(),mimetype='multipart/x-mixed-replace; boundary=frame')

def generate():
    while True:
        if current_image is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + current_image + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: text/plain\r\n\r\nNO image availabler\n')
            
def run_ros_node(topic_name):
    rclpy.init()
    node = ImageSubscriber(topic_name)
    rclpy.spin(node)
    image_subscriber.destroy_node()
    rclpy.shutdown()

def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('topic_name',type=str , help='topic name')
    args = parser.parse_args()

    ros_thread = threading.Thread(target=run_ros_node, args=(args.topic_name))
    ros_thread.start()
    app.run(host='0.0.0.0', port=5000,threaded = Ture)
