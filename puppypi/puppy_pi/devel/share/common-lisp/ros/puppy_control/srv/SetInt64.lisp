; Auto-generated. Do not edit!


(cl:in-package puppy_control-srv)


;//! \htmlinclude SetInt64-request.msg.html

(cl:defclass <SetInt64-request> (roslisp-msg-protocol:ros-message)
  ((data
    :reader data
    :initarg :data
    :type cl:integer
    :initform 0))
)

(cl:defclass SetInt64-request (<SetInt64-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetInt64-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetInt64-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name puppy_control-srv:<SetInt64-request> is deprecated: use puppy_control-srv:SetInt64-request instead.")))

(cl:ensure-generic-function 'data-val :lambda-list '(m))
(cl:defmethod data-val ((m <SetInt64-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader puppy_control-srv:data-val is deprecated.  Use puppy_control-srv:data instead.")
  (data m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetInt64-request>) ostream)
  "Serializes a message object of type '<SetInt64-request>"
  (cl:let* ((signed (cl:slot-value msg 'data)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 18446744073709551616) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetInt64-request>) istream)
  "Deserializes a message object of type '<SetInt64-request>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'data) (cl:if (cl:< unsigned 9223372036854775808) unsigned (cl:- unsigned 18446744073709551616))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetInt64-request>)))
  "Returns string type for a service object of type '<SetInt64-request>"
  "puppy_control/SetInt64Request")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetInt64-request)))
  "Returns string type for a service object of type 'SetInt64-request"
  "puppy_control/SetInt64Request")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetInt64-request>)))
  "Returns md5sum for a message object of type '<SetInt64-request>"
  "b8a3204d8bafe68f75673256846654f5")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetInt64-request)))
  "Returns md5sum for a message object of type 'SetInt64-request"
  "b8a3204d8bafe68f75673256846654f5")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetInt64-request>)))
  "Returns full string definition for message of type '<SetInt64-request>"
  (cl:format cl:nil "int64 data~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetInt64-request)))
  "Returns full string definition for message of type 'SetInt64-request"
  (cl:format cl:nil "int64 data~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetInt64-request>))
  (cl:+ 0
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetInt64-request>))
  "Converts a ROS message object to a list"
  (cl:list 'SetInt64-request
    (cl:cons ':data (data msg))
))
;//! \htmlinclude SetInt64-response.msg.html

(cl:defclass <SetInt64-response> (roslisp-msg-protocol:ros-message)
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

(cl:defclass SetInt64-response (<SetInt64-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetInt64-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetInt64-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name puppy_control-srv:<SetInt64-response> is deprecated: use puppy_control-srv:SetInt64-response instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <SetInt64-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader puppy_control-srv:success-val is deprecated.  Use puppy_control-srv:success instead.")
  (success m))

(cl:ensure-generic-function 'message-val :lambda-list '(m))
(cl:defmethod message-val ((m <SetInt64-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader puppy_control-srv:message-val is deprecated.  Use puppy_control-srv:message instead.")
  (message m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetInt64-response>) ostream)
  "Serializes a message object of type '<SetInt64-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'message))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'message))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetInt64-response>) istream)
  "Deserializes a message object of type '<SetInt64-response>"
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetInt64-response>)))
  "Returns string type for a service object of type '<SetInt64-response>"
  "puppy_control/SetInt64Response")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetInt64-response)))
  "Returns string type for a service object of type 'SetInt64-response"
  "puppy_control/SetInt64Response")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetInt64-response>)))
  "Returns md5sum for a message object of type '<SetInt64-response>"
  "b8a3204d8bafe68f75673256846654f5")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetInt64-response)))
  "Returns md5sum for a message object of type 'SetInt64-response"
  "b8a3204d8bafe68f75673256846654f5")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetInt64-response>)))
  "Returns full string definition for message of type '<SetInt64-response>"
  (cl:format cl:nil "bool success~%string message~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetInt64-response)))
  "Returns full string definition for message of type 'SetInt64-response"
  (cl:format cl:nil "bool success~%string message~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetInt64-response>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'message))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetInt64-response>))
  "Converts a ROS message object to a list"
  (cl:list 'SetInt64-response
    (cl:cons ':success (success msg))
    (cl:cons ':message (message msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'SetInt64)))
  'SetInt64-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'SetInt64)))
  'SetInt64-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetInt64)))
  "Returns string type for a service object of type '<SetInt64>"
  "puppy_control/SetInt64")