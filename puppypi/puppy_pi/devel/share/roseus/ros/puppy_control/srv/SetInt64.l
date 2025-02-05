;; Auto-generated. Do not edit!


(when (boundp 'puppy_control::SetInt64)
  (if (not (find-package "PUPPY_CONTROL"))
    (make-package "PUPPY_CONTROL"))
  (shadow 'SetInt64 (find-package "PUPPY_CONTROL")))
(unless (find-package "PUPPY_CONTROL::SETINT64")
  (make-package "PUPPY_CONTROL::SETINT64"))
(unless (find-package "PUPPY_CONTROL::SETINT64REQUEST")
  (make-package "PUPPY_CONTROL::SETINT64REQUEST"))
(unless (find-package "PUPPY_CONTROL::SETINT64RESPONSE")
  (make-package "PUPPY_CONTROL::SETINT64RESPONSE"))

(in-package "ROS")





(defclass puppy_control::SetInt64Request
  :super ros::object
  :slots (_data ))

(defmethod puppy_control::SetInt64Request
  (:init
   (&key
    ((:data __data) 0)
    )
   (send-super :init)
   (setq _data (round __data))
   self)
  (:data
   (&optional __data)
   (if __data (setq _data __data)) _data)
  (:serialization-length
   ()
   (+
    ;; int64 _data
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int64 _data
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _data (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _data) (= (length (_data . bv)) 2)) ;; bignum
              (write-long (ash (elt (_data . bv) 0) 0) s)
              (write-long (ash (elt (_data . bv) 1) -1) s))
             ((and (class _data) (= (length (_data . bv)) 1)) ;; big1
              (write-long (elt (_data . bv) 0) s)
              (write-long (if (>= _data 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _data s)(write-long (if (>= _data 0) 0 #xffffffff) s)))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int64 _data
#+(or :alpha :irix6 :x86_64)
      (setf _data (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _data (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;;
   self)
  )

(defclass puppy_control::SetInt64Response
  :super ros::object
  :slots (_success _message ))

(defmethod puppy_control::SetInt64Response
  (:init
   (&key
    ((:success __success) nil)
    ((:message __message) "")
    )
   (send-super :init)
   (setq _success __success)
   (setq _message (string __message))
   self)
  (:success
   (&optional (__success :null))
   (if (not (eq __success :null)) (setq _success __success)) _success)
  (:message
   (&optional __message)
   (if __message (setq _message __message)) _message)
  (:serialization-length
   ()
   (+
    ;; bool _success
    1
    ;; string _message
    4 (length _message)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _success
       (if _success (write-byte -1 s) (write-byte 0 s))
     ;; string _message
       (write-long (length _message) s) (princ _message s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _success
     (setq _success (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; string _message
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _message (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass puppy_control::SetInt64
  :super ros::object
  :slots ())

(setf (get puppy_control::SetInt64 :md5sum-) "b8a3204d8bafe68f75673256846654f5")
(setf (get puppy_control::SetInt64 :datatype-) "puppy_control/SetInt64")
(setf (get puppy_control::SetInt64 :request) puppy_control::SetInt64Request)
(setf (get puppy_control::SetInt64 :response) puppy_control::SetInt64Response)

(defmethod puppy_control::SetInt64Request
  (:response () (instance puppy_control::SetInt64Response :init)))

(setf (get puppy_control::SetInt64Request :md5sum-) "b8a3204d8bafe68f75673256846654f5")
(setf (get puppy_control::SetInt64Request :datatype-) "puppy_control/SetInt64Request")
(setf (get puppy_control::SetInt64Request :definition-)
      "int64 data
---
bool success
string message
")

(setf (get puppy_control::SetInt64Response :md5sum-) "b8a3204d8bafe68f75673256846654f5")
(setf (get puppy_control::SetInt64Response :datatype-) "puppy_control/SetInt64Response")
(setf (get puppy_control::SetInt64Response :definition-)
      "int64 data
---
bool success
string message
")



(provide :puppy_control/SetInt64 "b8a3204d8bafe68f75673256846654f5")


