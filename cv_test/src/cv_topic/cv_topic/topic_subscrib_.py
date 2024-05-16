from cv_bridge import CvBridge
from sensor_msgs.msg import Image

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