; Auto-generated. Do not edit!


(cl:in-package puppy_control-srv)


;//! \htmlinclude SetFloat64List-request.msg.html

(cl:defclass <SetFloat64List-request> (roslisp-msg-protocol:ros-message)
  ((data
    :reader data
    :initarg :data
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass SetFloat64List-request (<SetFloat64List-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetFloat64List-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetFloat64List-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name puppy_control-srv:<SetFloat64List-request> is deprecated: use puppy_control-srv:SetFloat64List-request instead.")))

(cl:ensure-generic-function 'data-val :lambda-list '(m))
(cl:defmethod data-val ((m <SetFloat64List-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader puppy_control-srv:data-val is deprecated.  Use puppy_control-srv:data instead.")
  (data m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetFloat64List-request>) ostream)
  "Serializes a message object of type '<SetFloat64List-request>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'data))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'data))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetFloat64List-request>) istream)
  "Deserializes a message object of type '<SetFloat64List-request>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'data) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'data)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetFloat64List-request>)))
  "Returns string type for a service object of type '<SetFloat64List-request>"
  "puppy_control/SetFloat64ListRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetFloat64List-request)))
  "Returns string type for a service object of type 'SetFloat64List-request"
  "puppy_control/SetFloat64ListRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetFloat64List-request>)))
  "Returns md5sum for a message object of type '<SetFloat64List-request>"
  "5739026f6f0517440e663ba60441de94")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetFloat64List-request)))
  "Returns md5sum for a message object of type 'SetFloat64List-request"
  "5739026f6f0517440e663ba60441de94")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetFloat64List-request>)))
  "Returns full string definition for message of type '<SetFloat64List-request>"
  (cl:format cl:nil "float64[] data~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetFloat64List-request)))
  "Returns full string definition for message of type 'SetFloat64List-request"
  (cl:format cl:nil "float64[] data~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetFloat64List-request>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'data) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetFloat64List-request>))
  "Converts a ROS message object to a list"
  (cl:list 'SetFloat64List-request
    (cl:cons ':data (data msg))
))
;//! \htmlinclude SetFloat64List-response.msg.html

(cl:defclass <SetFloat64List-response> (roslisp-msg-protocol:ros-message)
  ((success
    :reader success
    :initarg :success
    :type cl:boolean
    :initform cl:nil)
   (message
    :reader message
    :initarg :message
    :type cl:string
    :initform ""))
)

(cl:defclass SetFloat64List-response (<SetFloat64List-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetFloat64List-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetFloat64List-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name puppy_control-srv:<SetFloat64List-response> is deprecated: use puppy_control-srv:SetFloat64List-response instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <SetFloat64List-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader puppy_control-srv:success-val is deprecated.  Use puppy_control-srv:success instead.")
  (success m))

(cl:ensure-generic-function 'message-val :lambda-list '(m))
(cl:defmethod message-val ((m <SetFloat64List-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader puppy_control-srv:message-val is deprecated.  Use puppy_control-srv:message instead.")
  (message m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetFloat64List-response>) ostream)
  "Serializes a message object of type '<SetFloat64List-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'message))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'message))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetFloat64List-response>) istream)
  "Deserializes a message object of type '<SetFloat64List-response>"
    (cl:setf (cl:slot-value msg 'success) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'message) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'message) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetFloat64List-response>)))
  "Returns string type for a service object of type '<SetFloat64List-response>"
  "puppy_control/SetFloat64ListResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetFloat64List-response)))
  "Returns string type for a service object of type 'SetFloat64List-response"
  "puppy_control/SetFloat64ListResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetFloat64List-response>)))
  "Returns md5sum for a message object of type '<SetFloat64List-response>"
  "5739026f6f0517440e663ba60441de94")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetFloat64List-response)))
  "Returns md5sum for a message object of type 'SetFloat64List-response"
  "5739026f6f0517440e663ba60441de94")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetFloat64List-response>)))
  "Returns full string definition for message of type '<SetFloat64List-response>"
  (cl:format cl:nil "bool success~%string message~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetFloat64List-response)))
  "Returns full string definition for message of type 'SetFloat64List-response"
  (cl:format cl:nil "bool success~%string message~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetFloat64List-response>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'message))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetFloat64List-response>))
  "Converts a ROS message object to a list"
  (cl:list 'SetFloat64List-response
    (cl:cons ':success (success msg))
    (cl:cons ':message (message msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'SetFloat64List)))
  'SetFloat64List-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'SetFloat64List)))
  'SetFloat64List-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetFloat64List)))
  "Returns string type for a service object of type '<SetFloat64List>"
  "puppy_control/SetFloat64List")