
(cl:in-package :asdf)

(defsystem "puppy_control-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "SetFloat64" :depends-on ("_package_SetFloat64"))
    (:file "_package_SetFloat64" :depends-on ("_package"))
    (:file "SetFloat64List" :depends-on ("_package_SetFloat64List"))
    (:file "_package_SetFloat64List" :depends-on ("_package"))
    (:file "SetInt64" :depends-on ("_package_SetInt64"))
    (:file "_package_SetInt64" :depends-on ("_package"))
    (:file "SetRunActionName" :depends-on ("_package_SetRunActionName"))
    (:file "_package_SetRunActionName" :depends-on ("_package"))
  ))